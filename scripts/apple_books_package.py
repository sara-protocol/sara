#!/usr/bin/env python3
"""Generate Apple Books .itmsp package (Individual Publisher)

Target user: Independent author, single language (zh) and no ISBN (allowed).

Outputs:
  build/apple_books/<PackageName>.itmsp/
    metadata.xml
    assets/book.epub

Then use iTMSTransporter to verify/upload:
  iTMSTransporter -m verify -f <pkg.itmsp> -u $ACRE_APPLE_USER -p $ACRE_APPLE_PASS
  iTMSTransporter -m upload -f <pkg.itmsp> -u $ACRE_APPLE_USER -p $ACRE_APPLE_PASS
"""
from __future__ import annotations
from pathlib import Path
import shutil
import sys
import xml.sax.saxutils as sx

def load_yaml(path: Path):
    try:
        import yaml  # type: ignore
    except Exception:
        raise SystemExit("PyYAML not installed. Fix: python3 -m pip install pyyaml")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

def esc(s: str) -> str:
    return sx.escape(s, {'"': '&quot;'})

def main():
    root = Path(__file__).resolve().parent.parent
    meta = load_yaml(root / "metadata/book.yml")

    title = str(meta.get("title", "")).strip()
    author = str(meta.get("author", "")).strip()
    language = str(meta.get("language", "zh")).strip() or "zh"
    desc = str(meta.get("description", "")).strip()
    publisher = str(meta.get("publisher", "Independent")).strip()
    isbn = str(meta.get("isbn", "")).strip()  # optional

    apple = meta.get("apple_books", {}) or {}
    package_name = str(apple.get("package_name", "MyBook")).strip() or "MyBook"
    epub_rel = str(apple.get("epub_path", f"build/{language}/book.epub")).strip()
    epub = (root / epub_rel).resolve()

    if not title or not author or not desc:
        raise SystemExit("metadata/book.yml missing required fields: title/author/description")

    if not epub.exists():
        raise SystemExit(f"EPUB not found: {epub_rel} (run: make LANG={language} epub)")

    version = (root / "release" / "VERSION").read_text(encoding="utf-8").strip()
out_dir = root / "build" / "apple_books" / f"{package_name}-v{version}.itmsp"
    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    # Copy epub as book.epub
    shutil.copy2(epub, assets / "book.epub")

    # Minimal metadata.xml for independent author delivery.
    # Note: Apple exact schemas can vary; Transporter verify will be the source of truth.
    # We keep it minimal and standards-compliant, with no ISBN if blank.
    isbn_block = f"<isbn>{esc(isbn)}</isbn>" if isbn else ""

    metadata_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://apple.com/itunes/importer" version="book1.0">
  <book>
    <title>{esc(title)}</title>
    <author>{esc(author)}</author>
    <language>{esc(language)}</language>
    {isbn_block}
    <publisher>{esc(publisher)}</publisher>
    <description>{esc(desc)}</description>
    <assets>
      <asset type="book" filename="assets/book.epub"/>
    </assets>
  </book>
</package>
"""
    (out_dir / "metadata.xml").write_text(metadata_xml, encoding="utf-8")

    print(f"[apple-books] Package generated: {out_dir}")
    print(f"[apple-books] Next: make apple-books-verify (or apple-books-upload)")

if __name__ == "__main__":
    main()
