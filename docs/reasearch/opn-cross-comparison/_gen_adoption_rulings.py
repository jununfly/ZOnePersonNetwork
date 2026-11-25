#!/usr/bin/env python3
"""Generate adoption-rulings.md (supporting) from 16 EC×O rulings.

zj ruling (2026-11-25, planning-execution stage):
- Granularity: 16 EC×O pairs, one ruling each (not per-candidate, not per-scenario).
- Value domain: A/B1/B2/B3/C/D — the mother-model classify_candidate vocabulary.
- Stance: 确认 (ruling == reference signal) or 推翻 (ruling != reference signal,
  rationale mandatory). This pass: 16 确认 / 0 推翻.
- Module-level alignment: M3 (Human gate semantics self-built) and M8 (memory
  boundary self-built) rulings survive; adapter/plugin only carries trigger or
  storage, not the module-level semantics.

Fail-closed: reference signals parsed from requirements-fit-matrix §5.3.3
(derived, never hand-filled); EVIDs read from per-EC fit-input JSON; every cited
EVID checked against the sealed-ledger index; coverage exactly 16 cells; ruling
vocabulary closed; stance/rule agreement; deterministic, no timestamps.
No hand-filled SHA/EVID. Ratify bundle and fit-matrix are never modified.
"""
import glob as _glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FIT_MD = os.path.join(REPO, "docs", "designs", "requirements-fit-matrix.md")
FIT_BASE = os.path.join(REPO, "tmp", "skills-outputs", "zj-open-source-capability-fit")
REASEARCH_DIR = os.path.join(REPO, "docs", "reasearch")
DOC_OUT = os.path.join(REPO, "docs", "designs", "adoption-rulings.md")

# Instrument vocabulary is A/B/B1/B2/B3/C/D (B = small controllable gap with
# E<=E_MID and mode not further split); zj's requested domain A/B1/B2/B3/C/D
# is a subset, but §5.3.3 actually carries one B row (EC-03 × qm).
VALID_RULINGS = {"A", "B", "B1", "B2", "B3", "C", "D"}
VALID_STANCES = {"确认", "推翻"}
problems = []


def die(msg):
    problems.append(msg)


# ---------------------------------------------------------------------------
# Human rulings — explicit constant table. logic/basis are zj's initial draft
# text, confirmed 2026-11-25; ref is validated against §5.3.3 below.
# ---------------------------------------------------------------------------
RULINGS = [
    ("EC-01", "multica", "B1", "确认",
     "adapter 覆盖 issue→runtime→review 全链，门语义另判自研、不冲突",
     "§5.2 R1.1-1.4 全 satisfied；sealed「Review gates / work lands in review」"),
    ("EC-01", "loop-now", "D", "确认",
     "关键格全 <FIT_FAIL，插件信任分级不是工作流门",
     "R1.1=0.42 / R1.3=0.37 / R1.4=0.10"),
    ("EC-02", "loop-now", "D", "确认",
     "无 reject-with-feedback 门、无反馈归因链",
     "R2.1=0.06 / R2.2=0.16"),
    ("EC-02", "multica", "B1", "确认",
     "review gate + issue provenance 覆盖，反馈回写按 M3 自研补",
     "§5.2 R2.1-2.4 全 satisfied"),
    ("EC-03", "loop-now", "D", "确认",
     "one local installation 与双设备起点直接冲突",
     "R3.2=0.16 / R3.3=0.09"),
    ("EC-03", "multica", "B1", "确认",
     "self-host daemon + Skills 可作载体，handoff 语义自研补",
     "§5.2 R3.1-3.3 全 satisfied"),
    ("EC-03", "qm", "B", "确认",
     "scope sandbox 覆盖跨设备，接续状态未逐字证明但缺口可控",
     "must 覆盖 67% / R3.3=0.510 must_gap / E=73≤E_MID"),
    ("EC-05", "loop-now", "D", "确认",
     "仅执行记录、无共享知识层",
     "R5.1=0.13 / R5.2=0.18"),
    ("EC-05", "mem-vault", "C", "确认",
     "检索属主体能力禁区→自建，Markdown 只作 M8 载体",
     "§5.3.2 full-retrieval-memory 触碰；sealed「plain cloud-synced Markdown」"),
    ("EC-05", "multica", "B1", "确认",
     "Skills 覆盖沉淀，来源归属按 M8 补 scope",
     "§5.2 R5.1-5.2 satisfied"),
    ("EC-05", "qm", "B1", "确认",
     "qm scoped memory 即 M8 语义基准、adapter 采用",
     "§5.2 R5.1-5.2 satisfied"),
    ("EC-06", "ZAgenticOPN", "D", "确认",
     "scorecard 是汇总统计，非 run 时间点定位",
     "R6.1=0.29（参照物，仅诊断链初判）"),
    ("EC-06", "loop-now", "D", "确认",
     "timeline 可见但无失败标记/回放账本",
     "R6.1=0.48 / R6.2=0.32"),
    ("EC-06", "multica", "B1", "确认",
     "timestamped transcript + intent/run/diff 唯一强证据",
     "R6.1 L1=0.722 / §5.2 satisfied"),
    ("EC-06", "opencode-coordination", "D", "确认",
     "协作 ledger 非 run 步骤回放、provenance 粒度不足",
     "R6.2=0.36"),
    ("EC-06", "qm", "B1", "确认",
     "全审计 + per-tool 批准，重放链路须适配",
     "§5.2 R6.1-6.2 satisfied"),
]

# ---------------------------------------------------------------------------
# SoT 1: reference signals parsed from fit-matrix §5.3.3 (derived artifact)
# ---------------------------------------------------------------------------
def parse_references(path):
    if not os.path.exists(path):
        die(f"fit-matrix missing: {path}")
        return {}
    lines = open(path, encoding="utf-8").read().splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == "#### 5.3.3 assess 分类参考信号（仅 classification 输入）":
            start = i
            break
    if start is None:
        die("fit-matrix §5.3.3 heading not found")
        return {}
    refs = {}
    for ln in lines[start + 1:]:
        s = ln.strip()
        if not s.startswith("|"):
            # Skip the > note line and blank lines; stop at the next section.
            if s.startswith("#"):
                break
            continue
        cols = [c.strip() for c in s.strip("|").split("|")]
        if len(cols) < 3 or cols[0] in ("EC", "---"):
            continue
        ec, proj, rec = cols[0], cols[1], cols[2]
        if not re.fullmatch(r"EC-\d{2}", ec):
            continue
        if rec not in VALID_RULINGS:
            die(f"§5.3.3 invalid reference {rec!r} at ({ec}, {proj})")
            continue
        key = (ec, proj)
        if key in refs:
            die(f"§5.3.3 duplicate row {key}")
        refs[key] = rec
    return refs


# ---------------------------------------------------------------------------
# SoT 2: EVIDs read from per-EC classification inputs (never hand-filled)
# ---------------------------------------------------------------------------
def load_cell_evids():
    evids = {}
    for ec in sorted({r[0] for r in RULINGS}):
        ec_dir = ec.replace("-", "").lower() + "-scaffold"
        path = os.path.join(FIT_BASE, ec_dir, "fit-input-classification.json")
        if not os.path.exists(path):
            die(f"classification input missing: {path}")
            continue
        data = json.load(open(path, encoding="utf-8"))
        matrix = data.get("matrix", {})
        for proj, cells in matrix.items():
            found = []
            for rid, cell in cells.items():
                e = cell.get("evidence", "")
                if not re.fullmatch(r"EVID::[0-9a-f]{24}", e):
                    die(f"invalid evidence format {e!r} at ({ec}, {proj}, {rid})")
                    continue
                found.append(e[6:])
            evids[(ec, proj)] = sorted(set(found))
    return evids


# ---------------------------------------------------------------------------
# SoT 3: sealed-ledger EVID index (existence check only)
# ---------------------------------------------------------------------------
def load_evid_index():
    index = {}
    patterns = [
        os.path.join(REASEARCH_DIR, "**", "collect", "ledger-*.json"),
        os.path.join(REASEARCH_DIR, "**", "*ledger-response*.json"),
    ]
    files = []
    for pat in patterns:
        files.extend(_glob.glob(pat, recursive=True))
    for f in sorted(files):
        try:
            data = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue

        def walk(o):
            if isinstance(o, dict):
                eid = o.get("id") or o.get("sealedId") or o.get("sealed_id")
                txt = o.get("excerpt") or o.get("text") or o.get("statement") or o.get("content")
                if eid and txt and isinstance(eid, str) and re.fullmatch(r"[0-9a-f]{24}", str(eid)):
                    index.setdefault(str(eid), os.path.relpath(f, REPO))
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)

        walk(data)
    return index


refs = parse_references(FIT_MD)
cell_evids = load_cell_evids()
evid_index = load_evid_index()

# Fail-closed: constant table structure + SoT agreement
if len(RULINGS) != 16:
    die(f"RULINGS must have 16 rows, got {len(RULINGS)}")
keys = [(r[0], r[1]) for r in RULINGS]
if len(set(keys)) != len(keys):
    die("RULINGS has duplicate (EC, O) keys")
if set(keys) != set(refs):
    die(f"RULINGS keys != §5.3.3 keys: only-in-rulings={sorted(set(keys)-set(refs))}, "
        f"only-in-matrix={sorted(set(refs)-set(keys))}")
for ec, proj, ruling, stance, logic, basis in RULINGS:
    if ruling not in VALID_RULINGS:
        die(f"invalid ruling {ruling!r} at ({ec}, {proj})")
    if stance not in VALID_STANCES:
        die(f"invalid stance {stance!r} at ({ec}, {proj})")
    if not logic.strip() or not basis.strip():
        die(f"empty logic/basis at ({ec}, {proj})")
    ref = refs.get((ec, proj))
    if stance == "确认" and ruling != ref:
        die(f"stance=确认 but ruling {ruling} != reference {ref} at ({ec}, {proj})")
    if stance == "推翻" and ruling == ref:
        die(f"stance=推翻 but ruling == reference {ref} at ({ec}, {proj})")
    evs = cell_evids.get((ec, proj), [])
    if not evs:
        die(f"no EVID at ({ec}, {proj})")
    for e in evs:
        if e not in evid_index:
            die(f"EVID::{e} ({ec}, {proj}) not found in sealed ledger")
    if (ec, proj) not in cell_evids:
        die(f"no classification input cell for ({ec}, {proj})")

if problems:
    print("FAIL (adoption-rulings invariants):", file=sys.stderr)
    for p in problems:
        print("  -", p, file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Emit supporting page
# ---------------------------------------------------------------------------
def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


o = []
o.append("---")
o.append("doc-kind: reference")
o.append("authority: supporting")
o.append("authority-id: opn.adoption-rulings")
o.append("---")
o.append("")
o.append("# 采用 / 自研裁决 · 16 个 EC×O（supporting / 规划-执行阶段 Human 人工判断）")
o.append("")
o.append("> 本页是 zj 2026-11-25 在规划-执行阶段对 [需求拟合矩阵](requirements-fit-matrix.md) §5.3.3 的 16 行 `assess` 参考信号逐格作出的**人工裁决**，是 supporting 产物，不是产品计划、不实现。")
o.append("> 由 `docs/reasearch/opn-cross-comparison/_gen_adoption_rulings.py` 从 fit-matrix §5.3.3（参考信号）+ 显式裁决常量表派生；参考信号与 EVID 均机械读取、不手填，ratify bundle / fit-matrix 均不改写。")
o.append("")
o.append("## 1. 边界与口径（zj 2026-11-25 裁决）")
o.append("")
o.append("- **粒度**：16 个 EC×O 对逐格裁决——不是按 6 个候选合并、也不是按 5 条场景合并。覆盖 EC-01/02/03/05/06 的严格 native 交集候选。")
o.append("- **值域**：沿用母模型 `classify_candidate` 词表 `A/B/B1/B2/B3/C/D`，不引入新标签。zj 指定的 `A/B1/B2/B3/C/D` 是子集；§5.3.3 实际含 1 个 `B`（EC-03×qm，缺口小且可控、mode 未细分），如实保留，不为对齐子集而改判。")
o.append("- **处置**：`确认`=裁决值等于参考信号；`推翻`=裁决值不等于参考信号（本轮 16 确认 / 0 推翻）。")
o.append("- **D 的语义**：继续搜索（搜索循环回环态），**不是终态否决**——该候选在该场景既不自研也不采用，开放继续找。")
o.append("- **模块级裁决对齐**：M3「Human 门统一语义自研」与 M8「记忆边界自研」已在 primary 层裁过；multica 的 B1 / mem-vault 的 C 只让 adapter / Markdown 目录承载触发与存储，门语义与检索边界仍自研（R1.4/R2.x、full-retrieval-memory）。")
o.append("- **可逆性**：后续推翻某格须改生成器常量表后重跑，不得手改本页。")
o.append("")
o.append("## 2. 裁决表（16 格）")
o.append("")
o.append("| EC | O | 参考信号 | 裁决 | 处置 | 初判的逻辑和依据 | sealed EVID |")
o.append("|---|---|---|---|---|---|---|")
for ec, proj, ruling, stance, logic, basis in RULINGS:
    evs = cell_evids[(ec, proj)]
    short = ", ".join(f"`{e[:8]}…`" for e in evs)
    o.append(f"| {ec} | {proj} | {refs[(ec, proj)]} | **{ruling}** | {stance} | "
             f"{esc(logic)}；据：{esc(basis)} | {short} |")
o.append("")
from collections import Counter
dist = Counter(r[2] for r in RULINGS)
o.append("- **裁决分布**：" + " / ".join(f"{k}={v}" for k, v in sorted(dist.items())) +
         "；与 §5.3.3 参考分布一致（本轮无推翻）。")
o.append("")
o.append("## 3. 复核焦点（复核后如需改判，改常量表重跑）")
o.append("")
o.append("- **multica 的 5 个 B1**（EC-01/02/03/05/06）：#1/#4 涉 Human 门，按 M3 门语义自研处置，adapter 只作触发载体；若认为凡涉门语义即应推翻为 C，改这两格。")
o.append("- **mem-vault 的 C**（EC-05）：唯一 C，语义为「自建检索主体能力、Markdown 目录仅作 M8 载体」。若改为检索也采用，须推翻为 B。")
o.append("- **7 个 D**：维持继续搜索回环态，不是否决；对应候选在该场景暂无路径，开放继续找。")
o.append("")
o.append("## 4. 机械自检")
o.append("")
o.append(f"- 裁决格数={len(RULINGS)}；§5.3.3 参考格数={len(refs)}；键集合完全一致，无重复。")
o.append(f"- 裁决值全部在封闭词表 {sorted(VALID_RULINGS)} 内；处置全部在 {sorted(VALID_STANCES)} 内；确认格裁决值逐格等于参考信号，推翻格必须不同。")
o.append(f"- 每格 EVID 来自对应 EC 的 `fit-input-classification.json`，且在 sealed ledger 索引中存在（索引 {len(evid_index)} 条）；无手填 SHA/EVID。")
o.append("- 重跑字节一致（无时间戳、稳定排序）；本页 supporting；derived-from: opn.requirements-fit-matrix；不改写 ratify bundle、不改 fit-matrix。")
o.append("")

with open(DOC_OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o) + "\n")
print(f"wrote {os.path.relpath(DOC_OUT, REPO)} ({len(RULINGS)} rulings)")
