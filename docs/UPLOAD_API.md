# 平台上传（KDP / Apple Books）— v3.1

## Apple Books（官方支持：Transporter / iTMSTransporter）
ACRE 走 Apple 官方命令行上传路径：Transporter / iTMSTransporter。
你需要有 Apple Books 交付权限的账号，并使用 `.itmsp` 包上传。

### 环境变量
- `ACRE_APPLE_USER`：Apple 账号（通常是邮箱）
- `ACRE_APPLE_PASS`：建议使用 app-specific password
- `ACRE_APPLE_ITMSP`：`.itmsp` 路径（默认 `build/apple_books`）

### 执行
```bash
ACRE_APPLE_USER="you@example.com" ACRE_APPLE_PASS="xxxx-xxxx-xxxx-xxxx" \
  python3 scripts/upload_apple_books.py
```

## Amazon KDP（说明：无公开、官方支持的上传 API）
KDP 上传（eBook / paperback / hardcover）通过网页 Bookshelf 完成。
ACRE 不做“网页自动化上传”以避免账号/合规风险。

ACRE 提供的是 **KDP Ready Bundle**：
- `build/<lang>/kdp_bundle/`
  - `book.epub` / `book.pdf` / `cover.jpg`（若存在）
  - `kdp_metadata.json`（可扩展）

生成：
```bash
python3 scripts/upload_kdp.py
```
