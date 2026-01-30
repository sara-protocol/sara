#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

IMG_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
LINK_RE = re.compile(r'\[[^\]]+\]\(([^)]+)\)')

def is_url(s: str) -> bool:
    return s.startswith(("http://","https://","mailto:"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    args = ap.parse_args()

    md_path = Path(args.input).resolve()
    # build/<lang>/book_merged.md -> repo root is build/../..
    root = md_path.parent.parent.parent
    text = md_path.read_text(encoding="utf-8")

    errors = []
    for m in IMG_RE.finditer(text):
        target = m.group(1).strip()
        if is_url(target):
            continue
        p = (root / target).resolve()
        if not p.exists():
            errors.append(f"Missing image: {target} -> {p}")

    for m in LINK_RE.finditer(text):
        target = m.group(1).strip()
        if is_url(target) or target.startswith("#"):
            continue
        p = (root / target).resolve()
        if not p.exists():
            errors.append(f"Broken local link: {target} -> {p}")

    if "TODO" in text or "TBD" in text:
        errors.append("Found TODO/TBD markers in merged manuscript.")

    if errors:
        print("=== QA FAILED ===")
        for e in errors:
            print(" -", e)
        raise SystemExit(2)
    print("=== QA PASSED ===")

if __name__ == "__main__":
    main()
