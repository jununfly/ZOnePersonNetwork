---
doc-kind: reference
authority: supporting
authority-id: opn.requirements-fit-matrix
---

# 需求拟合矩阵 · 5 条 EC（supporting / 从基线拆 R）

> 本页覆盖采纳的 EC-01/02/03/05/06，是**拟合事实矩阵 + 拟合层判定**，不是产品计划、不是采用裁决。
> 由 `docs/reasearch/opn-cross-comparison/_gen_fit_matrix.py` 从横比 bundle / 复用证据账本 / 产品结构基线机械派生；
> Human 决策以带 SoT 存在性校验的显式常量表注入，Agent 不推断验收判据、不预置分类。

## 1. 边界与口径（zj 2026-11-24 裁决汇总）

- **范围**：EC-01 样板 + EC-02/03/05/06 铺开（Q10a 样本验收后 zj 选①）。共 5 条 EC、15 条 R、43 个 R×O 单元（EC-01 8 格 + 新增 35 格，L3 已全部由 zj 兜底并回灌）。
- **R 锚点**：锚 EC（Q1a），按 Human 可独立观察的验收节点切（Q6c/Q11a），不贴模块边界；模块只作归属标注。acceptance 由 Human 逐条校准（Q2a/Q3a）。
- **候选 O（Q1a 铺开口径）**：每条 EC 只取该 EC 全模块 sealed-native 交集；严格闸门不放宽。EC-02=2 家、EC-03=3 家、EC-05=4 家、EC-06=5 家，加上 EC-01=2 家，共 16 个 EC×O 对。
- **三层打分（Q7a）**：L1 客观打分（Agent 据本格 sealed EVID 原文评分 + 扣分理由）→ L2 机器复核（母模型仪器机械复算）→ L3 Human 兜底。模块级 hypothesis 只作参照，**不是打分来源**。
- **L3 状态（全量回灌）**：43/43 格均为 zj 逐格填写的原文（EC-01 8 格 + 新增 35 格），19 格 `认同 L2 未满足`（endorse）、24 格 `可以有`（raise_to_pass）。改动须改生成器 `HUMAN_FINAL` 常量表后重跑，不得手改产物。
- **双输入（Q1a/Q5a）**：每 EC 一对 `fit-input-l1.json`（L1 原值）+ `fit-input-classification.json`（复核分派生因子）。路径 `tmp/skills-outputs/zj-open-source-capability-fit/ec01-scaffold/` 等（目录名去掉 EC 中的连字符），EC-01 文件名与路径均沿用样板。
- **复核分进分类（Q3a/Q4a/Q6a）**：`可以有` 用两满一值 `[1.0,1.0,max(eff,FIT_OK)]`，eff 精确=FIT_OK；`认同 L2 未满足` 保持 L1 原值。判定只用母模型 `effective_fit`/`cell_satisfied`/`FIT_OK`/`FIT_FAIL`，**到拟合层为止，不出 A/B/C/D**。
- **成本维度（本轮重开 Q9b）**：zjj 给出逐候选 cost/E + adaptation **初判**，由常量表写入两份输入；只对 classification 输入跑 `assess` 得**参考分类**（§5.3）。E 单位已由 zj 认可标注为「相对成本点（≈人日量级）」，**仅供参考**；数值与分类均为参考信号，**是否自研/采用由 zj 在规划-执行阶段人工判断**。
- **priority/critical**：全部 R=`must` + `critical=true`（Q8a）。
- **URL/license**：sealed SoT 未采集，填占位；非闸门字段。

## 2. R 清单（5 条 EC，共 15 条）

| EC | R | 验收节点（Human 可观察） | acceptance（Human 校准） | 归属模块 | priority | critical |
|---|---|---|---|---|---|---|
| EC-01 | R1.1 | 目标提交后可见 | Human 提交目标后，能在列表看到对应 Work Item，其状态可读且能前进 | M1 | must | true |
| EC-01 | R1.2 | 执行进度可观察 | Human 能看到 Agent 已接收并在隔离边界内执行，进度/阻塞可见、互不污染 | M5 | must | true |
| EC-01 | R1.3 | 结果产物可复核 | Human 能看到本次产出，且来源/步骤可追溯 | M4 | must | true |
| EC-01 | R1.4 | Human 门验收可审计 | Human 在门上 approve/reject，动作有账本、可审计 | M3 | must | true |
| EC-02 | R2.1 | 拒绝与反馈在门上可见 | Human 在门上 reject 并写反馈后，该拒绝与反馈能在门上可见且关联到原结果、动作入账本 | M3 | must | true |
| EC-02 | R2.2 | 拒绝历史可查 | Human 能查到前次结果、反馈与来源，反馈不丢失 | M4 | must | true |
| EC-02 | R2.3 | Agent 带反馈重做 | 能看到 Agent 已带该反馈重新执行，工作区隔离、进度/阻塞可见 | M5 | must | true |
| EC-02 | R2.4 | 重做后再次进门可观察 | board/回放能看到前后两次结果与反馈应用情况 | M6 | must | true |
| EC-03 | R3.1 | 设备 A 会话上下文可见 | Human 在设备 A 发起会话后，能看到可接续的会话上下文（标识/当前进度） | M7 | must | true |
| EC-03 | R3.2 | 上下文进入共享记忆 | 设备 B 能看到设备 A 已沉淀的会话上下文/共享记忆，且可跨设备边界清晰 | M8 | must | true |
| EC-03 | R3.3 | 设备 B 接续运行 | 从该上下文继续同一会话，运行资源/沙箱按 scope 接入、接续前后状态连续 | M10 | must | true |
| EC-05 | R5.1 | 事实沉淀可追溯 | Human 完成协作并要求沉淀后，能看到事实写入共享记忆层，来源/归属可追溯 | M8 | must | true |
| EC-05 | R5.2 | 后续会话检索与复用 | 后续会话能检索到该事实并看到它被复用到新会话，引用可辨认 | M7 | must | true |
| EC-06 | R6.1 | 失败点可定位 | Human 在 board/审计视图中能定位一次失败或待审计的 run 及其时间点 | M6 | must | true |
| EC-06 | R6.2 | 从失败点回放 | 能从失败点重放该 run，看到相关步骤与产出来源/账本 | M4 | must | true |

## 3. 候选 O（按 EC 严格 native 交集）

| EC | 候选 O | 版本（reuse ledger pin 实读 40-hex） | 来源 sealed ledger |
|---|---|---|---|
| EC-01 | multica | `7a926b824fcf7a3687097f353d6a34f79d8b568d` | `docs/reasearch/opn-cross-comparison/collect/ledger-multica.json` |
| EC-01 | loop-now | `b7d6811877e6d7341ac539934ae87028df87b1e6` | `docs/reasearch/opn-cross-comparison/collect/ledger-loop-now.json` |
| EC-02 | loop-now | `b7d6811877e6d7341ac539934ae87028df87b1e6` | `docs/reasearch/opn-cross-comparison/collect/ledger-loop-now.json` |
| EC-02 | multica | `7a926b824fcf7a3687097f353d6a34f79d8b568d` | `docs/reasearch/opn-cross-comparison/collect/ledger-multica.json` |
| EC-03 | loop-now | `b7d6811877e6d7341ac539934ae87028df87b1e6` | `docs/reasearch/opn-cross-comparison/collect/ledger-loop-now.json` |
| EC-03 | multica | `7a926b824fcf7a3687097f353d6a34f79d8b568d` | `docs/reasearch/opn-cross-comparison/collect/ledger-multica.json` |
| EC-03 | qm | `605c259b28d54ee750c526b11925ddea3e0e6f59` | `docs/reasearch/opn-landscape/2026-11-08-ledger-response.json` |
| EC-05 | loop-now | `b7d6811877e6d7341ac539934ae87028df87b1e6` | `docs/reasearch/opn-cross-comparison/collect/ledger-loop-now.json` |
| EC-05 | mem-vault | `59f0b12134622c0ad93ef59ef6373cfe587deaf3` | `docs/reasearch/opn-landscape/2026-11-08-ledger-response.json` |
| EC-05 | multica | `7a926b824fcf7a3687097f353d6a34f79d8b568d` | `docs/reasearch/opn-cross-comparison/collect/ledger-multica.json` |
| EC-05 | qm | `605c259b28d54ee750c526b11925ddea3e0e6f59` | `docs/reasearch/opn-landscape/2026-11-08-ledger-response.json` |
| EC-06 | ZAgenticOPN | `2ff40cc052aae12fc7a324f89691e9f194985d24` | `docs/reasearch/opn-landscape/2026-11-08-ledger-response.json` |
| EC-06 | loop-now | `b7d6811877e6d7341ac539934ae87028df87b1e6` | `docs/reasearch/opn-cross-comparison/collect/ledger-loop-now.json` |
| EC-06 | multica | `7a926b824fcf7a3687097f353d6a34f79d8b568d` | `docs/reasearch/opn-cross-comparison/collect/ledger-multica.json` |
| EC-06 | opencode-coordination | `2c9dd06f21716d8fc5885a266b119e58e78f2a0d` | `docs/reasearch/opn-landscape/2026-11-08-ledger-response.json` |
| EC-06 | qm | `605c259b28d54ee750c526b11925ddea3e0e6f59` | `docs/reasearch/opn-landscape/2026-11-08-ledger-response.json` |

## 4. R×O 三层打分矩阵

| EC | R | O | status | 客观打分 cov/sem/comp（L1） | 扣分理由（L1） | 机器复核 eff/满足（L2） | Human复核分（L3） | Human 兜底原文（L3） | evidence |
|---|---|---|---|---|---|---|---|---|---|
| EC-01 | R1.1 | multica | native | 0.90/0.90/0.80 | EVID 显示 issue 分配/状态流转/report progress/raise blockers 齐备；扣分点：状态机是通用 issue 流转（available→claimed→completed），与我方 Objective→可验收工作项的语义同构性未证，接入需适配身份/Agent 网络。 | 0.648 / 未满足 | 0.900 | 可以有，它填充了 Objective→可验收工作项 的中间过程，是协作场景下的一种流转路径 | EVID::a67400762c931df62135608d |
| EC-01 | R1.1 | loop-now | native | 0.75/0.70/0.80 | EVID 偏对话 + task workflow 协调，可见性侧重 conversation/tool calls/who is working，而非显式的『提交目标生成工作项』结构化状态机；plugin 扩展点丰富利于组合。 | 0.420 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::3605745b0cae1cc75dd59c80 |
| EC-01 | R1.2 | multica | native | 0.90/0.90/0.80 | EVID 有 runtime you control + comments as it goes + raise blockers + intent/run/diff 同 issue；扣分点：『runtime you control』是部署层控制，是否等于 per-task 强隔离（worktree/容器）未在摘录明示，互不污染属推断。 | 0.648 / 未满足 | 0.900 | 可以有，它是待新增feature的备选 | EVID::76fd261e3f84f3c9e33a84c6 |
| EC-01 | R1.2 | loop-now | native | 0.90/0.90/0.70 | EVID 明确 each agent runs in its own working directory、server launches/recycles/bounds them，隔离证据强；扣分点：非 OS 级沙箱，且依赖外部 Pi 执行引擎与 plugin host，接入需适配。 | 0.567 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::598de2204e4d84a75a0020d4 |
| EC-01 | R1.3 | multica | native | 0.90/0.90/0.80 | EVID 有 intent/run/decisions/diff stay connected to the same issue，来源与步骤追溯强；扣分点：provenance 挂在 issue 粒度，完整审计账本结构未在摘录展示。 | 0.648 / 未满足 | 0.900 | 可以有，这是具体的使用细节，这些关联信息的侧重在于可观察、可回溯，不能直接用于审计 | EVID::5c1fa749e640c3dec0dbd328 |
| EC-01 | R1.3 | loop-now | native | 0.75/0.70/0.70 | EVID 有 artifacts and records stay after execution resources recycled、frozen workflow node by node；扣分点：『谁在何时做了什么』的细粒度溯源未展示，偏 workflow 记录而非审计账本。 | 0.367 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::0794e7e8dbb753920bae8a05 |
| EC-01 | R1.4 | multica | native | 0.85/0.85/0.75 | EVID 明确 Review gates → Work lands in review, not in main. You decide what ships，approve/reject 语义成立；扣分点：账本结构（谁批/何时/依据）未明示。刻意不因模块级『必须自研』假设压低——该假设与本格 sealed 证据冲突。 | 0.542 / 未满足 | 0.900 | 可以有，这是Human介入工作的门禁之一 | EVID::2cc46ac299adc52b807b122e |
| EC-01 | R1.4 | loop-now | native | 0.50/0.40/0.50 | EVID 讲插件安装信任分级（source grading / pre-install preview / one-click global disable），不是工作流中的 Human approve/reject 门、无审批账本语义；EVID 虽 sealed 但与我方 R1.4 验收节点语义错配，故三项压低。这是逐 O 差异，非模块级一刀切。 | 0.100 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::d3d21a128f2d058198f00504 |
| EC-02 | R2.1 | loop-now | native | 0.45/0.30/0.45 | EVID 是插件安装信任分级（source grading / pre-install preview / global disable），没有工作流中的 Human reject-with-feedback 门，也不记录打回历史；semantic_match 压到 0.30。 | 0.061 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::d3d21a128f2d058198f00504 |
| EC-02 | R2.1 | multica | native | 0.80/0.75/0.70 | EVID 有 Review gates → work lands in review → you decide what ships，Human 准出成立；扣分点：摘录未展示 reject 反馈如何回写为可追溯的打回历史，故语义与组合未满分。 | 0.420 / 未满足 | 0.900 | 可以有，这是Human介入工作的门禁之一 | EVID::2cc46ac299adc52b807b122e |
| EC-02 | R2.2 | loop-now | native | 0.60/0.45/0.60 | EVID 说 artifacts and records stay after execution resources are recycled、workflow frozen node by node，记录持久性成立；扣分点：看不到 reject-with-feedback 的归因链，反馈与前次结果的绑定未证。 | 0.162 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::0794e7e8dbb753920bae8a05 |
| EC-02 | R2.2 | multica | native | 0.90/0.80/0.80 | EVID 有 intent/run/decisions/diff stay connected to the same issue，general provenance 强；扣分点『拒绝历史』这一特定语义未在摘录出现，不能从通用 provenance 直接推出。 | 0.576 / 未满足 | 0.900 | 可以有 | EVID::5c1fa749e640c3dec0dbd328 |
| EC-02 | R2.3 | loop-now | native | 0.85/0.70/0.70 | EVID 明确 each agent runs in its own working directory、server launches/recycles/bounds them，隔离与重跑环境成立；扣分点：摘录没有『带反馈重做』的闭环语义，只有 frozen workflow 的线性/有界循环。 | 0.416 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::598de2204e4d84a75a0020d4 |
| EC-02 | R2.3 | multica | native | 0.80/0.70/0.75 | EVID 有 assigned issue → runtime you control → comments as it goes → hand back for review，具备重做载体；扣分点：没有展示反馈如何注入下一轮执行，重做仍是推断。 | 0.420 / 未满足 | 0.900 | 可以有 | EVID::76fd261e3f84f3c9e33a84c6 |
| EC-02 | R2.4 | loop-now | native | 0.85/0.75/0.70 | EVID 的 run timeline + bounded review loops + artifacts persist 让『重做后可见』成立；扣分点：Human 门再次进入的审批事件未在摘录出现，只有 workflow 层的 loop。 | 0.446 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::033b3e9e285ecc2cfabae1c4 |
| EC-02 | R2.4 | multica | native | 0.85/0.70/0.75 | EVID 的 live run transcript（每次 tool call/command 带时间戳、失败测试输出展开）覆盖强；扣分点：摘录证明可观察，但未证明前后两次结果与反馈应用被并排对照。 | 0.446 / 未满足 | 0.900 | 可以有 | EVID::71dfad6640e6f45a720f8a69 |
| EC-03 | R3.1 | loop-now | native | 0.85/0.85/0.70 | EVID 有 Keep work in context：continue conversation/workspace、same agent reusing task workspace and session across steps，连续语义强；扣分点：本地 console 单安装，跨设备的设备 A/B 身份未在摘录出现。 | 0.506 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::fc13fdb5c6a479f214a8e2a7 |
| EC-03 | R3.1 | multica | native | 0.70/0.60/0.70 | EVID 有 Chat + Projects 挂 repos/docs 作 context；扣分点：没有会话标识、断点状态或『接续』语义，只是可发起工作与查问题。 | 0.294 / 未满足 | 0.900 | 可以有 | EVID::fcf4cce4e1d126ce88bdffec |
| EC-03 | R3.1 | qm | native | 0.75/0.60/0.65 | EVID 有 each person/room scoped memory/files/keychain/permissions/durable sandbox，scope 边界强；扣分点：摘录未把 scope 映射到『一次会话的接续上下文』，语义需适配。 | 0.292 / 未满足 | 0.900 | 可以有 | EVID::1fcc9288e24457d7fa94240e |
| EC-03 | R3.2 | loop-now | native | 0.65/0.45/0.55 | EVID 有 server persists the message、artifacts/records stay；扣分点：明确是 one local installation（Go server + SQLite + local data dir），无跨设备共享记忆语义，semantic_match 压低。 | 0.161 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::5d1c4de928a7b36251220b69 |
| EC-03 | R3.2 | multica | native | 0.70/0.55/0.65 | EVID 有 daemon on your laptop or cloud box + Skills playbook every agent reuses，跨设备运行与复用载体存在；扣分点：没有被证实的『同一份会话上下文』跨设备可见，Skills 不等于会话记忆。 | 0.250 / 未满足 | 0.900 | 可以有 | EVID::0c8c6d5548bf9d364a4fec2b |
| EC-03 | R3.2 | qm | native | 0.80/0.70/0.70 | EVID 有 per person/room scoped memory + durable sandbox + run it in your own cloud（Slack/web），跨设备载体最完整；扣分点：会议级『会话上下文』与 scope memory 的映射仍须适配。 | 0.392 / 未满足 | 0.900 | 可以有 | EVID::e878e5271a78993966d88f0b |
| EC-03 | R3.3 | loop-now | native | 0.60/0.30/0.50 | EVID 明说 one local installation、SQLite in a local data directory、组件不构成独立可扩展服务；与『设备 B 接续同一会话』直接冲突，semantic_match 0.30。 | 0.090 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::56ca86a50db2ccf35d17f401 |
| EC-03 | R3.3 | multica | native | 0.75/0.60/0.70 | EVID 有 self-hostable + daemon on laptop/cloud + works with agent CLIs，跨设备运行可搭；扣分点：没有 session handoff 或接续后状态连续的证据。 | 0.315 / 未满足 | 0.900 | 可以有 | EVID::8d8aec7e4652ff51053e99ec |
| EC-03 | R3.3 | qm | native | 0.85/0.80/0.75 | EVID 有 multiplayer harness in Slack and on the web + own cloud + per-scope durable sandbox，设备 B 接入与资源隔离成立；扣分点：『接续前后状态连续』未在摘录逐字证明。 | 0.510 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::3ae4f38b4de2d1769a598bc0 |
| EC-05 | R5.1 | loop-now | native | 0.60/0.40/0.55 | EVID 有 server persists message + artifacts/records stay after recycle，但只是执行记录；扣分点：没有共享知识层、事实沉淀动作或来源/归属结构。 | 0.132 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::5d1c4de928a7b36251220b69 |
| EC-05 | R5.1 | mem-vault | native | 0.90/0.80/0.75 | EVID 明确 plain cloud-synced Markdown → shared knowledge base for every agent and every device，session-blackboard CONTEXT.md；扣分点：Markdown 的『来源/归属』是约定而非结构化 provenance。 | 0.540 / 未满足 | 0.900 | 可以有 | EVID::1eedaed644a280db74133572 |
| EC-05 | R5.1 | multica | native | 0.75/0.65/0.70 | EVID 有 Skills：turn a solved problem into a playbook every agent reuses，具备沉淀与复用载体；扣分点：摘录未展示知识来源归属与可追溯账本。 | 0.341 / 未满足 | 0.900 | 可以有 | EVID::0c8c6d5548bf9d364a4fec2b |
| EC-05 | R5.1 | qm | native | 0.80/0.65/0.70 | EVID 有 each person and each room has its own scoped memory/files，沉淀与 scope 归属成立；扣分点：没有『完成协作后要求沉淀』的显式动作与事实级溯源。 | 0.364 / 未满足 | 0.900 | 可以有 | EVID::e878e5271a78993966d88f0b |
| EC-05 | R5.2 | loop-now | native | 0.65/0.45/0.60 | EVID 有 same agent reusing its task workspace and session across steps，延续性成立；扣分点：没有检索接口，也没有『被复用到新会话』的可辨认引用。 | 0.176 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::fc13fdb5c6a479f214a8e2a7 |
| EC-05 | R5.2 | mem-vault | native | 0.90/0.85/0.75 | EVID 明确 any agent reads a single file and resumes the work from where another left off — no context loss，复用语义最强；扣分点：纯 Markdown 无索引/检索机制，引用可辨认靠约定。 | 0.574 / 未满足 | 0.900 | 可以有 | EVID::151608571341f37ee2297dcb |
| EC-05 | R5.2 | multica | native | 0.75/0.60/0.70 | EVID 有 Chat → ask your workspace a question、Projects attach repos/docs as context，类检索入口存在；扣分点：答复是否引用已沉淀事实、引用是否可辨认未证。 | 0.315 / 未满足 | 0.900 | 可以有 | EVID::fcf4cce4e1d126ce88bdffec |
| EC-05 | R5.2 | qm | native | 0.70/0.55/0.65 | EVID 有 scoped memory/files/keychain，事实可存在；扣分点：没有跨会话检索与引用显示，且 scope 边界与『新会话复用』的关系需适配。 | 0.250 / 未满足 | 0.900 | 可以有 | EVID::1fcc9288e24457d7fa94240e |
| EC-06 | R6.1 | ZAgenticOPN | native | 0.75/0.60/0.65 | EVID 有 Health scorecard（C1–C4、Human intervention、context defects、Git acceptance、三次复验），审计口径强；扣分点：scorecard 是汇总统计，不是『一次失败 run 的时间点定位』。 | 0.292 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::0a8445acfd470fba8cb2c18a |
| EC-06 | R6.1 | loop-now | native | 0.85/0.80/0.70 | EVID 有 tool calls/commands/usage flow back into the run timeline，run 级可见性成立；扣分点：摘录没展示失败标记或按失败筛选，定位仍需人工翻 timeline。 | 0.476 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::033b3e9e285ecc2cfabae1c4 |
| EC-06 | R6.1 | multica | native | 0.95/0.95/0.80 | EVID 直接是 A live run transcript: every tool call and command timestamped, with a failing test's output open，失败点与时间双证据；扣分点：是否与审计视图/board 联动未在摘录展示。 | 0.722 / 未满足 | 0.900 | 可以有 | EVID::71dfad6640e6f45a720f8a69 |
| EC-06 | R6.1 | opencode-coordination | native | 0.75/0.55/0.65 | EVID 有 one append-only ledger of roles/work items/messages/progress/history + board updates，协作审计强；扣分点：不是 run 级诊断视图，失败时间点不在摘录中。 | 0.268 / 未满足 | 0.900 | 可以有 | EVID::d537234df40dcab3100b4eac |
| EC-06 | R6.1 | qm | native | 0.60/0.40/0.55 | EVID 是 crons/watches/webhooks + search internal notes/email/documents/databases/web，偏运营检索；扣分点：没有 run timeline、失败标记或时间点定位语义，semantic_match 压低。 | 0.132 / 未满足 | 0.900 | 可以有 | EVID::b30ee3590bb6aaead44befb3 |
| EC-06 | R6.2 | ZAgenticOPN | native | 0.90/0.85/0.75 | EVID 有五字段结果 + structured blocker + Git provenance + reviewer re-claim + references 核验 + 完成条件，来源与账本强；扣分点：『从失败点重放 run』未逐字出现。 | 0.574 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::ddea4d90bb2b7e250b08b616 |
| EC-06 | R6.2 | loop-now | native | 0.75/0.65/0.65 | EVID 有 tasks follow frozen workflow node by node + artifacts/records stay after recycle，部分回放与产出留存成立；扣分点：没有 provenance 账本结构，重放是推断。 | 0.317 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::0794e7e8dbb753920bae8a05 |
| EC-06 | R6.2 | multica | native | 0.90/0.85/0.80 | EVID 有 intent/run/decisions/diff stay connected to the same issue — nobody reconstructs context；扣分点：强 provenance 不等于可按失败点重放，回放动作未在摘录证明。 | 0.612 / 未满足 | 0.900 | 可以有 | EVID::5c1fa749e640c3dec0dbd328 |
| EC-06 | R6.2 | opencode-coordination | native | 0.80/0.65/0.70 | EVID 的 append-only ledger + event recorded/PR checked/board updated 提供审计账本；扣分点：面向协作事件而非 run 步骤回放，产物 provenance 粒度不足。 | 0.364 / 未满足 | —（认同 L2 未满足） | 认同 L2 未满足 | EVID::01ccf2212f91bcc504af0818 |
| EC-06 | R6.2 | qm | native | 0.80/0.65/0.70 | EVID 有 everything it does is audited + strict human approval per tool call，审计强；扣分点：审计记录与失败点重放/产出来源之间的链路未在摘录展示。 | 0.364 / 未满足 | 0.900 | 可以有 | EVID::fec47fe206b51915b2e19fb4 |

### 三层说明（口径与边界）

- **L1**：逐格读该 (R,O) 的 sealed EVID 原文后评分并写扣分理由（`SCORES` 常量表，含 `by`）。模块级 hypothesis 仅列作参照，不参与打分。
- **L2**：母模型 `capability_fit.py` 的 `effective_fit`（cov×sem×comp）与 `cell_satisfied`，是**独立代码路径的机械复算**（抓手算漂移），不是第二意见——仪器无独立打分接口。
- **L3**：`认同 L2 未满足`→endorse（复核分留空不改）；`可以有`→raise_to_pass。43/43 格已由 zj 兜底（19 endorse / 24 raise_to_pass）。
- **Human复核分**：仅 `可以有` 格填 `max(L2 eff, FIT_OK)`；`FIT_OK=0.9` 由仪器机械读取。此列已按 Q4a 落入 classification 输入，L1 原值不动。

### 模块级 hypothesis（参照，非打分来源）

| 模块 | reuse ledger hypothesis（assumption） | 为何不参与打分 |
|---|---|---|
| M1 | adapted：5 实现但状态机互不相容（opencode 九态 vs ZAgenticOPN 四态）[matrix §5] | 模块级假设，无法区分同模块不同 O 的证据差异（如 M3: multica 有 Review gate、loop-now 仅插件信任分级） |
| M10 | qm 强（central core + Postgres + per-scope sandbox + substrate interface）[matrix §7] | 模块级假设，无法区分同模块不同 O 的证据差异（如 M3: multica 有 Review gate、loop-now 仅插件信任分级） |
| M3 | **必须自研统一语义**；四种表达冲突（全自动/例外/三姿态/review）[matrix §5/§6] | 模块级假设，无法区分同模块不同 O 的证据差异（如 M3: multica 有 Review gate、loop-now 仅插件信任分级） |
| M4 | adapted：append-only ledger + 五字段结果是少数明确契约 [matrix §5] | 模块级假设，无法区分同模块不同 O 的证据差异（如 M3: multica 有 Review gate、loop-now 仅插件信任分级） |
| M5 | native 偏多：4 项目均 worktree 模式 [matrix §5] | 模块级假设，无法区分同模块不同 O 的证据差异（如 M3: multica 有 Review gate、loop-now 仅插件信任分级） |
| M6 | adapted：四种形态，口径不统一 [matrix §5] | 模块级假设，无法区分同模块不同 O 的证据差异（如 M3: multica 有 Review gate、loop-now 仅插件信任分级） |
| M7 | L2 层事实 [matrix §4] | 模块级假设，无法区分同模块不同 O 的证据差异（如 M3: multica 有 Review gate、loop-now 仅插件信任分级） |
| M8 | **必须自研边界**：mem-vault 纯 Markdown ≠ qm scope-memory+Postgres ≠ ZAgenticOPN 结构化事实 [matrix §5] | 模块级假设，无法区分同模块不同 O 的证据差异（如 M3: multica 有 Review gate、loop-now 仅插件信任分级） |

## 5. 双输入 validate 闸门 + 拟合层判定（不出 A/B/C/D）

### 5.1 validate G1–G6

| EC | 输入 | O | 闸门 | 结果 | 说明 |
|---|---|---|---|---|---|
| EC-01 | L1 | multica | G1-matrix-complete | ✓ PASS | OK |
| EC-01 | L1 | multica | G2-req-fields | ✓ PASS | OK |
| EC-01 | L1 | multica | G3-version-pinned | ✓ PASS | OK |
| EC-01 | L1 | multica | G4-evidence-present | ✓ PASS | OK |
| EC-01 | L1 | multica | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-01 | L1 | multica | G6-adaptation-mode | ✓ PASS | OK |
| EC-01 | L1 | loop-now | G1-matrix-complete | ✓ PASS | OK |
| EC-01 | L1 | loop-now | G2-req-fields | ✓ PASS | OK |
| EC-01 | L1 | loop-now | G3-version-pinned | ✓ PASS | OK |
| EC-01 | L1 | loop-now | G4-evidence-present | ✓ PASS | OK |
| EC-01 | L1 | loop-now | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-01 | L1 | loop-now | G6-adaptation-mode | ✓ PASS | OK |
| EC-01 | classification | multica | G1-matrix-complete | ✓ PASS | OK |
| EC-01 | classification | multica | G2-req-fields | ✓ PASS | OK |
| EC-01 | classification | multica | G3-version-pinned | ✓ PASS | OK |
| EC-01 | classification | multica | G4-evidence-present | ✓ PASS | OK |
| EC-01 | classification | multica | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-01 | classification | multica | G6-adaptation-mode | ✓ PASS | OK |
| EC-01 | classification | loop-now | G1-matrix-complete | ✓ PASS | OK |
| EC-01 | classification | loop-now | G2-req-fields | ✓ PASS | OK |
| EC-01 | classification | loop-now | G3-version-pinned | ✓ PASS | OK |
| EC-01 | classification | loop-now | G4-evidence-present | ✓ PASS | OK |
| EC-01 | classification | loop-now | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-01 | classification | loop-now | G6-adaptation-mode | ✓ PASS | OK |
| EC-02 | L1 | loop-now | G1-matrix-complete | ✓ PASS | OK |
| EC-02 | L1 | loop-now | G2-req-fields | ✓ PASS | OK |
| EC-02 | L1 | loop-now | G3-version-pinned | ✓ PASS | OK |
| EC-02 | L1 | loop-now | G4-evidence-present | ✓ PASS | OK |
| EC-02 | L1 | loop-now | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-02 | L1 | loop-now | G6-adaptation-mode | ✓ PASS | OK |
| EC-02 | L1 | multica | G1-matrix-complete | ✓ PASS | OK |
| EC-02 | L1 | multica | G2-req-fields | ✓ PASS | OK |
| EC-02 | L1 | multica | G3-version-pinned | ✓ PASS | OK |
| EC-02 | L1 | multica | G4-evidence-present | ✓ PASS | OK |
| EC-02 | L1 | multica | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-02 | L1 | multica | G6-adaptation-mode | ✓ PASS | OK |
| EC-02 | classification | loop-now | G1-matrix-complete | ✓ PASS | OK |
| EC-02 | classification | loop-now | G2-req-fields | ✓ PASS | OK |
| EC-02 | classification | loop-now | G3-version-pinned | ✓ PASS | OK |
| EC-02 | classification | loop-now | G4-evidence-present | ✓ PASS | OK |
| EC-02 | classification | loop-now | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-02 | classification | loop-now | G6-adaptation-mode | ✓ PASS | OK |
| EC-02 | classification | multica | G1-matrix-complete | ✓ PASS | OK |
| EC-02 | classification | multica | G2-req-fields | ✓ PASS | OK |
| EC-02 | classification | multica | G3-version-pinned | ✓ PASS | OK |
| EC-02 | classification | multica | G4-evidence-present | ✓ PASS | OK |
| EC-02 | classification | multica | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-02 | classification | multica | G6-adaptation-mode | ✓ PASS | OK |
| EC-03 | L1 | loop-now | G1-matrix-complete | ✓ PASS | OK |
| EC-03 | L1 | loop-now | G2-req-fields | ✓ PASS | OK |
| EC-03 | L1 | loop-now | G3-version-pinned | ✓ PASS | OK |
| EC-03 | L1 | loop-now | G4-evidence-present | ✓ PASS | OK |
| EC-03 | L1 | loop-now | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-03 | L1 | loop-now | G6-adaptation-mode | ✓ PASS | OK |
| EC-03 | L1 | multica | G1-matrix-complete | ✓ PASS | OK |
| EC-03 | L1 | multica | G2-req-fields | ✓ PASS | OK |
| EC-03 | L1 | multica | G3-version-pinned | ✓ PASS | OK |
| EC-03 | L1 | multica | G4-evidence-present | ✓ PASS | OK |
| EC-03 | L1 | multica | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-03 | L1 | multica | G6-adaptation-mode | ✓ PASS | OK |
| EC-03 | L1 | qm | G1-matrix-complete | ✓ PASS | OK |
| EC-03 | L1 | qm | G2-req-fields | ✓ PASS | OK |
| EC-03 | L1 | qm | G3-version-pinned | ✓ PASS | OK |
| EC-03 | L1 | qm | G4-evidence-present | ✓ PASS | OK |
| EC-03 | L1 | qm | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-03 | L1 | qm | G6-adaptation-mode | ✓ PASS | OK |
| EC-03 | classification | loop-now | G1-matrix-complete | ✓ PASS | OK |
| EC-03 | classification | loop-now | G2-req-fields | ✓ PASS | OK |
| EC-03 | classification | loop-now | G3-version-pinned | ✓ PASS | OK |
| EC-03 | classification | loop-now | G4-evidence-present | ✓ PASS | OK |
| EC-03 | classification | loop-now | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-03 | classification | loop-now | G6-adaptation-mode | ✓ PASS | OK |
| EC-03 | classification | multica | G1-matrix-complete | ✓ PASS | OK |
| EC-03 | classification | multica | G2-req-fields | ✓ PASS | OK |
| EC-03 | classification | multica | G3-version-pinned | ✓ PASS | OK |
| EC-03 | classification | multica | G4-evidence-present | ✓ PASS | OK |
| EC-03 | classification | multica | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-03 | classification | multica | G6-adaptation-mode | ✓ PASS | OK |
| EC-03 | classification | qm | G1-matrix-complete | ✓ PASS | OK |
| EC-03 | classification | qm | G2-req-fields | ✓ PASS | OK |
| EC-03 | classification | qm | G3-version-pinned | ✓ PASS | OK |
| EC-03 | classification | qm | G4-evidence-present | ✓ PASS | OK |
| EC-03 | classification | qm | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-03 | classification | qm | G6-adaptation-mode | ✓ PASS | OK |
| EC-05 | L1 | loop-now | G1-matrix-complete | ✓ PASS | OK |
| EC-05 | L1 | loop-now | G2-req-fields | ✓ PASS | OK |
| EC-05 | L1 | loop-now | G3-version-pinned | ✓ PASS | OK |
| EC-05 | L1 | loop-now | G4-evidence-present | ✓ PASS | OK |
| EC-05 | L1 | loop-now | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-05 | L1 | loop-now | G6-adaptation-mode | ✓ PASS | OK |
| EC-05 | L1 | mem-vault | G1-matrix-complete | ✓ PASS | OK |
| EC-05 | L1 | mem-vault | G2-req-fields | ✓ PASS | OK |
| EC-05 | L1 | mem-vault | G3-version-pinned | ✓ PASS | OK |
| EC-05 | L1 | mem-vault | G4-evidence-present | ✓ PASS | OK |
| EC-05 | L1 | mem-vault | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-05 | L1 | mem-vault | G6-adaptation-mode | ✓ PASS | OK |
| EC-05 | L1 | multica | G1-matrix-complete | ✓ PASS | OK |
| EC-05 | L1 | multica | G2-req-fields | ✓ PASS | OK |
| EC-05 | L1 | multica | G3-version-pinned | ✓ PASS | OK |
| EC-05 | L1 | multica | G4-evidence-present | ✓ PASS | OK |
| EC-05 | L1 | multica | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-05 | L1 | multica | G6-adaptation-mode | ✓ PASS | OK |
| EC-05 | L1 | qm | G1-matrix-complete | ✓ PASS | OK |
| EC-05 | L1 | qm | G2-req-fields | ✓ PASS | OK |
| EC-05 | L1 | qm | G3-version-pinned | ✓ PASS | OK |
| EC-05 | L1 | qm | G4-evidence-present | ✓ PASS | OK |
| EC-05 | L1 | qm | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-05 | L1 | qm | G6-adaptation-mode | ✓ PASS | OK |
| EC-05 | classification | loop-now | G1-matrix-complete | ✓ PASS | OK |
| EC-05 | classification | loop-now | G2-req-fields | ✓ PASS | OK |
| EC-05 | classification | loop-now | G3-version-pinned | ✓ PASS | OK |
| EC-05 | classification | loop-now | G4-evidence-present | ✓ PASS | OK |
| EC-05 | classification | loop-now | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-05 | classification | loop-now | G6-adaptation-mode | ✓ PASS | OK |
| EC-05 | classification | mem-vault | G1-matrix-complete | ✓ PASS | OK |
| EC-05 | classification | mem-vault | G2-req-fields | ✓ PASS | OK |
| EC-05 | classification | mem-vault | G3-version-pinned | ✓ PASS | OK |
| EC-05 | classification | mem-vault | G4-evidence-present | ✓ PASS | OK |
| EC-05 | classification | mem-vault | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-05 | classification | mem-vault | G6-adaptation-mode | ✓ PASS | OK |
| EC-05 | classification | multica | G1-matrix-complete | ✓ PASS | OK |
| EC-05 | classification | multica | G2-req-fields | ✓ PASS | OK |
| EC-05 | classification | multica | G3-version-pinned | ✓ PASS | OK |
| EC-05 | classification | multica | G4-evidence-present | ✓ PASS | OK |
| EC-05 | classification | multica | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-05 | classification | multica | G6-adaptation-mode | ✓ PASS | OK |
| EC-05 | classification | qm | G1-matrix-complete | ✓ PASS | OK |
| EC-05 | classification | qm | G2-req-fields | ✓ PASS | OK |
| EC-05 | classification | qm | G3-version-pinned | ✓ PASS | OK |
| EC-05 | classification | qm | G4-evidence-present | ✓ PASS | OK |
| EC-05 | classification | qm | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-05 | classification | qm | G6-adaptation-mode | ✓ PASS | OK |
| EC-06 | L1 | ZAgenticOPN | G1-matrix-complete | ✓ PASS | OK |
| EC-06 | L1 | ZAgenticOPN | G2-req-fields | ✓ PASS | OK |
| EC-06 | L1 | ZAgenticOPN | G3-version-pinned | ✓ PASS | OK |
| EC-06 | L1 | ZAgenticOPN | G4-evidence-present | ✓ PASS | OK |
| EC-06 | L1 | ZAgenticOPN | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-06 | L1 | ZAgenticOPN | G6-adaptation-mode | ✓ PASS | OK |
| EC-06 | L1 | loop-now | G1-matrix-complete | ✓ PASS | OK |
| EC-06 | L1 | loop-now | G2-req-fields | ✓ PASS | OK |
| EC-06 | L1 | loop-now | G3-version-pinned | ✓ PASS | OK |
| EC-06 | L1 | loop-now | G4-evidence-present | ✓ PASS | OK |
| EC-06 | L1 | loop-now | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-06 | L1 | loop-now | G6-adaptation-mode | ✓ PASS | OK |
| EC-06 | L1 | multica | G1-matrix-complete | ✓ PASS | OK |
| EC-06 | L1 | multica | G2-req-fields | ✓ PASS | OK |
| EC-06 | L1 | multica | G3-version-pinned | ✓ PASS | OK |
| EC-06 | L1 | multica | G4-evidence-present | ✓ PASS | OK |
| EC-06 | L1 | multica | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-06 | L1 | multica | G6-adaptation-mode | ✓ PASS | OK |
| EC-06 | L1 | opencode-coordination | G1-matrix-complete | ✓ PASS | OK |
| EC-06 | L1 | opencode-coordination | G2-req-fields | ✓ PASS | OK |
| EC-06 | L1 | opencode-coordination | G3-version-pinned | ✓ PASS | OK |
| EC-06 | L1 | opencode-coordination | G4-evidence-present | ✓ PASS | OK |
| EC-06 | L1 | opencode-coordination | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-06 | L1 | opencode-coordination | G6-adaptation-mode | ✓ PASS | OK |
| EC-06 | L1 | qm | G1-matrix-complete | ✓ PASS | OK |
| EC-06 | L1 | qm | G2-req-fields | ✓ PASS | OK |
| EC-06 | L1 | qm | G3-version-pinned | ✓ PASS | OK |
| EC-06 | L1 | qm | G4-evidence-present | ✓ PASS | OK |
| EC-06 | L1 | qm | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-06 | L1 | qm | G6-adaptation-mode | ✓ PASS | OK |
| EC-06 | classification | ZAgenticOPN | G1-matrix-complete | ✓ PASS | OK |
| EC-06 | classification | ZAgenticOPN | G2-req-fields | ✓ PASS | OK |
| EC-06 | classification | ZAgenticOPN | G3-version-pinned | ✓ PASS | OK |
| EC-06 | classification | ZAgenticOPN | G4-evidence-present | ✓ PASS | OK |
| EC-06 | classification | ZAgenticOPN | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-06 | classification | ZAgenticOPN | G6-adaptation-mode | ✓ PASS | OK |
| EC-06 | classification | loop-now | G1-matrix-complete | ✓ PASS | OK |
| EC-06 | classification | loop-now | G2-req-fields | ✓ PASS | OK |
| EC-06 | classification | loop-now | G3-version-pinned | ✓ PASS | OK |
| EC-06 | classification | loop-now | G4-evidence-present | ✓ PASS | OK |
| EC-06 | classification | loop-now | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-06 | classification | loop-now | G6-adaptation-mode | ✓ PASS | OK |
| EC-06 | classification | multica | G1-matrix-complete | ✓ PASS | OK |
| EC-06 | classification | multica | G2-req-fields | ✓ PASS | OK |
| EC-06 | classification | multica | G3-version-pinned | ✓ PASS | OK |
| EC-06 | classification | multica | G4-evidence-present | ✓ PASS | OK |
| EC-06 | classification | multica | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-06 | classification | multica | G6-adaptation-mode | ✓ PASS | OK |
| EC-06 | classification | opencode-coordination | G1-matrix-complete | ✓ PASS | OK |
| EC-06 | classification | opencode-coordination | G2-req-fields | ✓ PASS | OK |
| EC-06 | classification | opencode-coordination | G3-version-pinned | ✓ PASS | OK |
| EC-06 | classification | opencode-coordination | G4-evidence-present | ✓ PASS | OK |
| EC-06 | classification | opencode-coordination | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-06 | classification | opencode-coordination | G6-adaptation-mode | ✓ PASS | OK |
| EC-06 | classification | qm | G1-matrix-complete | ✓ PASS | OK |
| EC-06 | classification | qm | G2-req-fields | ✓ PASS | OK |
| EC-06 | classification | qm | G3-version-pinned | ✓ PASS | OK |
| EC-06 | classification | qm | G4-evidence-present | ✓ PASS | OK |
| EC-06 | classification | qm | G5-unknown-poc-plan | ✓ PASS | OK |
| EC-06 | classification | qm | G6-adaptation-mode | ✓ PASS | OK |

- 每 EC 一对输入 JSON，路径见 §1；均由生成器机械写出，禁止手改。
- 两份输入均跑 `validate` G1–G6；`assess` 只对 classification 输入调用，产出**仅供参考的分类信号**（§5.3）。L1 输入不跑 assess，保留拟合层对照。

### 5.2 两输入拟合层判定对照

判定只用母模型 `effective_fit` / `cell_satisfied` / `FIT_OK(0.9)` / `FIT_FAIL(0.5)` 机械计算。43 格 L3 已全部裁决，class 判定对全部格计算，not_ready=0。

| EC | R | O | L1 eff | L1 判定 | class eff | class 判定 | 变化 |
|---|---|---|---|---|---|---|---|
| EC-01 | R1.1 | multica | 0.648 | must_gap | 0.900 | satisfied | must_gap → satisfied |
| EC-01 | R1.1 | loop-now | 0.420 | critical_gap | 0.420 | critical_gap | —（保持） |
| EC-01 | R1.2 | multica | 0.648 | must_gap | 0.900 | satisfied | must_gap → satisfied |
| EC-01 | R1.2 | loop-now | 0.567 | must_gap | 0.567 | must_gap | —（保持） |
| EC-01 | R1.3 | multica | 0.648 | must_gap | 0.900 | satisfied | must_gap → satisfied |
| EC-01 | R1.3 | loop-now | 0.367 | critical_gap | 0.367 | critical_gap | —（保持） |
| EC-01 | R1.4 | multica | 0.542 | must_gap | 0.900 | satisfied | must_gap → satisfied |
| EC-01 | R1.4 | loop-now | 0.100 | critical_gap | 0.100 | critical_gap | —（保持） |
| EC-02 | R2.1 | loop-now | 0.061 | critical_gap | 0.061 | critical_gap | —（保持） |
| EC-02 | R2.1 | multica | 0.420 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-02 | R2.2 | loop-now | 0.162 | critical_gap | 0.162 | critical_gap | —（保持） |
| EC-02 | R2.2 | multica | 0.576 | must_gap | 0.900 | satisfied | must_gap → satisfied |
| EC-02 | R2.3 | loop-now | 0.416 | critical_gap | 0.416 | critical_gap | —（保持） |
| EC-02 | R2.3 | multica | 0.420 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-02 | R2.4 | loop-now | 0.446 | critical_gap | 0.446 | critical_gap | —（保持） |
| EC-02 | R2.4 | multica | 0.446 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-03 | R3.1 | loop-now | 0.506 | must_gap | 0.506 | must_gap | —（保持） |
| EC-03 | R3.1 | multica | 0.294 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-03 | R3.1 | qm | 0.292 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-03 | R3.2 | loop-now | 0.161 | critical_gap | 0.161 | critical_gap | —（保持） |
| EC-03 | R3.2 | multica | 0.250 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-03 | R3.2 | qm | 0.392 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-03 | R3.3 | loop-now | 0.090 | critical_gap | 0.090 | critical_gap | —（保持） |
| EC-03 | R3.3 | multica | 0.315 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-03 | R3.3 | qm | 0.510 | must_gap | 0.510 | must_gap | —（保持） |
| EC-05 | R5.1 | loop-now | 0.132 | critical_gap | 0.132 | critical_gap | —（保持） |
| EC-05 | R5.1 | mem-vault | 0.540 | must_gap | 0.900 | satisfied | must_gap → satisfied |
| EC-05 | R5.1 | multica | 0.341 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-05 | R5.1 | qm | 0.364 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-05 | R5.2 | loop-now | 0.176 | critical_gap | 0.176 | critical_gap | —（保持） |
| EC-05 | R5.2 | mem-vault | 0.574 | must_gap | 0.900 | satisfied | must_gap → satisfied |
| EC-05 | R5.2 | multica | 0.315 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-05 | R5.2 | qm | 0.250 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-06 | R6.1 | ZAgenticOPN | 0.292 | critical_gap | 0.292 | critical_gap | —（保持） |
| EC-06 | R6.1 | loop-now | 0.476 | critical_gap | 0.476 | critical_gap | —（保持） |
| EC-06 | R6.1 | multica | 0.722 | must_gap | 0.900 | satisfied | must_gap → satisfied |
| EC-06 | R6.1 | opencode-coordination | 0.268 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-06 | R6.1 | qm | 0.132 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |
| EC-06 | R6.2 | ZAgenticOPN | 0.574 | must_gap | 0.574 | must_gap | —（保持） |
| EC-06 | R6.2 | loop-now | 0.317 | critical_gap | 0.317 | critical_gap | —（保持） |
| EC-06 | R6.2 | multica | 0.612 | must_gap | 0.900 | satisfied | must_gap → satisfied |
| EC-06 | R6.2 | opencode-coordination | 0.364 | critical_gap | 0.364 | critical_gap | —（保持） |
| EC-06 | R6.2 | qm | 0.364 | critical_gap | 0.900 | satisfied | critical_gap → satisfied |

- **EC-01**：L1 satisfied=0 / must_gap=5 / critical_gap=3；class satisfied=4 / must_gap=1 / critical_gap=3 / not_ready=0。
- **EC-02**：L1 satisfied=0 / must_gap=1 / critical_gap=7；class satisfied=4 / must_gap=0 / critical_gap=4 / not_ready=0。
- **EC-03**：L1 satisfied=0 / must_gap=2 / critical_gap=7；class satisfied=5 / must_gap=2 / critical_gap=2 / not_ready=0。
- **EC-05**：L1 satisfied=0 / must_gap=2 / critical_gap=6；class satisfied=6 / must_gap=0 / critical_gap=2 / not_ready=0。
- **EC-06**：L1 satisfied=0 / must_gap=3 / critical_gap=7；class satisfied=5 / must_gap=1 / critical_gap=4 / not_ready=0。

> `认同 L2 未满足` 格三因子不动，其 <FIT_FAIL 的格在两份输入里都如实为 `critical_gap`；`可以有` 格经两满一值映射后 eff 精确=FIT_OK、命中 `satisfied`。43 格全部参与 class 判定，not_ready=0。

### 5.3 成本 / E 与采用分类参考信号（zjj 初判；仅供参考，非自研裁决）

- **E 口径**：仪器硬编码 `E_LOW=20` / `E_MID=80` / `E_HIGH=200`；SSOT 只定义六分量、**未定义单位**，仪器自注「单位自定，跨候选须一致」。本初判用**相对成本点（≈人日量级）**，跨候选一致；**E 单位已由 zj 认可标注（2026-11-24），仅供参考**——它是估价尺度，不构成自研/采用的裁决依据。
- **状态**：以下六分量、scope 与分类全部是 **zjj 初判 / 参考信号**，不是 zj 裁决；每条 rationale 锚到本矩阵已引用的 sealed EVID，EVID 未直接给工作量的地方显式标 `JUDGMENT`。**是否自研/采用由 zj 在规划-执行阶段人工判断，本页不裁决。**

#### 5.3.1 逐候选 cost 六分量（相对成本点）

| O | initial_dev | integration | maintenance | upstream_adapt | ops | security_gov | E | 依据 / JUDGMENT |
|---|---|---|---|---|---|---|---|---|
| ZAgenticOPN | 12 | 10 | 10 | 8 | 6 | 9 | 55 | sealed EVID: 五字段结果 + claim authority + Git provenance + health scorecard + 三次复验；与我方诊断/审计语义同构度最高，成本主要是接线与持续审计维护。注意它是参照物，此处仅就 EC-06 诊断链作候选初判。JUDGMENT: 数值为相对点估算。 |
| loop-now | 22 | 16 | 16 | 10 | 12 | 12 | 88 | sealed EVID: one local installation + SQLite in a local data dir + each agent in its own working directory + plugin trust grading；跨设备接续、共享记忆、Human 门账本均需自建主体能力，故 initial_dev 与 maintenance 最高。JUDGMENT: 本地多实例运维与权限治理成本为估算。 |
| mem-vault | 14 | 12 | 10 | 6 | 8 | 9 | 59 | sealed EVID: plain cloud-synced Markdown → shared knowledge base for every agent/device + session-blackboard CONTEXT.md；本体极轻（upstream_adapt 最低），但 EVID 同时确认无索引/检索、无结构化 provenance，检索与溯源须自建，计入 initial_dev/integration。JUDGMENT: 数值为相对点估算。 |
| multica | 18 | 14 | 12 | 10 | 8 | 10 | 72 | sealed EVID: self-hostable daemon + Skills playbook + issue/run/decisions/diff provenance + review gates；接入需身份/Agent 网络映射、Objective→Work Item 语义转换、审批账本补齐，故 initial_dev 最高。上游工作流语义变动是主要升级成本；self-host 运维中等。JUDGMENT: 六分量数值为相对点估算，sealed EVID 未直接给工作量。 |
| opencode-coordination | 14 | 12 | 10 | 8 | 8 | 9 | 61 | sealed EVID: append-only ledger of roles/work items/messages/progress/history + board updates + event recorded/PR checked；账本体裁贴合审计，但 run 级失败时间点与产出来源回放需补齐。JUDGMENT: 数值为相对点估算。 |
| qm | 16 | 14 | 12 | 9 | 10 | 12 | 73 | sealed EVID: Slack/web harness + own cloud + per person/room scoped memory/files/keychain/permissions + durable sandbox + audited tool calls；主体能力较完整，成本集中在权限/数据治理与多端集成。JUDGMENT: 治理分量为估算。 |

#### 5.3.2 适配层边界（scope / mode）

| O | scope | mode | 责任不可控 | 依据 |
|---|---|---|---|---|
| ZAgenticOPN | provenance-adapt, state-transform | adapter | 否 | 结果五字段/Git provenance/scorecard 语义同构，仅需来源适配与状态映射薄层。 |
| loop-now | storage-sync-infra, full-retrieval-memory, identity-map | plugin | 否 | one local installation + local SQLite 决定跨设备与共享记忆必须自建存储同步和检索记忆流水线——按模型这属于主体能力禁区，不再是可移除薄层。 |
| mem-vault | full-retrieval-memory, provenance-adapt | adapter | 否 | sealed EVID 明确是纯 Markdown 文件同步、无索引/检索机制；R5.2 的可检索复用须自建完整检索或记忆流水线，触主体能力禁区。 |
| multica | identity-map, query-adapt, state-transform, provenance-adapt | adapter | 否 | sealed EVID 显示 issue/review/provenance 是它的主体；我们只写身份映射、查询适配、状态转换、来源适配薄层，可移除、不维护 fork（B1）。 |
| opencode-coordination | coord-semantics-claim-lease, provenance-adapt | adapter | 否 | append-only ledger + board 提供审计 substrate；仅补 claim/lease 小型协调语义与来源适配薄层。 |
| qm | identity-map, query-adapt, provenance-adapt | plugin | 否 | 其 scoped memory/permissions/durable sandbox 已是主体；我方只做身份映射与查询/来源适配，不自建 ACL 或完整检索记忆流水线。 |

#### 5.3.3 assess 分类参考信号（仅 classification 输入）

> `D` = 继续搜索（搜索循环回环态，非终态否决）；`B1/B2/B3` 按 mode 细分。分类是仪器**参考信号，仅供参考**；**是否自研/采用由 zj 在规划-执行阶段人工判断，本页不作裁决。**

| EC | O | 推荐 | must 覆盖 | avg_fit | E | 关键缺口 | 主体能力触碰 | 主要依据 |
|---|---|---|---|---|---|---|---|---|
| EC-01 | multica | B1 | 100% | 0.900 | 72 | 否 | 否 | 外部 Adapter/插件/sidecar 扩展、不维护 fork -> B1 |
| EC-01 | loop-now | D | 0% | 0.364 | 88 | 是 | 否 | 关键需求 R1.1 有效拟合度=0.42<0.5 -> 继续搜索(D); 关键需求 R1.3 有效拟合度=0.37<0.5 -> 继续搜索(D) |
| EC-02 | loop-now | D | 0% | 0.271 | 88 | 是 | 否 | 关键需求 R2.1 有效拟合度=0.06<0.5 -> 继续搜索(D); 关键需求 R2.2 有效拟合度=0.16<0.5 -> 继续搜索(D) |
| EC-02 | multica | B1 | 100% | 0.900 | 72 | 否 | 否 | 外部 Adapter/插件/sidecar 扩展、不维护 fork -> B1 |
| EC-03 | loop-now | D | 0% | 0.252 | 88 | 是 | 否 | 关键需求 R3.2 有效拟合度=0.16<0.5 -> 继续搜索(D); 关键需求 R3.3 有效拟合度=0.09<0.5 -> 继续搜索(D) |
| EC-03 | multica | B1 | 100% | 0.900 | 72 | 否 | 否 | 外部 Adapter/插件/sidecar 扩展、不维护 fork -> B1 |
| EC-03 | qm | B | 67% | 0.770 | 73 | 否 | 否 | 关键需求存在部分缺口但 E=73<=E_MID -> B |
| EC-05 | loop-now | D | 0% | 0.154 | 88 | 是 | 否 | 关键需求 R5.1 有效拟合度=0.13<0.5 -> 继续搜索(D); 关键需求 R5.2 有效拟合度=0.18<0.5 -> 继续搜索(D) |
| EC-05 | mem-vault | C | 100% | 0.900 | 59 | 否 | 是 | 适配层触碰主体能力(禁止类目): full-retrieval-memory(完整检索或记忆流水线) -> 至少降为 C; 主体能力建设但责任可控 -> C |
| EC-05 | multica | B1 | 100% | 0.900 | 72 | 否 | 否 | 外部 Adapter/插件/sidecar 扩展、不维护 fork -> B1 |
| EC-05 | qm | B1 | 100% | 0.900 | 73 | 否 | 否 | 外部 Adapter/插件/sidecar 扩展、不维护 fork -> B1 |
| EC-06 | ZAgenticOPN | D | 0% | 0.433 | 55 | 是 | 否 | 关键需求 R6.1 有效拟合度=0.29<0.5 -> 继续搜索(D) |
| EC-06 | loop-now | D | 0% | 0.396 | 88 | 是 | 否 | 关键需求 R6.1 有效拟合度=0.48<0.5 -> 继续搜索(D); 关键需求 R6.2 有效拟合度=0.32<0.5 -> 继续搜索(D) |
| EC-06 | multica | B1 | 100% | 0.900 | 72 | 否 | 否 | 外部 Adapter/插件/sidecar 扩展、不维护 fork -> B1 |
| EC-06 | opencode-coordination | D | 50% | 0.632 | 61 | 是 | 否 | 关键需求 R6.2 有效拟合度=0.36<0.5 -> 继续搜索(D) |
| EC-06 | qm | B1 | 100% | 0.900 | 73 | 否 | 否 | 外部 Adapter/插件/sidecar 扩展、不维护 fork -> B1 |

- **分布（参考信号）**：B=1 / B1=7 / C=1 / D=7。

## 6. 缺口与待办清单

- **L3 Human 兜底**：43/43 格已由 zj 逐格填写并机械回灌（EC-01 8 格 + 铺开 35 格；19 endorse / 24 raise_to_pass）；本页为派生产物，手改会被重跑覆盖。
- **Q5a 覆盖面说明**：Q1a 严格 native 交集把基线 §4.1 采纳该 EC 的部分素材项目挡在矩阵外；下表逐条列出，缺口经 reuse ledger 机械复核，标为非阻塞证据缺口，不改基线、不改 ratify bundle。

| EC | 被排除素材项目 | 缺口模块 | ledger 实况 |
|---|---|---|---|
| EC-02 | mozzie | M6 | unknown（native 闸门不放宽） |
| EC-03 | mem-vault | M10 | unknown（native 闸门不放宽） |
| EC-05 | tasktrooper | M7 | unknown（native 闸门不放宽） |
| EC-05 | ZAgenticOPN | M7 | unknown（native 闸门不放宽） |

- **拟合层判定 ≠ 采用分类 ≠ 自研裁决**：§5.2 是拟合事实层，§5.3 是仪器基于初判 cost/E 给出的参考信号；是否自研/采用由 zj 在规划-执行阶段人工判断，本页两者都不裁决。
- **成本/E 仅供参考**：E 单位已由 zj 认可标注（相对成本点，仅供参考）；§5.3 六分量、scope 与分类均为 zjj 初判参考信号，**不是自研/采用裁决**——该判断在规划-执行阶段由人工作出。
- **83 个 unknown 未纳入**：Q1a 只选 sealed-native；unknown 证据缺口仍在基线 §6 与账本中，不被本矩阵掩盖。
- **M3 Human 门语义冲突**：四种表达互不兼容（基线 §5）；R1.4 与各 O 的 EVID 逐格打分（multica 有 Review gate、loop-now 语义错配），语义裁决归后续规划阶段。

## 7. 机械自检

- EC 5 条；R 15 条；EC×O 对 16 个；矩阵单元 43 个（EC-01 8 + 铺开 35，全部 L3 已裁决），每单元 status=native 且 evidence 指向 sealed EVID。
- 每个 cited EVID 均在 sealed ledger 索引中存在；所有候选版本均为 ledger pin 实读 40-hex，非手填。
- `SCORES` 恰好覆盖 43 个单元，每格三因子在 [0,1] 且含 rationale + by；无档位默认回退。
- L3：43/43 格 zj 原文回灌（19 endorse / 24 raise_to_pass）；classification 输入按 action 机械派生：endorse 三因子与 L1 逐值相等，raise_to_pass 两满一值 eff 精确=FIT_OK（fail-closed 校验）。
- 复核分 action 由 zj 原文前缀机械派生（认同=19 / 可以有=24）；Q4a 两满一值映射 eff 精确=FIT_OK=0.9。
- 拟合层判定仅用母模型 `effective_fit`/`cell_satisfied`/`FIT_OK`(0.9)/`FIT_FAIL`(0.5)；每 EC 两份输入 G1–G6 全 PASS；`assess` 仅对 classification 输入调用并产出仅供参考的分类信号（§5.3），是否自研由规划-执行阶段人工判断。
- 本页 supporting；derived-from: opn.product-structure-baseline / opn.reuse-evidence-ledger / opn.module-matrix；不改写 ratify bundle。

