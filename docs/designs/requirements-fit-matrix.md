---
doc-kind: reference
authority: supporting
authority-id: opn.requirements-fit-matrix
---

# 需求拟合矩阵 · EC-01 样板（supporting / 从基线拆 R）

> 本页是 **EC-01 拆 R 的样板**，只覆盖一条端到端能力（EC-01 主闭环），不是完整 R 清单、不是产品计划、不是采用裁决。
> 由 `docs/reasearch/opn-cross-comparison/_gen_fit_matrix.py` 从横比 bundle / 复用证据账本 / 产品结构基线机械派生；
> Human 决策（Q1–Q13）以带 SoT 存在性校验的显式常量表注入，Agent 不推断验收判据、不预置分类。

## 1. 边界与口径（zj 2026-11-24 grill Q1–Q13 锁定）

- **产物范围**：只做 EC-01 样板（Q10a）；其余 4 条 EC 待样板验收后铺开。本轮不 commit。
- **R 锚点**：锚 EC（Q1a），按 **Human 可独立观察的验收节点**切（Q6c/Q11a），不贴模块边界；模块只作归属标注。
- **acceptance**：bundle 的 acceptance 是场景级、跨项目机械重复的通用短语，只当种子，由 Human 逐条校准（Q2a）；下表 acceptance 即校准结果。
- **三拟合因子**：Q3a 定为 Human 判断、Agent 只整理材料。本样板中的三因子是**分析初值、待 zj 逐格校准（Q12a）**，由可追溯档位规则从账本模块级 hypothesis 机械派生（见 §4），**不是 evidence、不是最终判断**。
- **校准唯一入口**：生成器 `_gen_fit_matrix.py` 的 `CALIBRATIONS` 常量表（键 (R,O)，逐格覆盖三因子，含 `by`/`rationale` 留痕；档位初值保留作 provenance）。本页与母模型 JSON 均由重跑机械再生成——**手工改文档/JSON 会被覆盖**，校准只认常量表。
- **status 口径**：横比 native → 母模型 native；unknown → unknown；adapted/unsupported 留给母模型判（守 `CTX::zopn-no-adopt-verdict`，符合上轮 adaptation-target 非缺口改判）。
- **M2/M3/M8**：Q7a 不预置为 D——照常填因子、让母模型独立复核；本轮更不出任何分类，故无结论被预置。
- **priority/critical**：全部 R=`must` + `critical=true`（Q8a，无优先级信号时不臆断）。
- **成本维度**：整体不进本轮（Q9b）。只跑 `validate`（G1–G6），**不跑 `assess`，不出 A/B/C/D**；`cost` 保留模板默认 0，不作为分类依据。
- **候选 O**：multica + loop-now（Q13a）——EC-01 覆盖的 M1/M3/M4/M5 四模块上两家均有 sealed native；版本用各自 sealed ledger 的 `revision.sha`（非 bundle 中已失准的记录值）。
- **URL/license**：sealed SoT 未采集，填占位；两者非 validate 闸门字段，不影响本轮结论。

## 2. R 清单（EC-01 按验收节点拆分 · 4 条）

| R | 验收节点（Human 可观察） | acceptance（Human 校准） | 归属模块 | priority | critical |
|---|---|---|---|---|---|
| R1.1 | 目标提交后可见 | Human 提交目标后，能在列表看到对应 Work Item，其状态可读且能前进 | M1 | must | true |
| R1.2 | 执行进度可观察 | Human 能看到 Agent 已接收并在隔离边界内执行，进度/阻塞可见、互不污染 | M5 | must | true |
| R1.3 | 结果产物可复核 | Human 能看到本次产出，且来源/步骤可追溯 | M4 | must | true |
| R1.4 | Human 门验收可审计 | Human 在门上 approve/reject，动作有账本、可审计 | M3 | must | true |

> 起始 EC-01：起点「Human 提交目标/创建 Work Item」、终点「Human 在 Human 门看到结果并验收完成」，跨 M1→M5→M4→M3（M2 身份 scope 横切，已在基线 §4.1）；此处按 Human 可观察节点切成 4 条独立可验收需求。

## 3. 候选 O（按 R 动态选取 · 2 家）

| 候选 O | 版本（sealed ledger 实值） | 来源 ledger | URL | license |
|---|---|---|---|---|
| multica | `7a926b824fcf7a3687097f353d6a34f79d8b568d` | `collect/ledger-multica.json` | (sealed SoT 未采集) | (未采集) |
| loop-now | `b7d6811877e6d7341ac539934ae87028df87b1e6` | `collect/ledger-loop-now.json` | (sealed SoT 未采集) | (未采集) |

## 4. R×O 拟合矩阵（分析初值 · 待 zj 校准）

| R | O | status | coverage | semantic_match | composability | effective_fit | evidence | 档位 |
|---|---|---|---|---|---|---|---|---|
| R1.1 | multica | native | 0.80 | 0.55 | 0.60 | 0.264 | EVID::a67400762c931df62135608d | adapted_incompatible |
| R1.1 | loop-now | native | 0.80 | 0.55 | 0.60 | 0.264 | EVID::3605745b0cae1cc75dd59c80 | adapted_incompatible |
| R1.2 | multica | native | 0.95 | 0.90 | 0.85 | 0.727 | EVID::76fd261e3f84f3c9e33a84c6 | native_strong |
| R1.2 | loop-now | native | 0.95 | 0.90 | 0.85 | 0.727 | EVID::598de2204e4d84a75a0020d4 | native_strong |
| R1.3 | multica | native | 0.85 | 0.75 | 0.70 | 0.446 | EVID::5c1fa749e640c3dec0dbd328 | adapted_contract |
| R1.3 | loop-now | native | 0.85 | 0.75 | 0.70 | 0.446 | EVID::0794e7e8dbb753920bae8a05 | adapted_contract |
| R1.4 | multica | native | 0.70 | 0.45 | 0.50 | 0.158 | EVID::2cc46ac299adc52b807b122e | must_selfbuild |
| R1.4 | loop-now | native | 0.70 | 0.45 | 0.50 | 0.158 | EVID::d3d21a128f2d058198f00504 | must_selfbuild |

### 档位规则（三因子的唯一来源，可追溯、非手填）

| 档位 | coverage | semantic_match | composability | 触发条件（账本模块级 hypothesis 文本） |
|---|---|---|---|---|
| native_strong | 0.95 | 0.90 | 0.85 | hypothesis 含「native 偏多」 |
| adapted_contract | 0.85 | 0.75 | 0.70 | hypothesis 含「明确契约」 |
| adapted_incompatible | 0.80 | 0.55 | 0.60 | hypothesis 含「互不相容」 |
| must_selfbuild | 0.70 | 0.45 | 0.50 | hypothesis 含「必须自研」 |

> 三因子按模块级 hypothesis 归一应用到该模块的所有 O（hypothesis 是模块级 assumption；四态 native/unknown 才是逐 O 事实）；档位列带「→zj校准」的格以 `CALIBRATIONS` 常量表实值为准、档位值仅作 provenance。`effective_fit = coverage × semantic_match × composability`，此处仅展示、不参与任何分类（本轮不跑 assess）。

## 5. validate 闸门结果（G1–G6 · 不出分类）

| 候选 O | 闸门 | 结果 | 说明 |
|---|---|---|---|
| multica | G1-matrix-complete | ✓ PASS | OK |
| multica | G2-req-fields | ✓ PASS | OK |
| multica | G3-version-pinned | ✓ PASS | OK |
| multica | G4-evidence-present | ✓ PASS | OK |
| multica | G5-unknown-poc-plan | ✓ PASS | OK |
| multica | G6-adaptation-mode | ✓ PASS | OK |
| loop-now | G1-matrix-complete | ✓ PASS | OK |
| loop-now | G2-req-fields | ✓ PASS | OK |
| loop-now | G3-version-pinned | ✓ PASS | OK |
| loop-now | G4-evidence-present | ✓ PASS | OK |
| loop-now | G5-unknown-poc-plan | ✓ PASS | OK |
| loop-now | G6-adaptation-mode | ✓ PASS | OK |

- 母模型输入 JSON：`tmp/skills-outputs/zj-open-source-capability-fit/ec01-scaffold/capability_fit_input.json`（相对仓库根）。
- **本轮只调用 `validate`**；`assess` 未调用，`cost` 全 0 不参与结论，**没有产出 A/B/C/D**。闸门全绿仅表示矩阵结构与证据形式合规，不代表采用建议。
- 关键缺口检测、适配层范围校验、E 阈值比较全部属于 `assess`，本轮有意不触发（Q9b）。

## 6. 缺口与待校准清单

- **三因子待 zj 逐格校准**：当前为档位派生的分析初值，不是最终判断；校准落点 = 生成器 `CALIBRATIONS` 常量表（见 §1「校准唯一入口」），校准后重跑本生成器，再跑 `assess`。
- **其余 4 条 EC 未铺开**：EC-02/03/05/06 待本样板验收后按同一模式拆 R。
- **成本/E 维度未测算**：A/B/C/D 留到成本数据可得时再跑（Q9b），当前强行分类会是假精确。
- **83 个 unknown 未纳入本样板**：Q13a 只选 sealed-native 覆盖充分的 O；unknown 证据缺口仍在基线 §6 与账本中，不被本矩阵掩盖。
- **M3 Human 门语义冲突**：四种表达互不兼容（基线 §5），R1.4 的因子已按「必须自研」档位给低初值，但语义裁决仍归后续规划阶段，本页不裁决。

## 7. 机械自检

- R 数 4（=4）；O 数 2（=2）；矩阵单元 8（=8），每单元 status=native 且 evidence 指向 sealed EVID。
- 每个 cited EVID 均在 sealed ledger 索引中存在（fail-closed 校验通过）；两候选 version 均为 ledger 实读 40-hex，非手填。
- 每个模块的 hypothesis 唯一命中档位规则（零命中/多重命中 fail-closed 拒绝生成）；三因子（含已校准格）均在 [0,1]；reuse ledger 行内多 EVID 时拒绝生成（不隐式取第一个）；validate G1–G6 全部 PASS。
- 本页 supporting；derived-from: opn.product-structure-baseline / opn.reuse-evidence-ledger / opn.module-matrix；不改写 ratify bundle。

