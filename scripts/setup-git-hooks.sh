#!/bin/sh
# .githooks/pre-commit を .git/hooks/pre-commit にコピーして実行権限を付与
cp -f .githooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
echo "Git hooks have been set up."
