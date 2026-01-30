# v1.x → v2.0 迁移 SOP（可审计）

> 目标：零中断迁移，保证旧项目随时可回滚。

## Phase 0：准备
1. 从 v1.x 主分支切新分支：
   ```bash
   git checkout -b migrate/v2
   ```

2. 升级前跑一次：
   ```bash
   make all
   ```
   作为“迁移前基线”。

## Phase 1：目录迁移（不改内容）
1. 创建多语言目录：
   ```bash
   mkdir -p manuscript/zh manuscript/en
   ```

2. 把旧章节移动到中文桶：
   ```bash
   git mv manuscript/*.md manuscript/zh/
   ```

3. 复制一份英文占位（可先空壳）：
   ```bash
   for f in manuscript/zh/*.md; do cp "$f" "manuscript/en/$(basename $f)"; done
   git add manuscript/en
   ```

> 说明：先保证结构一致，内容可以之后再翻译。

## Phase 2：元数据拆分
1. 复制元数据：
   ```bash
   cp metadata/book.yml metadata/book.zh.yml
   cp metadata/book.yml metadata/book.en.yml
   ```
2. 修改 `lang` 和 title/author（按需）。

## Phase 3：构建系统升级
1. 替换/合并 Makefile 与 scripts（引入 LANG 和 qa_strict）。
2. 跑中文：
   ```bash
   make LANG=zh all
   ```
3. 跑英文：
   ```bash
   make LANG=en all
   ```

## Phase 4：启用严苛 QA（建议分阶段）
1. 先跑 L1：
   ```bash
   make qa
   ```
2. 再跑严格：
   ```bash
   make qa-strict
   ```
若失败：优先修缺图/断链，再修字体/epub 规范，再修 DPI。

## Phase 5：CI 升级
- 合并 `.github/workflows/build.yml`
- PR 验证通过后合并进 main

## Phase 6：收尾
```bash
git commit -am "migrate: ACRE publishing infra v2.0"
git tag v2.0.0
git push --tags
```

## 回滚策略
- 任何时候可回退到 v1.x tag
- 迁移分支不 squash，保证可审计
