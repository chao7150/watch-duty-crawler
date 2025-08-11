import test from "node:test";
import assert from "node:assert";
import { createServer } from "http";
import { writeFileSync } from "fs";
import { service } from "../index.js";
import type { Site } from "../../../domain.js";

const html = `
<!DOCTYPE html>
<html>
<head><title>Test Title</title></head>
<body>
  <a href="/page2">Page2</a>
</body>
</html>
`;

const html2 = `
<!DOCTYPE html>
<html>
<head><title>Second Page</title></head>
<body>
  <a href="/">Home</a>
</body>
</html>
`;

test("service.fetch gets titles recursively", async () => {
  // モックサーバー起動
  const server = createServer((req, res) => {
    if (req.url === "/page2") {
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(html2);
    } else {
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(html);
    }
  });
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const port = (server.address() as any).port;
  const rootUrl = `http://localhost:${port}/`;

  const site: Site = { rootUrl } as any;
  const pages = await service.fetch(site);

  // 結果検証
  const titles = (pages as Array<{ title: string }>).map((p) => p.title).sort();
  assert.ok(titles.includes("Test Title"));
  assert.ok(titles.includes("Second Page"));

  writeFileSync("fetch-result.json", JSON.stringify(pages, null, 2), "utf-8");
  server.close();
});

// test("service.fetch gets titles from kaoruhana-anime.com", async () => {
//   const site: Site = { rootUrl: "https://kaoruhana-anime.com" } as any;
//   const pages = await service.fetch(site);

//   // 1ページ以上取得できていること
//   assert.ok(pages.length > 0);

//   const titles = pages.map((p) => p.title);
//   assert.ok(titles.some((t) => t.includes("薫る花は凛と咲く")));
// });

test("service.fetch gets titles from milkygalacticuniverse.com", async () => {
  const site: Site = {
    rootUrl: "https://www.tv-tokyo.co.jp/anime/pocketmonster2023/",
  } as any;
  const pages = await service.fetch(site);

  // 1ページ以上取得できていること
  assert.ok(pages.length > 0);

  const titles = pages.map((p) => p.title);
  assert.ok(
    titles.some((t) =>
      t.includes("スペシャル｜ポケットモンスター　テレビ東京アニメ公式")
    )
  );
  writeFileSync("fetch-result.json", JSON.stringify(pages, null, 2), "utf-8");
});
