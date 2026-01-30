#!/usr/bin/env python3
"""ACRE Release Gate v3.0

Enforces:
- readiness >= threshold
- QA all green
- baseline no regression

Then:
- git tag
- build artifacts
- optional upload hooks
"""
import json, subprocess, sys
from pathlib import Path
import yaml

def die(msg):
    print("=== RELEASE BLOCKED ===")
    print(msg)
    sys.exit(2)

def run(cmd):
    r = subprocess.run(cmd, text=True, capture_output=True)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        die(f"Command failed: {' '.join(cmd)}")
    return r.stdout.strip()

root = Path(__file__).resolve().parent.parent
cfg = yaml.safe_load((root/"config/release_gate.yml").read_text())

# Load readiness
dash = json.loads((root/"build/dashboard.json").read_text())
score = dash["readiness"]["score"]

if score < cfg["readiness_threshold"]:
    die(f"Readiness {score} < threshold {cfg['readiness_threshold']}")

# QA all green already enforced by qa-strict exit code, but double-check
if cfg["require"]["qa_all_green"]:
    if dash["readiness"]["total_qa_fail"] > 0:
        die("QA failures present")

# Baseline regression check via qa_report.json
for lang in ["zh","en"]:
    p = root/f"build/{lang}/qa_report.json"
    if not p.exists(): continue
    r = json.loads(p.read_text())
    diff = r.get("baseline",{}).get("diff",{})
    if diff.get("regressions"):
        die(f"Baseline regression detected in {lang}")

# Build artifacts
run(["make","all"])

# Tagging
version = (root/cfg["tag"]["source"]).read_text().strip()
tag = f"{cfg['tag']['prefix']}{version}"
run(["git","tag",tag])
print(f"Tagged {tag}")

# Upload hooks (mock)
# Apple Books (independent) preflight: generate package + verify
if cfg["upload"]["enabled"] and ("apple_books" in cfg["upload"]["targets"]):
    run(["make","apple-books-package"])
    run(["make","apple-books-verify"])

if cfg["upload"]["enabled"]:
    for t in cfg["upload"]["targets"]:
        print(f"[UPLOAD] {t} (hook placeholder)")

print("=== RELEASE SUCCESS ===")
print(f"Version {tag} is ready for publication.")
