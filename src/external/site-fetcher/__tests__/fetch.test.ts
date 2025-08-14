import assert from "node:assert";
import { writeFileSync } from "node:fs";
import { createServer } from "node:http";
import test from "node:test";
import { service } from "../index.js";
import type { Site } from "../../../domain.js";

const createHtml = (title: string, to: string[]) =>
	`<!DOCTYPE html><html><head><title>${title}</title></head><body>${to.map(createAnchorTo).join("")}</body></html>`;
const createAnchorTo = (to: string) => `<a href="${to}">${to}</a>`;

const routing = {
	"robots.txt":
		"User-agent: Googlebot\nDisallow: /googlebotForbidden\nUser-agent: watch-duty-crawler\nDisallow: /wdcForbidden\nDisallow: /forbidden\nUser-agent: *\nDisallow: /forbidden",
	"": createHtml("root", [
		"href",
		"forbidden",
		"googlebotForbidden",
		"wdcForbidden",
	]),
	href: createHtml("href", ["hrefRecursive"]),
	hrefRecursive: createHtml("hrefRecursive", ["noindex"]),
	noindex: String.raw`<!DOCTYPE html><html><head><title>noindex</title></head><body><meta name="robots" content="noindex"><a href="nofollow" rel="nofollow">nofollow</a></body></html>`,
	nofollow: createHtml("nofollow", []),
	forbidden: createHtml("forbidden", []),
	googlebotForbidden: createHtml("googlebotForbidden", []),
	wdcForbidden: createHtml("wdcForbidden", []),
};

test("service.fetch gets titles recursively", async () => {
	const server = createServer((req, res) => {
		if (req.url === undefined) {
			res.writeHead(200, { "content-type": "text/html" });
			return res.end(routing[""]);
		}
		if (req.url.slice(1) in routing) {
			res.writeHead(200, { "Content-Type": "text/html" });
			return res.end(routing[req.url.slice(1) as keyof typeof routing]);
		}
		return res.end();
	});
	await new Promise<void>((resolve) => server.listen(0, resolve));
	const port = (server.address() as any).port;
	const rootUrl = `http://localhost:${port}/`;

	const site: Site = { rootUrl } as any;
	const pages = await service.fetch(site);

	// 結果検証
	const titles = pages.map((p) => p.title).sort();

	assert.ok(titles.includes("root"), "rootページが取得されていません");
	assert.ok(titles.includes("href"), "hrefページが取得されていません");
	assert.ok(
		titles.includes("hrefRecursive"),
		"hrefRecursiveページが取得されていません",
	);
	// noindexを持つページはnoindexフラグを立てる
	assert.ok(titles.includes("noindex"), "noindexページが取得されていません");
	assert.ok(
		pages.find((p) => p.title === "noindex")?.noindex,
		"noindexページのnoindexフラグが設定されていません",
	);
	// nofollowリンクの先にあるページは取得しない
	assert.equal(
		titles.includes("nofollow"),
		false,
		"nofollowリンクの先のページが取得されています",
	);
	// robots.txtで指定されたページは取得しない
	assert.equal(
		titles.includes("forbidden"),
		false,
		"robots.txtで禁止されたforbiddenページが取得されています",
	);
	// 他のUAの禁止ルールは関知しない
	assert.ok(
		titles.includes("googlebotForbidden"),
		"googlebotForbiddenページが取得されていません",
	);
	// 自分のUAの禁止ルールは遵守する
	assert.equal(
		titles.includes("wdcForbidden"),
		false,
		"robots.txtで禁止されたwdcForbiddenページが取得されています",
	);

	writeFileSync("fetch-result.json", JSON.stringify(pages, null, 2), "utf-8");
	server.close();
});
