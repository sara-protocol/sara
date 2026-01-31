
# ACRE 出版基础设施 v2.0（Template Repo）

v2.0 目标：
- ✅ Hard QA 统一入口：`scripts/qa_strict.py`
- ✅ 多语言同源：`manuscript/zh` + `manuscript/en`
- ✅ AI 写作 CLI：`acre-ai draft ch05`
- ✅ CI：push/PR 自动构建 + 严苛 QA + artifacts

## 快速开始

### 1) 依赖（本地）
- Git
- Python 3
- Pandoc
- XeLaTeX（PDF）
- Java（EPUBCheck）
- poppler-utils（pdffonts）

Ubuntu/WSL:
```bash
sudo apt-get update
sudo apt-get install -y git python3 make pandoc   texlive-xetex texlive-fonts-recommended texlive-latex-recommended   fonts-noto-cjk default-jre poppler-utils
```

### 2) 构建（默认中文）
```bash
make all
```

### 3) 构建英文
```bash
make LANG=en all
```

### 4) AI 草稿（不会污染主稿）
```bash
./bin/acre-ai draft ch05 --lang zh --from outline
```

## 关键命令

- `make merge`：合并章节（按 chNN 文件名排序）
- `make qa`：L1 轻量 QA
- `make qa-strict`：L1 + EPUBCheck + PDF 字体嵌入 + 图片 DPI
- `make all`：qa-strict + pdf + epub + docx

生成日期：2026-01-29


## v2.1 新增
- YAML 可配置严苛 QA：`config/qa_rules.yml` + `config/language_exceptions.yml`
- acre-ai 章节流水线：outline → draft → review → apply


## v2.2 新增
- QA 分组 + 严重级别（warn/fail/off）
- glob 白名单/黑名单过滤（** 支持）


## v2.3 新增
- 每条规则独立 severity（fail|warn|off）
- Baseline 基线快照（只允许变好）
- JSON 报告输出（build/<lang>/qa_report.json）
cd ~/sara
cat > README.md <<'EOF'
# ACRE Publishing OS v2

**ACRE Publishing OS v2** is a production-grade, AI-assisted book publishing pipeline with **strict QA gates**, **multi-language single source**, and **multi-format output** (PDF / EPUB / DOCX).

It is designed for authors, publishers, and teams who treat book publishing as **engineering**, not ad-hoc document export.

---

## 🚀 What This Is

ACRE is not a demo.

It is a **fully working publishing operating system**, validated end-to-end on real servers and CI:

- ✅ Markdown → PDF / EPUB / DOCX
- ✅ zh / en multi-language from one source tree
- ✅ Strict, configurable QA gates
- ✅ AI-assisted writing workflow (without polluting main manuscript)
- ✅ GitHub Actions CI + GitHub Pages publication dashboard

**Live publication readiness dashboard:**  
👉 https://sara-protocol.github.io/sara/

---

## ✨ Core Features

### 📘 Multi-format Publishing
- PDF (XeLaTeX, font-embedded)
- EPUB (EPUBCheck-verified)
- DOCX (for editors & reviewers)

### 🌍 Multi-language, Single Source
- 
