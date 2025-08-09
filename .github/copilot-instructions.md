---
applyTo: "*.py"
---

# ディレクトリ構成と使用技術

- `src/watch_duty_crawler/` ... Pythonコード本体
  - `external/` ... 外部システムと通信する実装（ScriptExtractorImplなど）
  - `usecase/` ... ユースケース（ScriptExtractorなど）
- `tests/` ... テストコード

## 使用技術
- バックエンド: Python, FastAPI, Uvicorn
- テスト: pytest
- Lint: ruff
- 型チェック: mypy
- 仮想環境: venv

# 開発方針
- Uncle Bobのクリーンアーキテクチャの原則に従う
- t-wadaのTDDを実践する
- 仮想環境をactivateしてから開発する
- コードに変更を加えたら `make check-all` でテスト・型・lintを確認
