#!/usr/bin/env python3
"""Backward-compatible entrypoint for strict QA.

Use: `python3 scripts/qa_strict.py --lang zh`
Internally delegates to qa_engine.py (YAML rules engine).
"""
import subprocess
import sys
from pathlib import Path

def main():
    args = sys.argv[1:]
    repo_root = Path(__file__).resolve().parent.parent
    cmd = ["python3", str(repo_root / "scripts" / "qa_engine.py")] + args
    raise SystemExit(subprocess.run(cmd).returncode)

if __name__ == "__main__":
    main()
