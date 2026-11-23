---
doc-kind: reference
authority: supporting
authority-id: opn.product-structure-baseline
---

# 产品结构基线 · scope 内 context 结构化全集（supporting）

> 本页是 **supporting 基线页**，不是 R 清单、不是产品方案、不是技术设计、不实现。它的唯一职责：在显式 scope 内把决策相关 context 收全，并列呈现两个抽象维度，显式标注冲突/耦合但**不裁决、不归一**，缺口随基线保留不填平。
> 由 `docs/reasearch/opn-cross-comparison/_gen_baseline.py` 从 charter §4 / product-module-map §2 / 横比 bundle / human-gate-model 机械派生；端到端维度与交叉区因项目无现成材料，只提供骨架与待填位，**不编造**。
> 从这份基线拆 R（定粒度、填 acceptance、跑 A/B/C/D）是**未来规划阶段**的事；本切片不做。

## 1. 契约与切片边界

- **产出物**：scope 内决策相关 context 的结构化全集 + 缺口清单；不是 R（可独立验收需求），因为 R 要求 `acceptance`，粒度未定则填不出真实验收判据。
- **双维度并列**：模块维度（功能构成）与端到端能力维度（用户完整流程）是两个**正交抽象维度**，不是二选一、不是层级；谁也不包含谁。
- **交叉区只标注**：一个端到端能力横跨多模块、一个模块参与多能力 → 天然冲突/耦合。本页只显式记录，**不归一成单一 R、不合并、不裁决**。
- **缺口是一等公民**：unknown、alignment item、版本钉偏差、未定义契约项全部随基线保留，不隐藏、不填平。
- **决策延迟**：粒度、冲突消解、耦合处理全部延迟到规划/执行阶段；本页只提供决策所需的完整 context。

## 2. Scope 定义（四坐标）

### 2.1 六维观察透镜（charter §4）

| 维度 | 要回答什么（charter §4 原文） | 本基线中的落点 |
|---|---|---|
| 产品模块构成 | 系统由哪些用户可见的功能单元组成？每个模块的职责边界与对外契约是什么？ | §3 模块维度（13 模块清单） |
| 技术设计 | 每个模块的数据模型、状态机、协议/接口、持久化、隔离与安全、升级与版本偏斜、测试与验证方式 | §3 模块定义 + §6 缺口（M12 技术设计与部署） |
| 复用边界 | 每个模块是「可直接用 / 适配可用 / 必须自研」？依据是哪条 sealed Evidence？ | §3 reuse_signal 列（assumption，事实以账本为准）+ §6 缺口 |
| 组合顺序 | 模块间依赖关系是什么？最小可运行切片由哪几个模块组成？ | §5 交叉区骨架（端到端流程 × 模块依赖，待填） |
| 人机分工 | 哪些决策必须 Human、哪些可交给 Coding Agent、边界用什么机制表达（避免困在细节） | §2.4 Human 门六方 + §3 M3 行 |
| 工作量信号 | 模块数、接口数、必须自研的比例、上游治理（能否贡献 / 是否只能 fork） | §3 模块数/复用信号 + §6 unknown 缺口清单 |

### 2.2 模块坐标（13 模块，源自 product-module-map §2）

| 模块 | 语义层 | 定义 | 对应场景 |
|---|---|---|---|
| M1 Work Item 生命周期 | L1 | 状态机、claim 权限、流转 | SC::task-workitem |
| M2 身份与 scope | L1 | 谁拥有什么、边界 | SC::identity-scope |
| M3 审批与 Human 门 | L1 | Human 在哪一步介入 | SC::approval-human |
| M4 结果与 provenance | L1 | 产出与溯源 | SC::result-provenance |
| M5 执行与工作区隔离 | L2 | git worktree + CLI agent 单元 | SC::execution-workspace |
| M6 可观测与回放 | L2 | board / 审计 / scorecard | SC::observability |
| M7 会话上下文 | L2 | session 上下文 | SC::session-context |
| M8 共享记忆/知识层 | L3 | 共享事实边界与存储 | SC::memory-knowledge |
| M9 配置与策略 | L3 | 配置与策略面 | SC::config-strategy |
| M10 运行时集成 | L3 | scope 资源/沙箱/部署/substrate | SC::runtime-integration |
| M11 Agent 间协议 | L3 | typed messages / A2A/MCP | SC::agent-protocol |
| M12 技术设计与部署 | L3 | 架构与部署模式 | SC::tech-design |
| M13 能力地图参考 | L3 | 能力抽取参照 | 非横比场景（M13 例外） |

### 2.3 场景坐标（12 场景，SCENE-SET::zopn-v1 RATIFIED）

| # | 场景 | 对应模块 | unknown 缺口数（横比） |
|---|---|---|---|
| 1 | `SC::task-workitem` | M1 | 7 |
| 2 | `SC::identity-scope` | M2 | 8 |
| 3 | `SC::session-context` | M7 | 8 |
| 4 | `SC::execution-workspace` | M5 | 6 |
| 5 | `SC::approval-human` | M3 | 8 |
| 6 | `SC::result-provenance` | M4 | 7 |
| 7 | `SC::memory-knowledge` | M8 | 7 |
| 8 | `SC::observability` | M6 | 6 |
| 9 | `SC::config-strategy` | M9 | 7 |
| 10 | `SC::runtime-integration` | M10 | 5 |
| 11 | `SC::agent-protocol` | M11 | 8 |
| 12 | `SC::tech-design` | M12 | 6 |

### 2.4 Human 门六方（源自 human-gate-model 背景；M3 门模型已裁决，其余仅参照）

| 来源 | 门表达 | 状态 |
|---|---|---|
| tasktrooper | 全自动 | 参照表达（未采纳为默认） |
| ZAgenticOPN | 例外 | 参照表达（未采纳为默认） |
| qm | 三姿态 | 参照表达（未采纳为默认） |
| mozzie | review | 参照表达（未采纳为默认） |
| multica | Review gate + Inbox | 已被 zj 2026-11-20 采纳为基础模型（准入+准出双门） |
| orca | unknown 无 sealed 证据 | unknown，无 sealed 证据 |

## 3. 维度 A：模块构成（已有事实，机械派生）

> 本维度已有事实支撑。`reuse_signal` 列为 **assumption**（源 product-module-map §2，待母模型裁决）；「能力存在」的 sealed Evidence 事实以 `designs/reuse-evidence-ledger.md` 为准。本页不重复证据、不改判断。

| 模块 | 语义层 | 定义 | reuse_signal (assumption, 源 pmap §2) | 证据账本 |
|---|---|---|---|---|
| M1 Work Item 生命周期 | L1 | 状态机、claim 权限、流转 | adapted：5 实现但状态机互不相容（opencode 九态 vs ZAgenticOPN 四态）[matrix §5] | 见 reuse-evidence-ledger M1 行 |
| M2 身份与 scope | L1 | 谁拥有什么、边界 | **必须自研语义**：qm 每人每房 scope ≠ ZAgenticOPN Human→device→agent_instance，不可互推 [matrix §5] | 见 reuse-evidence-ledger M2 行 |
| M3 审批与 Human 门 | L1 | Human 在哪一步介入 | **必须自研统一语义**；四种表达冲突（全自动/例外/三姿态/review）[matrix §5/§6] | 见 reuse-evidence-ledger M3 行 |
| M4 结果与 provenance | L1 | 产出与溯源 | adapted：append-only ledger + 五字段结果是少数明确契约 [matrix §5] | 见 reuse-evidence-ledger M4 行 |
| M5 执行与工作区隔离 | L2 | git worktree + CLI agent 单元 | native 偏多：4 项目均 worktree 模式 [matrix §5] | 见 reuse-evidence-ledger M5 行 |
| M6 可观测与回放 | L2 | board / 审计 / scorecard | adapted：四种形态，口径不统一 [matrix §5] | 见 reuse-evidence-ledger M6 行 |
| M7 会话上下文 | L2 | session 上下文 | L2 层事实 [matrix §4] | 见 reuse-evidence-ledger M7 行 |
| M8 共享记忆/知识层 | L3 | 共享事实边界与存储 | **必须自研边界**：mem-vault 纯 Markdown ≠ qm scope-memory+Postgres ≠ ZAgenticOPN 结构化事实 [matrix §5] | 见 reuse-evidence-ledger M8 行 |
| M9 配置与策略 | L3 | 配置与策略面 | L3 层事实 [matrix §4] | 见 reuse-evidence-ledger M9 行 |
| M10 运行时集成 | L3 | scope 资源/沙箱/部署/substrate | qm 强（central core + Postgres + per-scope sandbox + substrate interface）[matrix §7] | 见 reuse-evidence-ledger M10 行 |
| M11 Agent 间协议 | L3 | typed messages / A2A/MCP | 可复用协议，非产品模块 [matrix §5] | 见 reuse-evidence-ledger M11 行 |
| M12 技术设计与部署 | L3 | 架构与部署模式 | L3 层事实 [matrix §4] | 见 reuse-evidence-ledger M12 行 |
| M13 能力地图参考 | L3 | 能力抽取参照 | 仅 ZAgenticOPN；作参考不单独成模块 [matrix §7] | 见 reuse-evidence-ledger M13 行 |

## 4. 维度 B：端到端能力（骨架 · 待 Human 填 · 不编造）

- **现状**：项目内**无成体系的端到端能力清单**。现有材料中「workflow」命中项均为 CI workflow / review workflow 等单点流程词，不是能力维度；因此本维度是净新增整理工作，不由账本派生。
- **约束**：以下为空位模板，**不得由执行 Agent 依据模块名或 README 字面推断填充**（守 charter §7 非目标）。每条能力须 Human 逐条梳理并给出来源。

| 能力 ID | 能力名（用户完整流程） | 起点 | 终点 | 跨越模块 | 来源/依据 | 状态 |
|---|---|---|---|---|---|---|
| EC-待填 | — | — | — | — | — | 待 Human 梳理 |

> 已知线索（非清单）：product-module-map §4 写有一条最小可运行切片流程「创建 → claim → 执行(worktree) → 结果+provenance → Human 门 → 完成」，可作端到端能力的候选种子，但是否成立、如何拆多条能力仍待 Human 裁决。

## 5. 交叉区：冲突 / 耦合标注（只标注，不裁决、不归一）

> 两维度天然多对多。本区只登记冲突/耦合的**位置与来源**，不合并成单一 R、不选边、不消解。现在维度 B 未填 → 跨维度交叉位暂为空；先登记已在模块维度内显式的语义冲突作为参照。

| 交叉项 | 冲突/耦合描述 | 来源 | 处理 |
|---|---|---|---|
| M1 状态机 | opencode 九态 vs ZAgenticOPN 四态，互不相容 | product-module-map §2 M1 | 标注，待规划阶段裁决 |
| M2 身份 scope | qm 每人每房 vs ZAgenticOPN Human→device→agent_instance，不可互推 | product-module-map §2 M2 | 标注，待规划阶段裁决 |
| M3 Human 门 | 六种门表达互不兼容（见 §2.4） | human-gate-model 背景 | 已裁基础模型，其余仅参照 |
| M8 记忆边界 | mem-vault 纯 Markdown vs qm scope-memory+Postgres vs ZAgenticOPN 结构化事实 | product-module-map §2 M8 | 标注，待规划阶段裁决 |
| 维度 B × 维度 A | — | — | 待 Human 填端到端能力后登记 |

## 6. 缺口清单（不隐藏、不填平）

### 6.1 unknown 证据缺口（横比 83 条，按场景）

| 场景 | unknown 数 |
|---|---|
| `SC::task-workitem` | 7 |
| `SC::identity-scope` | 8 |
| `SC::session-context` | 8 |
| `SC::execution-workspace` | 6 |
| `SC::approval-human` | 8 |
| `SC::result-provenance` | 7 |
| `SC::memory-knowledge` | 7 |
| `SC::observability` | 6 |
| `SC::config-strategy` | 7 |
| `SC::runtime-integration` | 5 |
| `SC::agent-protocol` | 8 |
| `SC::tech-design` | 6 |
| **合计** | **83** |

> unknown ≠ absent：以上只表示无 sealed 证据，不表示项目无该能力；不进复用判断、不填平。

### 6.2 alignment item / 边界约束

- **CTX::zopn-single-user**（constraint）：ZOnePersonNetwork 目标为单人个人协同网络；真实产品边界（单人/跨设备/多项目）是 alignment item
- **CTX::zopn-no-adopt-verdict**（constraint）：本横比仪器只产出场景×项目差异条目；采用/启动裁决属母模型 zj-open-source-capability-fit，不在本报告内

### 6.3 版本钉偏差（引用前须按实际 pin 复核）

- **loop-now**：main @ b7d6811877e6d7341ac539934ae87028df87b1e6 (collected HEAD; requested tag v0.2.0 = 8f504f61e8db628dacb52a4a00e6dc29567aa5af, collect ignores brief.repositories[].revision)
- **multica**：main @ 41885a6d816834663dad8e6944658e2ac8555844 (collected HEAD; requested tag v0.8.1 = b1ea927def64, collect ignores brief.repositories[].revision)

### 6.4 契约缺口

- **adaptation-target 未定义**：横比契约中该字段从未定义且属 Human 复核项，机械生成器不自判；adapted/unsupported 因此为空不是 bug。来源：2026-11-20 工作日志（复用边界收敛）。
- **端到端能力维度无现成材料**：见 §4。

## 7. 一致性自检（机械）

- 六维 6 项全部命中 charter §4；模块 13 项命中 pmap §2；场景 12 项命中 bundle；Human 门 6 方命中 human-gate-model。
- 模块→场景映射覆盖全部 12 场景（13 模块中 M13 为例外）；unknown 合计 83，与 bundle difference-entries 一致。
- 端到端维度与交叉区只含骨架/来源标注，无推断填充；所有 SHAs 机械派生自 SoT，无手填。

