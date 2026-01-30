# 严苛版 QA（qa_strict.py）使用说明

## 1) 依赖
- Java（EPUBCheck）
- poppler-utils（pdffonts）
- Pillow（图片 DPI）

Ubuntu:
```bash
sudo apt-get install -y default-jre poppler-utils
python3 -m pip install pillow
```

## 2) 安装 EPUBCheck（一次性）
将 epubcheck jar 放到：
```text
tools/epubcheck/epubcheck.jar
```

推荐做法（示例）：
1. 从 W3C EPUBCheck Releases 下载 zip
2. 解压后把 `epubcheck.jar` 复制到上述位置

## 3) 运行
```bash
make LANG=zh qa-strict
make LANG=en qa-strict
```

## 4) 常用开关
- 跳过 epubcheck：
  ```bash
  python3 scripts/qa_strict.py --lang zh --skip-epubcheck
  ```
- 调低 DPI 阈值（仅屏幕书）：
  ```bash
  python3 scripts/qa_strict.py --lang zh --min-dpi 150
  ```
