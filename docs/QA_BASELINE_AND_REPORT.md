# QA 基线快照（baseline）+ JSON 报告

本仓库的严苛 QA 已支持：
1) **每条规则独立 severity**（fail|warn|off）
2) **基线快照模式**（第一次生成 baseline，后续只允许变好不允许变差）
3) **JSON 报告输出**（给 CI/Dashboard/PR 注释）

---

## 1) 每条规则独立 severity

在 `config/qa_rules.yml` 配置：

```yaml
rule_severity:
  l1.broken_link: warn
  l1.todo_marker: warn
  epubcheck.validation: fail
```

规则 ID（rule_id）会出现在：
- 控制台输出
- JSON 报告

---

## 2) 基线快照模式

### 2.1 生成 baseline（第一次）
```bash
make LANG=zh baseline-init
make LANG=en baseline-init
```

会生成：
- `config/qa_baseline.zh.json`
- `config/qa_baseline.en.json`

### 2.2 执行严格 QA（对比 baseline）
```bash
make LANG=zh qa-strict
```

对比逻辑（只允许变好）：
- baseline 里存在、现在消失 → ✅ 改善（允许）
- baseline 里存在、现在仍存在 → ✅ 不算变差
- baseline 里不存在、现在新增 → ❌ 回归（regression）

> 注意：即使 severity 被你从 warn 改成 fail，也会被视为“策略变化”，不是内容回归。
> 回归判断依赖 fingerprint（与 severity 无关）。

### 2.3 baseline 缺失时行为
`baseline.strict=false`（默认）：
- baseline 文件不存在 → 不启用 baseline（但输出 JSON 报告）
`baseline.strict=true`：
- baseline 文件不存在 → 直接失败，强制你先 init baseline

---

## 3) JSON 报告

默认输出到：
- `build/<lang>/qa_report.json`

内容包括：
- findings（每条含 rule_id、severity、fingerprint、message、evidence）
- baseline 比对结果（regressions / improvements / unchanged）

你可以在 CI 里拿这个 JSON 做 PR 评论或 dashboard。
