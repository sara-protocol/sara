#!/usr/bin/env python3
"""KDP 'upload' hook.

Important:
Amazon KDP does not provide a public, supported API for uploading book manuscripts.
This script therefore:
- prepares a KDP-ready bundle (EPUB/PDF + cover + metadata)
- prints a deterministic manual checklist

If you choose to use browser automation/scraping, do it outside this repo and accept the risk
(TOS/account bans). This repo stays on the safe, supported path.
"""
from pathlib import Path
import json

def main():
    lang = "zh"
    bundle = Path(f"build/{lang}/kdp_bundle")
    bundle.mkdir(parents=True, exist_ok=True)

    for f in [f"build/{lang}/book.epub", f"build/{lang}/book.pdf", f"build/{lang}/cover.jpg"]:
        p = Path(f)
        if p.exists():
            (bundle/p.name).write_bytes(p.read_bytes())

    meta = {
        "title": "TODO_TITLE",
        "author": "TODO_AUTHOR",
        "description": "TODO_DESCRIPTION",
        "keywords": ["TODO"],
        "categories": ["TODO"],
        "language": lang,
    }
    (bundle/"kdp_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print("[kdp] Prepared bundle:", bundle)
    print("[kdp] Manual upload required (no public supported KDP upload API).")
    print("[kdp] Next: KDP Bookshelf → Edit eBook/Paperback Content → Upload manuscript/cover.")

if __name__ == "__main__":
    main()
