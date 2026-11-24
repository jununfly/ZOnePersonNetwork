#!/usr/bin/env python3
"""Generate the EC-01 R-splitting scaffold: requirements-fit-matrix.md + mother-model input.

Design (zj 2026-11-24 grill, 4 rounds, all decisions explicit):
- Q1-Q5: anchor EC (not modules); bundle acceptance phrases are seeds calibrated by
  Human; three fit factors are Human judgment (Agent only prepares material); O selected
  dynamically per R from sealed-native projects; output is a new supporting page.
- Q6c/Q11a: split EC-01 by Human-observable acceptance nodes (NOT module boundaries).
  EC-01 -> R1.1..R1.4 with Human-calibrated acceptance (constant table below).
- Q7a: do not pre-seed M2/M3/M8 as D; fill factors from sealed facts, let the mother
  model independently re-check. (This round does not classify at all, so no verdict is
  pre-seeded anywhere.)
- Q8a: every R priority=must, critical=true.
- Q9b + Q12b(revised): cost dimension OUT of this round; run validate only (G1-G6),
  NEVER assess -> no A/B/C/D emitted; three fit factors are explicitly ANALYTICAL
  INITIAL VALUES pending zj calibration, derived from a documented tier rule keyed on
  the module-level reuse hypothesis in the sealed ledger (never hand-filled per cell).
- Q10a: EC-01 scaffold only; no commit; other 4 ECs deferred until sample reviewed.
- Q13a: candidates = multica + loop-now (both have sealed-native coverage on all four
  modules M1/M3/M4/M5 that EC-01 spans).
- zj 2026-11-24 review (a+b): (1) tier keyword matching is fail-closed — zero-hit or
  multi-hit hypotheses die, the doc's "unique tier rule" claim is now mechanically
  enforced; (2) a reuse-ledger row with >1 EVID dies (no implicit evids[0] luck);
  (3) CAPABILITY_FIT_PY overridable via env var for portability; (4) CALIBRATIONS is
  the ONLY entry point for zj's per-cell factor calibration — regenerating never
  overwrites it, calibrated cells keep tier provenance + by/rationale trail.

Fail-closed invariants (die before emitting anything):
- bundle has 12 scenes; EC-01 present in baseline §4.1; every R's module present in the
  reuse ledger; every (module, O) is native with a non-empty EVID for both candidates;
- every cited EVID exists in a sealed ledger (no hand-filled SHA/ID);
- each candidate version = ledger revision.sha, a real 40-hex, read mechanically;
- every module hypothesis matches exactly one documented FIT_TIER rule;
- all three fit factors in [0,1]; mother-model validate G1-G6 all green.
Deterministic: no timestamps, no hand-filled hashes, stable ordering.
"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BUNDLE = os.path.join(HERE, "bundle.json")
LEDGER_MD = os.path.join(REPO, "docs", "designs", "reuse-evidence-ledger.md")
BASELINE_MD = os.path.join(REPO, "docs", "designs", "product-structure-baseline.md")
COLLECT_DIR = os.path.join(HERE, "collect")
FIT_OUT = os.path.join(
    REPO, "tmp", "skills-outputs", "zj-open-source-capability-fit",
    "ec01-scaffold", "capability_fit_input.json",
)
DOC_OUT = os.path.join(REPO, "docs", "designs", "requirements-fit-matrix.md")
CAPABILITY_FIT_PY = os.environ.get("CAPABILITY_FIT_PY") or os.path.expanduser(
    "~/.workbuddy/skills/zj-open-source-capability-fit/scripts/capability_fit.py"
)

problems = []


def die(msg):
    problems.append(msg)


# ---------------------------------------------------------------------------
# Human rulings (zj 2026-11-24). DECISIONS, not derivations — explicit constant
# tables, each cross-checked against SoT below. No SHA/ID is ever hand-filled:
# EVID and versions are resolved mechanically from the sealed ledgers.
# ---------------------------------------------------------------------------
R_SPLIT = [
    {
        "id": "R1.1",
        "node": "目标提交后可见",
        "acceptance": "Human 提交目标后，能在列表看到对应 Work Item，其状态可读且能前进",
        "module": "M1",
    },
    {
        "id": "R1.2",
        "node": "执行进度可观察",
        "acceptance": "Human 能看到 Agent 已接收并在隔离边界内执行，进度/阻塞可见、互不污染",
        "module": "M5",
    },
    {
        "id": "R1.3",
        "node": "结果产物可复核",
        "acceptance": "Human 能看到本次产出，且来源/步骤可追溯",
        "module": "M4",
    },
    {
        "id": "R1.4",
        "node": "Human 门验收可审计",
        "acceptance": "Human 在门上 approve/reject，动作有账本、可审计",
        "module": "M3",
    },
]
CANDIDATES = ["multica", "loop-now"]

# Analytical initial values (Q12a) — NOT evidence, NOT final judgment. Keyed on the
# module-level reuse hypothesis text from the sealed ledger; applied uniformly to all
# O because the hypothesis is module-level (four-state native/unknown is the per-O fact).
FIT_TIERS = {
    "native_strong": (0.95, 0.90, 0.85),
    "adapted_contract": (0.85, 0.75, 0.70),
    "adapted_incompatible": (0.80, 0.55, 0.60),
    "must_selfbuild": (0.70, 0.45, 0.50),
}

# Keyword -> tier. Uniqueness is mechanically enforced by tier_for: zero-hit or
# multi-hit hypotheses die instead of silently taking if-chain priority.
TIER_KEYWORDS = [
    ("must_selfbuild", "必须自研"),
    ("adapted_incompatible", "互不相容"),
    ("adapted_contract", "明确契约"),
    ("native_strong", "native 偏多"),
]

# Calibration layer (zj 2026-11-24, review a+b): the ONLY entry point for human
# calibration of the three fit factors. Key = (rid, proj); value overrides the
# tier-derived initial factors for that cell. Regeneration NEVER overwrites entries
# here — the tier value stays as provenance, and the doc marks calibrated cells with
# the by/rationale trail. Editing the emitted doc/JSON by hand is futile: they are
# mechanically re-derived on every run. Empty dict = nothing calibrated yet.
CALIBRATIONS = {
    # "R1.4": {
    #     "multica": {
    #         "coverage": 0.60, "semantic_match": 0.40, "composability": 0.50,
    #         "by": "zj", "rationale": "…为何与 must_selfbuild 档位初值不同…",
    #     },
    # },
}


def tier_for(hypothesis):
    """Map a module-level reuse hypothesis to exactly one documented tier.

    Fail-closed on ambiguity: returns (tier, None) on a unique hit, else
    (None, reason). The caller dies on reason — no silent if-chain priority.
    """
    hits = [name for name, kw in TIER_KEYWORDS if kw in hypothesis]
    if len(hits) == 1:
        return hits[0], None
    if len(hits) == 0:
        return None, f"hypothesis matches no tier keyword: {hypothesis[:80]}"
    return None, f"hypothesis matches {len(hits)} tier keywords {hits} — ambiguous, refuse: {hypothesis[:60]}"


def calibrated_factors(rid, proj):
    """Return (factors_dict_or_None, error). Validates the CALIBRATIONS entry."""
    cal = CALIBRATIONS.get(rid, {}).get(proj)
    if cal is None:
        return None, None
    missing = [k for k in ("coverage", "semantic_match", "composability") if k not in cal]
    if missing:
        return None, f"CALIBRATIONS[{rid}][{proj}] missing factors: {missing}"
    bad = [k for k in ("coverage", "semantic_match", "composability")
           if not isinstance(cal[k], (int, float)) or not 0.0 <= cal[k] <= 1.0]
    if bad:
        return None, f"CALIBRATIONS[{rid}][{proj}] factors out of [0,1] or non-numeric: {bad}"
    return cal, None


# ---------------------------------------------------------------------------
# SoT 1: bundle (scene set must be the ratified 12)
# ---------------------------------------------------------------------------
b = json.load(open(BUNDLE, encoding="utf-8"))
scenes = {s["id"] for s in b["scene-set"]["scenes"]}
if len(scenes) != 12:
    die(f"expected 12 ratified scenes, got {len(scenes)}")
for g in b["graphs"]:
    if g["project"] in CANDIDATES:
        for need in ("version-pin", "nodes"):
            if not g.get(need):
                die(f"bundle graph {g['project']} missing {need}")

# ---------------------------------------------------------------------------
# SoT 2: baseline — EC-01 must exist and span the modules the R split uses
# ---------------------------------------------------------------------------
baseline = open(BASELINE_MD, encoding="utf-8").read()
if "EC-01" not in baseline or "提交目标" not in baseline:
    die("baseline §4.1 EC-01 definition not found")
expected_modules = {"M1", "M5", "M4", "M3"}
if {r["module"] for r in R_SPLIT} != expected_modules:
    die("R_SPLIT modules must be exactly M1/M5/M4/M3 (EC-01 chain)")
if len({r["id"] for r in R_SPLIT}) != len(R_SPLIT):
    die("duplicate R id in R_SPLIT")

# ---------------------------------------------------------------------------
# SoT 3: reuse ledger — parse (module, project) -> (verdict, evid list, hypothesis)
# ---------------------------------------------------------------------------
ledger_md = open(LEDGER_MD, encoding="utf-8").read()
rows = {}
hypothesis_by_module = {}
for line in ledger_md.splitlines():
    m = re.match(r"^\|\s*(M\d+)\s*\|", line)
    if not m:
        continue
    cols = [c.strip() for c in line.split("|")]
    # cols: ['', module, criterion_id, 模块, 项目, pin, verdict, evidence_refs, hypothesis, ...]
    mid, proj, verdict = cols[1], cols[4], cols[6]
    evid_raw = cols[7]
    hyp = cols[8]
    evids = re.findall(r"EVID::([0-9a-f]{24})", evid_raw)
    rows[(mid, proj)] = {"verdict": verdict, "evids": evids}
    if mid in expected_modules:
        hypothesis_by_module[mid] = hyp

for mid in expected_modules:
    if mid not in hypothesis_by_module:
        die(f"module {mid} missing from reuse ledger")

# ---------------------------------------------------------------------------
# SoT 4: sealed ledger index (EVID existence) + candidate version (real 40-hex)
# ---------------------------------------------------------------------------
import glob as _glob

evid_index = {}
REASEARCH_DIR = os.path.join(REPO, "docs", "reasearch")
for _f in _glob.glob(os.path.join(REASEARCH_DIR, "**", "collect", "ledger-*.json"), recursive=True) \
        + _glob.glob(os.path.join(REASEARCH_DIR, "**", "*ledger-response*.json"), recursive=True):
    try:
        _d = json.load(open(_f, encoding="utf-8"))
    except Exception:
        continue

    def _walk(o):
        if isinstance(o, dict):
            eid = o.get("id") or o.get("sealedId") or o.get("sealed_id")
            txt = o.get("excerpt") or o.get("text") or o.get("statement") or o.get("content")
            if eid and txt and isinstance(eid, str):
                evid_index.setdefault(str(eid)[:24], os.path.basename(_f))
            for v in o.values():
                _walk(v)
        elif isinstance(o, list):
            for v in o:
                _walk(v)

    _walk(_d)

version_by_proj = {}
for proj in CANDIDATES:
    lf = os.path.join(COLLECT_DIR, f"ledger-{proj}.json")
    if not os.path.exists(lf):
        die(f"missing sealed ledger for candidate {proj}: {lf}")
        continue
    ld = json.load(open(lf, encoding="utf-8"))
    repos = ld.get("result", {}).get("repositories", [])
    if len(repos) != 1:
        die(f"candidate {proj}: expected 1 repository, got {len(repos)}")
        continue
    sha = repos[0].get("revision", {}).get("sha", "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        die(f"candidate {proj}: invalid revision.sha {sha!r}")
        continue
    version_by_proj[proj] = sha

# ---------------------------------------------------------------------------
# Build the fit matrix: R x O. Every cell must be native + EVID; factors from tier.
# ---------------------------------------------------------------------------
requirements = []
matrix = {}
fit_provenance = {}  # (rid, proj) -> (tier, hypothesis)

for r in R_SPLIT:
    rid, mid = r["id"], r["module"]
    requirements.append({
        "id": rid,
        "statement": f"{r['node']}（{mid}，EC-01 主闭环验收节点）",
        "priority": "must",
        "critical": True,
        "acceptance": r["acceptance"],
    })
    hyp = hypothesis_by_module[mid]
    tier, tier_err = tier_for(hyp)
    if tier is None:
        die(f"module {mid}: {tier_err}")
        continue
    for proj in CANDIDATES:
        row = rows.get((mid, proj))
        if row is None:
            die(f"reuse ledger missing ({mid}, {proj})")
            continue
        if row["verdict"] != "native" or not row["evids"]:
            die(f"({mid}, {proj}) not sealed-native with EVID: verdict={row['verdict']} evids={row['evids']}")
            continue
        if len(row["evids"]) > 1:
            die(f"({mid}, {proj}) row carries {len(row['evids'])} EVIDs {row['evids']} — "
                f"explicit semantic selection required, no implicit evids[0]")
        eid = row["evids"][0]
        if eid not in evid_index:
            die(f"EVID::{eid} (R={rid}, O={proj}) not found in any sealed ledger — refuse (no hand-filled ID)")
            continue
        cal, cal_err = calibrated_factors(rid, proj)
        if cal_err:
            die(cal_err)
            continue
        # Start from the tier-derived initial values EVERY iteration — a previous
        # proj's calibration must never leak into this cell (T3-caught bug).
        cov, sem, comp = FIT_TIERS[tier]
        if cal:
            cov, sem, comp = cal["coverage"], cal["semantic_match"], cal["composability"]
            notes = (
                f"zj 已校准（by {cal.get('by', 'zj')}）：{cal.get('rationale', '(无 rationale)')}；"
                f"档位 {tier} 初值仅作 provenance。"
                "status=native 仅表示能力存在的 sealed 事实，三因子表示与我方需求的语义/组合拟合，二者语义不同。"
            )
        else:
            notes = (
                f"分析初值·待 zj 校准；档位={tier}；依据模块级 hypothesis：{hyp[:70]}。"
                "status=native 仅表示能力存在的 sealed 事实，三因子表示与我方需求的语义/组合拟合初值，二者语义不同。"
            )
        matrix.setdefault(proj, {})[rid] = {
            "coverage": cov,
            "semantic_match": sem,
            "composability": comp,
            "status": "native",
            "evidence": f"EVID::{eid}",
            "notes": notes,
        }
        fit_provenance[(rid, proj)] = (tier, hyp, bool(cal))

if problems:
    print("FAIL (join invariants):", file=sys.stderr)
    for p in problems:
        print("  -", p, file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Load the mother-model instrument and compute gates mechanically (validate only).
# ---------------------------------------------------------------------------
if not os.path.exists(CAPABILITY_FIT_PY):
    die(f"mother-model instrument not found: {CAPABILITY_FIT_PY}")
    print("FAIL:", problems, file=sys.stderr)
    sys.exit(1)
spec = importlib.util.spec_from_file_location("capability_fit", CAPABILITY_FIT_PY)
cf = importlib.util.module_from_spec(spec)
# Python 3.13: @dataclass resolves its module via sys.modules during exec; without
# registering first, dataclasses._is_type hits None.__dict__. Register before exec.
sys.modules[spec.name] = cf
spec.loader.exec_module(cf)

fit_input = {
    "goal": "EC-01 主闭环（提交目标→拿到可验收结果）拆出的 4 条可独立验收需求 R1.1–R1.4 的开源能力拟合事实矩阵",
    "requirements": requirements,
    "candidates": [
        {
            "id": proj,
            "name": proj,
            "url": "(not present in sealed SoT; non-gated field)",
            "version": version_by_proj[proj],
            "license": "(not collected; non-gated field)",
        }
        for proj in CANDIDATES
    ],
    "matrix": matrix,
    "cost": {proj: {k: 0 for k in (
        "initial_dev", "integration", "maintenance", "upstream_adapt", "ops", "security_gov"
    )} for proj in CANDIDATES},
    "adaptation": {proj: {"scope": [], "mode": "", "responsibility_uncontrolled": False,
                          "poc_plan": ""} for proj in CANDIDATES},
    "poc_plan": "",
}

gate_results = {proj: cf.run_gates(fit_input, proj) for proj in CANDIDATES}
for proj, gates in gate_results.items():
    for g in gates:
        if not g.ok:
            die(f"mother-model validate GATE FAIL for {proj}: {g.name}: {g.message}")
if problems:
    print("FAIL (mother-model validate):", file=sys.stderr)
    for p in problems:
        print("  -", p, file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Emit mother-model input JSON (deterministic).
# ---------------------------------------------------------------------------
os.makedirs(os.path.dirname(FIT_OUT), exist_ok=True)
with open(FIT_OUT, "w", encoding="utf-8") as f:
    json.dump(fit_input, f, ensure_ascii=False, indent=2)
    f.write("\n")

# ---------------------------------------------------------------------------
# Emit supporting doc page.
# ---------------------------------------------------------------------------
def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


o = []
o.append("---")
o.append("doc-kind: reference")
o.append("authority: supporting")
o.append("authority-id: opn.requirements-fit-matrix")
o.append("---")
o.append("")
o.append("# 需求拟合矩阵 · EC-01 样板（supporting / 从基线拆 R）")
o.append("")
o.append("> 本页是 **EC-01 拆 R 的样板**，只覆盖一条端到端能力（EC-01 主闭环），不是完整 R 清单、不是产品计划、不是采用裁决。")
o.append("> 由 `docs/reasearch/opn-cross-comparison/_gen_fit_matrix.py` 从横比 bundle / 复用证据账本 / 产品结构基线机械派生；")
o.append("> Human 决策（Q1–Q13）以带 SoT 存在性校验的显式常量表注入，Agent 不推断验收判据、不预置分类。")
o.append("")

o.append("## 1. 边界与口径（zj 2026-11-24 grill Q1–Q13 锁定）")
o.append("")
o.append("- **产物范围**：只做 EC-01 样板（Q10a）；其余 4 条 EC 待样板验收后铺开。本轮不 commit。")
o.append("- **R 锚点**：锚 EC（Q1a），按 **Human 可独立观察的验收节点**切（Q6c/Q11a），不贴模块边界；模块只作归属标注。")
o.append("- **acceptance**：bundle 的 acceptance 是场景级、跨项目机械重复的通用短语，只当种子，由 Human 逐条校准（Q2a）；下表 acceptance 即校准结果。")
o.append("- **三拟合因子**：Q3a 定为 Human 判断、Agent 只整理材料。本样板中的三因子是**分析初值、待 zj 逐格校准（Q12a）**，由可追溯档位规则从账本模块级 hypothesis 机械派生（见 §4），**不是 evidence、不是最终判断**。")
o.append("- **校准唯一入口**：生成器 `_gen_fit_matrix.py` 的 `CALIBRATIONS` 常量表（键 (R,O)，逐格覆盖三因子，含 `by`/`rationale` 留痕；档位初值保留作 provenance）。本页与母模型 JSON 均由重跑机械再生成——**手工改文档/JSON 会被覆盖**，校准只认常量表。")
o.append("- **status 口径**：横比 native → 母模型 native；unknown → unknown；adapted/unsupported 留给母模型判（守 `CTX::zopn-no-adopt-verdict`，符合上轮 adaptation-target 非缺口改判）。")
o.append("- **M2/M3/M8**：Q7a 不预置为 D——照常填因子、让母模型独立复核；本轮更不出任何分类，故无结论被预置。")
o.append("- **priority/critical**：全部 R=`must` + `critical=true`（Q8a，无优先级信号时不臆断）。")
o.append("- **成本维度**：整体不进本轮（Q9b）。只跑 `validate`（G1–G6），**不跑 `assess`，不出 A/B/C/D**；`cost` 保留模板默认 0，不作为分类依据。")
o.append("- **候选 O**：multica + loop-now（Q13a）——EC-01 覆盖的 M1/M3/M4/M5 四模块上两家均有 sealed native；版本用各自 sealed ledger 的 `revision.sha`（非 bundle 中已失准的记录值）。")
o.append("- **URL/license**：sealed SoT 未采集，填占位；两者非 validate 闸门字段，不影响本轮结论。")
o.append("")

o.append("## 2. R 清单（EC-01 按验收节点拆分 · 4 条）")
o.append("")
o.append("| R | 验收节点（Human 可观察） | acceptance（Human 校准） | 归属模块 | priority | critical |")
o.append("|---|---|---|---|---|---|")
for r in R_SPLIT:
    o.append(f"| {r['id']} | {esc(r['node'])} | {esc(r['acceptance'])} | {r['module']} | must | true |")
o.append("")
o.append("> 起始 EC-01：起点「Human 提交目标/创建 Work Item」、终点「Human 在 Human 门看到结果并验收完成」，跨 M1→M5→M4→M3（M2 身份 scope 横切，已在基线 §4.1）；此处按 Human 可观察节点切成 4 条独立可验收需求。")
o.append("")

o.append("## 3. 候选 O（按 R 动态选取 · 2 家）")
o.append("")
o.append("| 候选 O | 版本（sealed ledger 实值） | 来源 ledger | URL | license |")
o.append("|---|---|---|---|---|")
for proj in CANDIDATES:
    o.append(f"| {proj} | `{version_by_proj[proj]}` | `collect/ledger-{proj}.json` | (sealed SoT 未采集) | (未采集) |")
o.append("")

o.append("## 4. R×O 拟合矩阵（分析初值 · 待 zj 校准）")
o.append("")
o.append("| R | O | status | coverage | semantic_match | composability | effective_fit | evidence | 档位 |")
o.append("|---|---|---|---|---|---|---|---|---|")
for r in R_SPLIT:
    rid = r["id"]
    for proj in CANDIDATES:
        cell = matrix[proj][rid]
        tier, _hyp, calibrated = fit_provenance[(rid, proj)]
        ef = cell["coverage"] * cell["semantic_match"] * cell["composability"]
        tier_label = f"{tier}→zj校准" if calibrated else tier
        o.append(
            f"| {rid} | {proj} | {cell['status']} | {cell['coverage']:.2f} "
            f"| {cell['semantic_match']:.2f} | {cell['composability']:.2f} | {ef:.3f} "
            f"| {cell['evidence']} | {tier_label} |"
        )
o.append("")
o.append("### 档位规则（三因子的唯一来源，可追溯、非手填）")
o.append("")
o.append("| 档位 | coverage | semantic_match | composability | 触发条件（账本模块级 hypothesis 文本） |")
o.append("|---|---|---|---|---|")
o.append("| native_strong | 0.95 | 0.90 | 0.85 | hypothesis 含「native 偏多」 |")
o.append("| adapted_contract | 0.85 | 0.75 | 0.70 | hypothesis 含「明确契约」 |")
o.append("| adapted_incompatible | 0.80 | 0.55 | 0.60 | hypothesis 含「互不相容」 |")
o.append("| must_selfbuild | 0.70 | 0.45 | 0.50 | hypothesis 含「必须自研」 |")
o.append("")
o.append("> 三因子按模块级 hypothesis 归一应用到该模块的所有 O（hypothesis 是模块级 assumption；四态 native/unknown 才是逐 O 事实）；档位列带「→zj校准」的格以 `CALIBRATIONS` 常量表实值为准、档位值仅作 provenance。`effective_fit = coverage × semantic_match × composability`，此处仅展示、不参与任何分类（本轮不跑 assess）。")
o.append("")

o.append("## 5. validate 闸门结果（G1–G6 · 不出分类）")
o.append("")
o.append("| 候选 O | 闸门 | 结果 | 说明 |")
o.append("|---|---|---|---|")
for proj in CANDIDATES:
    for g in gate_results[proj]:
        o.append(f"| {proj} | {esc(g.name)} | {'✓ PASS' if g.ok else '✗ FAIL'} | {esc(g.message)} |")
o.append("")
o.append(f"- 母模型输入 JSON：`tmp/skills-outputs/zj-open-source-capability-fit/ec01-scaffold/capability_fit_input.json`（相对仓库根）。")
o.append("- **本轮只调用 `validate`**；`assess` 未调用，`cost` 全 0 不参与结论，**没有产出 A/B/C/D**。闸门全绿仅表示矩阵结构与证据形式合规，不代表采用建议。")
o.append("- 关键缺口检测、适配层范围校验、E 阈值比较全部属于 `assess`，本轮有意不触发（Q9b）。")
o.append("")

o.append("## 6. 缺口与待校准清单")
o.append("")
o.append("- **三因子待 zj 逐格校准**：当前为档位派生的分析初值，不是最终判断；校准落点 = 生成器 `CALIBRATIONS` 常量表（见 §1「校准唯一入口」），校准后重跑本生成器，再跑 `assess`。")
o.append("- **其余 4 条 EC 未铺开**：EC-02/03/05/06 待本样板验收后按同一模式拆 R。")
o.append("- **成本/E 维度未测算**：A/B/C/D 留到成本数据可得时再跑（Q9b），当前强行分类会是假精确。")
o.append("- **83 个 unknown 未纳入本样板**：Q13a 只选 sealed-native 覆盖充分的 O；unknown 证据缺口仍在基线 §6 与账本中，不被本矩阵掩盖。")
o.append("- **M3 Human 门语义冲突**：四种表达互不兼容（基线 §5），R1.4 的因子已按「必须自研」档位给低初值，但语义裁决仍归后续规划阶段，本页不裁决。")
o.append("")

o.append("## 7. 机械自检")
o.append("")
o.append(f"- R 数 {len(R_SPLIT)}（=4）；O 数 {len(CANDIDATES)}（=2）；矩阵单元 {sum(len(v) for v in matrix.values())}（=8），每单元 status=native 且 evidence 指向 sealed EVID。")
o.append("- 每个 cited EVID 均在 sealed ledger 索引中存在（fail-closed 校验通过）；两候选 version 均为 ledger 实读 40-hex，非手填。")
o.append("- 每个模块的 hypothesis 唯一命中档位规则（零命中/多重命中 fail-closed 拒绝生成）；三因子（含已校准格）均在 [0,1]；reuse ledger 行内多 EVID 时拒绝生成（不隐式取第一个）；validate G1–G6 全部 PASS。")
o.append("- 本页 supporting；derived-from: opn.product-structure-baseline / opn.reuse-evidence-ledger / opn.module-matrix；不改写 ratify bundle。")
o.append("")

with open(DOC_OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o) + "\n")

print(f"wrote {DOC_OUT}")
print(f"wrote {FIT_OUT}")
print(f"R={len(R_SPLIT)} O={len(CANDIDATES)} cells={sum(len(v) for v in matrix.values())} "
      f"gates={sum(len(v) for v in gate_results.values())} all_pass=True")
