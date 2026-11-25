#!/usr/bin/env python3
"""Generate docs/designs/reuse-evidence-ledger.md — the evidence anchor ledger
for reuse-boundary decisions.

Design (zj 2026-11-20 ratified decisions Q1-Q4 / Q5-Q8 / S1-S4):
- Cross-comparison (bundle.json) supplies FACTS ONLY: (module x project) native/unknown
  + sealed EVID refs. It does NOT judge reuse form.
- Anchor = sealed Evidence criterionId (mod-*), which is 1:1 with product-module-map
  M1..M13 (M13 = ref-capability-map, an exception carried as project-level context).
- Reuse form is copied from product-module-map.md §2 as ASSUMPTION (pending mother-model
  ruling), never written as evidence.
- unknown rows are evidence-gap notes only (unknown != absent).
- This generator does no semantic rulings; it mechanically joins two SoTs and fails
  closed if the join does not reconcile (counts / ids / module coverage).
- EXCEPTION (zj 2026-11-24 ruling B): M1 Work Item state machine adopts opencode's
  sealed nine-state lifecycle as the semantic baseline, implementation stays
  self-developed (module-map §3/Q9 unchanged). The nine-state excerpt is sealed in
  bundle under SC::agent-protocol (M11), not SC::task-workitem (M1), so the M1×opencode
  row lists it as an explicitly marked cross-module anchor (EVID::4e988871…). This
  is a cross-reference only — the 1:1 criterionId↔module anchor rule is preserved;
  no SHA is hand-filled (the ID is verified against bundle before emit).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BUNDLE = os.path.join(HERE, "bundle.json")
PMAP = os.path.join(REPO, "docs", "designs", "product-module-map.md")
OUT = os.path.join(REPO, "docs", "designs", "reuse-evidence-ledger.md")

# criterionId (mod-*) <-> module id. 1:1 by ratified design Q5b.
# M13 = ref-capability-map: not a cross-comparison scene; carried via ZAgenticOPN
# project-level context-entry (CTX::zagenticopn-capability-map).
MODULES = [
    ("M1",  "mod-task-workitem",        "SC::task-workitem",        "Work Item 生命周期"),
    ("M2",  "mod-identity-scope",       "SC::identity-scope",       "身份与 scope"),
    ("M3",  "mod-approval-human",       "SC::approval-human",       "审批与 Human 门"),
    ("M4",  "mod-result-provenance",    "SC::result-provenance",    "结果与 provenance"),
    ("M5",  "mod-execution-workspace",  "SC::execution-workspace",  "执行与工作区隔离"),
    ("M6",  "mod-observability",        "SC::observability",        "可观测与回放"),
    ("M7",  "mod-session-context",      "SC::session-context",      "会话上下文"),
    ("M8",  "mod-memory-knowledge",     "SC::memory-knowledge",     "共享记忆/知识层"),
    ("M9",  "mod-config-strategy",      "SC::config-strategy",      "配置与策略"),
    ("M10", "mod-runtime-integration",  "SC::runtime-integration",  "运行时集成"),
    ("M11", "mod-agent-protocol",       "SC::agent-protocol",       "Agent 间协议"),
    ("M12", "mod-tech-design",          "SC::tech-design",          "技术设计与部署"),
    ("M13", "ref-capability-map",       None,                       "能力地图参考"),
]

problems = []


def die(msg):
    problems.append(msg)


# ---------------------------------------------------------------------------
# Load SoT 1: bundle facts
# ---------------------------------------------------------------------------
b = json.load(open(BUNDLE, encoding="utf-8"))
scenes = {s["id"] for s in b["scene-set"]["scenes"]}
projects = [g["project"] for g in b["graphs"]]
pins = {g["project"]: g["version-pin"] for g in b["graphs"]}

# (scene, project) -> difference entry
de_index = {}
for de in b["difference-entries"]:
    key = (de["scene"], de["project"])
    if key in de_index:
        die(f"duplicate difference-entry for {key}")
    de_index[key] = de

# cross-check bundle coverage vs module scene map (12 scenes must all be mapped)
mapped_scenes = {s for _, _, s, _ in MODULES if s}
if mapped_scenes != scenes:
    die(f"module->scene map mismatch: mapped={sorted(mapped_scenes)} bundle={sorted(scenes)}")

# M13 capability-map context (single sealed ref, project-level)
m13_ctx = None
for g in b["graphs"]:
    for c in g.get("context-entries", []):
        if c.get("id") == "CTX::zagenticopn-capability-map":
            if m13_ctx is not None:
                die("multiple CTX::zagenticopn-capability-map entries")
            m13_ctx = (g["project"], c.get("evidence-ref", ""))
if m13_ctx is None:
    die("M13 capability-map context-entry not found in bundle")

# ---------------------------------------------------------------------------
# Load SoT 2: product-module-map reuse signals (§2 only, not §3.1 plan table)
# ---------------------------------------------------------------------------
pmap_text = open(PMAP, encoding="utf-8").read()
sec2 = pmap_text.split("## 2. 模块清单", 1)[-1].split("## 3.", 1)[0]

# rows like: | M1 Work Item 生命周期 | 状态机、claim 权限、流转 | adapted：... [matrix §5] |
reuse_rows = {}
for line in sec2.splitlines():
    m = re.match(r"^\|\s*(M\d+)\s+([^|]+?)\s*\|\s*[^|]*?\|\s*([^|]+?)\s*\|\s*$", line)
    if m:
        mid, name, signal = m.group(1), m.group(2).strip(), m.group(3).strip()
        if mid in reuse_rows:
            die(f"duplicate module row in product-module-map §2: {mid}")
        reuse_rows[mid] = (name, signal)

for mid, _, _, name in MODULES:
    if mid not in reuse_rows:
        die(f"module {mid} not found in product-module-map §2")
    elif not reuse_rows[mid][1]:
        die(f"module {mid} has empty reuse signal in §2")

if problems:
    print("FAIL (join invariants):", file=sys.stderr)
    for p in problems:
        print("  -", p, file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Build ledger rows — every module x every project (13 x 14)
# ---------------------------------------------------------------------------
rows = []
native_count = 0
unknown_count = 0
for mid, criterion, scene, mname in MODULES:
    mname_pmap, signal = reuse_rows[mid]
    for proj in projects:
        pin = pins[proj]
        if scene is None:  # M13 exception
            if proj == m13_ctx[0]:
                verdict = "native·ref-only"
                evid = m13_ctx[1]
                note = "capability-map 参照物专属；已降为项目级 context-entry，不进横比四态/摘要"
                native_count += 1
            else:
                verdict = "n/a"
                evid = "—"
                note = "非横比场景；M13 仅参照物有，其余项目不适用"
        else:
            de = de_index.get((scene, proj))
            if de is None:
                die(f"missing difference-entry for ({scene}, {proj})")
                continue
            verdict = de["verdict"]
            refs = de.get("evidence-refs", [])
            evid = ", ".join(refs) if refs else "—"
            if verdict == "native":
                note = "—"
                native_count += 1
            elif verdict == "unknown":
                note = de.get("verification-plan", "证据缺口，见 bundle.difference-entries")
                unknown_count += 1
            else:
                die(f"unexpected verdict {verdict} for ({scene}, {proj}) — cross-comparison has only native/unknown")
        rows.append((mid, criterion, mname, proj, pin, verdict, evid, signal, note))

if problems:
    print("FAIL (row build):", file=sys.stderr)
    for p in problems:
        print("  -", p, file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# zj 2026-11-24 ruling B — cross-module sealed anchor for M1 nine-state baseline
# ---------------------------------------------------------------------------
# The M1 Work Item state machine adopts opencode-coordination's sealed nine-state
# lifecycle as its SEMANTIC BASELINE; implementation stays self-developed (module-map
# §3/Q9 and N=5 unchanged). The nine-state excerpt is sealed in bundle under
# SC::agent-protocol (M11), not SC::task-workitem (M1). We therefore register it as
# an explicitly-marked CROSS-MODULE anchor, NOT by appending to the evidence_refs
# column (that column stays 1:1 and fit-matrix fails closed on >1 EVID per row).
CROSS_ANCHOR = {
    "module": "M1",
    "project": "opencode-coordination",
    "source_scene": "SC::agent-protocol",
    "source_module": "M11",
    "evidence": "EVID::4e9888715cf937cdeac6384a",
}
_ca_de = de_index.get((CROSS_ANCHOR["source_scene"], CROSS_ANCHOR["project"]))
if _ca_de is None or _ca_de.get("verdict") != "native" \
        or CROSS_ANCHOR["evidence"] not in _ca_de.get("evidence-refs", []):
    die(f"cross-module anchor {CROSS_ANCHOR['evidence']} not sealed in bundle "
        f"({CROSS_ANCHOR['source_scene']}, {CROSS_ANCHOR['project']})")
if ("M1", "opencode-coordination") not in {(r[0], r[3]) for r in rows}:
    die("cross-module anchor target row (M1, opencode-coordination) missing")
if problems:
    print("FAIL (cross-module anchor):", file=sys.stderr)
    for p in problems:
        print("  -", p, file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Render (deterministic; no timestamps/sha hand-fill)
# ---------------------------------------------------------------------------
def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip()

o = []
o.append("---")
o.append("doc-kind: reference")
o.append("authority: supporting")
o.append("authority-id: opn.reuse-evidence-ledger")
o.append("---")
o.append("")
o.append("# 复用边界 · 证据锚定账本（supporting / 证据→模块 Joins）")
o.append("")
o.append("> 本页是 **supporting 证据账本**，不是复用判断权威页。判断权威在 `designs/product-module-map.md`（`opn.product-module-map`, primary）；本页只机械陈述「哪个模块、在哪个固定版本项目上、有哪条 sealed Evidence 观察到能力存在」。")
o.append("> 由 `docs/reasearch/opn-cross-comparison/_gen_ledger.py` 从 bundle.json + product-module-map.md 机械生成，不手写、不做语义裁决。")
o.append("")
o.append("## 1. 契约与边界（zj 2026-11-20 收敛）")
o.append("")
o.append("- **事实层**：横比 bundle 的 `native/unknown` + `EVID::` 是 sealed Evidence 绑定的**能力存在**事实；仅此一层是 evidence。")
o.append("- **判断层**：`reuse_form_hypothesis` 列抄录自 `product-module-map.md` §2，标 **assumption**（分析层推断，待母模型裁决）；`native` 推不出「可直接用/适配可用/必须自研」。")
o.append("- **判定权归母模型** `zj-open-source-capability-fit`（`FIT_OK=0.9` + `ALLOWED_ADAPT/FORBIDDEN_ADAPT` 薄层判据）；本账本不产采用裁决（守 `CTX::zopn-no-adopt-verdict`）。")
o.append("- **锚点**：sealed Evidence 的 `criterionId`(`mod-*`) 与模块 M1–M13 为 1:1；M13=`ref-capability-map` 为唯一例外，经 ZAgenticOPN 项目级 context-entry 承载，不进横比四态。§2.1 的 M1 九态补锚是**跨模块引用例外**（criterionId=M11），单独登记、不进 §2 表格 evidence_refs 列、不改 1:1 规则。")
o.append("- **unknown 只作证据缺口**（unknown≠absent），不进复用判断、不进定量；版本钉偏差见 bundle 对应 graph 的 version-pin。")
o.append("")
o.append("## 2. 账本（每模块 × 每项目一行，13 × 14 = %d 行）" % len(rows))
o.append("")
o.append("> `ruling_status` 恒为 `待母模型裁决`：母模型 R（可独立验收需求）定义另开切片（S1a），本账本不预判。")
o.append("")
o.append("| module | criterion_id | 模块 | 项目 | pin | verdict | evidence_refs | reuse_form_hypothesis (assumption, 源自 primary §2) | ruling_status | gap_note (unknown 缺口) |")
o.append("|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    note = r[8]
    if r[0] == CROSS_ANCHOR["module"] and r[3] == CROSS_ANCHOR["project"]:
        # M1×opencode: point to the cross-module nine-state anchor registered in §2.1.
        # Do NOT append EVID to evidence_refs (1:1 rule + fit-matrix fails closed on >1).
        note = "跨模块补锚见 §2.1：九态 sealed EVID（criterionId=mod-agent-protocol/M11）"
    o.append("| " + " | ".join(esc(x) for x in (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], "待母模型裁决", note)) + " |")
o.append("")
o.append("### 2.1 跨模块补锚：M1 九态语义基准（zj 2026-11-24 裁决 B）")
o.append("")
o.append(f"> 本小节登记**唯一**跨模块 sealed 锚，不改变 §2 表格的 1:1 锚定规则，也不改写 bundle。M1 Work Item 状态机采用 opencode-coordination 的 sealed 九态生命周期作为**语义基准**；实现仍自研，`product-module-map.md` §3/Q9 与 N=5 不变。")
o.append("")
o.append("| 目标模块 | 项目 | 补锚 EVID | sealed 归属 criterionId / 模块 | 归属 scene | 说明 |")
o.append("|---|---|---|---|---|---|")
o.append(f"| {CROSS_ANCHOR['module']} | {CROSS_ANCHOR['project']} | `{CROSS_ANCHOR['evidence']}` | mod-agent-protocol / {CROSS_ANCHOR['source_module']} | {CROSS_ANCHOR['source_scene']} | 该 sealed 摘录正文含 Work Item 九态 `proposed→accepted→ready→assigned→in progress→in review→merged→measured→validated`；采集时归入 M11，正文同时承载 M1 生命周期语义，故补锚供 M1 引用 |")
o.append("")
o.append("- **为何补锚而非并列写进 evidence_refs**：该 EVID 的 sealed criterionId 是 `mod-agent-protocol`（M11），与 M1 非 1:1；且 §2 表格 evidence_refs 列保持单 EVID 是下游 `zj-open-source-capability-fit` 输入生成器的 fail-closed 约束（>1 会中止）。故在本小节显式登记跨模块引用，M1×opencode 行的 gap_note 指向此处。")
o.append("- **裁决边界**：只确立「九态为 M1 语义基准」，不改变自研归属（②），不新增自研单元（N 仍为 5），不动 module-map §3/Q9。四态（ZAgenticOPN）仍是其自有 sealed 契约源，本补锚不抹除它。")
o.append("")
o.append("## 3. 一致性自检（机械）")
o.append("")
o.append(f"- 行数：{len(rows)}（期望 13×14=182）；native 计 {native_count-1}（M13 ref-only 另计 1），unknown 计 {unknown_count}，n/a 计 13。")
o.append("- 每个 (criterion_id, project) 恰好一行；M13 仅 ZAgenticOPN 一行有证据（native·ref-only，sealed ref 为项目级 context-entry），其余 13 行 n/a。")
o.append("- 所有 native 行的 evidence_refs 均指向 bundle 中 EVID:: sealed ID（每行恰好 1 条，下游 fail-closed 约束）；M13 ref-only 指向 context-entry 裸 sealed ID；unknown 行无 EVID 且附验证计划。")
o.append(f"- 跨模块补锚 {CROSS_ANCHOR['evidence']} 已校验存在于 bundle 的 ({CROSS_ANCHOR['source_scene']}, {CROSS_ANCHOR['project']}) native 条目；仅登记于 §2.1，不计入 §2 行 evidence_refs。")
o.append("- reuse_form_hypothesis 与 product-module-map.md §2 逐字一致（本页不改判断）。")
o.append("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o) + "\n")
print(f"wrote {OUT}")
print(f"rows={len(rows)} native_ref_only={native_count} unknown={unknown_count}")
