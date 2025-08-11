import { chromium } from "playwright";
import robotsParser from "robots-parser";
import { JSDOM } from "jsdom";
import { Readability } from "@mozilla/readability";
import type { Site, Page } from "../../domain.js";
import type { ISiteFetcher } from "../../usecase/interfaces.js";
import { None, Some, type Option } from "ts-results";

/**
 * rootUrlからrobots.txtのURLを生成する
 */
function getRobotsUrl(rootUrl: string): Option<string> {
  try {
    const u = new URL(rootUrl);
    return Some(`${u.origin}/robots.txt`);
  } catch {
    return None;
  }
}

export const service: ISiteFetcher = {
  fetch: async (site: Site): Promise<Array<Page>> => {
    const rootUrl = site.rootUrl;
    // robots.txt取得・解析
    const robotsUrl = getRobotsUrl(rootUrl).andThen(async (url) => {
      return fetch(url).then((res) => {
        if (!res.ok) throw new Error("Failed to fetch robots.txt");
        return res.text();
      });
    });
    let robots;
    const userAgent = "WatchDutyCrawler/0.1";
    if (robotsUrl) {
      try {
        const res = await fetch(robotsUrl);
        const robotsTxt = await res.text();
        robots = robotsParser.default(robotsUrl, robotsTxt);
        console.log("robots.txt loaded");
      } catch (e) {
        console.log("robots.txt取得失敗", e);
      }
    }

    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.setExtraHTTPHeaders({
      "User-Agent":
        "WatchDutyCrawler/0.1 (+https://github.com/chao7150/watch-duty-crawler)",
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
      console.log(
        `[${requestCount}] Fetching: ${url} (visited: ${visited.size}, queue: ${toVisit.length})`
      );
      await new Promise((res) => setTimeout(res, 2000));

      try {
        await Promise.race([
          page.goto(url, { waitUntil: "networkidle" }),
          new Promise((res) => setTimeout(res, 10000)),
        ]);
        const title = await page.title();
        const rawHtml = await page.content();
        let textContent = "";
        try {
          const dom = new JSDOM(rawHtml);
          const reader = new Readability(dom.window.document);
          const article = reader.parse();
          if (article && article.textContent) {
            textContent = article.textContent
              .split("\n")
              .map((line) => line.trim())
              .filter((line) => line.length > 0)
              .join("\n");
          }
        } catch (e) {
          textContent = "";
        }
        const normalizedRoot = rootUrl.endsWith("/") ? rootUrl : rootUrl + "/";
        let relativePath = url.startsWith(normalizedRoot)
          ? url.slice(normalizedRoot.length - 1)
          : url;
        results.push({
          title,
          content: textContent,
          relativePath,
        });
        console.log(`[${requestCount}] Success: ${title}`);

        const links = await page.$$eval("a[href]", (els: any) =>
          els.map((el: any) => el.href)
        );
        for (const href of links) {
          try {
            const next = new URL(href, url);
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
            const isImage = imageExts.some((ext) =>
              next.pathname.toLowerCase().endsWith(ext)
            );
            let normalizedUrl = next.toString();
            if (next.hash && next.hash.startsWith("#")) {
              // フラグメントを除去
              next.hash = "";
              normalizedUrl = next.toString();
            }
            // robots.txtクロール可否判定
            let isAllowed = true;
            if (robots) {
              isAllowed = robots.isAllowed(normalizedUrl, userAgent) !== false;
            }
            if (
              next.hostname === root.hostname &&
              next.pathname.startsWith(root.pathname) &&
              !visited.has(normalizedUrl) &&
              !isImage &&
              isAllowed
            ) {
              toVisit.push(normalizedUrl);
            }
          } catch {
            // 無効なURLはスキップ
          }
        }
      } catch (e) {
        console.log(`[${requestCount}] Failed: ${url} (${e})`);
      }
    }
    await browser.close();
    return results;
  },
};
