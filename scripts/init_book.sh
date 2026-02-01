#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-}"
if [[ -z "${NAME}" ]]; then
  echo "Usage: scripts/init_book.sh <book_repo_name>"
  exit 1
fi

ROOT="$(pwd)"
DEST="${ROOT%/}/${NAME}"

if [[ -e "${DEST}" ]]; then
  echo "ERR: ${DEST} already exists."
  exit 2
fi

echo "==> Creating new book skeleton at: ${DEST}"
mkdir -p "${DEST}"

# Copy core skeleton (adjust as needed)
for d in ai assets bin config docs manuscript metadata scripts templates tools .github; do
  if [[ -e "${ROOT}/${d}" ]]; then
    mkdir -p "${DEST}/${d}"
    rsync -a --exclude ".git" --exclude "build" --exclude "site" --exclude "release_bundle*" \
      "${ROOT}/${d}/" "${DEST}/${d}/"
  fi
done

# Ensure workflows dir exists
mkdir -p "${DEST}/.github/workflows"

# Write aligned .gitignore
cat > "${DEST}/.gitignore" <<'EOF'
# Build outputs
build/
site/
release_bundle/
release_bundle_*.tar.gz

# Allow QA baselines
!build/**/qa_baseline.json
!build/**/qa_report.json

# Tools
tools/epubcheck/epubcheck.jar

# Python
.venv/
__pycache__/
*.pyc

# OS / Editor
.DS_Store
Thumbs.db
.vscode/
.idea/
EOF

# If template repo has the aligned workflow, copy it; else create a sensible default
if [[ -f "${ROOT}/.github/workflows/build.yml" ]]; then
  cp -f "${ROOT}/.github/workflows/build.yml" "${DEST}/.github/workflows/build.yml"
fi

# Add release notes generator (if present in template)
if [[ -f "${ROOT}/scripts/gen_release_notes.sh" ]]; then
  cp -f "${ROOT}/scripts/gen_release_notes.sh" "${DEST}/scripts/gen_release_notes.sh"
  chmod +x "${DEST}/scripts/gen_release_notes.sh"
fi

# Fix README title if exists
if [[ -f "${DEST}/README.md" ]]; then
  perl -i -pe "s/^# .*/# ${NAME}/" "${DEST}/README.md" || true
fi

# Initialize git repo
(
  cd "${DEST}"
  if [[ ! -d ".git" ]]; then
    git init -q
    git branch -M main
  fi
)

cat <<EOF

==> DONE: ${NAME}

Next steps (recommended):
  cd ${DEST}
  git config user.name "sara-protocol"
  git config user.email "admin@sara-protocol.com"

  # local smoke test
  make LANG=zh all
  make LANG=en all

  # create QA baseline snapshots (then allow commit with -f)
  make LANG=zh baseline-init
  make LANG=en baseline-init

  git add -A
  git commit -m "chore: initialize ${NAME} skeleton"
  git remote add origin git@github.com:sara-protocol/${NAME}.git
  git push -u origin main

  # release
  git tag v0.1.0
  git push origin v0.1.0

GitHub settings:
  Settings → Pages → Source = GitHub Actions
  Settings → Actions → Workflow permissions = Read and write
EOF
