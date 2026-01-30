# Apple Books（独立作者 / 中文 / 无 ISBN）— v3.3

## 你得到的能力
- `.itmsp` 包名自动按版本号生成：`<package_name>-v<release/VERSION>.itmsp`
  - 例：`MyBook-v3.2.1.itmsp`
- Transporter verify/upload **落盘 JSON 回执**（可审计、可追踪）
  - 默认目录：`build/apple_books/receipts/`
- CI 最安全策略：PR 只 verify，main 才 upload

---

## 1) 填 metadata
编辑：`metadata/book.yml`
- title/author/description 必填
- isbn 留空即可（无 ISBN）
- package_name 设置包名前缀（不含版本号）
- epub_path 默认 `build/zh/book.epub`

---

## 2) 生成工件
```bash
make LANG=zh epub
```

---

## 3) 生成 .itmsp（自动附加版本号）
```bash
make apple-books-package
```
输出：
`build/apple_books/<package_name>-v<version>.itmsp/`

---

## 4) 校验（verify）
```bash
export ACRE_APPLE_USER="you@example.com"
export ACRE_APPLE_PASS="xxxx-xxxx-xxxx-xxxx"
make apple-books-verify
```

回执：
`build/apple_books/receipts/<pkg>.verify.<timestamp>.json`

---

## 5) 上传（upload）
```bash
make apple-books-upload
```

回执：
`build/apple_books/receipts/<pkg>.upload.<timestamp>.json`

---

## 6) Release Gate 自动上传（main 分支）
在 `config/release_gate.yml`：
```yaml
upload:
  enabled: true
  targets:
    - apple_books
```
然后：
```bash
make release
```
