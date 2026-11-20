---
doc-kind: architecture-map
authority: primary
authority-id: opn.docs-map
---

# ZOnePersonNetwork 文档地图

> 本文件是 `docs/` 的唯一导航权威（map）：它只声明「哪个页面回答哪个有界问题」以及页面间的 derived-from / supports / supersedes 关系，不承载正文。
> 被治理对象：`docs/`（greenfield 重建 pass `docs-rebuild`）。导航顺序不等于全局真伪优先级；两页对同一问题给出不同规范性主张时是 Human-review 信号。

## Bound authorities

- [产品模块地图与 A/B 两池决策](designs/product-module-map.md) — 产品由哪些模块构成、各模块归属 A/B 池及可复用来源三元组；role: supporting; authority-id: `opn.product-module-map`; relations: derived-from: opn.research-charter, derived-from: opn.module-matrix, derived-from: opn.adr-adoption-form, derived-from: opn.human-gate-model
- [M3 Human 门功能设计](designs/human-gate-model.md) — Work Item 在哪几步须 Human 放行：默认准入+准出双门、其余时机可配置；role: supporting; authority-id: `opn.human-gate-model`; relations: supports: opn.product-module-map, derived-from: opn.adr-adoption-form
- [采用形态 ADR 0001](zj-adr/0001-adoption-form-discovery-recovery.md) — 调研如何喂养产品的长期决策：项目级作废、功能级恢复；role: supporting; authority-id: `opn.adr-adoption-form`; relations: supports: opn.product-module-map, supersedes: opn.research-charter
- [调研章程](reasearch/2026-11-08-research-charter.md) — 跨主题调研框架、统一问题、证据规则与既有调研处置；role: supporting; authority-id: `opn.research-charter`
- [横向模块矩阵 SoT](reasearch/opn-landscape/2026-11-08-module-matrix.md) — 多项目按统一维度的模块覆盖与可复用边界事实层；role: supporting; authority-id: `opn.module-matrix`

## Categories

- `designs/` — long-lived：功能设计权威页与模块决策（当前 `designs/product-module-map.md`、`designs/human-gate-model.md`）。去日期命名，承载当前状态；`authority: primary` 页是各自契约的唯一权威来源。
- `zj-adr/` — long-lived：长期架构/产品裁决（当前仅 ADR 0001 采用形态）。M3 Human 门裁决已转为 `designs/human-gate-model.md` 功能设计权威页，不再是 ADR。
- `reasearch/` — target-defined 调研包目录（拼写是既有约定，不改）：内容为 commit-pinned 调研证据与过程材料（brief/ledger/status/report-ir/receipt/draft/findings、补采、受阻、碰撞预检、runtime-deviation、横比 REPORT）。其中跨 run 仍被引用的两份长期页——调研章程与横向模块矩阵 SoT——已作为 supporting 权威页注册于上方 map；其余为 evidence surface / process material，不进 map。
- 仓库根 `ZJ-CONTEXT.md` — root-level external entry：产品语境、术语与两池闸门契约，保持在根、不作为 docs/ 内页面。

## Pointer rules

- 一个 `authority-id` 只绑定一个页面（`MAP_AUTHORITY_CONFLICT` 为机械失败）。
- relations 词表封闭：`derived-from`（事实/契约来源）、`supports`（决策支撑）、`supersedes`（后续裁决推翻旧判定）。
- 页面退役顺序：改 `authority: historical` 并释放 map 绑定 → 有入链则留墓碑 → 入链清零 → 才提删除候选；删除需 Human 逐项确认，本 pass 不删除任何页面。
- 收尾状态：三份 2026-11-08 调研报告「结论层作废、事实层保留」由调研章程第 6 节记录，功能级恢复由 ADR 0001 裁决，二者闭环；`2026-11-16-sealed-resupply-blocked.md` 已带终态块，作为根因留档保留。均为 evidence/process surface，不进本 map。
