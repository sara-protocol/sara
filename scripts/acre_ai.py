#!/usr/bin/env python3
"""acre-ai v2.7
Adds chapter-level TODO fill pipeline: outline -> draft -> review -> apply (TODO-only).
"""
import argparse, json
from pathlib import Path

def load_report(lang):
    p = Path(f"build/{lang}/qa_report.json")
    if not p.exists():
        raise SystemExit(f"qa_report.json not found for {lang}")
    return json.loads(p.read_text(encoding="utf-8"))

def cmd_fill(ch, lang):
    report = load_report(lang)
    todos = [
        f for f in report.get("findings", [])
        if f["rule_id"] == "l1.todo_marker" and f["file"].startswith(ch)
    ]
    outdir = Path(f"ai/fill/{lang}/{ch}")
    outdir.mkdir(parents=True, exist_ok=True)

    prompts = []
    for t in todos:
        prompts.append(t.get("ai_prompt",""))

    (outdir/"prompts.txt").write_text("\n\n---\n\n".join(prompts), encoding="utf-8")
    print(f"[acre-ai] Generated {len(prompts)} TODO prompts for {ch} ({lang})")
    print(f"[acre-ai] → {outdir}/prompts.txt")
    print("Paste AI outputs into patches manually; no auto-apply performed.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fill"])
    ap.add_argument("chapter")
    ap.add_argument("--lang", default="zh")
    args = ap.parse_args()

    if args.cmd == "fill":
        cmd_fill(args.chapter, args.lang)

if __name__ == "__main__":
    main()
