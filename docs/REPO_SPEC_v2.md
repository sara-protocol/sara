# v2.0 Repo 目录规范（强制）

## 1) 单一事实源
- `manuscript/` 中的 Markdown 是唯一事实源
- 任何 AI 产出都必须落到 `ai/`，通过人工 review 再进入 `manuscript/`

## 2) 多语言同源结构
```text
manuscript/
  zh/
    ch01-*.md
    ch02-*.md
  en/
    ch01-*.md
    ch02-*.md
```

**绑定规则（硬规则）**
- 同一章节编号（chNN）在 zh/en 必须同时存在
- 不允许出现 zh 有 ch07 而 en 没有（除非在 `docs/LANG_EXCEPTIONS.md` 登记并解释）

## 3) 资产与模板
```text
assets/images/
assets/tables/
metadata/book.zh.yml
metadata/book.en.yml
metadata/style.css
templates/book.tex
templates/reference.docx
```

## 4) 构建输出（按语言分桶）
```text
build/
  zh/
    book.pdf
    book.epub
    book.docx
    book_merged.md
  en/
    ...
```

## 5) QA 分层
- `make qa`：L1（缺图/断链/TODO）
- `make qa-strict`：L1 + L2（EPUBCheck / PDF 字体嵌入 / 图片 DPI）
