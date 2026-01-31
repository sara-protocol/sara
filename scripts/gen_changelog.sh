#!/usr/bin/env bash
set -e

# Usage: ./scripts/gen_changelog.sh v2.0.0
TAG="$1"
if [ -z "$TAG" ]; then
  echo "Usage: gen_changelog.sh <tag>"
  exit 1
fi

# Get previous tag (if exists)
PREV_TAG=$(git tag --sort=-version:refname | grep -v "^$TAG$" | head -n 1)

DATE=$(date -u +"%Y-%m-%d")

echo "## [$TAG] - $DATE"
echo

if [ -n "$PREV_TAG" ]; then
  RANGE="$PREV_TAG..$TAG"
else
  RANGE="$TAG"
fi

git log $RANGE --pretty=format:"- %s" | while read -r line; do
  case "$line" in
    -\ feat:*)
      echo "$line" | sed 's/- feat:/- **Feature:**/'
      ;;
    -\ fix:*)
      echo "$line" | sed 's/- fix:/- **Fix:**/'
      ;;
    -\ ci:*)
      echo "$line" | sed 's/- ci:/- **CI:**/'
      ;;
    -\ docs:*)
      echo "$line" | sed 's/- docs:/- **Docs:**/'
      ;;
    -\ chore:*)
      echo "$line" | sed 's/- chore:/- **Chore:**/'
      ;;
    *)
      echo "$line"
      ;;
  esac
done

echo
