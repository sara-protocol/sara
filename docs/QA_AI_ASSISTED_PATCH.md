# AI-assisted Patch（v2.6）

v2.6 起，QA 引擎会为 `l1.todo_marker` 生成 **AI 辅助补丁建议**：
- 不自动写入
- 只提供 prompt + patch scaffold
- 人工确认后再 apply

## 你会得到什么？
在 `qa_report.json` 中，每个 TODO finding 会包含：
- `ai_prompt`：可直接复制到你常用的 LLM
- `patch`：安全的占位 diff（不会覆盖内容）

## 推荐工作流
1. 运行 QA：
```bash
make LANG=zh qa-strict
```

2. 提取 AI prompt：
```bash
jq -r '.findings[] | select(.ai_prompt!=null) | .ai_prompt' build/zh/qa_report.json
```

3. 把模型输出整理成最终段落

4. 应用 patch：
```bash
jq -r '.findings[] | select(.patch!=null) | .patch' build/zh/qa_report.json | git apply
```

5. 用生成的内容替换占位注释

## 原则
- AI = 写作助手，不是作者
- 所有 AI 内容必须人工 review
