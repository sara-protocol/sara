#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-}"
OWNER="${2:-sara-protocol}"     # 需要时可改
TEMPLATE_DIR="$(pwd)"

if [[ -z "$NAME" ]]; then
  echo "Usage: scripts/init_book.sh <repo_name> [owner]"
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh (GitHub CLI) not found."
  exit 2
fi

# 1) 复制模板 -> 新目录（排除 .git 与构建产物）
DEST="${TEMPLATE_DIR}/../${NAME}"
if [[ -e "$DEST" ]]; then
  echo "ERROR: destination exists: $DEST"
  exit 2
fi

rsync -a --delete \
  --exclude '.git/' \
  --exclude 'build/' \
  --exclude 'site/' \
  --exclude 'release_bundle*/' \
  --exclude '*.tar.gz' \
  "${TEMPLATE_DIR}/" "${DEST}/"

cd "${DEST}"

# 2) 初始化 git（干净起步）
rm -rf .git
git init
git branch -M main

# 3) 基础改名（可按你模板里 metadata 的结构再扩展）
#    - README: 替换标题里 sara -> book name（很保守）
if [[ -f README.md ]]; then
  perl -i -pe "s/\bsara\b/${NAME}/g if \$. <= 5" README.md || true
fi

# 4) 让 Pages workflow 可用：确保 workflow 文件存在
test -f .github/workflows/build.yml

# 5) 首次构建（可选：失败也不拦）
make dashboard >/dev/null 2>&1 || true
make site >/dev/null 2>&1 || true

# 6) 首次提交
git add -A
git commit -m "chore: init ${NAME} from ACRE Publishing OS template" >/dev/null

# 7) 创建 GitHub 私有仓库 + push
#    gh repo create 会自动加 origin 并 push（如果 --push）
gh repo create "${OWNER}/${NAME}" --private --source . --remote origin --push

# 8) 开启 Pages：build_type=workflow（让 Actions deploy-pages 生效）
#    POST 不存在时创建；已存在则 PUT 更新为 workflow
if gh api -X POST "repos/${OWNER}/${NAME}/pages" -f build_type=workflow >/dev/null 2>&1; then
  :
else
  gh api -X PUT "repos/${OWNER}/${NAME}/pages" -f build_type=workflow >/dev/null 2>&1 || true
fi

# 9) 输出访问地址（注意：private repo 的 Pages 是否可访问取决于你的 GitHub 计划/组织设置）
echo
echo "✅ Repo: https://github.com/${OWNER}/${NAME}"
echo "🌐 Pages: https://${OWNER}.github.io/${NAME}/"
echo
echo "Next:"
echo "  - push main => Pages 自动部署（Actions）"
echo "  - tag vx.y.z => 构建 artifacts（用于 Releases 一键下载）"
