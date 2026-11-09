#!/usr/bin/env python3
"""Emit a human-readable cross-comparison report markdown from bundle.json + metrics.json."""
import json, os

HERE = os.path.dirname(__file__)
b = json.load(open(os.path.join(HERE, "bundle.json"), encoding="utf-8"))
m = json.load(open(os.path.join(HERE, "metrics.json"), encoding="utf-8"))

SCENES = [s["id"].replace("SC::", "") for s in b["scene-set"]["scenes"]]
graphs = {g["project"]: g for g in b["graphs"]}
order = [g["project"] for g in b["graphs"]]
REPO = {"orca": "stablyai/orca", "loop-now": "AI-for-anyone/loop-now", "multica": "multica-ai/multica",
        "ZAgenticOPN": "jununfly/ZAgenticOPN", "herdr": "herdrdev/herdr", "qm": "yc-software/qm",
        "tasktrooper": "makifbaysal/tasktrooper", "opencode-coordination": "JF3Env/opencode-coordination",
        "agetor": "alamops/agetor", "lanes": "lanes-sh/app", "mozzie": "usemozzie/mozzie",
        "mem-vault": "songs-aaa/shared-memory-vault", "python-a2a": "themanojdesai/python-a2a",
        "dmux": "standardagents/dmux"}
# verdict matrix
matrix = {}
for de in b["difference-entries"]:
    matrix.setdefault(de["project"], {})[de["scene"].replace("SC::", "")] = de["verdict"]

def cell(v):
    return {"native": "●", "adapted": "◐", "unsupported": "✕", "unknown": "·"}.get(v, "?")

out = []
out.append("# 个人即协同网络 · 多项目场景锚定横比报告（过程材料 / PROVISIONAL）\n")
out.append("> 仪器：`zj-graphical-cross-comparison`。本报告由机械闸门 CHK-01..10 全过（0 ERROR / 0 WARN）后签发，"
           "但**固定场景集为 zj 草稿、待 ratify**，故在 zj 一句话认可前仅为过程材料，不是已签发横比报告。\n")
out.append("> **范围声明**：本仪器只产出「场景×项目」差异条目。\"以 orca 启动本项目\"的采用/启动裁决属母模型 "
           "`zj-open-source-capability-fit`，不在本报告内（见第 7 节回灌素材）。\n")

# 1. 项目图清单
out.append("## 1. 图清单与版本 pin\n")
out.append("| 项目 | 仓库 | 版本钉 |")
out.append("|---|---|---|")
for p in order:
    g = graphs[p]
    out.append(f"| {p} | `{REPO.get(p, g['project'])}` | `{g['version-pin']}` |")
out.append("")
out.append("域级上下文条目（旁挂，不进图）：")
for c in b["scene-set"]["context-entries"]:
    out.append(f"- **{c['id']}**（{c['kind']}）：{c['statement']}")

# 2. 场景集
out.append("\n## 2. 固定场景集（PROVISIONAL，待 zj ratify）\n")
out.append(f"- id：`{b['scene-set']['id']}`，version-pin：`{b['scene-set']['version-pin']}`")
out.append(f"- source：`{b['scene-set']['source']}`")
out.append(f"- derived-from-graphs：`{b['scene-set']['derived-from-graphs']}`（外部尺子，不来自任何项目图）\n")
out.append("| 场景 | 起点 → 终点 → 可观察结果 |")
out.append("|---|---|")
for s in b["scene-set"]["scenes"]:
    out.append(f"| `{s['id']}` | {s['start']} → {s['end']} → {s['observable']} |")

# 3. 差异矩阵
out.append("\n## 3. 差异条目矩阵（12 场景 × 14 项目）\n")
out.append("图例：● native（绑定 sealed Evidence） · unknown（证据缺口，附 verification-plan）· "
           "本集无 adapted / unsupported 条目（未见显式否定陈述，也未做适配判定）。\n")
hdr = "| 项目 | " + " | ".join(SCENES) + " |"
out.append(hdr)
out.append("|---" * (len(SCENES) + 1) + "|")
for p in order:
    row = [p] + [cell(matrix.get(p, {}).get(s)) for s in SCENES]
    out.append("| " + " | ".join(row) + " |")
out.append("")

# coverage count line
out.append("各项目 native 场景数：")
for p in order:
    n = sum(1 for v in matrix.get(p, {}).values() if v == "native")
    out.append(f"- {p}: **{n}/12**")

# 4. 可选场景集核对
out.append("\n## 4. 可选场景集核对留痕（Human 盲区核对）\n")
out.append(b["optional-scene-pool-review"]["notes"])

# 5. 等价裁决
out.append("\n## 5. 场景内语义等价裁决记录\n")
out.append("未裁决任何场景内语义等价（等价需引用双方 acceptance 且由 Human 裁决）。"
           "例如 qm 与 ZAgenticOPN 均覆盖 `identity-scope` 但语义互不相容——qm 是\"每人每房一个 scope\"，"
           "ZAgenticOPN 是 `Human→device→agent_instance`，**不得判等价**，只能各自保留为 unknown/待裁决。")

# 6. 指标
out.append("\n## 6. 摘要指标（display-only，不参与结论）\n")
out.append("> `not_for_conclusion=true`，`usage=display-only`。不得用于排序 / 裁决 / 回灌 / 优先级。\n")
out.append("| 项目 | 证据绑定覆盖 | 竖切片覆盖 | 共享度 | SCC | 最大依赖闭包 |")
out.append("|---|---|---|---|---|---|")
for g in m["graphs"]:
    out.append(f"| {g['project']} | {g['evidence-binding-coverage']} | {g['slice-coverage']} | "
               f"{g['sharing-degree']} | {g['scc-size-distribution']} | {g['max-dependency-closure']} |")
out.append(f"\n未决存量（undecided-stock）：{m['undecided-stock']}")

# 7. 回灌素材
out.append("\n## 7. 与母模型的可选回灌素材（非采用裁决）\n")
out.append("以下供 `zj-open-source-capability-fit` 在后续做 R×O 矩阵时消费；**本报告不产采用裁决**。\n")
out.append("- **orca 作为 startup 种子（L2 执行编排层证据最齐）**：在 `execution-workspace`(4 Evidence)、"
           "`runtime-integration`(2)、`agent-protocol`(1)、`result-provenance`(1)、`config-strategy`(1)、"
           "`tech-design`(1) 均为 native——契合\"以 orca 启动\"的设想，因为它补齐的是**执行/编排层**而非控制面。")
out.append("- **控制面语义须自研（痛点 2 的 0→1 集中处）**：orca 在 `task-workitem` / `identity-scope` / "
           "`session-context` / `approval-human` / `memory-knowledge` / `observability` 全部 unknown；"
           "这与 charter 痛点 2 一致——工作量集中在**语义所有权层**，不能直接复用现成实现。")
out.append("- **ZAgenticOPN（参照物）强在 L1 语义所有权**：`task-workitem`/`identity-scope`/`approval-human`/"
           "`result-provenance`/`memory-knowledge`/`observability` 均为 native，与 orca 互补而非替代。")
out.append("- **multica / loop-now 已 collect 取 12/12 sealed Evidence（本轮补采）**：multica 偏多-agent 团队/权限/集成"
           "（workspaces/squads/autopilots cron、Slack-Feishu-Lark 集成、Go+PostgreSQL17+Next.js），loop-now 偏本地桌面 agent 编排"
           "（Go server+SQLite+React、desktop app/Docker、plugins 无 sandbox 执行代码）。两者均可作执行编排层参照，但："
           "① multica 弱证据已解决：原 5 条因 keyword 路径子串误命中 docs/lark-*.md（谈媒体/配额维护）被判 native 仅因有 sealed ID；"
           "现全部 12 场景统一锚定根 README.md（canonical/英文/切题），5 条摘录已复核为对应场景原文（review gate / assign issue / squads / diff 连 issue / 运行成本）；"
           "② 两者均存在版本钉偏差（请求 tag v0.8.1 / v0.2.0 ≠ 实际钉到的 main HEAD），引用前须注意版本。")

# 8. 自检
out.append("\n## 8. 完成标准自检\n")
out.append("- 第三方 Agent 可凭 `bundle.json` 的 `difference-entries` 逐条复核：每条含 `scene`/`project`/`verdict`/"
           "`evidence-refs`（native）或 `verification-plan`（unknown）。")
out.append("- 来源三类区分：**evidence**=原生绑定 sealed Evidence ID；**human-ruling**=场景集与场景映射由 zj 给定；"
           "**assumption**=第 7 节回灌素材为分析层推断。")
out.append("- ⚠️ **签发前阻塞项**：固定场景集（`SCENE-SET::zopn-v1`）为 zj 草稿，需 zj 一句话 ratify 后方从\"过程材料\"升为\"已签发横比报告\"。")

with open(os.path.join(HERE, "REPORT.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("wrote REPORT.md")
