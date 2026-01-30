# 章节完成度 Dashboard

展示每章：
- TODO 数量
- AI 覆盖率（TODO 中有 AI prompt 的比例）
- QA 状态（fail / warn / pass）

## 生成
```bash
make dashboard
```

产物：
- build/dashboard.json（机器可读）
- build/dashboard.html（静态可视化）

## 指标解释
- TODO：当前章未完成占位
- AI Covered：已有 AI 写作建议的 TODO
- QA Status：
  - ❌ 有 fail
  - ⚠️ 只有 warn
  - ✅ 全通过
