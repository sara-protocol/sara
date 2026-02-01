#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   scripts/template_update.sh sara-protocol/sara main
#
# In a book repo:
#   make template-update

TEMPLATE_REPO="${1:-sara-protocol/sara}"
TEMPLATE_REF="${2:-main}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: git is required" >&2
  exit 2
fi
if ! command -v rsync >/dev/null 2>&1; then
  echo "ERROR: rsync is required" >&2
  exit 2
fi

TMP="$(mktemp -d)"
cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

SYNC_CFG="$ROOT/config/template_sync.yml"
if [[ ! -f "$SYNC_CFG" ]]; then
  echo "ERROR: missing config/template_sync.yml" >&2
  exit 2
fi

readarray -t INCLUDE < <(awk '
  $1=="include:"{in=1; next}
  $1=="exclude:"{in=0}
  in && match($0, /^[[:space:]]*-[[:space:]]*(.+)$/, a){print a[1]}
' "$SYNC_CFG")

readarray -t EXCLUDE < <(awk '
  $1=="exclude:"{in=1; next}
  in && match($0, /^[[:space:]]*-[[:space:]]*(.+)$/, a){print a[1]}
' "$SYNC_CFG")

echo "==> Fetching template: $TEMPLATE_REPO@$TEMPLATE_REF"
git clone --depth 1 --branch "$TEMPLATE_REF" "https://github.com/${TEMPLATE_REPO}.git" "$TMP/template" >/dev/null

T_SHA="$(cd "$TMP/template" && git rev-parse --short HEAD)"
echo "==> Template HEAD: $T_SHA"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: working tree is not clean. Commit/stash first." >&2
  exit 2
fi

echo "==> Sync allowed paths..."
for p in "${INCLUDE[@]}"; do
  src="$TMP/template/$p"
  if [[ ! -e "$src" ]]; then
    echo "WARN: template missing path: $p (skip)"
    continue
  fi
  mkdir -p "$(dirname "$ROOT/$p")"
  rsync -a --delete "$src" "$ROOT/$(dirname "$p")/"
done

for p in "${EXCLUDE[@]}"; do
  if [[ -e "$ROOT/$p" ]]; then
    :
  fi
done

chmod +x "$ROOT/scripts/"*.sh 2>/dev/null || true
chmod +x "$ROOT/bin/"* 2>/dev/null || true

git add -A

if git diff --cached --quiet; then
  echo "==> No template changes to apply."
  exit 0
fi

echo "==> Commit template sync"
git commit -m "chore(template): sync from ${TEMPLATE_REPO}@${T_SHA}"

echo "==> Smoke test (zh pdf + site). Fail => abort and rollback."
PREV="$(git rev-parse HEAD~1)"

set +e
make LANG=zh pdf
PDF_RC=$?
if [[ $PDF_RC -ne 0 ]]; then
  echo "ERROR: smoke test failed at LANG=zh pdf" >&2
  git reset --hard "$PREV" >/dev/null
  exit 3
fi

make site
SITE_RC=$?
if [[ $SITE_RC -ne 0 ]]; then
  echo "ERROR: smoke test failed at site" >&2
  git reset --hard "$PREV" >/dev/null
  exit 3
fi
set -e

echo "✅ Template sync + smoke test OK."
echo "Next: git push"
