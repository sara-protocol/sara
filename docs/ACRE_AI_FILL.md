# acre-ai fill（章节级 TODO 批量补全）

命令：
```bash
acre-ai fill ch03 --lang zh
```

作用：
- 读取 qa_report.json
- 仅提取该章节的 TODO findings
- 生成 **一组 AI 写作 prompt**
- 不修改 manuscript

输出：
```
ai/fill/<lang>/<chNN>/prompts.txt
```

## 推荐流程
1. 跑 QA
```bash
make LANG=zh qa-strict
```

2. 批量生成 TODO prompt
```bash
acre-ai fill ch03 --lang zh
```

3. 把 prompts.txt 交给 AI → 得到多个段落

4. 人工筛选 → 用 v2.6 的 patch scaffold 应用

## 设计边界
- 只补 TODO
- 不重写章节
- 不自动 apply
