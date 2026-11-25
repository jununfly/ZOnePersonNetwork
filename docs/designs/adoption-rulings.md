---
doc-kind: reference
authority: supporting
authority-id: opn.adoption-rulings
---

# 采用 / 自研裁决 · 16 个 EC×O（supporting / 规划-执行阶段 Human 人工判断）

> 本页是 zj 2026-11-25 在规划-执行阶段对 [需求拟合矩阵](requirements-fit-matrix.md) §5.3.3 的 16 行 `assess` 参考信号逐格作出的**人工裁决**，是 supporting 产物，不是产品计划、不实现。
> 由 `docs/reasearch/opn-cross-comparison/_gen_adoption_rulings.py` 从 fit-matrix §5.3.3（参考信号）+ 显式裁决常量表派生；参考信号与 EVID 均机械读取、不手填，ratify bundle / fit-matrix 均不改写。

## 1. 边界与口径（zj 2026-11-25 裁决）

- **粒度**：16 个 EC×O 对逐格裁决——不是按 6 个候选合并、也不是按 5 条场景合并。覆盖 EC-01/02/03/05/06 的严格 native 交集候选。
- **值域**：沿用母模型 `classify_candidate` 词表 `A/B/B1/B2/B3/C/D`，不引入新标签。zj 指定的 `A/B1/B2/B3/C/D` 是子集；§5.3.3 实际含 1 个 `B`（EC-03×qm，缺口小且可控、mode 未细分），如实保留，不为对齐子集而改判。
- **处置**：`确认`=裁决值等于参考信号；`推翻`=裁决值不等于参考信号（本轮 16 确认 / 0 推翻）。
- **D 的语义**：继续搜索（搜索循环回环态），**不是终态否决**——该候选在该场景既不自研也不采用，开放继续找。
- **模块级裁决对齐**：M3「Human 门统一语义自研」与 M8「记忆边界自研」已在 primary 层裁过；multica 的 B1 / mem-vault 的 C 只让 adapter / Markdown 目录承载触发与存储，门语义与检索边界仍自研（R1.4/R2.x、full-retrieval-memory）。
- **可逆性**：后续推翻某格须改生成器常量表后重跑，不得手改本页。

## 2. 裁决表（16 格）

| EC | O | 参考信号 | 裁决 | 处置 | 初判的逻辑和依据 | sealed EVID |
|---|---|---|---|---|---|---|
| EC-01 | multica | B1 | **B1** | 确认 | adapter 覆盖 issue→runtime→review 全链，门语义另判自研、不冲突；据：§5.2 R1.1-1.4 全 satisfied；sealed「Review gates / work lands in review」 | `2cc46ac2…`, `5c1fa749…`, `76fd261e…`, `a6740076…` |
| EC-01 | loop-now | D | **D** | 确认 | 关键格全 <FIT_FAIL，插件信任分级不是工作流门；据：R1.1=0.42 / R1.3=0.37 / R1.4=0.10 | `0794e7e8…`, `3605745b…`, `598de220…`, `d3d21a12…` |
| EC-02 | loop-now | D | **D** | 确认 | 无 reject-with-feedback 门、无反馈归因链；据：R2.1=0.06 / R2.2=0.16 | `033b3e9e…`, `0794e7e8…`, `598de220…`, `d3d21a12…` |
| EC-02 | multica | B1 | **B1** | 确认 | review gate + issue provenance 覆盖，反馈回写按 M3 自研补；据：§5.2 R2.1-2.4 全 satisfied | `2cc46ac2…`, `5c1fa749…`, `71dfad66…`, `76fd261e…` |
| EC-03 | loop-now | D | **D** | 确认 | one local installation 与双设备起点直接冲突；据：R3.2=0.16 / R3.3=0.09 | `56ca86a5…`, `5d1c4de9…`, `fc13fdb5…` |
| EC-03 | multica | B1 | **B1** | 确认 | self-host daemon + Skills 可作载体，handoff 语义自研补；据：§5.2 R3.1-3.3 全 satisfied | `0c8c6d55…`, `8d8aec7e…`, `fcf4cce4…` |
| EC-03 | qm | B | **B** | 确认 | scope sandbox 覆盖跨设备，接续状态未逐字证明但缺口可控；据：must 覆盖 67% / R3.3=0.510 must_gap / E=73≤E_MID | `1fcc9288…`, `3ae4f38b…`, `e878e527…` |
| EC-05 | loop-now | D | **D** | 确认 | 仅执行记录、无共享知识层；据：R5.1=0.13 / R5.2=0.18 | `5d1c4de9…`, `fc13fdb5…` |
| EC-05 | mem-vault | C | **C** | 确认 | 检索属主体能力禁区→自建，Markdown 只作 M8 载体；据：§5.3.2 full-retrieval-memory 触碰；sealed「plain cloud-synced Markdown」 | `15160857…`, `1eedaed6…` |
| EC-05 | multica | B1 | **B1** | 确认 | Skills 覆盖沉淀，来源归属按 M8 补 scope；据：§5.2 R5.1-5.2 satisfied | `0c8c6d55…`, `fcf4cce4…` |
| EC-05 | qm | B1 | **B1** | 确认 | qm scoped memory 即 M8 语义基准、adapter 采用；据：§5.2 R5.1-5.2 satisfied | `1fcc9288…`, `e878e527…` |
| EC-06 | ZAgenticOPN | D | **D** | 确认 | scorecard 是汇总统计，非 run 时间点定位；据：R6.1=0.29（参照物，仅诊断链初判） | `0a8445ac…`, `ddea4d90…` |
| EC-06 | loop-now | D | **D** | 确认 | timeline 可见但无失败标记/回放账本；据：R6.1=0.48 / R6.2=0.32 | `033b3e9e…`, `0794e7e8…` |
| EC-06 | multica | B1 | **B1** | 确认 | timestamped transcript + intent/run/diff 唯一强证据；据：R6.1 L1=0.722 / §5.2 satisfied | `5c1fa749…`, `71dfad66…` |
| EC-06 | opencode-coordination | D | **D** | 确认 | 协作 ledger 非 run 步骤回放、provenance 粒度不足；据：R6.2=0.36 | `01ccf221…`, `d537234d…` |
| EC-06 | qm | B1 | **B1** | 确认 | 全审计 + per-tool 批准，重放链路须适配；据：§5.2 R6.1-6.2 satisfied | `b30ee359…`, `fec47fe2…` |

- **裁决分布**：B=1 / B1=7 / C=1 / D=7；与 §5.3.3 参考分布一致（本轮无推翻）。

## 3. 复核焦点（复核后如需改判，改常量表重跑）

- **multica 的 5 个 B1**（EC-01/02/03/05/06）：#1/#4 涉 Human 门，按 M3 门语义自研处置，adapter 只作触发载体；若认为凡涉门语义即应推翻为 C，改这两格。
- **mem-vault 的 C**（EC-05）：唯一 C，语义为「自建检索主体能力、Markdown 目录仅作 M8 载体」。若改为检索也采用，须推翻为 B。
- **7 个 D**：维持继续搜索回环态，不是否决；对应候选在该场景暂无路径，开放继续找。

## 4. 机械自检

- 裁决格数=16；§5.3.3 参考格数=16；键集合完全一致，无重复。
- 裁决值全部在封闭词表 ['A', 'B', 'B1', 'B2', 'B3', 'C', 'D'] 内；处置全部在 ['推翻', '确认'] 内；确认格裁决值逐格等于参考信号，推翻格必须不同。
- 每格 EVID 来自对应 EC 的 `fit-input-classification.json`，且在 sealed ledger 索引中存在（索引 133 条）；无手填 SHA/EVID。
- 重跑字节一致（无时间戳、稳定排序）；本页 supporting；derived-from: opn.requirements-fit-matrix；不改写 ratify bundle、不改 fit-matrix。

