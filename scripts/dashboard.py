#!/usr/bin/env python3
"""ACRE Chapter Completion Dashboard + Readiness Score"""
import json
from pathlib import Path
from datetime import datetime

LANGS = ["zh", "en"]

def load_report(lang):
    p = Path(f"build/{lang}/qa_report.json")
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))

def load_cfg():
    import yaml
    return yaml.safe_load(Path("config/readiness.yml").read_text())

def main():
    cfg = load_cfg()
    dashboard = {
        "generated_at": datetime.utcnow().isoformat(),
        "chapters": {},
        "readiness": {}
    }

    total_todo = total_fail = total_warn = total_ai = total_todo_with_ai = 0

    for lang in LANGS:
        report = load_report(lang)
        if not report:
            continue

        for f in report.get("findings", []):
            ch = f.get("file","unknown").split("-",1)[0]
            entry = dashboard["chapters"].setdefault(ch, {"langs": {}})
            le = entry["langs"].setdefault(lang, {"todo":0,"ai":0,"fail":0,"warn":0})

            if f["rule_id"] == "l1.todo_marker":
                le["todo"] += 1
                total_todo += 1
                if f.get("ai_prompt"):
                    le["ai"] += 1
                    total_todo_with_ai += 1
            if f["severity"] == "fail":
                le["fail"] += 1
                total_fail += 1
            if f["severity"] == "warn":
                le["warn"] += 1
                total_warn += 1

    # Compute readiness score
    score = 100
    w = cfg["weights"]

    score -= min(score, total_todo * w["todo"])
    score -= min(score, total_fail * w["qa_fail"])
    score -= min(score, total_warn * w["qa_warn"])

    if total_todo > 0:
        coverage = total_todo_with_ai / max(1, total_todo)
        score += int(coverage * w["ai_coverage"])

    if total_fail > 0:
        score = min(score, cfg["floors"]["with_any_fail"])

    score = max(0, min(100, score))

    dashboard["readiness"] = {
        "score": score,
        "total_todo": total_todo,
        "total_qa_fail": total_fail,
        "total_qa_warn": total_warn,
        "ai_coverage_ratio": round((total_todo_with_ai / max(1,total_todo)),2) if total_todo else 1.0
    }

    out_json = Path("build/dashboard.json")
    out_json.write_text(json.dumps(dashboard, indent=2), encoding="utf-8")

    # HTML
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"/>
<title>ACRE Readiness</title>
<style>
body {{ font-family: sans-serif; }}
.score {{ font-size: 48px; font-weight: bold; }}
</style>
</head>
<body>
<h1>Publication Readiness</h1>
<div class="score">{score} / 100</div>
<ul>
<li>Total TODO: {total_todo}</li>
<li>Total QA Fail: {total_fail}</li>
<li>Total QA Warn: {total_warn}</li>
<li>AI Coverage: {dashboard['readiness']['ai_coverage_ratio']}</li>
</ul>
</body></html>"""
    Path("build/readiness.html").write_text(html, encoding="utf-8")

    print("Readiness score:", score)

if __name__ == "__main__":
    main()
