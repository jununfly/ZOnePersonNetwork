# 个人即协同网络 · 多项目场景锚定横比报告（过程材料 / PROVISIONAL）

> 仪器：`zj-graphical-cross-comparison`。本报告由机械闸门 CHK-01..10 全过（0 ERROR / 0 WARN）后签发，但**固定场景集为 zj 草稿、待 ratify**，故在 zj 一句话认可前仅为过程材料，不是已签发横比报告。

> **范围声明**：本仪器只产出「场景×项目」差异条目。"以 orca 启动本项目"的采用/启动裁决属母模型 `zj-open-source-capability-fit`，不在本报告内（见第 7 节回灌素材）。

## 1. 图清单与版本 pin

| 项目 | 仓库 | 版本钉 |
|---|---|---|
| orca | `stablyai/orca` | `v1.4.253 @ 27eb5e2a6c5017c6fdcba4fee16bf54256550c6f` |
| loop-now | `AI-for-anyone/loop-now` | `main @ b7d6811877e6d7341ac539934ae87028df87b1e6 (collected HEAD; requested tag v0.2.0 = 8f504f61e8db628dacb52a4a00e6dc29567aa5af, collect ignores brief.repositories[].revision)` |
| multica | `multica-ai/multica` | `main @ 41885a6d816834663dad8e6944658e2ac8555844 (collected HEAD; requested tag v0.8.1 = b1ea927def64, collect ignores brief.repositories[].revision)` |
| ZAgenticOPN | `jununfly/ZAgenticOPN` | `2ff40cc052aae12fc7a324f89691e9f194985d24` |
| herdr | `herdrdev/herdr` | `master ee5bfb5041bb3e4a49d591c72308aae3c81ecdde` |
| qm | `yc-software/qm` | `605c259b28d54ee750c526b11925ddea3e0e6f59` |
| tasktrooper | `makifbaysal/tasktrooper` | `ae5fb965c4758bbb25d2fac7f10f9bb26cb63823` |
| opencode-coordination | `JF3Env/opencode-coordination` | `2c9dd06f21716d8fc5885a266b119e58e78f2a0d` |
| agetor | `alamops/agetor` | `897b70afb6f7671dc418c6d1053dbf8fbc3c81e0` |
| lanes | `lanes-sh/app` | `7b9cb385d1100ded8a74986f81472f8856840578` |
| mozzie | `usemozzie/mozzie` | `80f3515684722a8909fbc0c17a0526664ec0349a` |
| mem-vault | `songs-aaa/shared-memory-vault` | `59f0b12134622c0ad93ef59ef6373cfe587deaf3` |
| python-a2a | `themanojdesai/python-a2a` | `40b969a465f85e8156793b7cfac16c5e23ed0b86` |
| dmux | `standardagents/dmux` | `8cb3d926631a9349ab67f7ece41d218427ac7e24` |

域级上下文条目（旁挂，不进图）：
- **CTX::zopn-single-user**（constraint）：ZOnePersonNetwork 目标为单人个人协同网络；真实产品边界（单人/跨设备/多项目）是 alignment item
- **CTX::zopn-no-adopt-verdict**（constraint）：本横比仪器只产出场景×项目差异条目；采用/启动裁决属母模型 zj-open-source-capability-fit，不在本报告内

## 2. 固定场景集（PROVISIONAL，待 zj ratify）

- id：`SCENE-SET::zopn-v1`，version-pin：`v1 (PROVISIONAL — zj draft 2026-11-09, pending ratification)`
- source：`zj 2026-11-08 charter 模块草案 + opn-landscape 13-维度 brief（Human 给定草稿，待 ratify）`
- derived-from-graphs：`False`（外部尺子，不来自任何项目图）

| 场景 | 起点 → 终点 → 可观察结果 |
|---|---|
| `SC::task-workitem` | 用户想让一个或多个 Agent 协作完成一件可追踪的工作 → 该工作以可推进的状态存在于协作面板上，可被认领与流转 → 工作项可见、状态机可前进（如 available→claimed→…→completed） |
| `SC::identity-scope` | 需要把人、Agent、设备组织进一个协作 scope → 成员与 scope 边界被定义且可鉴权 → 身份/成员/scope 可被查询且权限生效 |
| `SC::session-context` | 一次协作需要跨多轮/多 Agent 携带上下文 → 上下文被建立、携带并在中断后恢复 → 恢复后上下文一致、不丢状态 |
| `SC::execution-workspace` | Agent 需要执行一个任务 → 任务在隔离工作区完成，资源被编排分配 → 执行在隔离边界内发生、互不污染 |
| `SC::approval-human` | Agent 产出需要人工确认或存在高风险动作 → 人工 gate 被触发、决策被记录 → 审批/拒绝/干预可审计、有账本 |
| `SC::result-provenance` | 任务产生结果与产物 → 结果被 review、附 provenance 并验收 → 产物可复核、来源可追溯 |
| `SC::memory-knowledge` | 协作中产生可复用事实/经验 → 知识被沉淀、可检索、可复用 → 检索命中既有知识、复用生效 |
| `SC::observability` | 需要诊断一次协作发生了什么 → 状态可视化、事件可回放 → 事件流/状态可重放、可定位 |
| `SC::config-strategy` | 需要定义规则/skill/版本策略 → 策略被加载并约束行为 → 策略生效、版本偏斜被管控 |
| `SC::runtime-integration` | 需要在某主机/平台部署并随上游升级 → 运行时被安装、可升级、host adapter 工作 → 安装成功、升级可用、跨平台可运行 |
| `SC::agent-protocol` | 多个 Agent 需要彼此通信或被发现 → 消息/契约被交换、Agent 可发现 → Agent 间能交换结构化消息或经协议发现 |
| `SC::tech-design` | 需要评估项目的工程设计与质量门 → 核心循环/持久化/工具面/测试门被声明 → 技术设计事实可核验、质量门可观察 |

## 3. 差异条目矩阵（12 场景 × 14 项目）

图例：● native（绑定 sealed Evidence） · unknown（证据缺口，附 verification-plan）· 本集无 adapted / unsupported 条目（未见显式否定陈述，也未做适配判定）。

| 项目 | task-workitem | identity-scope | session-context | execution-workspace | approval-human | result-provenance | memory-knowledge | observability | config-strategy | runtime-integration | agent-protocol | tech-design |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| orca | · | · | · | ● | · | ● | · | · | ● | ● | ● | ● |
| loop-now | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| multica | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| ZAgenticOPN | ● | ● | · | · | ● | ● | ● | ● | ● | ● | · | · |
| herdr | · | · | ● | ● | · | · | · | ● | ● | ● | ● | ● |
| qm | · | ● | ● | · | ● | ● | ● | ● | ● | ● | · | ● |
| tasktrooper | ● | ● | · | · | · | · | ● | ● | · | ● | · | ● |
| opencode-coordination | ● | ● | · | · | ● | ● | · | ● | · | · | ● | · |
| agetor | · | · | ● | ● | · | · | · | ● | · | ● | · | ● |
| lanes | ● | · | · | ● | · | · | ● | · | · | ● | · | · |
| mozzie | ● | · | · | ● | ● | ● | · | · | · | · | · | · |
| mem-vault | · | · | ● | · | · | · | ● | · | · | · | · | ● |
| python-a2a | · | · | · | · | · | · | · | · | ● | · | ● | · |
| dmux | · | · | · | ● | · | · | · | · | · | · | · | · |

各项目 native 场景数：
- orca: **6/12**
- loop-now: **12/12**
- multica: **12/12**
- ZAgenticOPN: **8/12**
- herdr: **7/12**
- qm: **9/12**
- tasktrooper: **6/12**
- opencode-coordination: **6/12**
- agetor: **5/12**
- lanes: **4/12**
- mozzie: **4/12**
- mem-vault: **3/12**
- python-a2a: **2/12**
- dmux: **1/12**

## 4. 可选场景集核对留痕（Human 盲区核对）

盲区核对（Human / zj）：本轮固定场景集取 12 个可观察场景，对应 opn-landscape 的 13 个模块维度；其中 ref-capability-map 是 ZAgenticOPN 参照物专属能力地图（仅其有 E），不作为通用场景，已降为 ZAgenticOPN 项目级 context-entry。agent-protocol / tech-design 保留为独立场景。盲区：仍有若干项目在若干场景为 unknown（见差异条目，多为早期一手阅读未做 sealed 采集者）；multica 与 loop-now 本轮已跑 zj-research collect 取得 12/12 sealed Evidence（multica 曾有的 Lark 子系统弱证据已通过 README 锚定 brief 修复，见 CTX::multica-evidence-anchored；两者均含钉偏差 context-entry）。未自行推断任何场景内语义等价。

## 5. 场景内语义等价裁决记录

未裁决任何场景内语义等价（等价需引用双方 acceptance 且由 Human 裁决）。例如 qm 与 ZAgenticOPN 均覆盖 `identity-scope` 但语义互不相容——qm 是"每人每房一个 scope"，ZAgenticOPN 是 `Human→device→agent_instance`，**不得判等价**，只能各自保留为 unknown/待裁决。

## 6. 摘要指标（display-only，不参与结论）

> `not_for_conclusion=true`，`usage=display-only`。不得用于排序 / 裁决 / 回灌 / 优先级。

| 项目 | 证据绑定覆盖 | 竖切片覆盖 | 共享度 | SCC | 最大依赖闭包 |
|---|---|---|---|---|---|
| orca | 0.3158 | 1.0 | 0.0 | [] | 2 |
| loop-now | 0.3243 | 1.0 | 0.0 | [] | 2 |
| multica | 0.3243 | 1.0 | 0.0 | [] | 2 |
| ZAgenticOPN | 0.3333 | 1.0 | 0.0 | [] | 1 |
| herdr | 0.3182 | 1.0 | 0.0 | [] | 2 |
| qm | 0.3333 | 1.0 | 0.0 | [] | 1 |
| tasktrooper | 0.3333 | 1.0 | 0.0 | [] | 1 |
| opencode-coordination | 0.3333 | 1.0 | 0.0 | [] | 1 |
| agetor | 0.3125 | 1.0 | 0.0 | [] | 2 |
| lanes | 0.3077 | 1.0 | 0.0 | [] | 2 |
| mozzie | 0.3333 | 1.0 | 0.0 | [] | 1 |
| mem-vault | 0.3333 | 1.0 | 0.0 | [] | 1 |
| python-a2a | 0.3333 | 1.0 | 0.0 | [] | 1 |
| dmux | 0.3333 | 1.0 | 0.0 | [] | 1 |

未决存量（undecided-stock）：0

## 7. 与母模型的可选回灌素材（非采用裁决）

以下供 `zj-open-source-capability-fit` 在后续做 R×O 矩阵时消费；**本报告不产采用裁决**。

- **orca 作为 startup 种子（L2 执行编排层证据最齐）**：在 `execution-workspace`(4 Evidence)、`runtime-integration`(2)、`agent-protocol`(1)、`result-provenance`(1)、`config-strategy`(1)、`tech-design`(1) 均为 native——契合"以 orca 启动"的设想，因为它补齐的是**执行/编排层**而非控制面。
- **控制面语义须自研（痛点 2 的 0→1 集中处）**：orca 在 `task-workitem` / `identity-scope` / `session-context` / `approval-human` / `memory-knowledge` / `observability` 全部 unknown；这与 charter 痛点 2 一致——工作量集中在**语义所有权层**，不能直接复用现成实现。
- **ZAgenticOPN（参照物）强在 L1 语义所有权**：`task-workitem`/`identity-scope`/`approval-human`/`result-provenance`/`memory-knowledge`/`observability` 均为 native，与 orca 互补而非替代。
- **multica / loop-now 已 collect 取 12/12 sealed Evidence（本轮补采）**：multica 偏多-agent 团队/权限/集成（workspaces/squads/autopilots cron、Slack-Feishu-Lark 集成、Go+PostgreSQL17+Next.js），loop-now 偏本地桌面 agent 编排（Go server+SQLite+React、desktop app/Docker、plugins 无 sandbox 执行代码）。两者均可作执行编排层参照，但：① multica 弱证据已解决：原 5 条因 keyword 路径子串误命中 docs/lark-*.md（谈媒体/配额维护）被判 native 仅因有 sealed ID；现全部 12 场景统一锚定根 README.md（canonical/英文/切题），5 条摘录已复核为对应场景原文（review gate / assign issue / squads / diff 连 issue / 运行成本）；② 两者均存在版本钉偏差（请求 tag v0.8.1 / v0.2.0 ≠ 实际钉到的 main HEAD），引用前须注意版本。

## 8. 完成标准自检

- 第三方 Agent 可凭 `bundle.json` 的 `difference-entries` 逐条复核：每条含 `scene`/`project`/`verdict`/`evidence-refs`（native）或 `verification-plan`（unknown）。
- 来源三类区分：**evidence**=原生绑定 sealed Evidence ID；**human-ruling**=场景集与场景映射由 zj 给定；**assumption**=第 7 节回灌素材为分析层推断。
- ⚠️ **签发前阻塞项**：固定场景集（`SCENE-SET::zopn-v1`）为 zj 草稿，需 zj 一句话 ratify 后方从"过程材料"升为"已签发横比报告"。
