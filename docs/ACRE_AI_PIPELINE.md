# acre-ai 章节级流水线（outline → draft → review → apply）

> acre-ai 不直接调用任何模型：它负责把 AI 写作变成可审计、可回滚、可合并的工程流程。
> 你可以把 scaffold 内容复制到你常用的模型工具里生成输出，再粘回文件继续流水。

## 目录结构
```text
ai/
  prompts/
  work/<lang>/<chNN>/
    outline.md
    draft.md
    patch.diff
    review.md
```

## 流程

### 1) outline（可选）
```bash
./bin/acre-ai outline ch05 --lang zh
```
生成：`ai/work/zh/ch05/outline.md`

### 2) draft
```bash
./bin/acre-ai draft ch05 --lang zh --from rewrite
```
生成：`ai/work/zh/ch05/draft.md`
把模型输出粘到文件底部 `AI Output` 区域。

### 3) review
```bash
./bin/acre-ai review ch05 --lang zh
```
生成：
- `patch.diff`（统一 diff）
- `review.md`（检查清单）

### 4) apply（唯一会改 manuscript 的命令）
```bash
./bin/acre-ai apply ch05 --lang zh --yes
```

> 安全阀：没有 `--yes` 就不会写入主稿。

## 推荐实践
- `apply` 后立刻跑：`make LANG=zh qa-strict`
- 通过后再 `git commit`
