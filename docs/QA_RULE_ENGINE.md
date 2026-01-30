# QA 规则引擎（YAML 可配置 v2）

严苛 QA 由 `scripts/qa_engine.py` 实现，配置来自：

- `config/qa_rules.yml`：阈值 / 分组严重级别(warn vs fail) / glob 过滤
- `config/language_exceptions.yml`：多语言章节编号例外表（尽量少用）

## 运行

```bash
make LANG=zh qa-strict
make LANG=en qa-strict
```

---

## 1) 分组与严重级别（warn vs fail）

在 `config/qa_rules.yml` 里配置 `groups`：

```yaml
groups:
  epubcheck:
    enabled: true
    severity: warn   # fail|warn|off
```

- `fail`：发现问题 → 退出码非 0（CI 失败）
- `warn`：发现问题 → 打印 WARN，但退出码 0（CI 不挡）
- `off`：跳过该组

> 推荐策略：上线初期先设为 warn，清零后再改成 fail。

---

## 2) 白名单/黑名单（glob）

所有过滤都用 POSIX 路径风格，支持 `*` 和 `**`。

### 2.1 忽略缺图（按图片路径）
```yaml
filters:
  missing_images:
    deny:
      - "assets/images/drafts/**"
      - "assets/images/legacy/*"
```

### 2.2 只检查某一类图（allow）
```yaml
filters:
  low_dpi_images:
    allow:
      - "assets/images/fig-*.png"
```

### 2.3 忽略断链（按 target 字符串匹配）
```yaml
filters:
  broken_links:
    deny:
      - "assets/tables/raw/**"
```

### 2.4 TODO/TBD 只检查某些章节
```yaml
filters:
  todo_markers:
    allow_chapters: ["ch0*"]
    deny_chapters: ["ch99"]
```

---

## 3) 兼容旧 ignore 字段

`ignore.*` 仍然生效，会自动合并到对应 `filters.*.deny`。
