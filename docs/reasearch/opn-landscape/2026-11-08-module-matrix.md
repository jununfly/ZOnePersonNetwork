# 横向模块矩阵：个人即协同网络的候选项目（2026-11-08）

> 本文件是本轮调研的**统一 SoT**。它不是产品方案、技术方案，也不是编译器产出的决策报告；最终报告由 `zj-tech-research-report` 编译器产出，本矩阵作为 brief criteria 与 Report IR `comparisons` / `metrics` 的输入。

## 1. Run identity

- 决策框架：`docs/reasearch/2026-11-08-research-charter.md`（Problem discovery，**不排名采用形态**）。
- sealed ledger：`2026-11-08-ledger-response.json`，`briefFingerprint = b4367c64557fe12337effb03ed60298f8a6d48451a4f877f34b542d8b0dfc4a8`，`observedAt = 2026-11-08T03:55:00.776Z`。
- 采集状态：`fresh-collection`、preflight `authenticated`、`fallback.automatic = false`、`oldLedgerUsed = false`；`filesRead = 22`、`sourceBytesRead = 246,964`、`durationMs = 37,238`、`cacheHit = false`。
- 10 个仓库全部 commit-pinned：`qm 605c259b`、`tasktrooper ae5fb965`、`opencode-coordination 2c9dd06f`、`agetor 897b70af`、`lanes-sh/app 7b9cb385`、`mozzie 80f35156`、`shared-memory-vault 59f0b121`、`python-a2a 40b969a4`、`dmux 8cb3d926`、`ZAgenticOPN 2ff40cc0`。
- `evidence = 49`、`unknownCriteria = 81`（130 个 仓库×维度 组合）。**`unknown` 是本轮证据不足，不是该模块不存在**。
- `candidates` 的 `stars` / `topicMatch` 为 sealed 原值：qm 15655/0、tasktrooper 120/0、opencode-coordination 0/4、agetor 123/0、lanes 277/1、mozzie 48/1、mem-vault 100/0、python-a2a 1010/0、dmux 1816/0、ZAgenticOPN 0/0。**均不参与模块覆盖判断**。

## 2. 覆盖矩阵（E = 该仓库该维度有 commit-pinned sealed Evidence；unknown = 本轮未采集到声明）

| 模块维度 | qm | tasktrooper | opencode-coord | agetor | lanes | mozzie | mem-vault | python-a2a | dmux | ZAgenticOPN |
|---|---|---|---|---|---|---|---|---|---|---|
| mod-task-workitem | unknown | E | E | unknown | E | E | unknown | unknown | unknown | E |
| mod-identity-scope | E | E | E | unknown | unknown | unknown | unknown | unknown | unknown | E |
| mod-session-context | E | unknown | unknown | E | unknown | unknown | E | unknown | unknown | unknown |
| mod-execution-workspace | unknown | unknown | unknown | E | E | E | unknown | unknown | E | unknown |
| mod-approval-human | E | unknown | E | unknown | unknown | E | unknown | unknown | unknown | E |
| mod-result-provenance | E | unknown | E | unknown | unknown | E | unknown | unknown | unknown | E |
| mod-memory-knowledge | E | E | unknown | unknown | E | unknown | E | unknown | unknown | E |
| mod-observability | E | E | E | E | unknown | unknown | unknown | unknown | unknown | E |
| mod-config-strategy | E | unknown | unknown | unknown | unknown | unknown | unknown | E | unknown | E |
| mod-runtime-integration | E | E | unknown | E | E | unknown | unknown | unknown | unknown | E |
| mod-agent-protocol | unknown | unknown | E | unknown | unknown | unknown | unknown | E | unknown | unknown |
| mod-tech-design | E | E | unknown | E | unknown | unknown | E | unknown | unknown | unknown |
| ref-capability-map | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | E |

覆盖度：`qm 9/13`、`ZAgenticOPN 9/13`、`tasktrooper 6/13`、`opencode-coord 6/13`、`agetor 5/13`、`lanes 4/13`、`mozzie 4/13`、`mem-vault 3/13`、`python-a2a 2/13`、`dmux 1/13`。

**这是本轮最重要的实证结论之一：没有任何单一项目覆盖 13 个维度，最高仅 9/13。** 痛点 1（"应该由哪些产品模块构成不清晰"）不是 zj 没想清楚，而是这类产品在不同项目里本来就被切成了不同的模块集合；照搬任一个项目的模块划分都会漏掉别人的关键单元。

## 3. Evidence ID 清单（按仓库）

**yc-software/qm（9，全部 README.md）**：`mod-identity-scope` `114f13c4c8afc8424cdc1971` · `mod-session-context` `1fcc9288e24457d7fa94240e` · `mod-approval-human` `c8500b3857eb0e93cc9d25d3` · `mod-result-provenance` `fec47fe206b51915b2e19fb4` · `mod-memory-knowledge` `e878e5271a78993966d88f0b` · `mod-observability` `b30ee3590bb6aaead44befb3` · `mod-config-strategy` `ad01939f1a7e220edf96928f` · `mod-runtime-integration` `3ae4f38b4de2d1769a598bc0` · `mod-tech-design` `e38a7af1b2e8472ed82f40dd`

**makifbaysal/tasktrooper（6，全部 README.md）**：`mod-task-workitem` `90b8b4fc0e74bc12214889c4` · `mod-identity-scope` `4a0faa66eee9f3c15434dc32` · `mod-memory-knowledge` `d2423363b8e0d64ec8ce61cc` · `mod-observability` `6a0463be6d4575650cc64979` · `mod-runtime-integration` `e9a31903a5338a7b6eae212a` · `mod-tech-design` `834655c524dca5a255ddaf1f`

**JF3Env/opencode-coordination（6，全部 README.md）**：`mod-task-workitem` `9101cfa7145332b317a9353e` · `mod-identity-scope` `0b5fa995933066879753a0a5` · `mod-approval-human` `1a1c6d9852edef2c3f970f42` · `mod-result-provenance` `01ccf2212f91bcc504af0818` · `mod-observability` `d537234df40dcab3100b4eac` · `mod-agent-protocol` `4e9888715cf937cdeac6384a`

**alamops/agetor（5，全部 README.md）**：`mod-session-context` `7d2249b75c4ec5bac9284bda` · `mod-execution-workspace` `e6275d13fae90b3ea49ca276` · `mod-observability` `74a1e19ab3d67925c43d706c` · `mod-runtime-integration` `f44a67122e779c35ee472959` · `mod-tech-design` `c699464bb705742695f91592`

**lanes-sh/app（4，全部 README.md）**：`mod-task-workitem` `fc77e9f1b10477d753e74fab` · `mod-execution-workspace` `a8434e60ad92db78fedb7af2` · `mod-memory-knowledge` `ff178faee6ce5a1a5106b9e2` · `mod-runtime-integration` `d9b7b1edd17eeefaa26756c3`

**usemozzie/mozzie（4，全部 README.md）**：`mod-task-workitem` `14bb8d6ea36e18107fd51b3c` · `mod-execution-workspace` `6676d3f26c9b4f77443c5d2a` · `mod-approval-human` `3e8488d208de54fdd00a11c0` · `mod-result-provenance` `0b70106e3349d69e694526f5`

**songs-aaa/shared-memory-vault（3，全部 README.md）**：`mod-session-context` `151608571341f37ee2297dcb` · `mod-memory-knowledge` `1eedaed644a280db74133572` · `mod-tech-design` `de5482ebaca9a76160284089`

**themanojdesai/python-a2a（2，全部 README.md）**：`mod-config-strategy` `8a03946eaf6653ada1427dc9` · `mod-agent-protocol` `5d423995e3d4b2ed0d8aab78`

**standardagents/dmux（1，README.md）**：`mod-execution-workspace` `205fcc6c54e6dcc370eeeb85`

**jununfly/ZAgenticOPN（9，全部 docs/**）**：`mod-task-workitem` `3f9dde435394108a69009858`（capability-map） · `mod-identity-scope` `37c46d46405b7d6055e568d5`（PRD） · `mod-approval-human` `06b3135da98d7a9bec7b65a9`（EV-alignment） · `mod-result-provenance` `ddea4d90bb2b7e250b08b616`（capability-map） · `mod-memory-knowledge` `1b866cefa58726959ce1cd73`（capability-map） · `mod-observability` `0a8445acfd470fba8cb2c18a`（capability-map） · `mod-config-strategy` `6814fc75fc59e1f02bb5f756`（PRD） · `mod-runtime-integration` `5da1a8117f4c7765b67113c4`（capability-map） · `ref-capability-map` `984e472faa61310787ad09a9`（EV-alignment）

## 4. 三层分工浮现（对痛点 1 的直接回答）

把 10 个项目的模块声明按**语义层**归类，而不是按项目名归类：

| 层 | 该层持有的事实 | 代表项目（sealed 证据） | 典型模块 |
|---|---|---|---|
| L1 协作控制面 | Work Item 状态、claim 权限、review 结论、provenance、共享事实 | ZAgenticOPN（R1–R12、Work Item lifecycle、语义所有权）、opencode-coordination（append-only ledger、typed messages）、mozzie（review workflow） | task-workitem / result-provenance / identity-scope |
| L2 执行编排 | 任务如何落到隔离工作区、并行、board 流转、状态可观测 | tasktrooper（board 自动派发）、agetor（worktree kanban、restart-safe）、lanes（issue board + worktree + diff）、mozzie（work item 拆分 + dependency） | execution-workspace / observability / session-context |
| L3 运行时与资源 | scope、memory、权限、沙箱、skills、部署与接口抽象 | qm（personal/shared scope、scoped memory、durable sandbox、deployment directory、substrate interface）、mem-vault（纯 Markdown single source of truth）、python-a2a（A2A/MCP 协议） | memory-knowledge / config-strategy / runtime-integration / tech-design |

**关键**：qm 与 ZAgenticOPN 各覆盖 9/13，但**覆盖的格子不同**——qm 强在 L3（资源与部署），ZAgenticOPN 强在 L1（语义所有权）。两者不是替代关系，而是不同层的参照物。这解释了为什么"整个产品概念明确但模块构成不清晰"：概念跨了三层，而每个现有项目只做其中一到两层。

## 5. 复用边界与 0→1 工作量信号（分析层推断，标注待验证）

| 模块 | 有现成实现的项目数 | 复用判断 | 说明 |
|---|---|---|---|
| 任务与工作项 | 5（tasktrooper / opencode-coord / lanes / mozzie / ZAgenticOPN） | adapted（多实现可选，语义需统一） | 各家生命周期不同：opencode-coord 是 `proposed→…→validated` 九态，ZAgenticOPN 是 `available→claimed→awaiting_agent_review→completed`，不能照搬状态机 |
| 执行与工作区隔离 | 4（agetor / lanes / mozzie / dmux） | native 偏多（可复用模式） | 几乎都以 git worktree + CLI agent 为单元；差异在 board 与 restart 策略 |
| 可观测与回放 | 5（qm / tasktrooper / opencode-coord / agetor / ZAgenticOPN） | adapted | board、notification、scorecard、审计日志四种形态，指标口径不统一 |
| 结果与 provenance | 4（qm / opencode-coord / mozzie / ZAgenticOPN） | adapted | append-only ledger 与五字段结果是少数明确契约 |
| 身份与 scope | 4（qm / tasktrooper / opencode-coord / ZAgenticOPN） | **必须自研语义** | qm 是"每人每房一个 scope"，ZAgenticOPN 是 `Human→device→agent_instance`，二者不能互相推导 |
| 共享事实 / 知识层 | 5（qm / tasktrooper / lanes / mem-vault / ZAgenticOPN） | **必须自研边界** | mem-vault 是纯 Markdown 单真相，qm 是 scope-authorized memory + Postgres，ZAgenticOPN 明确"shared context 只存结构化事实与 canonical Git references" |
| Agent 间协议 | 2（opencode-coord / python-a2a） | 可复用协议，但非产品模块 | typed messages / A2A 是通信层，不提供 Work Item 语义 |
| 审批与 Human 门 | 4（qm / opencode-coord / mozzie / ZAgenticOPN） | **必须自研统一语义** | 见第 6 节，四种表达彼此冲突 |

**对痛点 2 的回答**：0→1 工作量并不集中在"任务板 / worktree / 终端"这些有多个现成实现的模块，而集中在**语义所有权层**（身份与 scope 的定义、共享事实边界、Human 门统一语义、跨模块 provenance）。这些格子虽然有 sealed 声明，但**每家的定义互不相容**，无法直接复用，只能重新定义后再挑实现。这正是 ZAgenticOPN 当年"大多数内容从 0 到 1"的结构性原因，不是团队执行力问题。

## 6. 人机分工的三种冲突表达（方案讨论前必须裁决）

| 来源 | sealed Evidence | 表达 |
|---|---|---|
| tasktrooper | `6a0463be6d4575650cc64979` | "You don't drive the agents, the board does." 卡片进入列即自动派发，Human 不按 run |
| ZAgenticOPN | `0a8445acfd470fba8cb2c18a`、`06b3135da98d7a9bec7b65a9` | Human action script：一次初始目标 + 三次"检查 shared context"激活；Human 只处理例外，未列出的动作计入 intervention |
| qm | `c8500b3857eb0e93cc9d25d3` | Strict / Auto / Dangerous 三种安全姿态，严格模式下每个工具调用都暂停等人批准 |
| mozzie | `3e8488d208de54fdd00a11c0` | Review workflow：approve to push / reject with feedback，Agent 从拒绝历史学习 |

**这是四个不同的"Human 在哪一步"**，从完全自动到逐工具审批。若不先裁决，Coding Agent 会在实现细节里反复改派发与审批逻辑——正是"人和 Agents 困在细节里"的具体机制。本轮只记录分歧，**不做裁决**。

## 7. 与参照物的闭环（值得单独标出）

`ZAgenticOPN` 的 `docs/designs/agent-self-service-collaboration-selective-reuse-capability-map.md`（Evidence `3f9dde435394108a69009858`、`ddea4d90bb2b7e250b08b616` 等）已把 **`qm（ref）`** 列入"可抽取单位能力"表：

- 可抽取：`ClaimStore/delivery drain claim`、`TaskStore CAS`、`scope-authorized memory`、`revision/restore`、`session recovery`；
- 明确不能承担：直接替代 Work Item authority 或 shared coordination schema；
- 准入方式：先写黑盒/契约 fixture 再决定是否抽取。

也就是说，zj 这次指定调研 `yc-software/qm`，与参照物里已有的判断形成闭环：qm 不是"要不要采用"的候选，而是**L3 运行时与资源层的能力来源参照**。本轮 sealed 证据（qm 的 scope / memory / sandbox / deployment directory / substrate interface）与那份能力地图的条目方向一致，但该判断仍属**分析层推断**，需后续用契约 fixture 验证。

## 8. Non-sealed primary-source reading（只用于风险与验证门，不是 canonical 能力结论）

编译器的 `isCanonicalPath` 只允许 `docs/**/*.md`、若干命名 md 与少量 manifest；本轮除 ZAgenticOPN 外的 9 个仓库都走 fallback，只读到根 `README.md`（40 条 Evidence 来自 README）。以下来自同一 commit 的 GitHub API 原文读取，**不是 sealed Evidence**，复核命令：

```sh
# 以 qm 为例，其余仓库替换 owner/name 与 SHA
SHA=605c259b28d54ee750c526b11925ddea3e0e6f59
/opt/homebrew/bin/gh api "repos/yc-software/qm/contents/docs/SPEC.md?ref=$SHA" --jq .content | base64 -d
/opt/homebrew/bin/gh api "repos/yc-software/qm/contents/docs/memory-records.md?ref=$SHA" --jq .content | base64 -d
/opt/homebrew/bin/gh api "repos/yc-software/qm/contents/docs/capability-tokens.md?ref=$SHA" --jq .content | base64 -d
/opt/homebrew/bin/gh api "repos/yc-software/qm/contents/SECURITY.md?ref=$SHA" --jq .content | base64 -d
```

- **qm 技术设计层**：`docs/SPEC.md`、`docs/memory-records.md`、`docs/memory-providers.md`、`docs/capability-tokens.md`、`docs/persistent-subagent-sessions.md`、`docs/loop-ingestion.md`、`docs/mcp-connectors.md`、`docs/credential-refresh-handoff.md` 等构成完整的子系统文档；`CONTRIBUTING.md` 只接受 human-written 文本贡献（ADR 形式），不接受代码 PR，与 herdr 那轮的上游治理风险同型。
- **tasktrooper**：README 的 `## How a task runs`、`## How it compares / Side by side` 提供任务流转与同类项目对比；`## Layout` 给出仓库模块布局。
- **agetor / lanes / mozzie**：README 的 Architecture / Data layer / Security 章节含技术栈与本地 API 细节，但本轮关键词未命中为 canonical Evidence。
- **协议层**：python-a2a 的 `## Workflow Engine`、`Agent Flow UI`、`Agent Discovery` 是工作流与发现面的设计参考。

## 9. 信息缺口与下一步（81 个 unknown 显式保留）

| Gap | Nature | Next step |
|---|---|---|
| 49 条 Evidence 中 40 条来自根 README，实现层与技术子系统文档未进入 sealed 范围 | compiler canonical 覆盖限制 | 用指向 `docs/**/*.md` 的判别性短语重采一轮，或走 `zj-research` primary-source reading 单独出 findings |
| 81 个 `仓库×维度` 组合为 unknown | 本轮证据不足，不是能力缺失 | 不得写成 absent；对 qm 的 task/execution/protocol 等空格，用判别性短语补采（如 "Track a project in a shared channel"、"runs commands in the scope's own isolated sandbox"） |
| 复用边界与工作量信号是分析层推断 | unverified | 用契约 fixture 逐模块验证"可直接用 / 适配可用 / 必须自研"，再进入总体方案讨论 |
| 人机分工四种表达冲突 | 待裁决，不是技术缺口 | 方案讨论前先定 Human 介入点，再让 Coding Agent 落地 |
| 部分项目只有 1–2 条 Evidence（dmux、python-a2a） | 覆盖薄弱 | 若它们进入总体方案，必须单独补采；否则只作为类别代表保留 |
| zj 的真实产品边界（单人 / 跨设备 / 多项目） | alignment item | 沿用 charter 假设；若边界变化，模块清单与分层需重做 |
