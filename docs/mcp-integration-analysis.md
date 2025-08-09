# OpenRouter API × Playwright MCP 統合実装の分析と推奨事項

## 現在の実装の分析

### 1. 実装済みの内容
- MCPクライアント基盤クラス（PlaywrightMCPClient）
- OpenRouter APIの基本的な統合（web検索機能付き）
- MCP toolsの型変換機能

### 2. 実装の問題点と課題

#### A. 誤解していた統合方法
最初に実装された方法では、OpenRouter APIのリクエスト内に直接MCPツールを含めようとしていましたが、これは正しくありません。

**間違った実装例:**
```python
# これは動作しません
data = {
    "model": "openai/gpt-4o-mini:online",
    "tools": await get_playwright_tools(),  # これは無効
    # ...
}
```

#### B. 正しい統合方法
OpenRouterのドキュメントによると、MCPは**クライアント側で管理される独立したサーバー**です。正しい統合方法は：

1. **別プロセスでMCPサーバーを起動**
2. **クライアント側でOpenRouter API + MCPサーバーを調整**
3. **OpenRouter APIからの応答でツール実行が必要な場合、MCPサーバーにリクエスト**

### 3. 推奨される実装アプローチ

#### Option A: OpenRouterのWeb検索機能を利用（推奨）
最も簡単で確実な方法は、OpenRouterの内蔵web検索機能を活用することです：

```python
data = {
    "model": "openai/gpt-4o-mini:online",  # `:online`でweb検索有効
    "web_search_options": {
        "search_context_size": "high",
        "max_search_results": 5
    },
    # プロンプトで明確にweb検索を指示
}
```

#### Option B: 将来的なMCP統合（高度）
より高度な制御が必要な場合は、OpenRouterのドキュメント例に従って実装：

```python
# 1. 別プロセスでPlaywright MCPサーバーを起動
# 2. OpenRouter APIでfunction callingを使用
# 3. tool callが必要な場合、MCPサーバーに個別リクエスト
# 4. 結果をOpenRouter APIに再投下
```

### 4. 現在の実装で十分な理由

アニメサブタイトル取得の用途では、以下の理由でOption Aで十分です：

1. **シンプルな検索タスク**: 複雑なブラウザ操作は不要
2. **公開情報**: アニメサブタイトルは通常公開されている
3. **信頼性**: OpenRouterの内蔵検索は安定している
4. **メンテナンス性**: 追加の依存関係やサーバー管理が不要

### 5. 実装推奨事項

#### 即座に実装すべきこと：
1. `ai_extractor_impl.py`でOpenRouterのweb検索機能を活用
2. プロンプトの改善（検索キーワードの明示）
3. エラーハンドリングの強化

#### 将来的に検討すべきこと：
1. より複雑なケース（認証が必要なサイトなど）でのMCP統合
2. スクレイピング機能の拡張時のPlaywright MCP利用

## 結論

現在の実装は正しい方向に向かっていますが、以下の調整が推奨されます：

1. **MCPツールの直接統合は削除**（OpenRouter APIには渡さない）
2. **OpenRouterのweb検索機能を最大活用**
3. **プロンプト最適化でより正確な結果を取得**

この方針により、実装の複雑性を下げつつ、目的（アニメサブタイトル取得）を効率的に達成できます。
