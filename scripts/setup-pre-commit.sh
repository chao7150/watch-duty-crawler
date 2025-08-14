#!/bin/sh
# Biome lint/formatをコミット前に自動実行するpre-commitフックをセットアップ

HOOK_PATH=".git/hooks/pre-commit"

cat <<'EOF' > "$HOOK_PATH"
#!/bin/sh
npm run biome:all
if [ $? -ne 0 ]; then
  echo "Biomeのlint/formatに失敗しました。コミットを中断します。"
  exit 1
fi
EOF

chmod +x "$HOOK_PATH"
echo "pre-commit hookをセットアップしました。"
