---
doc-kind: design
authority: primary
authority-id: opn.human-gate-model
---

# M3 Human 门设计：准入/准出双门，其余可配置

> 本文件是 M3「审批与 Human 门」的**功能设计权威页**（doc-kind: design, authority: primary）。
> 它定义 Work Item 生命周期中 Human 授权门的位置、触发语义与放行主体（契约层），是 Coding Agent 实现该模块的唯一输入。
> 由 zj 2026-11-20 拍板，回答调研章程与模块矩阵 §6 悬置的「Human 在哪一步介入」分歧：
> **采用 multica 的门模型作为基础，默认在「准入」与「准出」两个环节强制 Human 介入；其他时机的门通过配置增删调整。**

## 背景（为何现在必须定）

- 模块矩阵 §6 记录四种互不兼容的表达（tasktrooper 全自动 / ZAgenticOPN 例外 / qm 三姿态 / mozzie review）；后续横比补入 multica（Review gate + Inbox 按需召唤）与 orca（本维度 unknown，无 sealed 证据）。六种表达里没有可直接互推的语义。
- M3 属 L1 语义所有权层（与身份、Human 门、provenance 同类）。按 Q5 例外与采用形态 ADR（ADR 0001），L1 语义须自研统一、只取契约另写实现（②），不得照抄任一来源代码；multica 的 Apache+附加条件亦未过闸门 3。
- 不定型的直接后果：Coding Agent 会在派发与审批逻辑间反复改——正是调研章程 §2「人与 Coding Agent 困在细节里」的具体机制。

## 设计决策

1. **基础模型**：采用 multica 的双面 Human 门思路，默认只保留两道**强制门**：
   - **准入门** — Work Item 进入执行前须 Human 放行。其依据来自 multica "assign work to AI coding agents the way you'd assign it to a teammate — they pick up the issue…"（sealed E `a67400762c931df62135608d`）：Human 在开工前分配/放行，Agent 才 pick up。
   - **准出门** — Work Item 结果进入交付/合并前须 Human 放行。依据 multica "Review gates — Work lands in review, not in main. You decide what ships."（sealed E `2cc46ac299adc52b807b122e`）；同理 "nothing ships without a human saying so"（E `5c1fa749…`）。
   - 上述 Evidence ID 来自 `docs/reasearch/opn-cross-comparison/collect/ledger-multica.json`（commit-pinned，pin `41885a6d816834663dad8e6944658e2ac8555844`）。
2. **可配置面**：执行中途的审批、工具级确认、例外升级等其他时机**不进默认契约**，通过配置按需增删。此面吸收 multica "Inbox — Get pinged when an agent needs a call, not for every step"（同一 sealed E `2cc46ac2…`）的按需召唤思路，但从「默认强制」降为「可选配置」。
3. **设计对象**：门的**位置、触发语义与放行主体**（契约层），不是任何来源的代码；实现按 ② 自研。

### 取舍记录（Q7 · 摄取→裁切）

| 来源 | 裁切 | 依据 |
|---|---|---|
| multica 准出 Review gate | 保留为默认强制门 | sealed E `2cc46ac2…` |
| multica 开工前 assign | 固化为默认强制准入门 | sealed E `a67400762…` |
| multica 执行中 Inbox 按需 ping | 从默认行为降为可配置门 | zj 裁决：默认只留准入/准出两门 |
| mozzie approve/reject + 拒绝历史学习 | 不摄取（与准出门位置重叠） | 交付前放行由准出门承担 |
| qm Strict 逐工具审批 | 不设默认门；列为可配置候选 | 频次过高，与「默认两门」冲突 |
| ZAgenticOPN 例外处理 + intervention 记账 | 不整体摄取；记账口径单独对齐（见实现约束） | 门模型不同，但记账是横比共同验收项 |

## 为何此页是权威

- **难逆**：M3 是 Work Item 状态机的 L1 语义核心，一旦 Coding Agent 按某套门逻辑写开，改动等于重写状态机与审计链。
- **无上下文会费解**：只读调研章程 §6「结论层作废」会以为 M3 无定型；实际是「项目级不作废、门位置已定」。
- **真实取舍**：在「全自动不设门」与「逐工具审批」之间选了第三条路——端到端两道默认门 + 中间门可配置。
- **单一输入**：本页以 `authority: primary` 绑定 `opn.human-gate-model`，是 M3 门契约的唯一权威来源；其他页面只引用、不复述本页规则。

## 实现约束（Consequences）

- M3 按 **② 自研契约**，不摄取 multica 代码（L1 语义需自研，且 license 未复核）。Coding Agent 的输入是本设计定义的门契约，不是「参考 multica 改一改」。
- Work Item 状态机须在「待执行 → 执行」与「完成候选 → 已交付」两处具备**可配置 gate 钩子**：默认开，其余时机默认关。
- 每次放行/拒绝须**记账**，口径对齐 ZAgenticOPN 的 `task-specific Human intervention` 与横比 `SC::approval-human` 的「审批/拒绝/干预可审计、有账本」。
- **待细化（不阻塞本设计）**：准入门的放行主体与触发条件、准出门的验收口径、配置项数据结构、与 M4 provenance 的字段对接——在后续 M3 契约细化中定。
- orca 在 `approval-human` 仍为 unknown，不作 M3 源；qm Strict 仅作可配置门的候选档位，非默认。
