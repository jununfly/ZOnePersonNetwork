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
- Gaps are first-class: 83 unknown + alignment items + version-pin deviations
  are carried, not filled in. adaptation-target was clarified 2026-11-23 as a
  NON-gap (field exists but semantically undefined / Human-ruled / zero instances;
  adapt/unsupported ruling belongs to the mother model). The alignment item
  single-user/cross-device/multi-project was ruled 2026-11-23 into a STAGING
  working assumption (3 orthogonal axes, research upper-bound vs landing start),
  encoded as a fail-closed constant table; the raw CTX statement is kept as history.
- §6.1 carries the 83-unknown supplemental-collection PILOT result (zj 2026-11-23
  ruling A: reached the literal gate but exposed risk). Numbers are read
  mechanically from pilot-evidence-audit.json (dual-rate: mechanical hits vs
  semantic-acceptable); every audited sealed ID is validated against the two
  pilot ledgers (fail closed). Separate ledgers only — the ratified bundle is
  untouched.
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

# Q1a (zj 2026-11-23): version-pin rows carry THREE distinct SHAs —
#   requested tag (ignored by collect), bundle-recorded HEAD (may be stale),
#   ledger revision.sha (the ACTUAL pin). The multica bundle record (41885a6d…)
#   does not exist in the ledger; the real pin is 7a926b82…. Never hand-fill:
#   read revision.sha mechanically from the sealed ledger and fail closed if absent.
def ledger_actual_pin(project):
    lf = os.path.join(COLLECT_DIR, f"ledger-{project}.json")
    if not os.path.exists(lf):
        die(f"version-pin: missing ledger for {project}: {lf}")
        return None
    ld = json.load(open(lf, encoding="utf-8"))
    repos = ld.get("result", {}).get("repositories", [])
    if len(repos) != 1:
        die(f"version-pin: expected 1 repository in {lf}, got {len(repos)}")
        return None
    sha = repos[0].get("revision", {}).get("sha", "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        die(f"version-pin: invalid revision.sha in {lf}: {sha!r}")
        return None
    return sha

pin_deviations = []  # (project, requested_tag, bundle_recorded_sha, ledger_actual_sha)
for g in b["graphs"]:
    vp = g["version-pin"]
    if "requested tag" in vp:
        proj = g["project"]
        m = re.search(r"requested tag (\S+) = ([0-9a-f]+)", vp)
        req_tag = m.group(1) if m else "?"
        req_sha = m.group(2) if m else "?"
        mh = re.match(r"^\S+ @ ([0-9a-f]{40})", vp)
        bundle_sha = mh.group(1) if mh else "?"
        actual_sha = ledger_actual_pin(proj)
        pin_deviations.append((proj, req_tag, req_sha, bundle_sha, actual_sha))

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
# SoT 6: pilot supplemental-collection audit (83-unknown probe, zj 2026-11-23).
# Numbers are read mechanically from the audit JSON — never hand-filled.
# Fail closed: schema, arithmetic, and every audited sealed ID must reconcile
# against the two pilot ledgers before §6.1 may be emitted.
# ---------------------------------------------------------------------------
AUDIT_JSON = os.path.join(COLLECT_DIR, "pilot-evidence-audit.json")
PILOT_LEDGERS = {
    "dmux": os.path.join(COLLECT_DIR, "pilot-dmux", "ledger-dmux.json"),
    "mem-vault": os.path.join(COLLECT_DIR, "pilot-mem-vault", "ledger-mem-vault.json"),
}
audit = None
if not os.path.exists(AUDIT_JSON):
    die(f"pilot audit: missing {AUDIT_JSON}")
else:
    audit = json.load(open(AUDIT_JSON, encoding="utf-8"))
    if audit.get("schema") != "zj-pilot-evidence-audit/v1":
        die(f"pilot audit: unexpected schema {audit.get('schema')!r}")
    # build the sealed-ID universe of the two pilot ledgers
    pilot_ids = set()
    for proj, lf in PILOT_LEDGERS.items():
        if not os.path.exists(lf):
            die(f"pilot audit: missing pilot ledger for {proj}: {lf}")
            continue
        _pd = json.load(open(lf, encoding="utf-8"))
        for _e in _pd.get("result", {}).get("evidence", []):
            pilot_ids.add(_e.get("id"))
    _a_rows = audit.get("rows", [])
    _mh = audit.get("mechanical_hits")
    _tc = audit.get("targeted_cells")
    _sc = audit.get("semantic_counts", {})
    if _mh != len(_a_rows):
        die(f"pilot audit: mechanical_hits {_mh} != len(rows) {len(_a_rows)}")
    if sum(_sc.get(k, 0) for k in ("acceptable", "weak", "mismatched")) != _mh:
        die(f"pilot audit: semantic_counts do not sum to mechanical_hits {_mh}")
    if not isinstance(_tc, int) or _tc <= 0:
        die(f"pilot audit: invalid targeted_cells {_tc!r}")
    for _r in _a_rows:
        if _r.get("sealed_id") not in pilot_ids:
            die(f"pilot audit: sealed_id {str(_r.get('sealed_id'))[:12]} not found in pilot ledgers — refuse to emit (no hand-filled ID)")
    # every duplicate-excerpt member must be a real row key (project/criterion)
    _row_keys = {(r.get("project"), r.get("criterion_id")) for r in _a_rows}
    for _dup_key, _members in audit.get("duplicate_excerpt_groups", {}).items():
        for _m in _members:
            _pp, _, _cc = _m.partition("/")
            if (_pp, _cc) not in _row_keys:
                die(f"pilot audit: duplicate-excerpt member {_m!r} not in rows")

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

# ---------------------------------------------------------------------------
# Human ruling (zj 2026-11-23 grill: alignment item 单人/跨设备/多项目).
# DECISION, not derivation. Three ORTHOGONAL boundary axes, each with a
# research upper-bound and (where decided) a landing start point. Encoded as
# explicit constant table; fail-closed against the facts it cites.
# ---------------------------------------------------------------------------
BOUNDARY_RULING = {
    "qualification": "三词 = 三个正交边界轴（owner / 设备 / 项目），非三选一；斜杠并列是文档措辞缺陷",
    "effect": "阶段性工作假设（charter §7 本阶段不做产品方案），非终局定稿",
    "landing": "就地更新基线页 §6.2；不动横比 bundle/report（守 ratify 边界）",
    "axes": [
        {"axis": "owner", "upper": "多人", "start": "单人",
         "rationale": "单人是多人的特例；先解决单人（多人问题太开放，短期难做可用产品）"},
        {"axis": "设备", "upper": "跨设备", "start": "（Q8c：起点按原则推导，不逐轴锁死）",
         "rationale": "EC-03 跨设备接续已采纳；参照物 roadmap 1-2-2 同向"},
        {"axis": "项目", "upper": "多项目", "start": "（Q8c：起点按原则推导，不逐轴锁死）",
         "rationale": "M2 身份 scope / M8 记忆边界冲突只有多项目下才暴露；取单项目会让缺口消失"},
    ],
    "principle": "先解决约束更强的特例，泛化延迟（Q8c）——不逐轴锁死起点值，规划阶段按同一原则推导",
    "reopen": "进入产品方案阶段拆 R 时（Q7a）；风险留痕：调研中发现上界不可行不自动触发复核",
    "ct_note": "CTX::zopn-single-user 原 statement『目标为单人个人协同网络』降为历史留痕：『单人』现为落地起点，非目标边界；上界已扩展为多人/跨设备/多项目",
}

# Fail closed: the ruling must cite facts that actually exist in the SoTs.
if {ax["axis"] for ax in BOUNDARY_RULING["axes"]} != {"owner", "设备", "项目"}:
    die("BOUNDARY_RULING axes must be exactly owner/设备/项目")
if not any(ec["id"] == "EC-03" for ec in EC_LIST):
    die("BOUNDARY_RULING cites EC-03 but it is absent from EC_LIST")
# M2/M8 conflict lines must exist in pmap §2 (rationale for 项目上界)
if "每人每房" not in pmap or "scope" not in pmap:
    die("BOUNDARY_RULING cites M2 scope conflict but pmap §2 lacks it")
if "mem-vault" not in pmap or "scope-memory" not in pmap:
    die("BOUNDARY_RULING cites M8 memory conflict but pmap §2 lacks it")
# CTX entry still present (already checked above at line 105); confirm statement hook
if "单人个人协同网络" not in ctx["CTX::zopn-single-user"].get("statement", ""):
    die("BOUNDARY_RULING ct_note hook missing from CTX::zopn-single-user statement")

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
o.append("- **缺口是一等公民**：unknown、alignment item、版本钉偏差全部随基线保留，不隐藏、不填平；adaptation-target 已于 2026-11-23 改判为非缺口（见 §6.4）。")
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

# Pilot supplemental-collection result (zj 2026-11-23 ruling A). All numbers
# below are read from `audit` (validated fail-closed in SoT 6), never hand-filled.
if audit is not None:
    _mh = audit["mechanical_hits"]
    _tc = audit["targeted_cells"]
    _acc = audit["semantic_counts"]["acceptable"]
    _weak = audit["semantic_counts"]["weak"]
    _mis = audit["semantic_counts"]["mismatched"]
    _dup_groups = audit.get("duplicate_excerpt_groups", {})
    _dup_members = sum(len(v) for v in _dup_groups.values())
    o.append("**补采试点（83 unknown 探针 · zj 2026-11-23 定性 A：达标但暴露风险）**")
    o.append("")
    o.append(f"- 为验证「补采 {unknown_total} unknown」是否可行，选 dmux（11 criteria）+ mem-vault（9 criteria）两仓做 fresh collect 试点；独立 ledger，**不回灌已 ratify 的 bundle**。新证据 sealed ID 经两仓 ledger 存在性校验（fail-closed），未手填。")
    o.append(f"- **双口径结果**：目标格 {_tc}；机械 sealed 命中 **{_mh}/{_tc}（{100*_mh/_tc:.0f}%）**（Q6a 字面达标：≥1 条 sealed native）；但语义复核仅 **{_acc} 条合格**（dmux `mod-runtime-integration` HTTP Callback API；mem-vault `mod-result-provenance` handoff+changelog）→ 真实可补率 **{_acc}/{_tc}（{100*_acc/_tc:.0f}%）**；弱相关 {_weak}、明确错配 {_mis}（其中 {_dup_members} 条为**完全相同**的 README/CONTRIBUTING/AGENTS 文件清单摘录，被导航器误钉成 {_dup_members} 个不同场景——reconfirm「sealed ≠ 语义有效」陷阱）。")
    o.append(f"- **结论**：按字面判据试点达标，但语义落差证明「全量补采 {unknown_total} unknown」若不逐条语义复核会灌入大量错配证据 → **全量补采不划算、且必须逐条语义复核**。此结论为分析层判断（assumption），随基线保留，不填平缺口、不改任何 native 判断。")
    o.append("- **出处**：`docs/reasearch/opn-cross-comparison/collect/pilot-evidence-audit.json`（审计）、`collect/pilot-dmux/ledger-dmux.json` + `collect/pilot-mem-vault/ledger-mem-vault.json`（独立试点 ledger）。")
    o.append("")

o.append("### 6.2 alignment item / 边界约束")
o.append("")
for cid in ("CTX::zopn-single-user", "CTX::zopn-no-adopt-verdict"):
    c = ctx[cid]
    o.append(f"- **{cid}**（{c.get('kind','')}）：{esc(c.get('statement',''))}")
o.append("")
o.append("> 上两条为横比 bundle 的原始留痕（已 ratify，不改写）。其中 `CTX::zopn-single-user` 已于 2026-11-23 由 zj 裁决消解为工作假设，见下表。")
o.append("")
o.append("**已裁决工作假设（zj 2026-11-23 grill，阶段性非终局）**")
o.append("")
o.append(f"- **定性**：{BOUNDARY_RULING['qualification']}")
o.append(f"- **效力**：{BOUNDARY_RULING['effect']}")
o.append(f"- **落点**：{BOUNDARY_RULING['landing']}")
o.append("")
o.append("| 边界轴 | 调研上界（本轮锁定） | 落地起点 | 依据 |")
o.append("|---|---|---|---|")
for ax in BOUNDARY_RULING["axes"]:
    o.append(f"| {ax['axis']} | {ax['upper']} | {ax['start']} | {esc(ax['rationale'])} |")
o.append("")
o.append(f"- **落地序列原则**：{BOUNDARY_RULING['principle']}")
o.append(f"- **重开条件**：{BOUNDARY_RULING['reopen']}")
o.append(f"- **CTX 措辞处置**：{BOUNDARY_RULING['ct_note']}")
o.append("")
o.append("### 6.3 版本钉偏差（引用前须按 ledger 实际 pin 复核）")
o.append("")
o.append("> 根因：collect 编译器 `resolveRevision` 恒取默认分支 HEAD、忽略 brief 的 `repositories[].revision`，属仓库外固有限制（zj-research 为纯适配层，本仓库不可修）。下表三个 SHA **互不相同**：请求 tag（被忽略）、bundle 记录 HEAD（历史留痕，可能失准）、**ledger 实际 pin（引用时以此为唯一准绳，机械读取 `result.repositories[].revision.sha`，非手填）**。")
o.append("")
o.append("| 项目 | 请求 tag（被忽略） | bundle 记录 HEAD（历史） | ledger 实际 pin（采用） |")
o.append("|---|---|---|---|")
for proj, req_tag, req_sha, bundle_sha, actual_sha in pin_deviations:
    if actual_sha is None:
        die(f"version-pin render: {proj} has no ledger actual pin")
        actual_sha = "<unverified>"
    o.append(f"| {proj} | `{req_tag}` = `{req_sha}` | `{bundle_sha}` | **`{actual_sha}`** |")
o.append("")
stale = [(p, bs, a) for p, _, _, bs, a in pin_deviations if a and bs != a]
if stale:
    parts = [f"{p}（bundle `{bs[:8]}…` → ledger 实际 `{a[:8]}…`）" for p, bs, a in stale]
    o.append(f"- **失准标记**：{'；'.join(parts)}。bundle 记录 HEAD 在现存 sealed ledger 中不存在；引用这些项目的证据须按 ledger 实际 pin 复核。失准源于早期 bundle 手工记录，非 hash 伪造——已按 ledger 实值纠正展示，ratify 过的 bundle 原文不动。")
else:
    o.append("- **失准标记**：无（所有 bundle 记录 HEAD 均与 ledger 实际 pin 一致）。")
o.append("")
o.append("### 6.4 契约状态（原列为缺口，2026-11-23 认定为非缺口）")
o.append("")
o.append("- **adaptation-target：非缺口（契约未 exercised 区域）**。zj 2026-11-23 裁决：该字段名在横比契约中真实存在（`model-contract.md` / `cross_compare.py` CHK-06），CHK-06 仅在 adapted 条目**已存在**时校验其非空、无「必须四态齐全」断言；字段语义从未定义、属 Human 复核项、零 filled 实例——这是「未 exercised 的契约区域」，不是缺口。改判依据：上轮 Q4 已把「适配可用 / unsupported」判定权交母模型 `zj-open-source-capability-fit`（`FIT_OK` + `ALLOWED_ADAPT`/`FORBIDDEN_ADAPT`），横比只供 native/unknown 事实、不重复裁决（守 `CTX::zopn-no-adopt-verdict`）；母模型本身无 `adaptation-target` 字段，故「定义责任已转移」无落点，而是**该字段在两端都不参与判定**。adapted/unsupported 为空属预期。来源：2026-11-20 复用边界收敛 + 2026-11-23 zj 裁决。")
o.append("- **我方 EC 的 acceptance 未定**：§4.1 的 5 条 EC 是用户目标闭环、无验收判据；拆 R（定粒度/填 acceptance/跑 A B C D）仍属未来规划阶段。")
o.append("")
o.append("## 7. 一致性自检（机械）")
o.append("")
o.append(f"- 六维 {len(SIX_DIMS)} 项全部命中 charter §4；模块 {len(modules)} 项命中 pmap §2；场景 {len(scenes)} 项命中 bundle；Human 门 {len(GATE_SIX)} 方命中 human-gate-model。")
o.append(f"- 模块→场景映射覆盖全部 12 场景（13 模块中 M13 为例外）；unknown 合计 {unknown_total}，与 bundle difference-entries 一致。")
o.append(f"- 端到端维度 §4.1 含 {len(EC_LIST)} 条采纳 EC（+{len(EC_REJECTED)} 条否决留痕）、§4.2 含 {len(REF_FLOWS)} 家参考产品拓扑；全部由 zj 裁决常量表注入，每条引用 EVID 已通过 ledger 存在性校验（fail-closed），无手填 SHA。")
o.append(f"- 版本钉：{len(pin_deviations)} 条偏差的 ledger 实际 pin 均机械读取 `result.repositories[].revision.sha`（非手填）；multica bundle 记录失准已标注、展示按实值纠正。")
o.append("- adaptation-target 于 2026-11-23 改判为非缺口（契约未 exercised 区域），判定权归母模型；横比 bundle 原文未动（守 ratify 边界）。")
o.append("- 交叉区只标注不裁决；所有 SHAs 机械派生自 SoT，无手填。")
o.append(f"- 边界 alignment item 已于 2026-11-23 裁决为阶段性工作假设：{len(BOUNDARY_RULING['axes'])} 个正交轴，上界/起点分层，Q7a 重开条件与 Q8c 原则齐全；横比 CTX 原 statement 保留历史留痕未改写。")
if audit is not None:
    o.append(f"- 补采试点结论（§6.1）：机械命中 {audit['mechanical_hits']}/{audit['targeted_cells']}、语义合格 {audit['semantic_counts']['acceptable']}/{audit['targeted_cells']} 全部机械读自审计 JSON；每条 sealed ID 通过两仓 ledger 存在性校验（fail-closed），零手填；独立 ledger、未回灌 bundle。")
o.append("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o) + "\n")
print(f"wrote {OUT}")
print(f"modules={len(modules)} scenes={len(scenes)} dims={len(SIX_DIMS)} gates={len(GATE_SIX)} unknown={unknown_total} pin_dev={len(pin_deviations)} EC={len(EC_LIST)} rejected={len(EC_REJECTED)} ref_flows={len(REF_FLOWS)}")
if audit is not None:
    print(f"pilot: mechanical={audit['mechanical_hits']}/{audit['targeted_cells']} acceptable={audit['semantic_counts']['acceptable']} weak={audit['semantic_counts']['weak']} mismatched={audit['semantic_counts']['mismatched']}")
