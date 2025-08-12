# Copilot Instructions for This Project

## プロジェクトの目的
- アニメ公式サイトを対象に一次情報を効率的に検索できるシステムを構築する
- URLリストに基づき定期クロール、本文抽出、抄録生成、日本語全文検索を提供
- 著作権や倫理に配慮し、検索結果は URL + 短い抄録 のみ返す

## 実装時の重要ポイント
1. **クロール**
   - playwright を利用
   - robots.txt を必ず確認して遵守
   - Last-Modified/ETag を使い差分クロール

2. **本文抽出**
   - @mozilla/readability を使う
   - 役割分類（NEWS, EPISODE, ON-AIR, CHARACTER など）はURLパターンやキーワードで判定

3. **DB設計**
   - PostgreSQL + PGroonga で日本語全文検索
   - 主キーは `url`
   - 検索対象は `title` と `excerpt`（aliasesテーブルで同義語検索も可）

4. **API**
   - Fastifyで実装
   - `/search` エンドポイントはクエリパラメータ `q`, `role`, `from`, `to`, `site`, `size` を受け付ける
   - レスポンスは JSON 配列（URL, title, excerpt, published_at, role, site）

5. **倫理的配慮**
   - noindex ページは公開検索結果に含めない
   - 本文全文や画像は保存・配信しない
   - 出典元URLを必ず返す

6. **運用**
   - node-cron で定期クロール
   - pm2 または systemd で常駐
   - ログはJSON形式で出力（pino推奨）

## コーディングスタイル
- TypeScriptのstrictモード有効
- ESLint + Prettierで整形
- 関数・モジュールは小さく保つ（単一責任原則）
- 非同期処理は `async/await` を標準にする
- ECMAScript2023の時代のベストプラクティスに従う

## 優先すべきこと
- 精度の高い本文抽出
- 安定したクロール（対象サイトに負荷をかけない）
- 検索の応答速度（日本語形態素解析対応）
- コードの可読性と保守性
