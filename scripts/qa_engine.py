#!/usr/bin/env python3
"""ACRE Hard QA Engine v2.6
Adds AI-assisted patch suggestions for TODO markers (scaffold only).
"""
from __future__ import annotations
import argparse, fnmatch, hashlib, json, re, subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime, timezone

IMG_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
BEGIN_RE = re.compile(r'<!-- BEGIN (.*?) -->')

def sha1(s:str)->str:
    return hashlib.sha1(s.encode()).hexdigest()

def load_yaml(path:Path)->Dict[str,Any]:
    import yaml
    return yaml.safe_load(path.read_text())

def cfg_get(d, path, default=None):
    cur=d
    for p in path.split('.'):
        if not isinstance(cur,dict) or p not in cur: return default
        cur=cur[p]
    return cur

@dataclass
class Finding:
    rule_id:str
    severity:str
    message:str
    file:str
    line:int
    evidence:Dict[str,Any]
    fingerprint:str
    patch:str|None
    ai_prompt:str|None

class Engine:
    def __init__(self, root:Path, lang:str, rules:Dict[str,Any]):
        self.root=root; self.lang=lang; self.rules=rules
        self.findings:List[Finding]=[]
        self.build=root/'build'/lang
        self.merged=self.build/'book_merged.md'

    def sev(self, rule):
        return cfg_get(self.rules,'rule_severity',{}).get(rule,cfg_get(self.rules,'defaults.severity','fail'))

    def emit(self, rule, msg, file, line, ev, patch=None, ai_prompt=None):
        sev=self.sev(rule)
        if sev=='off': return
        fp=sha1(rule+file+str(line)+json.dumps(ev,sort_keys=True))
        self.findings.append(Finding(rule,sev,msg,file,line,ev,fp,patch,ai_prompt))

    def scan_l1(self):
        text=self.merged.read_text().splitlines()
        cur_file="unknown"; cur_start=0
        for i,line in enumerate(text, start=1):
            m=BEGIN_RE.match(line)
            if m:
                cur_file=m.group(1)
                cur_start=i
                continue

            # TODO with AI-assisted prompt
            if "TODO" in line or "TBD" in line:
                ai_prompt=f"""You are helping complete a book chapter.

Context:
- Language: {self.lang}
- File: {cur_file}
- Line number: {i-cur_start}
- Surrounding text:
{line}

Task:
Replace the TODO with a concise, accurate paragraph suitable for a technical book.
Do NOT invent data or citations. If uncertain, provide a neutral explanation or mark assumptions clearly.
"""
                patch=f"""--- a/manuscript/{self.lang}/{cur_file}
+++ b/manuscript/{self.lang}/{cur_file}
@@ -{i-cur_start},1 +{i-cur_start},1 @@
- {line}
+ <!-- AI SUGGESTION BELOW (REVIEW REQUIRED) -->
+ <!-- {line} -->
+ <!-- Paste approved content here -->
"""
                self.emit(
                    "l1.todo_marker",
                    "TODO/TBD found (AI-assisted suggestion available)",
                    cur_file,
                    i-cur_start,
                    {},
                    patch,
                    ai_prompt
                )

            # broken link auto-fix (same as v2.5)
            for m in LINK_RE.finditer(line):
                tgt=m.group(1)
                if tgt.startswith("http") or tgt.startswith("#"): continue
                patch=f"""--- a/manuscript/{self.lang}/{cur_file}
+++ b/manuscript/{self.lang}/{cur_file}
@@ -{i-cur_start},1 +{i-cur_start},1 @@
- {line}
+ {line.replace(tgt,'#FIXME_LINK')}
"""
                self.emit(
                    "l1.broken_link",
                    f"Broken link: {tgt}",
                    cur_file,
                    i-cur_start,
                    {"target":tgt},
                    patch,
                    None
                )

    def run(self):
        self.scan_l1()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--lang",default="zh")
    ap.add_argument("--config",default="config/qa_rules.yml")
    ap.add_argument("--json",default=None)
    args=ap.parse_args()

    root=Path(__file__).resolve().parent.parent
    rules=load_yaml(root/args.config)
    eng=Engine(root,args.lang,rules)
    eng.run()

    report={
      "meta":{"lang":args.lang,"time":datetime.now(timezone.utc).isoformat()},
      "findings":[asdict(f) for f in eng.findings]
    }

    out=Path(args.json) if args.json else root/f"build/{args.lang}/qa_report.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2))

    if any(f.severity=="fail" for f in eng.findings):
        raise SystemExit(2)

if __name__=="__main__":
    main()
