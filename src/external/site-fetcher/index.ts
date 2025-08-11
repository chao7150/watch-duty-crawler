import { chromium } from "playwright";
import robotsParser from "robots-parser";
import { JSDOM } from "jsdom";
import { Readability } from "@mozilla/readability";
import type { Site, Page } from "../../domain.js";
import type { ISiteFetcher } from "../../usecase/interfaces.js";

const USER_AGENT =
  "watch-duty-crawler/0.1 (+https://github.com/chao7150/watch-duty-crawler)";
const imageExts = [
  ".jpg",
  ".jpeg",
  ".png",
  ".gif",
  ".webp",
  ".svg",
  ".bmp",
  ".ico",
  ".tiff",
];

/**
 * rootUrlからrobots.txtのURLを生成する
 */
async function getRobotsAssorter(
  rootUrl: string
): Promise<{ isAllowed: (url: string) => boolean }> {
  try {
    const u = new URL(rootUrl);
    const robotsUrl = `${u.origin}/robots.txt`;
    const robotsTxt = await fetch(robotsUrl).then((res) => res.text());
    const robots = robotsParser.default(robotsUrl, robotsTxt);
    return {
      isAllowed: (url: string) => {
        // robots.txtの内容をチェックして、アクセスを許可するかどうかを判断する
        if (!robots) return true;
        return Boolean(robots.isAllowed(url, USER_AGENT));
      },
    };
  } catch {
    return { isAllowed: () => true };
  }
}

const getRelativePath = (url: string, rootUrl: string): string => {
  const normalizedRoot = rootUrl.endsWith("/") ? rootUrl : rootUrl + "/";
  return url.startsWith(normalizedRoot)
    ? url.slice(normalizedRoot.length - 1)
    : url;
};

const extractTextContent = (rawHtml: string): string => {
  try {
    const dom = new JSDOM(rawHtml);
    const reader = new Readability(dom.window.document);
    const article = reader.parse();
    if (article && article.textContent) {
      return article.textContent
        .split("\n")
        .map((line) => line.trim())
        .filter((line) => line.length > 0)
        .join("\n");
    }
    return "";
  } catch (e) {
    return "";
  }
};

const isString = (v: unknown): v is string => typeof v === "string";

export const service: ISiteFetcher = {
  fetch: async (site: Site): Promise<Array<Page>> => {
    const rootUrl = site.rootUrl;
    // robots.txt取得・解析
    const robots = await getRobotsAssorter(rootUrl);

    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.setExtraHTTPHeaders({
      "User-Agent": USER_AGENT,
    });
    const visited = new Set<string>();
    const toVisit = [rootUrl];
    const root = new URL(rootUrl);
    const results: Array<Page> = [];

    let requestCount = 0;
    while (toVisit.length > 0) {
      const url = toVisit.pop()!;
      if (visited.has(url)) continue;
      visited.add(url);

      requestCount++;
      if (process.env["NODE_ENV"] === "test") {
        console.log(
          `[${requestCount}] Fetching: ${url} (visited: ${visited.size}, queue: ${toVisit.length})`
        );
      }

      await new Promise((res) => setTimeout(res, 2000));

      try {
        await Promise.race([
          page.goto(url, { waitUntil: "networkidle" }),
          new Promise((res) => setTimeout(res, 10000)),
        ]);
        const title = await page.title();
        const rawHtml = await page.content();

        results.push({
          title,
          content: extractTextContent(rawHtml),
          relativePath: getRelativePath(url, rootUrl),
        });

        const links: string[] = await page.$$eval("a[href]", (els: any) =>
          els.map((el: HTMLAnchorElement) => el.href)
        );

        const filteredLinks = links
          .filter(isString)
          .map((href) => new URL(href, url))
          .filter(
            (nextUrl) =>
              !imageExts.some((ext) =>
                nextUrl.pathname.toLowerCase().endsWith(ext)
              )
          )
          .filter(
            (nextUrl) =>
              nextUrl.origin === root.origin &&
              nextUrl.pathname.startsWith(root.pathname)
          )
          .map((nextUrl) => {
            const nextUrlString = nextUrl.toString();
            if (nextUrl.hash) {
              // フラグメントを除去
              nextUrl.hash = "";
              return nextUrl.toString();
            }
            return nextUrlString;
          })
          .filter((nextUrl) => !visited.has(nextUrl))
          .filter(robots.isAllowed);
        toVisit.push(...filteredLinks);
      } catch (e) {
        if (process.env["NODE_ENV"] === "test") {
          console.log(`[${requestCount}] Failed: ${url} (${e})`);
        }
        // エラーハンドリング
      }
    }
    await browser.close();
    return results;
  },
};
