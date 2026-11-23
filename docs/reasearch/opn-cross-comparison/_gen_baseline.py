#!/usr/bin/env python3
"""Generate docs/designs/product-structure-baseline.md — the context baseline.

Design (zj 2026-11-23 repurposed the "mother-model R slice" into a context baseline):
- This page is a STRUCTURED FULL SET of decision-relevant context inside an explicit
  scope, plus a gap list. It is NOT an R list, NOT a product plan, NOT a ruling.
- Two dimensions are presented SIDE BY SIDE, never merged:
    A. module dimension (M1..M13) — already has facts, mechanically derived;
    B. end-to-end capability dimension — no existing material in the repo, kept as
       a skeleton with explicit "to be filled by Human" slots, never fabricated.
- The intersection area records conflicts/couplings WITHOUT adjudication or
  normalization (decision deferred to the planning/execution stage).
- Gaps are first-class: 83 unknown + alignment items + version-pin deviations +
  undefined adaptation-target are carried, not filled in.
- R splitting (granularity / acceptance / A B C D) happens LATER, from this baseline.

This generator does no semantic rulings: it joins SoTs and fails closed if any
join does not reconcile. No timestamps, no hand-filled SHAs.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BUNDLE = os.path.join(HERE, "bundle.json")
PMAP = os.path.join(REPO, "docs", "designs", "product-module-map.md")
HUMANGATE = os.path.join(REPO, "docs", "designs", "human-gate-model.md")
CHARTER = os.path.join(REPO, "docs", "reasearch", "2026-11-08-research-charter.md")
LOG = os.path.join(REPO, ".workbuddy", "memory", "2026-11-20.md")
OUT = os.path.join(REPO, "docs", "designs", "product-structure-baseline.md")

problems = []


def die(msg):
    problems.append(msg)


# ---------------------------------------------------------------------------
# SoT 1: charter §4 six dimensions
# ---------------------------------------------------------------------------
charter = open(CHARTER, encoding="utf-8").read()
sec4 = charter.split("## 4. 新的统一调研问题", 1)[-1].split("## 5.", 1)[0]
SIX_DIMS = ["产品模块构成", "技术设计", "复用边界", "组合顺序", "人机分工", "工作量信号"]
for d in SIX_DIMS:
    if d not in sec4:
        die(f"charter §4 missing dimension: {d}")

# ---------------------------------------------------------------------------
# SoT 2: product-module-map §2 modules (id, name, definition, reuse signal)
# ---------------------------------------------------------------------------
pmap = open(PMAP, encoding="utf-8").read()
sec2 = pmap.split("## 2. 模块清单", 1)[-1].split("## 3.", 1)[0]
modules = []  # (mid, name, definition, reuse_signal, layer)
layer = None
for line in sec2.splitlines():
    mh = re.match(r"^###\s+(L[123])\s+", line)
    if mh:
        layer = mh.group(1)
        continue
    mr = re.match(r"^\|\s*(M\d+)\s+([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", line)
    if mr:
        modules.append((mr.group(1), mr.group(2).strip(), mr.group(3).strip(), mr.group(4).strip(), layer))
if len(modules) != 13:
    die(f"expected 13 modules from pmap §2, got {len(modules)}")
if len({m[0] for m in modules}) != len(modules):
    die("duplicate module id in pmap §2")

# M -> scene mapping (ratified Q5b: criterionId mod-* 1:1 with M1..M13; M13 exception)
MOD_SCENE = {
    "M1": "SC::task-workitem", "M2": "SC::identity-scope", "M3": "SC::approval-human",
    "M4": "SC::result-provenance", "M5": "SC::execution-workspace", "M6": "SC::observability",
    "M7": "SC::session-context", "M8": "SC::memory-knowledge", "M9": "SC::config-strategy",
    "M10": "SC::runtime-integration", "M11": "SC::agent-protocol", "M12": "SC::tech-design",
    "M13": None,
}

# ---------------------------------------------------------------------------
# SoT 3: bundle scenes / context entries / difference entries / pin deviations
# ---------------------------------------------------------------------------
b = json.load(open(BUNDLE, encoding="utf-8"))
scenes = [s["id"] for s in b["scene-set"]["scenes"]]
if len(scenes) != 12:
    die(f"expected 12 scenes, got {len(scenes)}")
mapped = {s for s in MOD_SCENE.values() if s}
if mapped != set(scenes):
    die(f"module->scene map mismatch: mapped={sorted(mapped)} bundle={sorted(scenes)}")

unknown_by_scene = {}
for de in b["difference-entries"]:
    if de["verdict"] == "unknown":
        unknown_by_scene[de["scene"]] = unknown_by_scene.get(de["scene"], 0) + 1
    elif de["verdict"] != "native":
        die(f"unexpected verdict {de['verdict']} — cross-comparison has only native/unknown")
unknown_total = sum(unknown_by_scene.values())

ctx = {c["id"]: c for c in b["scene-set"].get("context-entries", [])}
for need in ("CTX::zopn-single-user", "CTX::zopn-no-adopt-verdict"):
    if need not in ctx:
        die(f"missing scene-set context-entry: {need}")

pin_deviations = []
for g in b["graphs"]:
    vp = g["version-pin"]
    if "requested tag" in vp:
        pin_deviations.append((g["project"], vp))

# ---------------------------------------------------------------------------
# SoT 4: human-gate-model six expressions (verify presence, no extraction)
# ---------------------------------------------------------------------------
hg = open(HUMANGATE, encoding="utf-8").read()
GATE_SIX = [
    ("tasktrooper", "全自动"), ("ZAgenticOPN", "例外"), ("qm", "三姿态"),
    ("mozzie", "review"), ("multica", "Review gate + Inbox"), ("orca", "unknown 无 sealed 证据"),
]
for name, _ in GATE_SIX:
    if name not in hg:
        die(f"human-gate-model missing gate expression source: {name}")

# adapt-target-gap fact must exist in the 2026-11-20 log (audit trail)
log = open(LOG, encoding="utf-8").read()
if "adaptation-target 契约从未定义" not in log:
    die("2026-11-20 log missing adaptation-target undefined fact")

if problems:
    print("FAIL (join invariants):", file=sys.stderr)
    for p in problems:
        print("  -", p, file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Render (deterministic)
# ---------------------------------------------------------------------------
def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


o = []
o.append("---")
o.append("doc-kind: reference")
o.append("authority: supporting")
o.append("authority-id: opn.product-structure-baseline")
o.append("---")
o.append("")
o.append("# 产品结构基线 · scope 内 context 结构化全集（supporting）")
o.append("")
o.append("> 本页是 **supporting 基线页**，不是 R 清单、不是产品方案、不是技术设计、不实现。它的唯一职责：在显式 scope 内把决策相关 context 收全，并列呈现两个抽象维度，显式标注冲突/耦合但**不裁决、不归一**，缺口随基线保留不填平。")
o.append("> 由 `docs/reasearch/opn-cross-comparison/_gen_baseline.py` 从 charter §4 / product-module-map §2 / 横比 bundle / human-gate-model 机械派生；端到端维度与交叉区因项目无现成材料，只提供骨架与待填位，**不编造**。")
o.append("> 从这份基线拆 R（定粒度、填 acceptance、跑 A/B/C/D）是**未来规划阶段**的事；本切片不做。")
o.append("")
o.append("## 1. 契约与切片边界")
o.append("")
o.append("- **产出物**：scope 内决策相关 context 的结构化全集 + 缺口清单；不是 R（可独立验收需求），因为 R 要求 `acceptance`，粒度未定则填不出真实验收判据。")
o.append("- **双维度并列**：模块维度（功能构成）与端到端能力维度（用户完整流程）是两个**正交抽象维度**，不是二选一、不是层级；谁也不包含谁。")
o.append("- **交叉区只标注**：一个端到端能力横跨多模块、一个模块参与多能力 → 天然冲突/耦合。本页只显式记录，**不归一成单一 R、不合并、不裁决**。")
o.append("- **缺口是一等公民**：unknown、alignment item、版本钉偏差、未定义契约项全部随基线保留，不隐藏、不填平。")
o.append("- **决策延迟**：粒度、冲突消解、耦合处理全部延迟到规划/执行阶段；本页只提供决策所需的完整 context。")
o.append("")
o.append("## 2. Scope 定义（四坐标）")
o.append("")
o.append("### 2.1 六维观察透镜（charter §4）")
o.append("")
o.append("| 维度 | 要回答什么（charter §4 原文） | 本基线中的落点 |")
o.append("|---|---|---|")
lens_landing = {
    "产品模块构成": "§3 模块维度（13 模块清单）",
    "技术设计": "§3 模块定义 + §6 缺口（M12 技术设计与部署）",
    "复用边界": "§3 reuse_signal 列（assumption，事实以账本为准）+ §6 缺口",
    "组合顺序": "§5 交叉区骨架（端到端流程 × 模块依赖，待填）",
    "人机分工": "§2.4 Human 门六方 + §3 M3 行",
    "工作量信号": "§3 模块数/复用信号 + §6 unknown 缺口清单",
}
for d in SIX_DIMS:
    # pull the charter table row verbatim
    row = next((ln for ln in sec4.splitlines() if ln.strip().startswith("| " + d + " ")), "")
    answer = row.split("|")[2].strip() if row else "（见 charter §4）"
    o.append(f"| {d} | {esc(answer)} | {lens_landing[d]} |")
o.append("")
o.append("### 2.2 模块坐标（13 模块，源自 product-module-map §2）")
o.append("")
o.append("| 模块 | 语义层 | 定义 | 对应场景 |")
o.append("|---|---|---|---|")
for mid, name, definition, signal, layer in modules:
    o.append(f"| {mid} {name} | {layer} | {esc(definition)} | {MOD_SCENE[mid] or '非横比场景（M13 例外）'} |")
o.append("")
o.append("### 2.3 场景坐标（12 场景，SCENE-SET::zopn-v1 RATIFIED）")
o.append("")
o.append("| # | 场景 | 对应模块 | unknown 缺口数（横比） |")
o.append("|---|---|---|---|")
for i, s in enumerate(scenes, 1):
    mid = next((m[0] for m in modules if MOD_SCENE[m[0]] == s), "—")
    o.append(f"| {i} | `{s}` | {mid} | {unknown_by_scene.get(s, 0)} |")
o.append("")
o.append("### 2.4 Human 门六方（源自 human-gate-model 背景；M3 门模型已裁决，其余仅参照）")
o.append("")
o.append("| 来源 | 门表达 | 状态 |")
o.append("|---|---|---|")
for source, expr in GATE_SIX:
    status = "已被 zj 2026-11-20 采纳为基础模型（准入+准出双门）" if source == "multica" else (
        "unknown，无 sealed 证据" if source == "orca" else "参照表达（未采纳为默认）")
    o.append(f"| {source} | {expr} | {status} |")
o.append("")
o.append("## 3. 维度 A：模块构成（已有事实，机械派生）")
o.append("")
o.append("> 本维度已有事实支撑。`reuse_signal` 列为 **assumption**（源 product-module-map §2，待母模型裁决）；「能力存在」的 sealed Evidence 事实以 `designs/reuse-evidence-ledger.md` 为准。本页不重复证据、不改判断。")
o.append("")
o.append("| 模块 | 语义层 | 定义 | reuse_signal (assumption, 源 pmap §2) | 证据账本 |")
o.append("|---|---|---|---|---|")
for mid, name, definition, signal, layer in modules:
    o.append(f"| {mid} {name} | {layer} | {esc(definition)} | {esc(signal)} | 见 reuse-evidence-ledger {mid} 行 |")
o.append("")
o.append("## 4. 维度 B：端到端能力（骨架 · 待 Human 填 · 不编造）")
o.append("")
o.append("- **现状**：项目内**无成体系的端到端能力清单**。现有材料中「workflow」命中项均为 CI workflow / review workflow 等单点流程词，不是能力维度；因此本维度是净新增整理工作，不由账本派生。")
o.append("- **约束**：以下为空位模板，**不得由执行 Agent 依据模块名或 README 字面推断填充**（守 charter §7 非目标）。每条能力须 Human 逐条梳理并给出来源。")
o.append("")
o.append("| 能力 ID | 能力名（用户完整流程） | 起点 | 终点 | 跨越模块 | 来源/依据 | 状态 |")
o.append("|---|---|---|---|---|---|---|")
o.append("| EC-待填 | — | — | — | — | — | 待 Human 梳理 |")
o.append("")
o.append("> 已知线索（非清单）：product-module-map §4 写有一条最小可运行切片流程「创建 → claim → 执行(worktree) → 结果+provenance → Human 门 → 完成」，可作端到端能力的候选种子，但是否成立、如何拆多条能力仍待 Human 裁决。")
o.append("")
o.append("## 5. 交叉区：冲突 / 耦合标注（只标注，不裁决、不归一）")
o.append("")
o.append("> 两维度天然多对多。本区只登记冲突/耦合的**位置与来源**，不合并成单一 R、不选边、不消解。现在维度 B 未填 → 跨维度交叉位暂为空；先登记已在模块维度内显式的语义冲突作为参照。")
o.append("")
o.append("| 交叉项 | 冲突/耦合描述 | 来源 | 处理 |")
o.append("|---|---|---|---|")
o.append("| M1 状态机 | opencode 九态 vs ZAgenticOPN 四态，互不相容 | product-module-map §2 M1 | 标注，待规划阶段裁决 |")
o.append("| M2 身份 scope | qm 每人每房 vs ZAgenticOPN Human→device→agent_instance，不可互推 | product-module-map §2 M2 | 标注，待规划阶段裁决 |")
o.append("| M3 Human 门 | 六种门表达互不兼容（见 §2.4） | human-gate-model 背景 | 已裁基础模型，其余仅参照 |")
o.append("| M8 记忆边界 | mem-vault 纯 Markdown vs qm scope-memory+Postgres vs ZAgenticOPN 结构化事实 | product-module-map §2 M8 | 标注，待规划阶段裁决 |")
o.append("| 维度 B × 维度 A | — | — | 待 Human 填端到端能力后登记 |")
o.append("")
o.append("## 6. 缺口清单（不隐藏、不填平）")
o.append("")
o.append(f"### 6.1 unknown 证据缺口（横比 {unknown_total} 条，按场景）")
o.append("")
o.append("| 场景 | unknown 数 |")
o.append("|---|---|")
for s in scenes:
    o.append(f"| `{s}` | {unknown_by_scene.get(s, 0)} |")
o.append(f"| **合计** | **{unknown_total}** |")
o.append("")
o.append("> unknown ≠ absent：以上只表示无 sealed 证据，不表示项目无该能力；不进复用判断、不填平。")
o.append("")
o.append("### 6.2 alignment item / 边界约束")
o.append("")
for cid in ("CTX::zopn-single-user", "CTX::zopn-no-adopt-verdict"):
    c = ctx[cid]
    o.append(f"- **{cid}**（{c.get('kind','')}）：{esc(c.get('statement',''))}")
o.append("")
o.append("### 6.3 版本钉偏差（引用前须按实际 pin 复核）")
o.append("")
for proj, vp in pin_deviations:
    o.append(f"- **{proj}**：{esc(vp)}")
o.append("")
o.append("### 6.4 契约缺口")
o.append("")
o.append("- **adaptation-target 未定义**：横比契约中该字段从未定义且属 Human 复核项，机械生成器不自判；adapted/unsupported 因此为空不是 bug。来源：2026-11-20 工作日志（复用边界收敛）。")
o.append("- **端到端能力维度无现成材料**：见 §4。")
o.append("")
o.append("## 7. 一致性自检（机械）")
o.append("")
o.append(f"- 六维 {len(SIX_DIMS)} 项全部命中 charter §4；模块 {len(modules)} 项命中 pmap §2；场景 {len(scenes)} 项命中 bundle；Human 门 {len(GATE_SIX)} 方命中 human-gate-model。")
o.append(f"- 模块→场景映射覆盖全部 12 场景（13 模块中 M13 为例外）；unknown 合计 {unknown_total}，与 bundle difference-entries 一致。")
o.append("- 端到端维度与交叉区只含骨架/来源标注，无推断填充；所有 SHAs 机械派生自 SoT，无手填。")
o.append("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o) + "\n")
print(f"wrote {OUT}")
print(f"modules={len(modules)} scenes={len(scenes)} dims={len(SIX_DIMS)} gates={len(GATE_SIX)} unknown={unknown_total} pin_dev={len(pin_deviations)}")
