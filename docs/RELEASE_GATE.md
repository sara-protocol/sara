# Release Gate（v3.0）

命令：
```bash
make release
```

只有当以下条件全部满足：
- Readiness ≥ threshold
- QA 全绿（无 fail）
- baseline 无回退

才会：
1. 打 git tag
2. 生成发布工件（PDF / EPUB / DOCX）
3. （可选）上传到发布平台

## 配置
```text
config/release_gate.yml
```

## 上传
默认关闭（upload.enabled=false）。
你可以在这里接入：
- Amazon KDP API
- Apple Books API

## 设计原则
- Release = 决策，不是构建
- 所有 gate 都可审计
- 永不 silent release
