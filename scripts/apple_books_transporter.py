#!/usr/bin/env python3
"""Verify/upload Apple Books .itmsp via iTMSTransporter, with JSON receipts.

Env:
- ACRE_APPLE_MODE: verify|upload (default verify)
- ACRE_APPLE_USER / ACRE_APPLE_PASS: credentials
- ACRE_APPLE_ITMSP: path to a .itmsp or directory containing *.itmsp (default build/apple_books)
- ACRE_APPLE_RECEIPTS: receipts directory (default build/apple_books/receipts)
"""
import os, shutil, subprocess, json, time
from pathlib import Path
from datetime import datetime, timezone

def find_itms():
    if shutil.which("iTMSTransporter"):
        return "iTMSTransporter"
    cand = Path("/usr/local/itms/bin/iTMSTransporter")
    if cand.exists():
        return str(cand)
    raise SystemExit("iTMSTransporter not found. Install Transporter / iTMSTransporter.")

def scrub_cmd(cmd, pwd):
    # replace password for logging
    return ["***" if (pwd and x == pwd) else x for x in cmd]

def write_receipt(receipts_dir: Path, pkg: Path, mode: str, cmd_scrubbed, rc: int, stdout: str, stderr: str, started: float, ended: float):
    receipts_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = f"{pkg.stem}.{mode}.{ts}.json"
    out = receipts_dir / name
    data = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "package": str(pkg),
        "command": cmd_scrubbed,
        "returncode": rc,
        "duration_sec": round(ended - started, 3),
        "stdout": stdout,
        "stderr": stderr,
    }
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out

def main():
    mode = os.environ.get("ACRE_APPLE_MODE", "verify").strip().lower()
    user = os.environ.get("ACRE_APPLE_USER")
    pwd  = os.environ.get("ACRE_APPLE_PASS")
    if not user or not pwd:
        raise SystemExit("Missing ACRE_APPLE_USER / ACRE_APPLE_PASS env vars.")

    pkg_path = Path(os.environ.get("ACRE_APPLE_ITMSP","build/apple_books")).resolve()
    if not pkg_path.exists():
        raise SystemExit(f"Package path not found: {pkg_path}")

    receipts_dir = Path(os.environ.get("ACRE_APPLE_RECEIPTS","build/apple_books/receipts")).resolve()

    itms = find_itms()
    pkgs = [p for p in ([pkg_path] if pkg_path.suffix==".itmsp" else pkg_path.glob("*.itmsp"))]
    if not pkgs:
        raise SystemExit(f"No .itmsp packages found in {pkg_path}")

    if mode not in ("verify","upload"):
        raise SystemExit("ACRE_APPLE_MODE must be verify or upload")

    for p in pkgs:
        cmd = [itms, "-m", mode, "-f", str(p), "-u", user, "-p", pwd, "-v", "eXtreme"]
        cmd_scrub = scrub_cmd(cmd, pwd)
        print("[apple_books]", mode, ":", " ".join(cmd_scrub))
        started = time.time()
        r = subprocess.run(cmd, text=True, capture_output=True)
        ended = time.time()

        receipt = write_receipt(receipts_dir, p, mode, cmd_scrub, r.returncode, r.stdout or "", r.stderr or "", started, ended)
        print("[apple_books] receipt:", receipt)

        if r.returncode != 0:
            # echo short tail to console
            tail = (r.stderr or r.stdout or "").strip()[-1500:]
            print("[apple_books] transporter failed (tail):")
            print(tail)
            raise SystemExit(r.returncode)

    print("[apple_books] done")

if __name__ == "__main__":
    main()
