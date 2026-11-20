---
doc-kind: design
authority: primary
authority-id: opn.product-module-map
---

# 产品模块地图与 A/B 两池决策（R3 · zj 2026-11-16 拍板）

> 本文件是 `zj-grill-with-docs` R3 产物。依据：
> - `docs/reasearch/opn-landscape/2026-11-08-module-matrix.md` §4/§5（三层分工 + 复用边界信号，sealed Evidence）
> - `docs/reasearch/opn-maturity/2026-11-13-maturity-evidence.md`（14 仓库 license/CI/test 事实，non-sealed，仅作验证门）
> - R2 锁定的 Q5/Q6/Q7/Q8/Q9 规则
>
> **本文件不是 PRD、不是技术方案、不实现。** 每条判定标 `[证据]`（matrix sealed / maturity non-sealed）或 `[推断]`（分析层，待 fixture 验证）。闸门状态见 `ZJ-CONTEXT.md` 的「两池判定闸门」。

---

## 1. 规则回顾（R2 锁定）

- **Q5 摄取**：默认 ① 复制代码进仓库；Human 确认可降级为 ② 只取契约另写实现。
- **Q6 闸门**：① 可运行实现 · ② 测试/契约门 · ③ 法律有权 fork+own（不看上游是否收 PR）。过 1+2+3 → A 池默认①；过 1+2 不过 3 → ②；不过 1 或 2 → B 池。
- **Q7 取舍**：只发生在模块契约层，每次「摄取→裁切」留取舍记录。
- **Q8 成功判据**：三计数（摄取 / 裁切 / 自建）+ 硬门「最小切片自建模块数 ≤ N」；只数模块不数功能点。
- **Q9 核心抽象**：**Work Item 是唯一一等公民**，意图只是创建工作项时的输入文本。

---

## 2. 模块清单（按 L1/L2/L3 语义层，源自 matrix §4）

按语义层归类而非按项目名——这是矩阵 §4 对痛点 1 的直接回答。

### L1 协作控制面（语义所有权 — 自研语义优先 ②）
| 模块 | 定义 | 复用信号 [证据] |
|---|---|---|
| M1 Work Item 生命周期 | 状态机、claim 权限、流转 | adapted：5 实现但状态机互不相容（opencode 九态 vs ZAgenticOPN 四态）[matrix §5] |
| M2 身份与 scope | 谁拥有什么、边界 | **必须自研语义**：qm 每人每房 scope ≠ ZAgenticOPN Human→device→agent_instance，不可互推 [matrix §5] |
| M3 审批与 Human 门 | Human 在哪一步介入 | **必须自研统一语义**；四种表达冲突（全自动/例外/三姿态/review）[matrix §5/§6] |
| M4 结果与 provenance | 产出与溯源 | adapted：append-only ledger + 五字段结果是少数明确契约 [matrix §5] |

### L2 执行编排（低语义冲突 — ① 复制）
| 模块 | 定义 | 复用信号 [证据] |
|---|---|---|
| M5 执行与工作区隔离 | git worktree + CLI agent 单元 | native 偏多：4 项目均 worktree 模式 [matrix §5] |
| M6 可观测与回放 | board / 审计 / scorecard | adapted：四种形态，口径不统一 [matrix §5] |
| M7 会话上下文 | session 上下文 | L2 层事实 [matrix §4] |

### L3 运行时与资源（① 复制）
| 模块 | 定义 | 复用信号 [证据] |
|---|---|---|
| M8 共享记忆/知识层 | 共享事实边界与存储 | **必须自研边界**：mem-vault 纯 Markdown ≠ qm scope-memory+Postgres ≠ ZAgenticOPN 结构化事实 [matrix §5] |
| M9 配置与策略 | 配置与策略面 | L3 层事实 [matrix §4] |
| M10 运行时集成 | scope 资源/沙箱/部署/substrate | qm 强（central core + Postgres + per-scope sandbox + substrate interface）[matrix §7] |
| M11 Agent 间协议 | typed messages / A2A/MCP | 可复用协议，非产品模块 [matrix §5] |
| M12 技术设计与部署 | 架构与部署模式 | L3 层事实 [matrix §4] |
| M13 能力地图参考 | 能力抽取参照 | 仅 ZAgenticOPN；作参考不单独成模块 [matrix §7] |

---

## 3. A/B 两池初分提案（三元组精准定位 · zj 2026-11-16 拍板）

`定位格式`：`<模块, 仓库, GIT_COMMIT_ID>`。每条来源精确到 40 位 commit SHA，全部取自 `maturity-evidence.md` 的 pinned SHA（与 sealed ledger 一致），杜绝「照抄了别的版本」的漂移。

`角色标注`（三元组定位暴露的关键区分）：
- **契约源（②用）**：该 commit 上有此模块的 sealed Evidence（矩阵 §3 的 `mod-*` ID），定位到功能声明原文。
- **实现源（①用）**：该 commit 所在仓库闸门 1+2+3 全过，可复制代码。
- **⚠ 两者可能落在不同 commit**：契约源有 sealed 功能证据但闸门未必过；实现源闸门全过但可能无该功能的 sealed 证据。见 §5 待验证第 5 条。

`模式`：① 复制代码 / ② 只取契约另写 / 参考。

### 3.1 A 池模块表（12 模块全在此）

| 模块 | 模式 | 依据 |
|---|---|---|
| M1 Work Item 生命周期 | ② 状态机自研 + ① ledger 机械 | Q9 Work Item 一等公民 → 状态机必须自研；ledger 机械可复制 [证据] |
| M2 身份与 scope | ② 契约重写 | matrix §5 必须自研，qm≠ZAgenticOPN 不可互推 [证据] |
| M3 审批与 Human 门 | ② 契约重写 + 需 zj 裁决模型 | matrix §6 四表达冲突，未裁决 [证据] |
| M4 结果与 provenance | ① ledger 复制 + ② provenance 语义 | matrix §5 append-only ledger 是明确契约 [证据] |
| M5 执行与工作区隔离 | ① 复制 | matrix §5 native；实现源闸门全过 [证据]，但 sealed 功能证据在另一批 commit [⚠] |
| M6 可观测与回放 | ① 复制 + 适配 | matrix §5 adapted [证据]，实现源同 M5 [⚠] |
| M7 会话上下文 | ① 复制 | matrix §4 L2 [证据] |
| M8 共享记忆/知识层 | ② 边界自研 + ① 存储机械 | matrix §5 必须自研边界 [证据] |
| M9 配置与策略 | ① 复制 | matrix §4 L3 [证据] |
| M10 运行时集成 | ① 复制 | matrix §7 参照物已把 qm 列 L3 能力来源 [证据] |
| M11 Agent 间协议 | ① 复制协议 | matrix §5 可复用协议 [证据] |
| M12 技术设计与部署 | ① 复制模式 | matrix §4 L3 [证据]，实现源同 M5 [⚠] |
| M13 能力地图参考 | 参考 | matrix §7 [证据] |

### 3.2 A 池来源三元组（逐模块，精确到 commit）

```
<M1 Work Item 生命周期, JF3Env/opencode-coordination, 2c9dd06f21716d8fc5885a266b119e58e78f2a0d>   契约源(九态 ledger, E 9101cfa7) + ①ledger 实现源(闸门全过)
<M1 Work Item 生命周期, jununfly/ZAgenticOPN, 2ff40cc052aae12fc7a324f89691e9f194985d24>           契约源(四态, E 3f9dde43; 自有)

<M2 身份与 scope, yc-software/qm, 605c259b28d54ee750c526b11925ddea3e0e6f59>                        契约源(E 114f13c4) + ①实现源(闸门全过)
<M2 身份与 scope, jununfly/ZAgenticOPN, 2ff40cc052aae12fc7a324f89691e9f194985d24>                  契约源(E 37c46d46; 自有)

<M3 审批与 Human 门, yc-software/qm, 605c259b28d54ee750c526b11925ddea3e0e6f59>                     契约源(三姿态, E c8500b38) + ①实现源
<M3 审批与 Human 门, JF3Env/opencode-coordination, 2c9dd06f21716d8fc5885a266b119e58e78f2a0d>       契约源(E 1a1c6d98)
<M3 审批与 Human 门, usemozzie/mozzie, 80f3515684722a8909fbc0c17a0526664ec0349a>                   契约源(review, E 3e8488d2) [B池闸门2不过]
<M3 审批与 Human 门, jununfly/ZAgenticOPN, 2ff40cc052aae12fc7a324f89691e9f194985d24>               契约源(E 06b3135d; 自有)

<M4 结果与 provenance, JF3Env/opencode-coordination, 2c9dd06f21716d8fc5885a266b119e58e78f2a0d>     契约源+①ledger 实现源(E 01ccf221, 闸门全过)
<M4 结果与 provenance, jununfly/ZAgenticOPN, 2ff40cc052aae12fc7a324f89691e9f194985d24>             契约源(E ddea4d90; 自有)

<M5 执行与工作区隔离, alamops/agetor, 897b70afb6f7671dc418c6d1053dbf8fbc3c81e0>                   契约源(E e6275d13) [B池闸门2不过]
<M5 执行与工作区隔离, lanes-sh/app, 7b9cb385d1100ded8a74986f81472f8856840578>                      契约源(E a8434e60) [B池闸门2+3不过]
<M5 执行与工作区隔离, standardagents/dmux, 8cb3d926631a9349ab67f7ece41d218427ac7e24>              契约源(E 205fcc6c) [覆盖薄弱]
<M5 执行与工作区隔离, stablyai/orca, cbd75eb0084aaa16feb04a079140f77631be6892>                 ✅①实现源 sealed 证据 `6a6126dd`（B1, "each in its own worktree"；采自 ba1f8f9e）；⚠SHA 为当前 HEAD，摄取前须重解析
<M5 执行与工作区隔离, AI-for-anyone/loop-now, 1e04ed00da0e7410c2240c6e21f4546933eb4af8>            ✅①实现源 sealed 证据 `18a7347e`（B4, concepts.md APFS clone + task workspace 复用）
<M5 执行与工作区隔离, herdrdev/herdr, ee5bfb5041bb3e4a49d591c72308aae3c81ecdde>                    ✅①实现源 sealed 证据 `a15db661`（B4, AGENTS.md dedicated worktree + no nested）

<M6 可观测与回放, yc-software/qm, 605c259b28d54ee750c526b11925ddea3e0e6f59>                        契约源(E b30ee359) + ①实现源
<M6 可观测与回放, jununfly/ZAgenticOPN, 2ff40cc052aae12fc7a324f89691e9f194985d24>                  契约源(E 0a8445ac; 自有)
<M6 可观测与回放, stablyai/orca, cbd75eb0084aaa16feb04a079140f77631be6892>                 ❌①实现源无 sealed 证据（三轮采集失败）；orca 不宜作 M6 源，unknown 保留；⚠SHA 为采集瞬时 HEAD
<M6 可观测与回放, AI-for-anyone/loop-now, 1e04ed00da0e7410c2240c6e21f4546933eb4af8>            ✅①实现源 sealed 证据 `b55ea9ef`（task nodes/review loops/retries）
<M6 可观测与回放, herdrdev/herdr, ee5bfb5041bb3e4a49d591c72308aae3c81ecdde>                    ✅①实现源 B2 事实层 `7f5eae80`（detection evidence）+ `be630dc8`（pane 状态标记）

<M7 会话上下文, yc-software/qm, 605c259b28d54ee750c526b11925ddea3e0e6f59>                          契约源(E 1fcc9288, 弱语义) + ①实现源
<M7 会话上下文, alamops/agetor, 897b70afb6f7671dc418c6d1053dbf8fbc3c81e0>                         契约源(E 7d2249b7) [B池闸门2不过]
<M7 会话上下文, songs-aaa/shared-memory-vault, 59f0b12134622c0ad93ef59ef6373cfe587deaf3>          契约源(E 15160857) [B池闸门2不过]

<M8 共享记忆/知识层, yc-software/qm, 605c259b28d54ee750c526b11925ddea3e0e6f59>                     契约源(E e878e527) + ①存储机械实现源
<M8 共享记忆/知识层, songs-aaa/shared-memory-vault, 59f0b12134622c0ad93ef59ef6373cfe587deaf3>      契约源(纯 Markdown, E 1eedaed6) [B池闸门2不过]
<M8 共享记忆/知识层, jununfly/ZAgenticOPN, 2ff40cc052aae12fc7a324f89691e9f194985d24>              契约源(E 1b866cef; 自有)

<M9 配置与策略, yc-software/qm, 605c259b28d54ee750c526b11925ddea3e0e6f59>                          契约源(E ad01939f) + ①实现源
<M9 配置与策略, themanojdesai/python-a2a, 40b969a465f85e8156793b7cfac16c5e23ed0b86>              契约源(E 8a03946e) + ①实现源(闸门全过)
<M9 配置与策略, jununfly/ZAgenticOPN, 2ff40cc052aae12fc7a324f89691e9f194985d24>                   契约源(E 6814fc75; 自有)

<M10 运行时集成, yc-software/qm, 605c259b28d54ee750c526b11925ddea3e0e6f59>                        契约源(E 3ae4f38b) + ①实现源(substrate interface, 闸门全过)
<M10 运行时集成, jununfly/ZAgenticOPN, 2ff40cc052aae12fc7a324f89691e9f194985d24>                  契约源(E 5da1a811; 自有)

<M11 Agent 间协议, JF3Env/opencode-coordination, 2c9dd06f21716d8fc5885a266b119e58e78f2a0d>        契约源(typed messages, E 4e988871) + ①实现源
<M11 Agent 间协议, themanojdesai/python-a2a, 40b969a465f85e8156793b7cfac16c5e23ed0b86>           契约源(A2A/MCP, E 5d423995) + ①实现源(闸门全过)

<M12 技术设计与部署, yc-software/qm, 605c259b28d54ee750c526b11925ddea3e0e6f59>                    契约源(E e38a7af1) + ①实现源
<M12 技术设计与部署, makifbaysal/tasktrooper, ae5fb965c4758bbb25d2fac7f10f9bb26cb63823>           契约源(E 834655c5) + ①实现源(闸门全过)
<M12 技术设计与部署, stablyai/orca, cbd75eb0084aaa16feb04a079140f77631be6892>                 ✅①实现源 sealed 证据 `2924c46e`（B3, Remote Server/cloud VM/laptop；采自 cbd75eb0；已弃用弱证据 `fa800718`）
<M12 技术设计与部署, AI-for-anyone/loop-now, 1e04ed00da0e7410c2240c6e21f4546933eb4af8>           ✅①实现源 sealed 证据 `186172e0`（loopdata volume/SQLite/docker compose）
<M12 技术设计与部署, herdrdev/herdr, ee5bfb5041bb3e4a49d591c72308aae3c81ecdde>                   ✅①实现源 B2 事实层 `96de34e8`（state/runtime 分离）+ `43a2fb18`（codec 不可变）+ `1590f5d5`（单二进制）

<M13 能力地图参考, jununfly/ZAgenticOPN, 2ff40cc052aae12fc7a324f89691e9f194985d24>               契约源(E 984e472f; 自有)
```

### 3.3 B 池（模块列表 · zj 2026-11-16 改为模块粒度）

按 zj 原始定义（R1 Q4），B 池主体是**功能/模块候选**而非仓库。每条用三元组定位，并标注进池理由分两类：**[不成熟]** 无可运行实现/测试门；**[法律受阻]** 功能成形但无法合法复制。

```
[M5 执行与工作区隔离, alamops/agetor, 897b70afb6f7671dc418c6d1053dbf8fbc3c81e0]                 [不成熟] 闸门2 无 CI/test
[M5 执行与工作区隔离, lanes-sh/app, 7b9cb385d1100ded8a74986f81472f8856840578]                    [法律受阻] 闸门2+3 无 license（功能成形，E a8434e60）
[M3 审批与 Human 门, usemozzie/mozzie, 80f3515684722a8909fbc0c17a0526664ec0349a]                 [不成熟] 闸门2 无测试目录
[M7 会话上下文, alamops/agetor, 897b70afb6f7671dc418c6d1053dbf8fbc3c81e0]                        [不成熟] 闸门2
[M8 共享记忆/知识层, songs-aaa/shared-memory-vault, 59f0b12134622c0ad93ef59ef6373cfe587deaf3]    [不成熟] 闸门2 无 CI/test（纯 Markdown 模式仍作 M8 边界参考）
[M5 执行与工作区隔离, standardagents/dmux, 8cb3d926631a9349ab67f7ece41d218427ac7e24]             [不成熟] 覆盖薄弱（1 条 Evidence）
[M-待定, multica-ai/multica, 41885a6d816834663dad8e6944658e2ac8555844]                           [法律受阻] Apache+附加条件待复核；无 sealed 功能证据，模块归属待定
```

**重复出现说明**：M5/M3/M7/M8 同时出现在 A 池（有别的仓库可作来源）和 B 池（另有仓库的该功能模块不成熟/受阻）——这是**同一功能的不同来源候选成熟度不同**，不是矛盾。B 池是这些来源的「待 PoC」标签，不是把模块整体踢出 A 池。

---

## 4. 最小可运行切片建议（接 Q8）

**切片目标**：让「一个人类用户 + 多 Agent」跑通一条 Work Item：`创建 → claim → 执行(worktree) → 结果+provenance → Human 门 → 完成`。

**该切片需要的模块**：M1(②)、M2(②)、M3(② 先选一种 Human 模型)、M4(① ledger + ② prov)、M5(①)、M10(①)、M11(①)。

**自建模块数（Q8 硬门）**：L1 语义自研单元 = M1 状态机、M2 身份/scope、M3 Human 门、M4 provenance、M8 边界 ≈ **4–5 个**。建议 **N=5**（最小切片内自建 ≤5），其余走 ① 复制。

**三计数初估（待 R4 细化，只数模块）**：
- 摄取（① 复制）：M4-ledger、M5、M6、M7、M9、M10、M11、M12 的可复制部分 ≈ 7–8
- 裁切（② 契约重写）：M1 状态机、M2、M3、M4-prov、M8 边界 ≈ 5
- 自建（L1 语义核心）：M1/M2/M3/M4-prov/M8 ≈ 4–5（即 N 上限）
- B 池（待 PoC，不计入 v1 分母）：7 条来源三元组（见 §3.3），其中 [不成熟] 5 条 / [法律受阻] 2 条

---

## 5. 待 zj 裁决 / 待验证

1. **Human 门四种模型（M3）**：tasktrooper 全自动 / ZAgenticOPN 例外处理 / qm 三姿态 / mozzie review——须在 Coding 前定一种（matrix §6 明示不裁决）。这是 L1 自研语义的第一个硬决策。
2. **multica license 复核**：Apache+附加条件，① 前需你确认附加条件。
3. **L1 语义 fixture 验证**：matrix §5/§9 标注「复用边界是分析层推断，待 fixture 验证」。M2/M3/M8 边界建议先写黑盒契约 fixture 再定 ①/②。
4. **ZAgenticOPN 迁入补 license**：自有仓库无牌，迁入 ZOnePersonNetwork 后补一份 license 声明（避免新仓库代码成无牌状态）。
5. **契约源 / 实现源错位 — 已补采，9 格中 8 格解决（2026-11-16）**：zj 选 A，对 M5/M6/M12 做了三轮定向 sealed 采集（B1 正文短语 / B3 单仓库短语 / B4 路径导航）。结果见 `docs/reasearch/opn-maturity/2026-11-16-resupply.findings.md`：M5 三仓库全拿到直接证据（orca `6a6126dd` / loop-now `18a7347e` / herdr `a15db661`）；M6 有 loop-now `b55ea9ef` + herdr `7f5eae80`/`be630dc8`；M12 三仓库全有（orca `2924c46e` 替换了旧弱证据 `fa800718` / loop-now `186172e0` / herdr B2 多条）。**唯一未覆盖：orca-M6**——三轮均失败，orca 文档无可密封的产品级可观测声明，unknown 保留（不写 absent，不伪造、不把非 sealed 升级为 sealed）；R4 若需 orca 作 M6 源，只能按 charter 第 8 节走非 sealed 一手阅读，仅作风险与验证门。
6. **三元组 SHA 的来源纪律与漂移机制（风险 1 已处置）**：漂移不是 orca 个案——`resolve_head.py --check` 实测 **13 个仓库中 4 个已漂移**（orca `ba1f8f9e→cbd75eb0`、agetor `897b70af→1cb338de`、tasktrooper `ae5fb965→d9131b50`、qm `605c259b→340e5536`），其余 9 个未变。纪律：
   - **三元组 SHA 表达「摄取哪个版本」，Evidence ID 表达「语义从哪来」，二者解耦**。当前文档三元组已统一到解析时刻的 HEAD；每条证据另标其采集批次 pin（如 M5-orca 证据采自 `ba1f8f9e`，三元组写当前 `cbd75eb0`）。
   - **R4 摄取任一仓库前必须运行** `python3 docs/reasearch/opn-maturity/resolve_head.py --check docs/designs/product-module-map.md`；输出 DRIFT 即先回填三元组 SHA 再摄取。退出码 1 = 有漂移。
   - 因编译器只钉 HEAD（见第 7 条），"按历史 SHA 摄取"物理不可行——不要试图把三元组改回旧的 11-08 pin。证据溯源靠 Evidence ID，不靠三元组 SHA 的一致性。
7. **补采工具链限制（留痕）**：编译器 `resolveRevision` 只钉默认分支 HEAD、忽略 brief 的 revision/pin，无法按历史 SHA 采集。受控实验与四条替代路径见 `docs/reasearch/opn-maturity/2026-11-16-sealed-resupply-blocked.md`。本轮选 A（重 pin 到 HEAD），已如实记录，未静默偏差。

---

## 6. 与 R2 决策的闭环

- Q5「默认 ①」在 L2/L3（M5/M6/M7/M9/M10/M11/M12）充分兑现；L1（M1/M2/M3/M4/M8）按 Q5 例外走 ②，由 Human 逐模块确认语义所有权。
- Q6 闸门 3「法律有权」把 `lanes-sh/app`（无 license）与 `multica`（自定义 license）挡在 ① 之外——证明 Gate 3 不是橡皮章。
- Q8「只数模块」：本提案全程以模块为计数单位，未引入功能点/覆盖率。
- Q9：M1 即 Work Item 一等公民，状态机自研属预期内的 L1 0→1 工作量，已计入 N=5。
