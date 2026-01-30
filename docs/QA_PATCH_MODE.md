# Patch Mode（自动修复建议）

v2.5 起，QA 引擎会为以下规则生成 **可选 patch diff**：
- l1.todo_marker
- l1.broken_link

patch 不会自动应用，只作为建议输出在 qa_report.json 中。

## 使用方式
1. 运行 QA
```bash
make LANG=zh qa-strict
```
2. 查看 JSON
```bash
jq '.findings[] | select(.patch!=null)' build/zh/qa_report.json
```
3. 人工挑选 patch，应用：
```bash
git apply <(jq -r '.findings[].patch' build/zh/qa_report.json)
```

## 原则
- 永不自动写主分支
- patch = suggestion，不是强制修复
