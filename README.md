# Official Anime Site Search Engine

## 概要
アニメ公式サイトのURLリストを基にクロールし、一次情報を整理・インデックス化して検索できるシステムです。  
URLと短い抄録（要約）のみを保存・公開し、著作権や運用ポリシーに配慮しています。  
検索結果はJSON APIおよびMCPサーバを通じて利用可能です。

## 主な機能
- **URLリスト管理**（人力+自動発見）
- **差分クロール**（robots.txt遵守、Last-Modified/ETag対応）
- **本文抽出・抄録生成**（200〜400字）
- **日本語全文検索**（PostgreSQL + PGroonga）
- **JSON API / MCPサーバ** 提供
- **倫理的配慮**：
  - noindexは公開検索で表示しない
  - 本文全文や画像は保存・配信しない
  - 出典URLを必ず明記

## 技術スタック
- **言語**: TypeScript (Node.js)
- **クロール**: playwright（必要時のみ）
- **本文抽出**: @mozilla/readability
- **DB**: PostgreSQL + PGroonga + Kysely + pg
- **API**: Fastify
- **スケジューラ**: node-cron
- **プロセス管理**: pm2 または systemd

## ディレクトリ構造（例）
```
project-root/
├── src/
│ ├── crawler/ # クロール・差分判定
│ ├── extractor/ # 本文抽出・抄録生成
│ ├── db/ # DB接続・検索クエリ
│ ├── api/ # Fastify APIルート
│ ├── mcp/ # MCPツール実装
│ └── utils/ # 共通処理
├── scripts/ # メンテ・一括処理用
├── config/ # 設定ファイル（URLリスト等）
├── README.md
└── copilot-instructions.md
```

```bash
# 依存関係インストール
sudo apt update && sudo apt install postgresql-client
npm install

# 開発用DB起動
sudo nerdctl compose -f container/compose.dev.yml up -d db

# 環境変数設定
cp .env.example .env
# POSTGRES_URL=postgres://...

# マイグレーション
npm run migrate

# 開発サーバ起動
npm run dev
```

## 倫理ポリシー
- robots.txt を尊重
- noindex ページは公開検索に出さない（内部DBでは保持可）
- 出典元を必ず表示
- 削除依頼には即時対応

## ライセンス
このプロジェクトのコードはMITライセンスで公開しますが、収集対象サイトのコンテンツには各権利者の著作権が帰属します。