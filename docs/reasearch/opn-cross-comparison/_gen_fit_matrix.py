#!/usr/bin/env python3
"""Generate requirements-fit-matrix.md + per-EC mother-model inputs.

Design rulings (zj 2026-11-24):
- Q1-Q5: anchor EC (not modules); bundle acceptance is only a seed; O selected
  per EC from sealed-native projects; output is a supporting page.
- Q6c/Q11a: split each EC by Human-observable acceptance nodes (not module names).
- Q7a: three-layer scoring — L1 objective score + deduction rationale (agent,
  from that cell's sealed EVID), L2 mechanical recheck by capability_fit.py,
  L3 Human endorsement by zj. Module-level hypothesis is REFERENCE ONLY.
- Q8a: every R priority=must, critical=true.
- Q9b (superseded 2026-11-24): cost was OUT and assess was banned. zj later
  asked for a cost/E pass; COST_DRAFT + ADAPTATION_DRAFT are zjj DRAFT values
  (relative cost points). E unit is zj-ACCEPTED as reference-only (2026-11-24);
  every A/B/C/D is a reference signal, NOT a build/adopt ruling — that call is
  deferred to zj's manual judgment in the planning-execution stage.
- Q1a-Q6a (review score enters classification): two inputs per EC —
  fit-input-l1.json (originals) and fit-input-classification.json. For L3
  "可以有" (raise_to_pass): [1.0,1.0,max(eff,FIT_OK)] => eff exactly FIT_OK.
  For "认同 L2 未满足" (endorse): factors unchanged. Verdict uses only the
  instrument's effective_fit/cell_satisfied/FIT_OK/FIT_FAIL.
- Roll-out ruling (zj 2026-11-24, after EC-01 sample):
  Q1a candidate O = strict all-module native intersection per EC.
  Q2a R split by module chain, 11 new R (R2.1..R2.4, R3.1..R3.3,
    R5.1..R5.2, R6.1..R6.2).
  Q3a acceptance drafts approved as listed below.
  Q4a new 35 cells L3 originally pending; zj has since filled all 35 by hand
    and those verbatim rulings were back-filled into HUMAN_FINAL (43/43).
  Q5a excluded source projects are recorded with their exact native gap.
  Q6a same supporting page extended to 5 ECs; one generator, one authority-id.

Fail-closed: baseline definitions, module chains, sealed EVID, EVID existence,
candidate versions (40-hex from sealed ledger), SCORES coverage, L3 key sets,
classification mapping, cost/adaptation vocabularies, mother-model G1-G6.
No hand-filled SHA/EVID. E unit zj-accepted reference-only; A/B/C/D are reference signals, not rulings — build/adopt is a planning-execution-stage human call.
Deterministic: no timestamps, stable ordering.
"""
from collections import Counter
import glob as _glob
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
FIT_BASE = os.path.join(
    REPO, "tmp", "skills-outputs", "zj-open-source-capability-fit"
)
DOC_OUT = os.path.join(REPO, "docs", "designs", "requirements-fit-matrix.md")
CAPABILITY_FIT_PY = os.environ.get("CAPABILITY_FIT_PY") or os.path.expanduser(
    "~/.workbuddy/skills/zj-open-source-capability-fit/scripts/capability_fit.py"
)

FACTOR_KEYS = ("coverage", "semantic_match", "composability")
problems = []


def die(msg):
    problems.append(msg)


# ---------------------------------------------------------------------------
# Human decisions — explicit constant tables, cross-checked against SoT below.
# ---------------------------------------------------------------------------
EC_SPECS = [
    {
        "ec": "EC-01",
        "name": "提交目标 → 拿到可验收结果（主闭环）",
        "keyword": "提交目标",
        "chain": ["M1", "M5", "M4", "M3"],
        "candidates": ["multica", "loop-now"],
        "r_split": [
            {"id": "R1.1", "node": "目标提交后可见", "acceptance": "Human 提交目标后，能在列表看到对应 Work Item，其状态可读且能前进", "module": "M1"},
            {"id": "R1.2", "node": "执行进度可观察", "acceptance": "Human 能看到 Agent 已接收并在隔离边界内执行，进度/阻塞可见、互不污染", "module": "M5"},
            {"id": "R1.3", "node": "结果产物可复核", "acceptance": "Human 能看到本次产出，且来源/步骤可追溯", "module": "M4"},
            {"id": "R1.4", "node": "Human 门验收可审计", "acceptance": "Human 在门上 approve/reject，动作有账本、可审计", "module": "M3"},
        ],
    },
    {
        "ec": "EC-02",
        "name": "review 打回 → Agent 从拒绝历史学习 → 重做",
        "keyword": "review 打回",
        "chain": ["M3", "M4", "M5", "M6"],
        "candidates": ["loop-now", "multica"],
        "r_split": [
            {"id": "R2.1", "node": "拒绝与反馈在门上可见", "acceptance": "Human 在门上 reject 并写反馈后，该拒绝与反馈能在门上可见且关联到原结果、动作入账本", "module": "M3"},
            {"id": "R2.2", "node": "拒绝历史可查", "acceptance": "Human 能查到前次结果、反馈与来源，反馈不丢失", "module": "M4"},
            {"id": "R2.3", "node": "Agent 带反馈重做", "acceptance": "能看到 Agent 已带该反馈重新执行，工作区隔离、进度/阻塞可见", "module": "M5"},
            {"id": "R2.4", "node": "重做后再次进门可观察", "acceptance": "board/回放能看到前后两次结果与反馈应用情况", "module": "M6"},
        ],
    },
    {
        "ec": "EC-03",
        "name": "跨设备接续会话",
        "keyword": "跨设备接续会话",
        "chain": ["M7", "M8", "M10"],
        "candidates": ["loop-now", "multica", "qm"],
        "r_split": [
            {"id": "R3.1", "node": "设备 A 会话上下文可见", "acceptance": "Human 在设备 A 发起会话后，能看到可接续的会话上下文（标识/当前进度）", "module": "M7"},
            {"id": "R3.2", "node": "上下文进入共享记忆", "acceptance": "设备 B 能看到设备 A 已沉淀的会话上下文/共享记忆，且可跨设备边界清晰", "module": "M8"},
            {"id": "R3.3", "node": "设备 B 接续运行", "acceptance": "从该上下文继续同一会话，运行资源/沙箱按 scope 接入、接续前后状态连续", "module": "M10"},
        ],
    },
    {
        "ec": "EC-05",
        "name": "共享事实沉淀与检索",
        "keyword": "共享事实沉淀",
        "chain": ["M8", "M7"],
        "candidates": ["loop-now", "mem-vault", "multica", "qm"],
        "r_split": [
            {"id": "R5.1", "node": "事实沉淀可追溯", "acceptance": "Human 完成协作并要求沉淀后，能看到事实写入共享记忆层，来源/归属可追溯", "module": "M8"},
            {"id": "R5.2", "node": "后续会话检索与复用", "acceptance": "后续会话能检索到该事实并看到它被复用到新会话，引用可辨认", "module": "M7"},
        ],
    },
    {
        "ec": "EC-06",
        "name": "运行诊断与回放",
        "keyword": "运行诊断",
        "chain": ["M6", "M4"],
        "candidates": ["ZAgenticOPN", "loop-now", "multica", "opencode-coordination", "qm"],
        "r_split": [
            {"id": "R6.1", "node": "失败点可定位", "acceptance": "Human 在 board/审计视图中能定位一次失败或待审计的 run 及其时间点", "module": "M6"},
            {"id": "R6.2", "node": "从失败点回放", "acceptance": "能从失败点重放该 run，看到相关步骤与产出来源/账本", "module": "M4"},
        ],
    },
]

R_SPLIT = [r for spec in EC_SPECS for r in spec["r_split"]]
CANDIDATES = sorted({p for spec in EC_SPECS for p in spec["candidates"]})
EXPECTED_MODULES = sorted({m for spec in EC_SPECS for m in spec["chain"]})

# Project display name -> repository.name in the sealed ledgers. This is a name
# mapping only; every SHA is read mechanically from revision.sha below.
REPO_NAME_BY_PROJ = {
    "multica": "multica",
    "loop-now": "loop-now",
    "qm": "qm",
    "mem-vault": "shared-memory-vault",
    "ZAgenticOPN": "ZAgenticOPN",
    "opencode-coordination": "opencode-coordination",
}

# Q5a — source projects named in baseline §4.1 that Q1a's strict-native gate
# excludes. The gap module is verified against the reuse ledger below.
EXCLUDED_SOURCE_NOTES = {
    "EC-02": [("mozzie", "M6")],
    "EC-03": [("mem-vault", "M10")],
    "EC-05": [("tasktrooper", "M7"), ("ZAgenticOPN", "M7")],
    "EC-06": [],
}

# ---------------------------------------------------------------------------
# LAYER 1 — objective scores from the sealed EVID excerpt of EACH (R,O) cell.
# EC-01's 8 entries are the reviewed sample and must remain byte-stable.
# The 35 roll-out entries are new evidence-based initial scores; their L3 is
# pending by Q4a, so they do NOT yet enter the fit-layer classification.
# ---------------------------------------------------------------------------
SCORES = {
    # ---- EC-01 (reviewed sample; unchanged from the ratified scaffold) ----
    ("R1.1", "multica"): {
        "coverage": 0.90, "semantic_match": 0.90, "composability": 0.80,
        "by": "zjj-evidence",
        "rationale": "EVID 显示 issue 分配/状态流转/report progress/raise blockers 齐备；扣分点：状态机是通用 issue 流转（available→claimed→completed），与我方 Objective→可验收工作项的语义同构性未证，接入需适配身份/Agent 网络。",
    },
    ("R1.1", "loop-now"): {
        "coverage": 0.75, "semantic_match": 0.70, "composability": 0.80,
        "by": "zjj-evidence",
        "rationale": "EVID 偏对话 + task workflow 协调，可见性侧重 conversation/tool calls/who is working，而非显式的『提交目标生成工作项』结构化状态机；plugin 扩展点丰富利于组合。",
    },
    ("R1.2", "multica"): {
        "coverage": 0.90, "semantic_match": 0.90, "composability": 0.80,
        "by": "zjj-evidence",
        "rationale": "EVID 有 runtime you control + comments as it goes + raise blockers + intent/run/diff 同 issue；扣分点：『runtime you control』是部署层控制，是否等于 per-task 强隔离（worktree/容器）未在摘录明示，互不污染属推断。",
    },
    ("R1.2", "loop-now"): {
        "coverage": 0.90, "semantic_match": 0.90, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 明确 each agent runs in its own working directory、server launches/recycles/bounds them，隔离证据强；扣分点：非 OS 级沙箱，且依赖外部 Pi 执行引擎与 plugin host，接入需适配。",
    },
    ("R1.3", "multica"): {
        "coverage": 0.90, "semantic_match": 0.90, "composability": 0.80,
        "by": "zjj-evidence",
        "rationale": "EVID 有 intent/run/decisions/diff stay connected to the same issue，来源与步骤追溯强；扣分点：provenance 挂在 issue 粒度，完整审计账本结构未在摘录展示。",
    },
    ("R1.3", "loop-now"): {
        "coverage": 0.75, "semantic_match": 0.70, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 有 artifacts and records stay after execution resources recycled、frozen workflow node by node；扣分点：『谁在何时做了什么』的细粒度溯源未展示，偏 workflow 记录而非审计账本。",
    },
    ("R1.4", "multica"): {
        "coverage": 0.85, "semantic_match": 0.85, "composability": 0.75,
        "by": "zjj-evidence",
        "rationale": "EVID 明确 Review gates → Work lands in review, not in main. You decide what ships，approve/reject 语义成立；扣分点：账本结构（谁批/何时/依据）未明示。刻意不因模块级『必须自研』假设压低——该假设与本格 sealed 证据冲突。",
    },
    ("R1.4", "loop-now"): {
        "coverage": 0.50, "semantic_match": 0.40, "composability": 0.50,
        "by": "zjj-evidence",
        "rationale": "EVID 讲插件安装信任分级（source grading / pre-install preview / one-click global disable），不是工作流中的 Human approve/reject 门、无审批账本语义；EVID 虽 sealed 但与我方 R1.4 验收节点语义错配，故三项压低。这是逐 O 差异，非模块级一刀切。",
    },
    # ---- EC-02 ----
    ("R2.1", "loop-now"): {
        "coverage": 0.45, "semantic_match": 0.30, "composability": 0.45,
        "by": "zjj-evidence",
        "rationale": "EVID 是插件安装信任分级（source grading / pre-install preview / global disable），没有工作流中的 Human reject-with-feedback 门，也不记录打回历史；semantic_match 压到 0.30。",
    },
    ("R2.1", "multica"): {
        "coverage": 0.80, "semantic_match": 0.75, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 有 Review gates → work lands in review → you decide what ships，Human 准出成立；扣分点：摘录未展示 reject 反馈如何回写为可追溯的打回历史，故语义与组合未满分。",
    },
    ("R2.2", "loop-now"): {
        "coverage": 0.60, "semantic_match": 0.45, "composability": 0.60,
        "by": "zjj-evidence",
        "rationale": "EVID 说 artifacts and records stay after execution resources are recycled、workflow frozen node by node，记录持久性成立；扣分点：看不到 reject-with-feedback 的归因链，反馈与前次结果的绑定未证。",
    },
    ("R2.2", "multica"): {
        "coverage": 0.90, "semantic_match": 0.80, "composability": 0.80,
        "by": "zjj-evidence",
        "rationale": "EVID 有 intent/run/decisions/diff stay connected to the same issue，general provenance 强；扣分点『拒绝历史』这一特定语义未在摘录出现，不能从通用 provenance 直接推出。",
    },
    ("R2.3", "loop-now"): {
        "coverage": 0.85, "semantic_match": 0.70, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 明确 each agent runs in its own working directory、server launches/recycles/bounds them，隔离与重跑环境成立；扣分点：摘录没有『带反馈重做』的闭环语义，只有 frozen workflow 的线性/有界循环。",
    },
    ("R2.3", "multica"): {
        "coverage": 0.80, "semantic_match": 0.70, "composability": 0.75,
        "by": "zjj-evidence",
        "rationale": "EVID 有 assigned issue → runtime you control → comments as it goes → hand back for review，具备重做载体；扣分点：没有展示反馈如何注入下一轮执行，重做仍是推断。",
    },
    ("R2.4", "loop-now"): {
        "coverage": 0.85, "semantic_match": 0.75, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 的 run timeline + bounded review loops + artifacts persist 让『重做后可见』成立；扣分点：Human 门再次进入的审批事件未在摘录出现，只有 workflow 层的 loop。",
    },
    ("R2.4", "multica"): {
        "coverage": 0.85, "semantic_match": 0.70, "composability": 0.75,
        "by": "zjj-evidence",
        "rationale": "EVID 的 live run transcript（每次 tool call/command 带时间戳、失败测试输出展开）覆盖强；扣分点：摘录证明可观察，但未证明前后两次结果与反馈应用被并排对照。",
    },
    # ---- EC-03 ----
    ("R3.1", "loop-now"): {
        "coverage": 0.85, "semantic_match": 0.85, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 有 Keep work in context：continue conversation/workspace、same agent reusing task workspace and session across steps，连续语义强；扣分点：本地 console 单安装，跨设备的设备 A/B 身份未在摘录出现。",
    },
    ("R3.1", "multica"): {
        "coverage": 0.70, "semantic_match": 0.60, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 有 Chat + Projects 挂 repos/docs 作 context；扣分点：没有会话标识、断点状态或『接续』语义，只是可发起工作与查问题。",
    },
    ("R3.1", "qm"): {
        "coverage": 0.75, "semantic_match": 0.60, "composability": 0.65,
        "by": "zjj-evidence",
        "rationale": "EVID 有 each person/room scoped memory/files/keychain/permissions/durable sandbox，scope 边界强；扣分点：摘录未把 scope 映射到『一次会话的接续上下文』，语义需适配。",
    },
    ("R3.2", "loop-now"): {
        "coverage": 0.65, "semantic_match": 0.45, "composability": 0.55,
        "by": "zjj-evidence",
        "rationale": "EVID 有 server persists the message、artifacts/records stay；扣分点：明确是 one local installation（Go server + SQLite + local data dir），无跨设备共享记忆语义，semantic_match 压低。",
    },
    ("R3.2", "multica"): {
        "coverage": 0.70, "semantic_match": 0.55, "composability": 0.65,
        "by": "zjj-evidence",
        "rationale": "EVID 有 daemon on your laptop or cloud box + Skills playbook every agent reuses，跨设备运行与复用载体存在；扣分点：没有被证实的『同一份会话上下文』跨设备可见，Skills 不等于会话记忆。",
    },
    ("R3.2", "qm"): {
        "coverage": 0.80, "semantic_match": 0.70, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 有 per person/room scoped memory + durable sandbox + run it in your own cloud（Slack/web），跨设备载体最完整；扣分点：会议级『会话上下文』与 scope memory 的映射仍须适配。",
    },
    ("R3.3", "loop-now"): {
        "coverage": 0.60, "semantic_match": 0.30, "composability": 0.50,
        "by": "zjj-evidence",
        "rationale": "EVID 明说 one local installation、SQLite in a local data directory、组件不构成独立可扩展服务；与『设备 B 接续同一会话』直接冲突，semantic_match 0.30。",
    },
    ("R3.3", "multica"): {
        "coverage": 0.75, "semantic_match": 0.60, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 有 self-hostable + daemon on laptop/cloud + works with agent CLIs，跨设备运行可搭；扣分点：没有 session handoff 或接续后状态连续的证据。",
    },
    ("R3.3", "qm"): {
        "coverage": 0.85, "semantic_match": 0.80, "composability": 0.75,
        "by": "zjj-evidence",
        "rationale": "EVID 有 multiplayer harness in Slack and on the web + own cloud + per-scope durable sandbox，设备 B 接入与资源隔离成立；扣分点：『接续前后状态连续』未在摘录逐字证明。",
    },
    # ---- EC-05 ----
    ("R5.1", "loop-now"): {
        "coverage": 0.60, "semantic_match": 0.40, "composability": 0.55,
        "by": "zjj-evidence",
        "rationale": "EVID 有 server persists message + artifacts/records stay after recycle，但只是执行记录；扣分点：没有共享知识层、事实沉淀动作或来源/归属结构。",
    },
    ("R5.1", "mem-vault"): {
        "coverage": 0.90, "semantic_match": 0.80, "composability": 0.75,
        "by": "zjj-evidence",
        "rationale": "EVID 明确 plain cloud-synced Markdown → shared knowledge base for every agent and every device，session-blackboard CONTEXT.md；扣分点：Markdown 的『来源/归属』是约定而非结构化 provenance。",
    },
    ("R5.1", "multica"): {
        "coverage": 0.75, "semantic_match": 0.65, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 有 Skills：turn a solved problem into a playbook every agent reuses，具备沉淀与复用载体；扣分点：摘录未展示知识来源归属与可追溯账本。",
    },
    ("R5.1", "qm"): {
        "coverage": 0.80, "semantic_match": 0.65, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 有 each person and each room has its own scoped memory/files，沉淀与 scope 归属成立；扣分点：没有『完成协作后要求沉淀』的显式动作与事实级溯源。",
    },
    ("R5.2", "loop-now"): {
        "coverage": 0.65, "semantic_match": 0.45, "composability": 0.60,
        "by": "zjj-evidence",
        "rationale": "EVID 有 same agent reusing its task workspace and session across steps，延续性成立；扣分点：没有检索接口，也没有『被复用到新会话』的可辨认引用。",
    },
    ("R5.2", "mem-vault"): {
        "coverage": 0.90, "semantic_match": 0.85, "composability": 0.75,
        "by": "zjj-evidence",
        "rationale": "EVID 明确 any agent reads a single file and resumes the work from where another left off — no context loss，复用语义最强；扣分点：纯 Markdown 无索引/检索机制，引用可辨认靠约定。",
    },
    ("R5.2", "multica"): {
        "coverage": 0.75, "semantic_match": 0.60, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 有 Chat → ask your workspace a question、Projects attach repos/docs as context，类检索入口存在；扣分点：答复是否引用已沉淀事实、引用是否可辨认未证。",
    },
    ("R5.2", "qm"): {
        "coverage": 0.70, "semantic_match": 0.55, "composability": 0.65,
        "by": "zjj-evidence",
        "rationale": "EVID 有 scoped memory/files/keychain，事实可存在；扣分点：没有跨会话检索与引用显示，且 scope 边界与『新会话复用』的关系需适配。",
    },
    # ---- EC-06 ----
    ("R6.1", "ZAgenticOPN"): {
        "coverage": 0.75, "semantic_match": 0.60, "composability": 0.65,
        "by": "zjj-evidence",
        "rationale": "EVID 有 Health scorecard（C1–C4、Human intervention、context defects、Git acceptance、三次复验），审计口径强；扣分点：scorecard 是汇总统计，不是『一次失败 run 的时间点定位』。",
    },
    ("R6.1", "loop-now"): {
        "coverage": 0.85, "semantic_match": 0.80, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 有 tool calls/commands/usage flow back into the run timeline，run 级可见性成立；扣分点：摘录没展示失败标记或按失败筛选，定位仍需人工翻 timeline。",
    },
    ("R6.1", "multica"): {
        "coverage": 0.95, "semantic_match": 0.95, "composability": 0.80,
        "by": "zjj-evidence",
        "rationale": "EVID 直接是 A live run transcript: every tool call and command timestamped, with a failing test's output open，失败点与时间双证据；扣分点：是否与审计视图/board 联动未在摘录展示。",
    },
    ("R6.1", "opencode-coordination"): {
        "coverage": 0.75, "semantic_match": 0.55, "composability": 0.65,
        "by": "zjj-evidence",
        "rationale": "EVID 有 one append-only ledger of roles/work items/messages/progress/history + board updates，协作审计强；扣分点：不是 run 级诊断视图，失败时间点不在摘录中。",
    },
    ("R6.1", "qm"): {
        "coverage": 0.60, "semantic_match": 0.40, "composability": 0.55,
        "by": "zjj-evidence",
        "rationale": "EVID 是 crons/watches/webhooks + search internal notes/email/documents/databases/web，偏运营检索；扣分点：没有 run timeline、失败标记或时间点定位语义，semantic_match 压低。",
    },
    ("R6.2", "ZAgenticOPN"): {
        "coverage": 0.90, "semantic_match": 0.85, "composability": 0.75,
        "by": "zjj-evidence",
        "rationale": "EVID 有五字段结果 + structured blocker + Git provenance + reviewer re-claim + references 核验 + 完成条件，来源与账本强；扣分点：『从失败点重放 run』未逐字出现。",
    },
    ("R6.2", "loop-now"): {
        "coverage": 0.75, "semantic_match": 0.65, "composability": 0.65,
        "by": "zjj-evidence",
        "rationale": "EVID 有 tasks follow frozen workflow node by node + artifacts/records stay after recycle，部分回放与产出留存成立；扣分点：没有 provenance 账本结构，重放是推断。",
    },
    ("R6.2", "multica"): {
        "coverage": 0.90, "semantic_match": 0.85, "composability": 0.80,
        "by": "zjj-evidence",
        "rationale": "EVID 有 intent/run/decisions/diff stay connected to the same issue — nobody reconstructs context；扣分点：强 provenance 不等于可按失败点重放，回放动作未在摘录证明。",
    },
    ("R6.2", "opencode-coordination"): {
        "coverage": 0.80, "semantic_match": 0.65, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 的 append-only ledger + event recorded/PR checked/board updated 提供审计账本；扣分点：面向协作事件而非 run 步骤回放，产物 provenance 粒度不足。",
    },
    ("R6.2", "qm"): {
        "coverage": 0.80, "semantic_match": 0.65, "composability": 0.70,
        "by": "zjj-evidence",
        "rationale": "EVID 有 everything it does is audited + strict human approval per tool call，审计强；扣分点：审计记录与失败点重放/产出来源之间的链路未在摘录展示。",
    },
}

# LAYER 3 — all 43 cells are zj's verbatim L3 endorsements, mechanically
# extracted from his direct edit of the rendered L3 column (2026-11-24).
# Never default a cell to "认同"; every entry here is a real Human ruling.
HUMAN_FINAL = {
    ('R1.1', 'multica'): {"by": "zj", "rationale": "可以有，它填充了 Objective→可验收工作项 的中间过程，是协作场景下的一种流转路径"},  # EC-01
    ('R1.1', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-01
    ('R1.2', 'multica'): {"by": "zj", "rationale": "可以有，它是待新增feature的备选"},  # EC-01
    ('R1.2', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-01
    ('R1.3', 'multica'): {"by": "zj", "rationale": "可以有，这是具体的使用细节，这些关联信息的侧重在于可观察、可回溯，不能直接用于审计"},  # EC-01
    ('R1.3', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-01
    ('R1.4', 'multica'): {"by": "zj", "rationale": "可以有，这是Human介入工作的门禁之一"},  # EC-01
    ('R1.4', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-01
    ('R2.1', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-02
    ('R2.1', 'multica'): {"by": "zj", "rationale": "可以有，这是Human介入工作的门禁之一"},  # EC-02
    ('R2.2', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-02
    ('R2.2', 'multica'): {"by": "zj", "rationale": "可以有"},  # EC-02
    ('R2.3', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-02
    ('R2.3', 'multica'): {"by": "zj", "rationale": "可以有"},  # EC-02
    ('R2.4', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-02
    ('R2.4', 'multica'): {"by": "zj", "rationale": "可以有"},  # EC-02
    ('R3.1', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-03
    ('R3.1', 'multica'): {"by": "zj", "rationale": "可以有"},  # EC-03
    ('R3.1', 'qm'): {"by": "zj", "rationale": "可以有"},  # EC-03
    ('R3.2', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-03
    ('R3.2', 'multica'): {"by": "zj", "rationale": "可以有"},  # EC-03
    ('R3.2', 'qm'): {"by": "zj", "rationale": "可以有"},  # EC-03
    ('R3.3', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-03
    ('R3.3', 'multica'): {"by": "zj", "rationale": "可以有"},  # EC-03
    ('R3.3', 'qm'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-03
    ('R5.1', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-05
    ('R5.1', 'mem-vault'): {"by": "zj", "rationale": "可以有"},  # EC-05
    ('R5.1', 'multica'): {"by": "zj", "rationale": "可以有"},  # EC-05
    ('R5.1', 'qm'): {"by": "zj", "rationale": "可以有"},  # EC-05
    ('R5.2', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-05
    ('R5.2', 'mem-vault'): {"by": "zj", "rationale": "可以有"},  # EC-05
    ('R5.2', 'multica'): {"by": "zj", "rationale": "可以有"},  # EC-05
    ('R5.2', 'qm'): {"by": "zj", "rationale": "可以有"},  # EC-05
    ('R6.1', 'ZAgenticOPN'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-06
    ('R6.1', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-06
    ('R6.1', 'multica'): {"by": "zj", "rationale": "可以有"},  # EC-06
    ('R6.1', 'opencode-coordination'): {"by": "zj", "rationale": "可以有"},  # EC-06
    ('R6.1', 'qm'): {"by": "zj", "rationale": "可以有"},  # EC-06
    ('R6.2', 'ZAgenticOPN'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-06
    ('R6.2', 'loop-now'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-06
    ('R6.2', 'multica'): {"by": "zj", "rationale": "可以有"},  # EC-06
    ('R6.2', 'opencode-coordination'): {"by": "zj", "rationale": "认同 L2 未满足"},  # EC-06
    ('R6.2', 'qm'): {"by": "zj", "rationale": "可以有"},  # EC-06
}


def human_action(hf):
    if hf is None:
        return "pending"
    text = hf["rationale"]
    if text.startswith("认同"):
        return "endorse"
    if text.startswith("可以有"):
        return "raise_to_pass"
    die(f"unrecognized HUMAN_FINAL rationale prefix: {text[:24]!r}")
    return "invalid"


def human_review_score(action, eff, fit_ok):
    if action == "raise_to_pass":
        return max(float(eff), float(fit_ok))
    return None


# ---------------------------------------------------------------------------
# COST / E + ADAPTATION — zjj DRAFT (2026-11-24), explicitly NOT a zj ruling.
# Instrument constants: E_LOW=20 / E_MID=80 / E_HIGH=200 (hard-coded in
# capability_fit.py); SSOT defines six components but no unit. The instrument
# itself says "单位自定，跨候选须一致". This draft uses relative cost points,
# roughly person-day magnitude. zj accepted the unit as reference-only
# (2026-11-24); six-component numbers stay zjj draft estimates.
# Every rationale is anchored to the sealed EVID already cited in SCORES; where
# the excerpt does not speak to cost, that is called out as JUDGMENT.
# ---------------------------------------------------------------------------
COST_DRAFT = {
    "multica": {
        "initial_dev": 18, "integration": 14, "maintenance": 12,
        "upstream_adapt": 10, "ops": 8, "security_gov": 10,
        "rationale": "sealed EVID: self-hostable daemon + Skills playbook + issue/run/decisions/diff provenance + review gates；接入需身份/Agent 网络映射、Objective→Work Item 语义转换、审批账本补齐，故 initial_dev 最高。上游工作流语义变动是主要升级成本；self-host 运维中等。JUDGMENT: 六分量数值为相对点估算，sealed EVID 未直接给工作量。",
    },
    "loop-now": {
        "initial_dev": 22, "integration": 16, "maintenance": 16,
        "upstream_adapt": 10, "ops": 12, "security_gov": 12,
        "rationale": "sealed EVID: one local installation + SQLite in a local data dir + each agent in its own working directory + plugin trust grading；跨设备接续、共享记忆、Human 门账本均需自建主体能力，故 initial_dev 与 maintenance 最高。JUDGMENT: 本地多实例运维与权限治理成本为估算。",
    },
    "qm": {
        "initial_dev": 16, "integration": 14, "maintenance": 12,
        "upstream_adapt": 9, "ops": 10, "security_gov": 12,
        "rationale": "sealed EVID: Slack/web harness + own cloud + per person/room scoped memory/files/keychain/permissions + durable sandbox + audited tool calls；主体能力较完整，成本集中在权限/数据治理与多端集成。JUDGMENT: 治理分量为估算。",
    },
    "mem-vault": {
        "initial_dev": 14, "integration": 12, "maintenance": 10,
        "upstream_adapt": 6, "ops": 8, "security_gov": 9,
        "rationale": "sealed EVID: plain cloud-synced Markdown → shared knowledge base for every agent/device + session-blackboard CONTEXT.md；本体极轻（upstream_adapt 最低），但 EVID 同时确认无索引/检索、无结构化 provenance，检索与溯源须自建，计入 initial_dev/integration。JUDGMENT: 数值为相对点估算。",
    },
    "ZAgenticOPN": {
        "initial_dev": 12, "integration": 10, "maintenance": 10,
        "upstream_adapt": 8, "ops": 6, "security_gov": 9,
        "rationale": "sealed EVID: 五字段结果 + claim authority + Git provenance + health scorecard + 三次复验；与我方诊断/审计语义同构度最高，成本主要是接线与持续审计维护。注意它是参照物，此处仅就 EC-06 诊断链作候选初判。JUDGMENT: 数值为相对点估算。",
    },
    "opencode-coordination": {
        "initial_dev": 14, "integration": 12, "maintenance": 10,
        "upstream_adapt": 8, "ops": 8, "security_gov": 9,
        "rationale": "sealed EVID: append-only ledger of roles/work items/messages/progress/history + board updates + event recorded/PR checked；账本体裁贴合审计，但 run 级失败时间点与产出来源回放需补齐。JUDGMENT: 数值为相对点估算。",
    },
}

ADAPTATION_DRAFT = {
    "multica": {
        "scope": ["identity-map", "query-adapt", "state-transform", "provenance-adapt"],
        "mode": "adapter", "responsibility_uncontrolled": False,
        "rationale": "sealed EVID 显示 issue/review/provenance 是它的主体；我们只写身份映射、查询适配、状态转换、来源适配薄层，可移除、不维护 fork（B1）。",
    },
    "loop-now": {
        "scope": ["storage-sync-infra", "full-retrieval-memory", "identity-map"],
        "mode": "plugin", "responsibility_uncontrolled": False,
        "rationale": "one local installation + local SQLite 决定跨设备与共享记忆必须自建存储同步和检索记忆流水线——按模型这属于主体能力禁区，不再是可移除薄层。",
    },
    "qm": {
        "scope": ["identity-map", "query-adapt", "provenance-adapt"],
        "mode": "plugin", "responsibility_uncontrolled": False,
        "rationale": "其 scoped memory/permissions/durable sandbox 已是主体；我方只做身份映射与查询/来源适配，不自建 ACL 或完整检索记忆流水线。",
    },
    "mem-vault": {
        "scope": ["full-retrieval-memory", "provenance-adapt"],
        "mode": "adapter", "responsibility_uncontrolled": False,
        "rationale": "sealed EVID 明确是纯 Markdown 文件同步、无索引/检索机制；R5.2 的可检索复用须自建完整检索或记忆流水线，触主体能力禁区。",
    },
    "ZAgenticOPN": {
        "scope": ["provenance-adapt", "state-transform"],
        "mode": "adapter", "responsibility_uncontrolled": False,
        "rationale": "结果五字段/Git provenance/scorecard 语义同构，仅需来源适配与状态映射薄层。",
    },
    "opencode-coordination": {
        "scope": ["coord-semantics-claim-lease", "provenance-adapt"],
        "mode": "adapter", "responsibility_uncontrolled": False,
        "rationale": "append-only ledger + board 提供审计 substrate；仅补 claim/lease 小型协调语义与来源适配薄层。",
    },
}

COST_FIELDS = ("initial_dev", "integration", "maintenance",
               "upstream_adapt", "ops", "security_gov")


# ---------------------------------------------------------------------------
# SoT 1: bundle (ratified 12 scenes)
# ---------------------------------------------------------------------------
b = json.load(open(BUNDLE, encoding="utf-8"))
scenes = {s["id"] for s in b["scene-set"]["scenes"]}
if len(scenes) != 12:
    die(f"expected 12 ratified scenes, got {len(scenes)}")

# ---------------------------------------------------------------------------
# SoT 2: baseline — all 5 EC definitions + their module chains
# ---------------------------------------------------------------------------
baseline = open(BASELINE_MD, encoding="utf-8").read()
for spec in EC_SPECS:
    if spec["ec"] not in baseline or spec["keyword"] not in baseline:
        die(f"baseline §4.1 definition not found for {spec['ec']} / {spec['keyword']}")
if len({r["id"] for r in R_SPLIT}) != len(R_SPLIT):
    die("duplicate R id in R_SPLIT")

# ---------------------------------------------------------------------------
# SoT 3: reuse ledger — (module, project) -> (verdict, EVID, hypothesis, pin)
# ---------------------------------------------------------------------------
ledger_md = open(LEDGER_MD, encoding="utf-8").read()
rows = {}
hypothesis_by_module = {}
version_by_proj = {}
for line in ledger_md.splitlines():
    m = re.match(r"^\|\s*(M\d+)\s*\|", line)
    if not m:
        continue
    cols = [c.strip() for c in line.split("|")]
    # ['', module, criterion_id, 模块, 项目, pin, verdict, evidence_refs, hypothesis, ...]
    if len(cols) < 9:
        continue
    mid, proj, verdict = cols[1], cols[4], cols[6]
    evids = re.findall(r"EVID::([0-9a-f]{24})", cols[7])
    rows[(mid, proj)] = {"verdict": verdict, "evids": evids}
    if mid in EXPECTED_MODULES:
        hypothesis_by_module[mid] = cols[8]

for mid in EXPECTED_MODULES:
    if mid not in hypothesis_by_module:
        die(f"module {mid} missing from reuse ledger")

# Q5a — excluded source projects must really be non-native on the stated module
for ec, exclusions in EXCLUDED_SOURCE_NOTES.items():
    for proj, mid in exclusions:
        row = rows.get((mid, proj))
        if row is None:
            die(f"Q5a exclusion {ec}/{proj}/{mid}: ledger row missing")
        elif row["verdict"] == "native":
            die(f"Q5a exclusion {ec}/{proj}/{mid}: actually native; note is wrong")

# ---------------------------------------------------------------------------
# SoT 4: sealed ledger index (EVID existence + source file)
# ---------------------------------------------------------------------------
evid_index = {}
evid_source = {}
wanted_by_repo = {repo_name: proj for proj, repo_name in REPO_NAME_BY_PROJ.items()}
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
                key = str(eid)[:24]
                evid_index.setdefault(key, os.path.relpath(_f, REPO))
                evid_source.setdefault(key, os.path.relpath(_f, REPO))
            repo_obj = o.get("repository")
            rev_obj = o.get("revision")
            if isinstance(repo_obj, dict) and isinstance(rev_obj, dict):
                proj = wanted_by_repo.get(repo_obj.get("name"))
                sha = rev_obj.get("sha")
                if proj and isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{40}", sha):
                    version_by_proj.setdefault(proj, sha)
            for v in o.values():
                _walk(v)
        elif isinstance(o, list):
            for v in o:
                _walk(v)

    _walk(_d)

for proj in CANDIDATES:
    sha = version_by_proj.get(proj, "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        die(f"candidate {proj}: no real 40-hex version in sealed ledger revision.sha: {sha!r}")

ledger_src_by_proj = {}
for proj in CANDIDATES:
    for (mid, p), row in rows.items():
        if p != proj or not row["evids"]:
            continue
        src = evid_source.get(row["evids"][0])
        if src:
            ledger_src_by_proj[proj] = src
            break
    if proj not in ledger_src_by_proj:
        die(f"candidate {proj}: sealed ledger source not resolvable from EVID")

# ---------------------------------------------------------------------------
# SCORES / HUMAN_FINAL coverage, then build L1 matrix per EC
# ---------------------------------------------------------------------------
spec_by_rid = {r["id"]: spec for spec in EC_SPECS for r in spec["r_split"]}
expected_cells_all = {(r["id"], p) for spec in EC_SPECS for r in spec["r_split"] for p in spec["candidates"]}
if set(SCORES) != expected_cells_all:
    die(f"SCORES cell set mismatch: missing={sorted(expected_cells_all - set(SCORES))} "
        f"extra={sorted(set(SCORES) - expected_cells_all)}")
for key, entry in SCORES.items():
    for fk in FACTOR_KEYS:
        v = entry.get(fk)
        if not isinstance(v, (int, float)) or isinstance(v, bool) or not 0.0 <= v <= 1.0:
            die(f"SCORES{key}.{fk} invalid: {v!r}")
    if not str(entry.get("rationale", "")).strip():
        die(f"SCORES{key} missing rationale")
    if not str(entry.get("by", "")).strip():
        die(f"SCORES{key} missing by")
if not set(HUMAN_FINAL) <= set(SCORES):
    die(f"HUMAN_FINAL has unknown cells: {sorted(set(HUMAN_FINAL) - set(SCORES))}")
for key, entry in HUMAN_FINAL.items():
    if not str(entry.get("rationale", "")).strip():
        die(f"HUMAN_FINAL{key} missing rationale")
    if human_action(entry) not in ("endorse", "raise_to_pass"):
        die(f"HUMAN_FINAL{key} unrecognized action")
for spec in EC_SPECS:
    cells = {(r["id"], p) for r in spec["r_split"] for p in spec["candidates"]}
    filled = cells & set(HUMAN_FINAL)
    if filled != cells:
        die(f"{spec['ec']} L3 must be fully endorsed by zj; missing={sorted(cells - filled)}")
ENDORSE_N = sum(1 for e in HUMAN_FINAL.values() if human_action(e) == "endorse")
RAISE_N = sum(1 for e in HUMAN_FINAL.values() if human_action(e) == "raise_to_pass")

results = {}
for spec in EC_SPECS:
    ec = spec["ec"]
    requirements, matrix, cell_meta = [], [], {}
    for r in spec["r_split"]:
        rid, mid = r["id"], r["module"]
        node_label = "EC-01 主闭环验收节点" if ec == "EC-01" else f"{ec} 验收节点"
        requirements.append({
            "id": rid,
            "statement": f"{r['node']}（{mid}，{node_label}）",
            "priority": "must",
            "critical": True,
            "acceptance": r["acceptance"],
        })
        for proj in spec["candidates"]:
            row = rows.get((mid, proj))
            if row is None:
                die(f"reuse ledger missing ({mid}, {proj})")
                continue
            if row["verdict"] != "native" or not row["evids"]:
                die(f"({mid}, {proj}) not sealed-native with EVID: verdict={row['verdict']}")
                continue
            if len(row["evids"]) > 1:
                die(f"({mid}, {proj}) row carries {len(row['evids'])} EVIDs — explicit selection required")
                continue
            eid = row["evids"][0]
            if eid not in evid_index:
                die(f"EVID::{eid} (R={rid}, O={proj}) not found in sealed ledger")
                continue
            score = SCORES[(rid, proj)]
            hf = HUMAN_FINAL.get((rid, proj))
            action = human_action(hf)
            action_note = {
                "endorse": "认同 L2 未满足（Human 接受该格未满足的结论，复核分留空、不改数值）",
                "raise_to_pass": "Human 判定可通过，复核分 = max(L2 eff, FIT_OK)：已合格保留原值、未合格抬至合格值",
                "pending": "待 zj 最终复核（not-ready，本轮不进拟合层判定）",
            }[action]
            hf_text = (f"by {hf.get('by', 'zj')}：{hf['rationale']}") if hf else "待 zj 最终复核（not-ready）"
            notes = (
                f"L1 客观打分 by {score['by']}（据本格 sealed EVID 原文，非模块级 hypothesis 档位）："
                f"{score['rationale']} "
                f"L3 Human 兜底：{hf_text}"
                f"（action={action}：{action_note}）。"
                "status=native 仅表示能力存在的 sealed 事实，三因子表示与我方需求的语义/组合拟合判断，二者语义不同。"
            )
            matrix.append({
                "R": rid,
                "O": proj,
                "coverage": score["coverage"],
                "semantic_match": score["semantic_match"],
                "composability": score["composability"],
                "status": "native",
                "evidence": f"EVID::{eid}",
                "notes": notes,
            })
            cell_meta[(rid, proj)] = {"score": score, "human": hf, "hyp": hypothesis_by_module[mid], "eid": eid}

    matrix_by_or = {}
    for cell in matrix:
        matrix_by_or.setdefault(cell["O"], {})[cell["R"]] = {
            k: cell[k] for k in ("coverage", "semantic_match", "composability", "status", "evidence", "notes")
        }
    results[ec] = {
        "spec": spec,
        "requirements": requirements,
        "matrix": matrix,
        "cell_meta": cell_meta,
        "matrix_by_or": matrix_by_or,
    }

if problems:
    print("FAIL (join invariants):", file=sys.stderr)
    for p in problems:
        print("  -", p, file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Load instrument
# ---------------------------------------------------------------------------
if not os.path.exists(CAPABILITY_FIT_PY):
    die(f"mother-model instrument not found: {CAPABILITY_FIT_PY}")
    print("FAIL:", problems, file=sys.stderr)
    sys.exit(1)
spec_cf = importlib.util.spec_from_file_location("capability_fit", CAPABILITY_FIT_PY)
cf = importlib.util.module_from_spec(spec_cf)
sys.modules[spec_cf.name] = cf
spec_cf.loader.exec_module(cf)

# Cost/adaptation draft: fail-closed checks against the instrument's own
# vocabularies; no free-text scope or unvalidated number may reach assess.
for proj in CANDIDATES:
    cd = COST_DRAFT.get(proj)
    ad = ADAPTATION_DRAFT.get(proj)
    if cd is None or ad is None:
        die(f"cost/adaptation draft missing for {proj}")
        continue
    for f in COST_FIELDS:
        v = cd.get(f)
        if not isinstance(v, (int, float)) or isinstance(v, bool) or v < 0:
            die(f"COST_DRAFT[{proj}].{f} invalid: {v!r}")
    if not str(cd.get("rationale", "")).strip():
        die(f"COST_DRAFT[{proj}] missing rationale")
    if not isinstance(ad.get("scope"), list) or not ad["scope"]:
        die(f"ADAPTATION_DRAFT[{proj}].scope invalid: {ad.get('scope')!r}")
    for s in ad["scope"]:
        if s not in cf.ALLOWED_ADAPT and s not in cf.FORBIDDEN_ADAPT:
            die(f"ADAPTATION_DRAFT[{proj}] unknown scope token: {s!r}")
    if ad.get("mode") not in sorted(cf.VALID_B_MODE):
        die(f"ADAPTATION_DRAFT[{proj}].mode invalid: {ad.get('mode')!r}")
    if not isinstance(ad.get("responsibility_uncontrolled"), bool):
        die(f"ADAPTATION_DRAFT[{proj}].responsibility_uncontrolled must be bool")
    if not str(ad.get("rationale", "")).strip():
        die(f"ADAPTATION_DRAFT[{proj}] missing rationale")


def build_fit_input(res, matrix_data):
    ec = res["spec"]["ec"]
    if ec == "EC-01":
        goal = "EC-01 主闭环（提交目标→拿到可验收结果）拆出的 4 条可独立验收需求 R1.1–R1.4 的开源能力拟合事实矩阵"
    else:
        goal = (f"{ec} {res['spec']['name']} 拆出的 {len(res['requirements'])} 条可独立验收需求 "
                f"的开源能力拟合事实矩阵")
    cands = res["spec"]["candidates"]
    return {
        "goal": goal,
        "requirements": res["requirements"],
        "candidates": [
            {
                "id": proj, "name": proj,
                "url": "(not present in sealed SoT; non-gated field)",
                "version": version_by_proj[proj],
                "license": "(not collected; non-gated field)",
            }
            for proj in cands
        ],
        "matrix": matrix_data,
        "cost": {proj: {k: COST_DRAFT[proj][k] for k in COST_FIELDS} for proj in cands},
        "adaptation": {proj: {
            "scope": list(ADAPTATION_DRAFT[proj]["scope"]),
            "mode": ADAPTATION_DRAFT[proj]["mode"],
            "responsibility_uncontrolled": ADAPTATION_DRAFT[proj]["responsibility_uncontrolled"],
            "poc_plan": "",
        } for proj in cands},
        "poc_plan": "",
    }


def fit_verdict(cell):
    eff = cf.effective_fit(cell)
    if cell.get("status") in (cf.STATUS_UNSUPPORTED, cf.STATUS_UNKNOWN):
        return "critical_gap", eff
    if eff < cf.FIT_FAIL:
        return "critical_gap", eff
    if cf.cell_satisfied(cell):
        return "satisfied", eff
    return "must_gap", eff


# classification input, verdicts, gates, recheck — per EC
for ec, res in results.items():
    spec = res["spec"]
    matrix_by_or_class = {}
    for proj in spec["candidates"]:
        matrix_by_or_class[proj] = {}
        for r in spec["r_split"]:
            rid = r["id"]
            src = res["matrix_by_or"][proj][rid]
            hf = HUMAN_FINAL.get((rid, proj))
            action = human_action(hf)
            new_cell = dict(src)
            if action == "raise_to_pass":
                eff_l1 = cf.effective_fit(src)
                rev = human_review_score(action, eff_l1, cf.FIT_OK)
                new_cell["coverage"] = 1.0
                new_cell["semantic_match"] = 1.0
                new_cell["composability"] = rev
                new_cell["notes"] = src["notes"] + (
                    f" [classification input] Q4a 两满一值映射 factors=[1.0,1.0,{rev:.3f}] "
                    f"= [1,1,max(L1 eff={eff_l1:.3f}, FIT_OK={cf.FIT_OK})]；eff 精确=FIT_OK、命中 satisfied。"
                )
            elif action == "endorse":
                new_cell["notes"] = src["notes"] + (
                    " [classification input] Q2a 认同 L2 未满足：三因子保持 L1 原值不变，不映射、不抬分。"
                )
            else:  # pending — Q4a: honest not-ready, never default to endorse
                new_cell["notes"] = src["notes"] + (
                    " [classification input] Q4a L3 pending：not-ready，三因子保持 L1 原值，"
                    "不进拟合层判定；不得默认『认同』或抬分。"
                )
            matrix_by_or_class[proj][rid] = new_cell

    # fail-closed mapping check
    for proj in spec["candidates"]:
        for r in spec["r_split"]:
            rid = r["id"]
            src = res["matrix_by_or"][proj][rid]
            dst = matrix_by_or_class[proj][rid]
            action = human_action(HUMAN_FINAL.get((rid, proj)))
            if action == "raise_to_pass":
                if not cf.cell_satisfied(dst) or abs(cf.effective_fit(dst) - cf.FIT_OK) > 1e-9:
                    die(f"classification mapping failed: {rid}/{proj} raise_to_pass not exactly FIT_OK")
                if dst["coverage"] != 1.0 or dst["semantic_match"] != 1.0:
                    die(f"classification mapping failed: {rid}/{proj} not two-full")
            else:  # endorse / pending — factors byte-equal to L1
                for fk in FACTOR_KEYS:
                    if src[fk] != dst[fk]:
                        die(f"classification mapping: {action} cell {rid}/{proj} factor {fk} changed")

    res["matrix_by_or_class"] = matrix_by_or_class
    res["input_l1"] = build_fit_input(res, res["matrix_by_or"])
    res["input_class"] = build_fit_input(res, matrix_by_or_class)

    res["verdict"] = {"l1": {}, "class": {}}
    for proj in spec["candidates"]:
        for r in spec["r_split"]:
            rid = r["id"]
            res["verdict"]["l1"][(rid, proj)] = fit_verdict(res["matrix_by_or"][proj][rid])
            if human_action(HUMAN_FINAL.get((rid, proj))) == "pending":
                res["verdict"]["class"][(rid, proj)] = ("not_ready", None)
            else:
                res["verdict"]["class"][(rid, proj)] = fit_verdict(matrix_by_or_class[proj][rid])

    res["gates_l1"] = {p: cf.run_gates(res["input_l1"], p) for p in spec["candidates"]}
    res["gates_class"] = {p: cf.run_gates(res["input_class"], p) for p in spec["candidates"]}
    # zjj DRAFT adoption classes — computed from the same instrument, on the
    # classification input only. NOT a zj ruling; rendered as a draft for review.
    res["assess"] = {p: cf.classify_candidate(res["input_class"], p) for p in spec["candidates"]}
    for label, gr in (("L1", res["gates_l1"]), ("classification", res["gates_class"])):
        for proj, gates in gr.items():
            for g in gates:
                if not g.ok:
                    die(f"mother-model GATE FAIL [{ec}/{label}] {proj}: {g.name}: {g.message}")

    res["recheck"] = {(c["R"], c["O"]): (cf.effective_fit(c), cf.cell_satisfied(c)) for c in res["matrix"]}

if problems:
    print("FAIL (mapping / fit-verdict / mother-model validate):", file=sys.stderr)
    for p in problems:
        print("  -", p, file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Emit per-EC input JSONs (EC-01 path/names unchanged from the sample)
# ---------------------------------------------------------------------------
for ec, res in results.items():
    out_dir = os.path.join(FIT_BASE, f"{ec.replace('-', '').lower()}-scaffold")
    os.makedirs(out_dir, exist_ok=True)
    for name, data in (("fit-input-l1.json", res["input_l1"]),
                       ("fit-input-classification.json", res["input_class"])):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")

# ---------------------------------------------------------------------------
# Emit supporting doc page
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
o.append("# 需求拟合矩阵 · 5 条 EC（supporting / 从基线拆 R）")
o.append("")
o.append("> 本页覆盖采纳的 EC-01/02/03/05/06，是**拟合事实矩阵 + 拟合层判定**，不是产品计划、不是采用裁决。")
o.append("> 由 `docs/reasearch/opn-cross-comparison/_gen_fit_matrix.py` 从横比 bundle / 复用证据账本 / 产品结构基线机械派生；")
o.append("> Human 决策以带 SoT 存在性校验的显式常量表注入，Agent 不推断验收判据、不预置分类。")
o.append("")

o.append("## 1. 边界与口径（zj 2026-11-24 裁决汇总）")
o.append("")
o.append("- **范围**：EC-01 样板 + EC-02/03/05/06 铺开（Q10a 样本验收后 zj 选①）。共 5 条 EC、15 条 R、43 个 R×O 单元（EC-01 8 格 + 新增 35 格，L3 已全部由 zj 兜底并回灌）。")
o.append("- **R 锚点**：锚 EC（Q1a），按 Human 可独立观察的验收节点切（Q6c/Q11a），不贴模块边界；模块只作归属标注。acceptance 由 Human 逐条校准（Q2a/Q3a）。")
o.append("- **候选 O（Q1a 铺开口径）**：每条 EC 只取该 EC 全模块 sealed-native 交集；严格闸门不放宽。EC-02=2 家、EC-03=3 家、EC-05=4 家、EC-06=5 家，加上 EC-01=2 家，共 16 个 EC×O 对。")
o.append("- **三层打分（Q7a）**：L1 客观打分（Agent 据本格 sealed EVID 原文评分 + 扣分理由）→ L2 机器复核（母模型仪器机械复算）→ L3 Human 兜底。模块级 hypothesis 只作参照，**不是打分来源**。")
o.append(f"- **L3 状态（全量回灌）**：{len(HUMAN_FINAL)}/{len(expected_cells_all)} 格均为 zj 逐格填写的原文（EC-01 8 格 + 新增 35 格），{ENDORSE_N} 格 `认同 L2 未满足`（endorse）、{RAISE_N} 格 `可以有`（raise_to_pass）。改动须改生成器 `HUMAN_FINAL` 常量表后重跑，不得手改产物。")
o.append("- **双输入（Q1a/Q5a）**：每 EC 一对 `fit-input-l1.json`（L1 原值）+ `fit-input-classification.json`（复核分派生因子）。路径 `tmp/skills-outputs/zj-open-source-capability-fit/ec01-scaffold/` 等（目录名去掉 EC 中的连字符），EC-01 文件名与路径均沿用样板。")
o.append("- **复核分进分类（Q3a/Q4a/Q6a）**：`可以有` 用两满一值 `[1.0,1.0,max(eff,FIT_OK)]`，eff 精确=FIT_OK；`认同 L2 未满足` 保持 L1 原值。判定只用母模型 `effective_fit`/`cell_satisfied`/`FIT_OK`/`FIT_FAIL`，**到拟合层为止，不出 A/B/C/D**。")
o.append("- **成本维度（本轮重开 Q9b）**：zjj 给出逐候选 cost/E + adaptation **初判**，由常量表写入两份输入；只对 classification 输入跑 `assess` 得**参考分类**（§5.3）。E 单位已由 zj 认可标注为「相对成本点（≈人日量级）」，**仅供参考**；数值与分类均为参考信号，**是否自研/采用由 zj 在规划-执行阶段人工判断**。")
o.append("- **priority/critical**：全部 R=`must` + `critical=true`（Q8a）。")
o.append("- **URL/license**：sealed SoT 未采集，填占位；非闸门字段。")
o.append("")

o.append("## 2. R 清单（5 条 EC，共 15 条）")
o.append("")
o.append("| EC | R | 验收节点（Human 可观察） | acceptance（Human 校准） | 归属模块 | priority | critical |")
o.append("|---|---|---|---|---|---|---|")
for spec in EC_SPECS:
    for r in spec["r_split"]:
        o.append(f"| {spec['ec']} | {r['id']} | {esc(r['node'])} | {esc(r['acceptance'])} | {r['module']} | must | true |")
o.append("")

o.append("## 3. 候选 O（按 EC 严格 native 交集）")
o.append("")
o.append("| EC | 候选 O | 版本（reuse ledger pin 实读 40-hex） | 来源 sealed ledger |")
o.append("|---|---|---|---|")
for spec in EC_SPECS:
    for proj in spec["candidates"]:
        o.append(f"| {spec['ec']} | {proj} | `{version_by_proj[proj]}` | `{ledger_src_by_proj[proj]}` |")
o.append("")

o.append("## 4. R×O 三层打分矩阵")
o.append("")
o.append("| EC | R | O | status | 客观打分 cov/sem/comp（L1） | 扣分理由（L1） | 机器复核 eff/满足（L2） | Human复核分（L3） | Human 兜底原文（L3） | evidence |")
o.append("|---|---|---|---|---|---|---|---|---|---|")
for ec, res in results.items():
    for r in res["spec"]["r_split"]:
        rid = r["id"]
        for proj in res["spec"]["candidates"]:
            cell = next(c for c in res["matrix"] if c["R"] == rid and c["O"] == proj)
            meta = res["cell_meta"][(rid, proj)]
            sc, hf = meta["score"], meta["human"]
            ef, sat = res["recheck"][(rid, proj)]
            score_str = f"{sc['coverage']:.2f}/{sc['semantic_match']:.2f}/{sc['composability']:.2f}"
            human_str = esc(hf["rationale"]) if hf else "待 zj 最终复核（not-ready）"
            action = human_action(hf)
            rev = human_review_score(action, ef, cf.FIT_OK)
            rev_str = f"{rev:.3f}" if rev is not None else ("—（认同 L2 未满足）" if hf else "—（pending）")
            o.append(
                f"| {ec} | {rid} | {proj} | {cell['status']} | {score_str} | {esc(sc['rationale'])} "
                f"| {ef:.3f} / {'满足' if sat else '未满足'} | {rev_str} | {human_str} | {cell['evidence']} |"
            )
o.append("")
o.append("### 三层说明（口径与边界）")
o.append("")
o.append("- **L1**：逐格读该 (R,O) 的 sealed EVID 原文后评分并写扣分理由（`SCORES` 常量表，含 `by`）。模块级 hypothesis 仅列作参照，不参与打分。")
o.append("- **L2**：母模型 `capability_fit.py` 的 `effective_fit`（cov×sem×comp）与 `cell_satisfied`，是**独立代码路径的机械复算**（抓手算漂移），不是第二意见——仪器无独立打分接口。")
o.append(f"- **L3**：`认同 L2 未满足`→endorse（复核分留空不改）；`可以有`→raise_to_pass。{len(HUMAN_FINAL)}/{len(expected_cells_all)} 格已由 zj 兜底（{ENDORSE_N} endorse / {RAISE_N} raise_to_pass）。")
o.append(f"- **Human复核分**：仅 `可以有` 格填 `max(L2 eff, FIT_OK)`；`FIT_OK={cf.FIT_OK}` 由仪器机械读取。此列已按 Q4a 落入 classification 输入，L1 原值不动。")
o.append("")
o.append("### 模块级 hypothesis（参照，非打分来源）")
o.append("")
o.append("| 模块 | reuse ledger hypothesis（assumption） | 为何不参与打分 |")
o.append("|---|---|---|")
for mid in EXPECTED_MODULES:
    o.append(f"| {mid} | {esc(hypothesis_by_module[mid])} | 模块级假设，无法区分同模块不同 O 的证据差异（如 M3: multica 有 Review gate、loop-now 仅插件信任分级） |")
o.append("")

o.append("## 5. 双输入 validate 闸门 + 拟合层判定（不出 A/B/C/D）")
o.append("")
o.append("### 5.1 validate G1–G6")
o.append("")
o.append("| EC | 输入 | O | 闸门 | 结果 | 说明 |")
o.append("|---|---|---|---|---|---|")
for ec, res in results.items():
    for label, gr in (("L1", res["gates_l1"]), ("classification", res["gates_class"])):
        for proj, gates in gr.items():
            for g in gates:
                o.append(f"| {ec} | {label} | {proj} | {esc(g.name)} | {'✓ PASS' if g.ok else '✗ FAIL'} | {esc(g.message)} |")
o.append("")
o.append("- 每 EC 一对输入 JSON，路径见 §1；均由生成器机械写出，禁止手改。")
o.append("- 两份输入均跑 `validate` G1–G6；`assess` 只对 classification 输入调用，产出**仅供参考的分类信号**（§5.3）。L1 输入不跑 assess，保留拟合层对照。")
o.append("")
o.append("### 5.2 两输入拟合层判定对照")
o.append("")
o.append(f"判定只用母模型 `effective_fit` / `cell_satisfied` / `FIT_OK({cf.FIT_OK})` / `FIT_FAIL({cf.FIT_FAIL})` 机械计算。43 格 L3 已全部裁决，class 判定对全部格计算，not_ready=0。")
o.append("")
o.append("| EC | R | O | L1 eff | L1 判定 | class eff | class 判定 | 变化 |")
o.append("|---|---|---|---|---|---|---|---|")
for ec, res in results.items():
    for r in res["spec"]["r_split"]:
        rid = r["id"]
        for proj in res["spec"]["candidates"]:
            v_l1, e_l1 = res["verdict"]["l1"][(rid, proj)]
            v_cl, e_cl = res["verdict"]["class"][(rid, proj)]
            if v_cl == "not_ready":
                change = "—（L3 pending）"
                cl_eff = "—"
                cl_txt = "not-ready"
            else:
                change = "—（保持）" if v_l1 == v_cl else f"{v_l1} → {v_cl}"
                cl_eff = f"{e_cl:.3f}"
                cl_txt = v_cl
            o.append(f"| {ec} | {rid} | {proj} | {e_l1:.3f} | {v_l1} | {cl_eff} | {cl_txt} | {change} |")
o.append("")
for ec, res in results.items():
    l1_counts = {k: 0 for k in ("satisfied", "must_gap", "critical_gap")}
    cl_counts = {k: 0 for k in ("satisfied", "must_gap", "critical_gap", "not_ready")}
    for v, _ in res["verdict"]["l1"].values():
        l1_counts[v] += 1
    for v, _ in res["verdict"]["class"].values():
        cl_counts[v] += 1
    o.append(f"- **{ec}**：L1 satisfied={l1_counts['satisfied']} / must_gap={l1_counts['must_gap']} / critical_gap={l1_counts['critical_gap']}；"
             f"class satisfied={cl_counts['satisfied']} / must_gap={cl_counts['must_gap']} / critical_gap={cl_counts['critical_gap']} / not_ready={cl_counts['not_ready']}。")
o.append("")
o.append("> `认同 L2 未满足` 格三因子不动，其 <FIT_FAIL 的格在两份输入里都如实为 `critical_gap`；`可以有` 格经两满一值映射后 eff 精确=FIT_OK、命中 `satisfied`。43 格全部参与 class 判定，not_ready=0。")
o.append("")

o.append("### 5.3 成本 / E 与采用分类参考信号（zjj 初判；仅供参考，非自研裁决）")
o.append("")
o.append(f"- **E 口径**：仪器硬编码 `E_LOW={cf.E_LOW:g}` / `E_MID={cf.E_MID:g}` / `E_HIGH={cf.E_HIGH:g}`；SSOT 只定义六分量、**未定义单位**，仪器自注「单位自定，跨候选须一致」。本初判用**相对成本点（≈人日量级）**，跨候选一致；**E 单位已由 zj 认可标注（2026-11-24），仅供参考**——它是估价尺度，不构成自研/采用的裁决依据。")
o.append("- **状态**：以下六分量、scope 与分类全部是 **zjj 初判 / 参考信号**，不是 zj 裁决；每条 rationale 锚到本矩阵已引用的 sealed EVID，EVID 未直接给工作量的地方显式标 `JUDGMENT`。**是否自研/采用由 zj 在规划-执行阶段人工判断，本页不裁决。**")
o.append("")
o.append("#### 5.3.1 逐候选 cost 六分量（相对成本点）")
o.append("")
o.append("| O | initial_dev | integration | maintenance | upstream_adapt | ops | security_gov | E | 依据 / JUDGMENT |")
o.append("|---|---|---|---|---|---|---|---|---|")
for proj in CANDIDATES:
    cd = COST_DRAFT[proj]
    e_total = sum(cd[k] for k in COST_FIELDS)
    cells = " | ".join(str(cd[k]) for k in COST_FIELDS)
    o.append(f"| {proj} | {cells} | {e_total:g} | {esc(cd['rationale'])} |")
o.append("")
o.append("#### 5.3.2 适配层边界（scope / mode）")
o.append("")
o.append("| O | scope | mode | 责任不可控 | 依据 |")
o.append("|---|---|---|---|---|")
for proj in CANDIDATES:
    ad = ADAPTATION_DRAFT[proj]
    flag = "是" if ad["responsibility_uncontrolled"] else "否"
    o.append(f"| {proj} | {esc(', '.join(ad['scope']))} | {ad['mode']} | {flag} | {esc(ad['rationale'])} |")
o.append("")
o.append("#### 5.3.3 assess 分类参考信号（仅 classification 输入）")
o.append("")
o.append("> `D` = 继续搜索（搜索循环回环态，非终态否决）；`B1/B2/B3` 按 mode 细分。分类是仪器**参考信号，仅供参考**；**是否自研/采用由 zj 在规划-执行阶段人工判断，本页不作裁决。**")
o.append("")
o.append("| EC | O | 推荐 | must 覆盖 | avg_fit | E | 关键缺口 | 主体能力触碰 | 主要依据 |")
o.append("|---|---|---|---|---|---|---|---|---|")
for ec, res in results.items():
    for proj in res["spec"]["candidates"]:
        a = res["assess"][proj]
        o.append(f"| {ec} | {proj} | {a.recommended} | {a.must_coverage:.0%} | {a.avg_fit:.3f} | {a.total_e:g} "
                 f"| {'是' if a.critical_gap else '否'} | {'是' if a.forbidden_touched else '否'} | {esc('; '.join(a.reasons[:2]))} |")
o.append("")
dist = Counter(a.recommended for res in results.values() for a in res["assess"].values())
o.append("- **分布（参考信号）**：" + " / ".join(f"{k}={v}" for k, v in sorted(dist.items())) + "。")
o.append("")

o.append("## 6. 缺口与待办清单")
o.append("")
filled_n = len(HUMAN_FINAL)
pending_n = len(expected_cells_all) - filled_n
o.append(f"- **L3 Human 兜底**：{filled_n}/{filled_n} 格已由 zj 逐格填写并机械回灌（EC-01 8 格 + 铺开 35 格；{ENDORSE_N} endorse / {RAISE_N} raise_to_pass）；本页为派生产物，手改会被重跑覆盖。")
o.append("- **Q5a 覆盖面说明**：Q1a 严格 native 交集把基线 §4.1 采纳该 EC 的部分素材项目挡在矩阵外；下表逐条列出，缺口经 reuse ledger 机械复核，标为非阻塞证据缺口，不改基线、不改 ratify bundle。")
o.append("")
o.append("| EC | 被排除素材项目 | 缺口模块 | ledger 实况 |")
o.append("|---|---|---|---|")
for spec in EC_SPECS:
    exclusions = EXCLUDED_SOURCE_NOTES.get(spec["ec"], [])
    if not exclusions:
        continue
    for proj, mid in exclusions:
        o.append(f"| {spec['ec']} | {proj} | {mid} | {rows[(mid, proj)]['verdict']}（native 闸门不放宽） |")
o.append("")
o.append("- **拟合层判定 ≠ 采用分类 ≠ 自研裁决**：§5.2 是拟合事实层，§5.3 是仪器基于初判 cost/E 给出的参考信号；是否自研/采用由 zj 在规划-执行阶段人工判断，本页两者都不裁决。")
o.append("- **成本/E 仅供参考**：E 单位已由 zj 认可标注（相对成本点，仅供参考）；§5.3 六分量、scope 与分类均为 zjj 初判参考信号，**不是自研/采用裁决**——该判断在规划-执行阶段由人工作出。")
o.append("- **83 个 unknown 未纳入**：Q1a 只选 sealed-native；unknown 证据缺口仍在基线 §6 与账本中，不被本矩阵掩盖。")
o.append("- **M3 Human 门语义冲突**：四种表达互不兼容（基线 §5）；R1.4 与各 O 的 EVID 逐格打分（multica 有 Review gate、loop-now 语义错配），语义裁决归后续规划阶段。")
o.append("")

o.append("## 7. 机械自检")
o.append("")
o.append(f"- EC {len(EC_SPECS)} 条；R {len(R_SPLIT)} 条；EC×O 对 {sum(len(s['candidates']) for s in EC_SPECS)} 个；矩阵单元 {sum(len(r['matrix']) for r in results.values())} 个（EC-01 8 + 铺开 35，全部 L3 已裁决），每单元 status=native 且 evidence 指向 sealed EVID。")
o.append(f"- 每个 cited EVID 均在 sealed ledger 索引中存在；所有候选版本均为 ledger pin 实读 40-hex，非手填。")
o.append(f"- `SCORES` 恰好覆盖 {len(expected_cells_all)} 个单元，每格三因子在 [0,1] 且含 rationale + by；无档位默认回退。")
o.append(f"- L3：{filled_n}/{filled_n} 格 zj 原文回灌（{ENDORSE_N} endorse / {RAISE_N} raise_to_pass）；classification 输入按 action 机械派生：endorse 三因子与 L1 逐值相等，raise_to_pass 两满一值 eff 精确=FIT_OK（fail-closed 校验）。")
o.append(f"- 复核分 action 由 zj 原文前缀机械派生（认同={sum(1 for e in HUMAN_FINAL.values() if human_action(e)=='endorse')} / 可以有={sum(1 for e in HUMAN_FINAL.values() if human_action(e)=='raise_to_pass')}）；Q4a 两满一值映射 eff 精确=FIT_OK={cf.FIT_OK}。")
o.append(f"- 拟合层判定仅用母模型 `effective_fit`/`cell_satisfied`/`FIT_OK`({cf.FIT_OK})/`FIT_FAIL`({cf.FIT_FAIL})；每 EC 两份输入 G1–G6 全 PASS；`assess` 仅对 classification 输入调用并产出仅供参考的分类信号（§5.3），是否自研由规划-执行阶段人工判断。")
o.append("- 本页 supporting；derived-from: opn.product-structure-baseline / opn.reuse-evidence-ledger / opn.module-matrix；不改写 ratify bundle。")
o.append("")

with open(DOC_OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o) + "\n")

gates_total = sum(
    sum(len(v) for v in res["gates_l1"].values()) + sum(len(v) for v in res["gates_class"].values())
    for res in results.values()
)
print(f"wrote {DOC_OUT}")
print(f"ECs={len(EC_SPECS)} R={len(R_SPLIT)} cells={sum(len(r['matrix']) for r in results.values())} "
      f"gates={gates_total} all_pass=True")
for ec, res in results.items():
    print(f"  {ec}: R={len(res['spec']['r_split'])} O={len(res['spec']['candidates'])} "
          f"cells={len(res['matrix'])}")
