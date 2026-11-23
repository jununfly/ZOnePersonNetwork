#!/usr/bin/env python3
"""Generate docs/designs/product-structure-baseline.md — the context baseline.

Design (zj 2026-11-23 repurposed the "mother-model R slice" into a context baseline):
- This page is a STRUCTURED FULL SET of decision-relevant context inside an explicit
  scope, plus a gap list. It is NOT an R list, NOT a product plan, NOT a ruling.
- Two dimensions are presented SIDE BY SIDE, never merged:
    A. module dimension (M1..M13) — already has facts, mechanically derived;
    B. end-to-end capability dimension — Human-ruled on 2026-11-23 via 3 grill
       rounds: 5 accepted ECs (user-goal closed loops) + 4 reference-product flow
       topologies kept separate (no normalization). Rulings are an explicit
       constant table in this generator, each cited EVID validated against the
       sealed ledger index (fail closed); the agent never infers capabilities.
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
COLLECT_DIR = os.path.join(HERE, "collect")
REASEARCH_DIR = os.path.join(REPO, "docs", "reasearch")

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

# ---------------------------------------------------------------------------
# SoT 5: sealed EVID index — for fail-closed validation of §4 Human rulings
# ---------------------------------------------------------------------------
import glob as _glob

evid_index = {}  # 24-hex prefix -> (ledger filename, excerpt text)
for _f in (_glob.glob(os.path.join(REASEARCH_DIR, "**", "collect", "ledger-*.json"), recursive=True)
           + _glob.glob(os.path.join(REASEARCH_DIR, "**", "*ledger-response*.json"), recursive=True)):
    try:
        _d = json.load(open(_f, encoding="utf-8"))
    except Exception:
        continue

    def _walk(o):
        if isinstance(o, dict):
            eid = o.get("id") or o.get("sealedId") or o.get("sealed_id")
            txt = o.get("excerpt") or o.get("text") or o.get("statement") or o.get("content")
            if eid and txt and isinstance(eid, str):
                evid_index.setdefault(eid[:24], (os.path.basename(_f), " ".join(str(txt).split())))
            for v in o.values():
                _walk(v)
        elif isinstance(o, list):
            for v in o:
                _walk(v)
    _walk(_d)

# ---------------------------------------------------------------------------
# Human rulings (zj 2026-11-23 grill: rounds 1-3). These are DECISIONS, not
# mechanical derivations; encoded here as an explicit, auditable constant table.
# Every cited EVID must exist in evid_index (fail closed) — no hand-filled SHA.
# ---------------------------------------------------------------------------
EC_LIST = [
    {
        "id": "EC-01", "name": "提交目标 → 拿到可验收结果（主闭环）",
        "start": "Human 提交一个目标 / 创建 Work Item",
        "end": "Human 在 Human 门看到结果并验收完成",
        "mods": "M1 → M2 → M5 → M4 → M3",
        "material": "EVID::a67400762c931df62135608d (multica assign-work→review) + ZAgenticOPN 最小切片 (pmap §4)",
        "evid": ["a67400762c931df62135608d"],
        "ruling": "zj 2026-11-23 采纳",
    },
    {
        "id": "EC-02", "name": "review 打回 → Agent 从拒绝历史学习 → 重做",
        "start": "Human 在 Human 门 reject with feedback",
        "end": "Agent 带反馈重做后再次进入门",
        "mods": "M3 → M4 → M5 → M6",
        "material": "EVID::3e8488d208de54fdd00a11c0 (mozzie reject-with-feedback) + loop-now review loops (pmap §3 M6)",
        "evid": ["3e8488d208de54fdd00a11c0"],
        "ruling": "zj 2026-11-23 采纳",
    },
    {
        "id": "EC-03", "name": "跨设备接续会话",
        "start": "Human 在设备 A 发起会话",
        "end": "Human 在设备 B 接续同一会话",
        "mods": "M7 → M8 → M10",
        "material": "EVID::1eedaed644a280db74133572 (mem-vault session-blackboard/跨设备同步)",
        "evid": ["1eedaed644a280db74133572"],
        "ruling": "zj 2026-11-23 采纳",
    },
    {
        "id": "EC-05", "name": "共享事实沉淀与检索",
        "start": "Human 完成一次协作并要求沉淀事实",
        "end": "Human 后续检索 / 被复用到新会话",
        "mods": "M8 → M7",
        "material": "EVID::d2423363b8e0d64ec8ce61cc (tasktrooper 四 scope memory) + ZAgenticOPN 结构化事实 (draft.md:77)",
        "evid": ["d2423363b8e0d64ec8ce61cc"],
        "ruling": "zj 2026-11-23 采纳",
    },
    {
        "id": "EC-06", "name": "运行诊断与回放",
        "start": "Human 发现一次运行失败 / 想审计",
        "end": "Human 定位到失败点并重放该 run",
        "mods": "M6 → M4",
        "material": "EVID::71dfad6640e6f45a720f8a69 (multica run transcript) + loop-now board/review loops (pmap §3 M6)",
        "evid": ["71dfad6640e6f45a720f8a69"],
        "ruling": "zj 2026-11-23 采纳（S4a 补漏）",
    },
]
EC_REJECTED = [
    {"id": "EC-04", "name": "scope 内隔离执行", "reason": "起点是系统派发、终点是代码产出，Human 不可独立触发 → 属 Q2a 操作序列/技术设计，归维度 A 的 M5/M10，不作独立 EC", "ruling": "zj 2026-11-23 否决"},
]

REF_FLOWS = [
    {
        "project": "multica", "metaphor": "团队隐喻（assign like a teammate）",
        "why_separate": "组织协作闭环：Human 把 agent 当队友指派，关注 hand-back 与 ship 决策；非我方单人目标闭环口径",
        "nodes": [
            ("指派 issue", "a67400762c931df62135608d"),
            ("自主 pick up（受控 runtime）", "76fd261e3f84f3c9e33a84c6"),
            ("进度 + blockers（comment as it goes）", "76fd261e3f84f3c9e33a84c6"),
            ("hand back（review gate）", "2cc46ac299adc52b807b122e"),
            ("Inbox 叫人（needs a call）", "2cc46ac299adc52b807b122e"),
        ],
    },
    {
        "project": "orca", "metaphor": "编排器隐喻（parallel worktree + remote run）",
        "why_separate": "工具运行闭环：关注并行隔离、diff 批注与远程常驻；无 Work Item / 验收语义",
        "nodes": [
            ("并行 worktree（any CLI agent）", "2ed6d70d48ae1d10a19026a0"),
            ("diff 逐行批注（focused feedback）", "a16d037b586eabaa4c616d4a"),
            ("Remote / SSH / cloud VM", "0a6cfe851c86d1535e2d2fdc"),
            ("持续运行（laptop 睡眠不断）", "0a6cfe851c86d1535e2d2fdc"),
        ],
    },
    {
        "project": "mozzie", "metaphor": "管理型 workforce 隐喻（managed workforce）",
        "why_separate": "目标拆解 + 依赖编排 + review 队列的桌面编排闭环；以 work item 为单元但其拆-item/依赖图语义属参照，不归一为我方 EC",
        "nodes": [
            ("描述目标 → 拆 work items", "6676d3f26c9b4f77443c5d2a"),
            ("独立 worktree + 并行 agent", "3e8488d208de54fdd00a11c0"),
            ("依赖图 / blocked 自动触发", "3e8488d208de54fdd00a11c0"),
            ("review：approve / reject with feedback", "3e8488d208de54fdd00a11c0"),
        ],
    },
    {
        "project": "tasktrooper", "metaphor": "board 自治隐喻（the board drives）",
        "why_separate": "列自治派发闭环（board 把任务交下一列，无人按 run）；全自动姿态与我方 Human 门语义冲突，仅作参照",
        "nodes": [
            ("任务放上 board", "6a0463be6d4575650cc64979"),
            ("列拥有者 agent 自主 pick up", "6a0463be6d4575650cc64979"),
            ("clone → plan → implement → test → PR", "90b8b4fc0e74bc12214889c4"),
            ("交下一列 / 人全程观察 run", "6a0463be6d4575650cc64979"),
        ],
    },
]

# Fail closed: every EVID cited in EC_LIST and REF_FLOWS must exist in the ledger.
_cited = set()
for ec in EC_LIST:
    _cited.update(ec["evid"])
for fl in REF_FLOWS:
    _cited.update(eid for _label, eid in fl["nodes"])
for _eid in sorted(_cited):
    if _eid not in evid_index:
        die(f"§4 cites EVID::{_eid} not found in any sealed ledger — refuse to emit (no hand-filled SHA)")
if len({ec["id"] for ec in EC_LIST}) != len(EC_LIST):
    die("duplicate EC id in EC_LIST")
if len(REF_FLOWS) != 4:
    die(f"expected 4 reference-product flows (S3c), got {len(REF_FLOWS)}")

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
o.append("> 由 `docs/reasearch/opn-cross-comparison/_gen_baseline.py` 从 charter §4 / product-module-map §2 / 横比 bundle / human-gate-model 机械派生；端到端维度 §4 由 zj 2026-11-23 grill 逐条裁决（作为带 EVID 存在性校验的显式常量表注入生成器，非 Agent 推断），交叉区只标注不裁决。")
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
    "组合顺序": "§4 EC 链路（跨越模块列）+ §5 交叉区耦合标注",
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
o.append("## 4. 维度 B：端到端能力（Human 逐条梳理 · zj 2026-11-23）")
o.append("")
o.append("> 本维度项目内原无成体系清单，是净新增整理工作。zj 2026-11-23 用三轮 grill 锁定口径后逐条裁决生成，执行 Agent **不依据模块名或 README 字面推断**（守 charter §7 非目标）。")
o.append("> **口径（Q1–Q5 锁定）**：① 参照物流程聚成候选种子、Human 逐条裁决；② 一条能力 = 一个**用户目标闭环**（起点→终点均 Human 可触发/可观察）；③ 起点/终点按 Human 主体记，非系统事件；④ 来源分「素材出处 + Human 裁决」两部分；⑤ ID 顺序编号不表语义。")
o.append("")
o.append("### 4.1 我方端到端能力清单（EC · 已采纳）")
o.append("")
o.append("| 能力 ID | 能力名（用户完整流程） | 起点（Human） | 终点（Human） | 跨越模块 | 素材出处 | Human 裁决 |")
o.append("|---|---|---|---|---|---|---|")
for ec in EC_LIST:
    o.append(f"| {ec['id']} | {esc(ec['name'])} | {esc(ec['start'])} | {esc(ec['end'])} | {esc(ec['mods'])} | {esc(ec['material'])} | {esc(ec['ruling'])} |")
o.append("")
o.append("**已否决候选（留痕，不进清单）**：")
for rj in EC_REJECTED:
    o.append(f"- {rj['id']} {esc(rj['name'])} —— {esc(rj['reason'])}（{esc(rj['ruling'])}）")
o.append("")
o.append("> 这些 EC 是**用户目标闭环**，不是 R（可独立验收需求）：无 acceptance、无 priority/critical，粒度未定；拆 R 仍属未来规划阶段（§1）。")
o.append("")
o.append("### 4.2 参考产品端到端拓扑（单独拓扑 · 不归一、不裁决）")
o.append("")
o.append("> 四家为 zj 指定的**优先参考产品**（S3c）。其端到端链路均从 sealed 原文直抽，每节点挂 EVID；口径与我方 EC 不同（组织协作 / 工具运行 / 编排器 / board 自治），故**单独拓扑，不并入 §4.1、不裁决**——与基线「双维度并列、冲突只标注」一致。")
o.append("")
for fl in REF_FLOWS:
    o.append(f"**{esc(fl['project'])}** — {esc(fl['metaphor'])}")
    o.append("")
    chain = " → ".join(f"{lab} `[EVID::{eid}]`" for lab, eid in fl["nodes"])
    o.append(f"- 链路：{chain}")
    p = lambda eid: evid_index.get(eid, ("<missing>", ""))[0]
    o.append(f"- 每节点出处：`{', '.join(sorted({p(eid) for _lab, eid in fl['nodes']}))}`")
    o.append(f"- 口径差异（为何单独）：{esc(fl['why_separate'])}")
    o.append("")
o.append("> 附：multica 的 Review gate + Inbox 已由 zj 2026-11-20 采纳为 M3 门模型基础（准入+准出双门，见 §2.4）——那是**模块级裁决**，与本节的端到端拓扑是不同层次，不冲突。")
o.append("")
o.append("## 5. 交叉区：冲突 / 耦合标注（只标注，不裁决、不归一）")
o.append("")
o.append("> 两维度天然多对多。本区只登记冲突/耦合的**位置与来源**，不合并成单一 R、不选边、不消解。维度 B 已在 §4 逐条裁决，先登记已在模块维度内显式的语义冲突作为参照；EC × 模块的精确耦合在规划阶段拆 R 时展开。")
o.append("")
o.append("| 交叉项 | 冲突/耦合描述 | 来源 | 处理 |")
o.append("|---|---|---|---|")
o.append("| M1 状态机 | opencode 九态 vs ZAgenticOPN 四态，互不相容 | product-module-map §2 M1 | 标注，待规划阶段裁决 |")
o.append("| M2 身份 scope | qm 每人每房 vs ZAgenticOPN Human→device→agent_instance，不可互推 | product-module-map §2 M2 | 标注，待规划阶段裁决 |")
o.append("| M3 Human 门 | 六种门表达互不兼容（见 §2.4） | human-gate-model 背景 | 已裁基础模型，其余仅参照 |")
o.append("| M8 记忆边界 | mem-vault 纯 Markdown vs qm scope-memory+Postgres vs ZAgenticOPN 结构化事实 | product-module-map §2 M8 | 标注，待规划阶段裁决 |")
o.append("| EC-04 隔离执行 | 起点系统派发、终点代码产出，Human 不可独立触发 → 归 M5/M10 技术设计 | zj 2026-11-23 裁决（§4.1 否决留痕） | 已否决为独立 EC；执行段归入模块维度 |")
o.append("| 参考产品拓扑 × 我方 EC | multica 组织协作 / orca 工具运行 / mozzie 编排器 / tasktrooper board 自治，四种口径均≠我方用户目标闭环 | §4.2 sealed 原文 | 单独拓扑，不归一、不裁决 |")
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
o.append("- **我方 EC 的 acceptance 未定**：§4.1 的 5 条 EC 是用户目标闭环、无验收判据；拆 R（定粒度/填 acceptance/跑 A B C D）仍属未来规划阶段。")
o.append("")
o.append("## 7. 一致性自检（机械）")
o.append("")
o.append(f"- 六维 {len(SIX_DIMS)} 项全部命中 charter §4；模块 {len(modules)} 项命中 pmap §2；场景 {len(scenes)} 项命中 bundle；Human 门 {len(GATE_SIX)} 方命中 human-gate-model。")
o.append(f"- 模块→场景映射覆盖全部 12 场景（13 模块中 M13 为例外）；unknown 合计 {unknown_total}，与 bundle difference-entries 一致。")
o.append(f"- 端到端维度 §4.1 含 {len(EC_LIST)} 条采纳 EC（+{len(EC_REJECTED)} 条否决留痕）、§4.2 含 {len(REF_FLOWS)} 家参考产品拓扑；全部由 zj 裁决常量表注入，每条引用 EVID 已通过 ledger 存在性校验（fail-closed），无手填 SHA。")
o.append("- 交叉区只标注不裁决；所有 SHAs 机械派生自 SoT，无手填。")
o.append("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o) + "\n")
print(f"wrote {OUT}")
print(f"modules={len(modules)} scenes={len(scenes)} dims={len(SIX_DIMS)} gates={len(GATE_SIX)} unknown={unknown_total} pin_dev={len(pin_deviations)} EC={len(EC_LIST)} rejected={len(EC_REJECTED)} ref_flows={len(REF_FLOWS)}")
