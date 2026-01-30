#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run(cmd: list[str]) -> None:
    print(">>", " ".join(cmd))
    subprocess.run(cmd, check=True)

def merge_chapters(lang: str) -> Path:
    manuscript = ROOT / "manuscript" / lang
    build_dir = ROOT / "build" / lang
    build_dir.mkdir(parents=True, exist_ok=True)

    merged = build_dir / "book_merged.md"
    files = sorted(manuscript.glob("*.md"))
    if not files:
        raise SystemExit(f"No .md files found in {manuscript}")

    with merged.open("w", encoding="utf-8") as out:
        for p in files:
            out.write(f"\n\n<!-- BEGIN {p.name} -->\n\n")
            out.write(p.read_text(encoding="utf-8"))
            out.write(f"\n\n<!-- END {p.name} -->\n")
    print(f"==> merged: {merged}")
    return merged

def build_all(lang: str, merged: Path, pdf: bool, epub: bool, docx: bool) -> None:
    meta = ROOT / "metadata" / f"book.{lang}.yml"
    css = ROOT / "metadata" / "style.css"
    tex = ROOT / "templates" / "book.tex"
    ref = ROOT / "templates" / "reference.docx"
    out_dir = ROOT / "build" / lang

    do_any = pdf or epub or docx
    if (not do_any) or pdf:
        run([
            "pandoc", str(merged),
            "--metadata-file", str(meta),
            "--pdf-engine=xelatex",
            "--template", str(tex),
            "--output", str(out_dir / "book.pdf"),
        ])
    if (not do_any) or epub:
        run([
            "pandoc", str(merged),
            "--metadata-file", str(meta),
            "--css", str(css),
            "--toc", "--toc-depth=3",
            "--output", str(out_dir / "book.epub"),
        ])
    if (not do_any) or docx:
        run([
            "pandoc", str(merged),
            "--metadata-file", str(meta),
            "--reference-doc", str(ref),
            "--output", str(out_dir / "book.docx"),
        ])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="zh", choices=["zh","en"])
    ap.add_argument("--merge-only", action="store_true")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--epub", action="store_true")
    ap.add_argument("--docx", action="store_true")
    args = ap.parse_args()

    merged = merge_chapters(args.lang)
    if args.merge_only:
        return
    build_all(args.lang, merged, args.pdf, args.epub, args.docx)
    print("=== Build Complete ===")

if __name__ == "__main__":
    main()
