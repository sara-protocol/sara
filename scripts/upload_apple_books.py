#!/usr/bin/env python3
"""Apple Books upload via iTMSTransporter (Transporter CLI).

Requires:
- Transporter installed (iTMSTransporter available in PATH or /usr/local/itms/bin/iTMSTransporter)
- Apple account with Apple Books / iTunes Connect delivery permissions
- Credentials via env:
    ACRE_APPLE_USER
    ACRE_APPLE_PASS   (app-specific password recommended)

Input:
- .itmsp package directory or a folder containing .itmsp packages
"""
import os, shutil, subprocess
from pathlib import Path

def find_itms():
    if shutil.which("iTMSTransporter"):
        return "iTMSTransporter"
    cand = Path("/usr/local/itms/bin/iTMSTransporter")
    if cand.exists():
        return str(cand)
    raise SystemExit("iTMSTransporter not found. Install Transporter / iTMSTransporter.")

def main():
    user = os.environ.get("ACRE_APPLE_USER")
    pwd  = os.environ.get("ACRE_APPLE_PASS")
    if not user or not pwd:
        raise SystemExit("Missing ACRE_APPLE_USER / ACRE_APPLE_PASS env vars.")

    pkg = Path(os.environ.get("ACRE_APPLE_ITMSP","build/apple_books")).resolve()
    if not pkg.exists():
        raise SystemExit(f"Package path not found: {pkg}")

    itms = find_itms()

    pkgs = [p for p in ([pkg] if pkg.suffix==".itmsp" else pkg.glob("*.itmsp"))]
    if not pkgs:
        raise SystemExit(f"No .itmsp packages found in {pkg}")

    for p in pkgs:
        cmd = [itms, "-m", "upload", "-f", str(p), "-u", user, "-p", pwd, "-v", "eXtreme"]
        print("[apple_books] upload:", " ".join(cmd[:-2] + ["***"]))
        r = subprocess.run(cmd)
        if r.returncode != 0:
            raise SystemExit(r.returncode)

    print("[apple_books] done")

if __name__ == "__main__":
    main()
