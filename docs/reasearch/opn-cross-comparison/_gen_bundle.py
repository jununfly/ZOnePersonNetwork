#!/usr/bin/env python3
"""Generate the zj-graphical-cross-comparison bundle for ZOnePersonNetwork launch study.

Evidence base (all commit-pinned sealed Evidence IDs):
- 10 opn-landscape repos + ZAgenticOPN: docs/reasearch/opn-landscape/2026-11-08-module-matrix.md
- orca: docs/reasearch/orca/2026-11-08-findings.md (v2 sealed ledger)
- herdr: docs/reasearch/herdr/2026-11-08-findings.md (v2 sealed ledger)
- loop-now: fresh primary-source read of README@v0.2.0 (NON-sealed -> all unknown w/ verification-plan)

Scene set is a HUMAN-GIVEN DRAFT (translated from zj's 2026-11-08 charter module draft +
opn-landscape 13-dimension brief). Marked PROVISIONAL / pending zj ratification.
"""
import json
import os

OUT = os.path.join(os.path.dirname(__file__), "bundle.json")

# ---------------------------------------------------------------------------
# 12 scenes (Human-given draft). Each observable: start -> end -> observable.
# Maps 1:1 to opn-landscape module dimensions (minus ref-capability-map).
# ---------------------------------------------------------------------------
SCENES = {
    "task-workitem": {
        "start": "用户想让一个或多个 Agent 协作完成一件可追踪的工作",
        "end": "该工作以可推进的状态存在于协作面板上，可被认领与流转",
        "observable": "工作项可见、状态机可前进（如 available→claimed→…→completed）",
    },
    "identity-scope": {
        "start": "需要把人、Agent、设备组织进一个协作 scope",
        "end": "成员与 scope 边界被定义且可鉴权",
        "observable": "身份/成员/scope 可被查询且权限生效",
    },
    "session-context": {
        "start": "一次协作需要跨多轮/多 Agent 携带上下文",
        "end": "上下文被建立、携带并在中断后恢复",
        "observable": "恢复后上下文一致、不丢状态",
    },
    "execution-workspace": {
        "start": "Agent 需要执行一个任务",
        "end": "任务在隔离工作区完成，资源被编排分配",
        "observable": "执行在隔离边界内发生、互不污染",
    },
    "approval-human": {
        "start": "Agent 产出需要人工确认或存在高风险动作",
        "end": "人工 gate 被触发、决策被记录",
        "observable": "审批/拒绝/干预可审计、有账本",
    },
    "result-provenance": {
        "start": "任务产生结果与产物",
        "end": "结果被 review、附 provenance 并验收",
        "observable": "产物可复核、来源可追溯",
    },
    "memory-knowledge": {
        "start": "协作中产生可复用事实/经验",
        "end": "知识被沉淀、可检索、可复用",
        "observable": "检索命中既有知识、复用生效",
    },
    "observability": {
        "start": "需要诊断一次协作发生了什么",
        "end": "状态可视化、事件可回放",
        "observable": "事件流/状态可重放、可定位",
    },
    "config-strategy": {
        "start": "需要定义规则/skill/版本策略",
        "end": "策略被加载并约束行为",
        "observable": "策略生效、版本偏斜被管控",
    },
    "runtime-integration": {
        "start": "需要在某主机/平台部署并随上游升级",
        "end": "运行时被安装、可升级、host adapter 工作",
        "observable": "安装成功、升级可用、跨平台可运行",
    },
    "agent-protocol": {
        "start": "多个 Agent 需要彼此通信或被发现",
        "end": "消息/契约被交换、Agent 可发现",
        "observable": "Agent 间能交换结构化消息或经协议发现",
    },
    "tech-design": {
        "start": "需要评估项目的工程设计与质量门",
        "end": "核心循环/持久化/工具面/测试门被声明",
        "observable": "技术设计事实可核验、质量门可观察",
    },
}

# ---------------------------------------------------------------------------
# Projects: coverage[scene] = list of sealed Evidence IDs (native) or None (unknown)
# ---------------------------------------------------------------------------
P = {}

P["orca"] = {
    "repo": "stablyai/orca",
    "pin": "v1.4.253 @ 27eb5e2a6c5017c6fdcba4fee16bf54256550c6f",
    "url": "https://github.com/stablyai/orca",
    "coverage": {
        "task-workitem": None,
        "identity-scope": None,
        "session-context": None,
        "execution-workspace": ["2ed6d70d48ae1d10a19026a0", "75e13f823450ea22d6c7f09f",
                                 "3dc1ea964ea53bfbc291171d", "0a6cfe851c86d1535e2d2fdc"],
        "approval-human": None,
        "result-provenance": ["a16d037b586eabaa4c616d4a"],
        "memory-knowledge": None,
        "observability": None,
        "config-strategy": ["17641629769edf434adb6a32"],
        "runtime-integration": ["0a6cfe851c86d1535e2d2fdc", "65802a5a91d96fbb669449e8"],
        "agent-protocol": ["d716c3704d37f7d2b36d2a19"],
        "tech-design": ["bde86e5bbc69853b1656c85c"],
    },
    "contexts": [
        {"id": "CTX::orca-daily-release", "scope": "project", "kind": "constraint",
         "statement": "orca 日更发布，changelog 才是真实特性清单，特性列表非稳定契约",
         "evidence-ref": "2ed6d70d48ae1d10a19026a0/17641629769edf434adb6a32 (sealed)"},
        {"id": "CTX::orca-privacy", "scope": "project", "kind": "constraint",
         "statement": "隐私姿态仅以文档链接形式声明，telemetry 实际行为未实测",
         "evidence-ref": "be542a3a9b72fd240e344418 (sealed, README only)"},
    ],
}

P["herdr"] = {
    "repo": "herdrdev/herdr",
    "pin": "master ee5bfb5041bb3e4a49d591c72308aae3c81ecdde",
    "url": "https://github.com/herdrdev/herdr",
    "coverage": {
        "task-workitem": None,
        "identity-scope": None,
        "session-context": ["8108ad662e318f347dfb172f"],
        "execution-workspace": ["47182a0e1869703551a60363", "e3545bea44fa352f51b5393e",
                                "905629f76105cc74192dc7ba"],
        "approval-human": None,
        "result-provenance": None,
        "memory-knowledge": None,
        "observability": ["be630dc8ed685d364a63d139", "7f5eae80cae7a1a16ebadf0e"],
        "config-strategy": ["6965f9991cffb4f28ee08f14", "ffe7879a993380564295355d"],
        "runtime-integration": ["daac3c9036fb77b32c5b40bf", "1590f5d5483d72a8fcdeaee5",
                                "90e06efa6fd8bbd7d30dfa16"],
        "agent-protocol": ["e3545bea44fa352f51b5393e", "43a2fb182ecb9f6306f7c1d5"],
        "tech-design": ["96de34e84950a4b0c05ef927", "4e2792d94dc3f81c170c6368",
                        "43a2fb182ecb9f6306f7c1d5", "ca1d50cb753ed7b8ed717692"],
    },
    "contexts": [
        {"id": "CTX::herdr-pr-gate", "scope": "project", "kind": "external-dep",
         "statement": "上游不接受 unsolicited implementation PR，定制/修复几乎只能 fork，ownership cost 高",
         "evidence-ref": "herdr CONTRIBUTING.md (non-sealed, findings §non-sealed)"},
    ],
}

P["ZAgenticOPN"] = {
    "repo": "jununfly/ZAgenticOPN",
    "pin": "2ff40cc052aae12fc7a324f89691e9f194985d24",
    "url": "https://github.com/jununfly/ZAgenticOPN",
    "coverage": {
        "task-workitem": ["3f9dde435394108a69009858"],
        "identity-scope": ["37c46d46405b7d6055e568d5"],
        "session-context": None,
        "execution-workspace": None,
        "approval-human": ["06b3135da98d7a9bec7b65a9"],
        "result-provenance": ["ddea4d90bb2b7e250b08b616"],
        "memory-knowledge": ["1b866cefa58726959ce1cd73"],
        "observability": ["0a8445acfd470fba8cb2c18a"],
        "config-strategy": ["6814fc75fc59e1f02bb5f756"],
        "runtime-integration": ["5da1a8117f4c7765b67113c4"],
        "agent-protocol": None,
        "tech-design": None,
    },
    "contexts": [
        {"id": "CTX::zagenticopn-capability-map", "scope": "project", "kind": "constraint",
         "statement": "参照物能力地图把 qm 列为 L3 运行时/资源层可抽取单位能力来源，但不能替代 Work Item authority",
         "evidence-ref": "984e472faa61310787ad09a9 (sealed, ref-capability-map)"},
    ],
}

# opn-landscape matrix repos (sealed Evidence IDs from module-matrix §3)
P["qm"] = {
    "repo": "yc-software/qm", "pin": "605c259b28d54ee750c526b11925ddea3e0e6f59",
    "url": "https://github.com/yc-software/qm",
    "coverage": {
        "task-workitem": None,
        "identity-scope": ["114f13c4c8afc8424cdc1971"],
        "session-context": ["1fcc9288e24457d7fa94240e"],
        "execution-workspace": None,
        "approval-human": ["c8500b3857eb0e93cc9d25d3"],
        "result-provenance": ["fec47fe206b51915b2e19fb4"],
        "memory-knowledge": ["e878e5271a78993966d88f0b"],
        "observability": ["b30ee3590bb6aaead44befb3"],
        "config-strategy": ["ad01939f1a7e220edf96928f"],
        "runtime-integration": ["3ae4f38b4de2d1769a598bc0"],
        "agent-protocol": None,
        "tech-design": ["e38a7af1b2e8472ed82f40dd"],
    },
    "contexts": [],
}
P["tasktrooper"] = {
    "repo": "makifbaysal/tasktrooper", "pin": "ae5fb965c4758bbb25d2fac7f10f9bb26cb63823",
    "url": "https://github.com/makifbaysal/tasktrooper",
    "coverage": {
        "task-workitem": ["90b8b4fc0e74bc12214889c4"],
        "identity-scope": ["4a0faa66eee9f3c15434dc32"],
        "session-context": None,
        "execution-workspace": None,
        "approval-human": None,
        "result-provenance": None,
        "memory-knowledge": ["d2423363b8e0d64ec8ce61cc"],
        "observability": ["6a0463be6d4575650cc64979"],
        "config-strategy": None,
        "runtime-integration": ["e9a31903a5338a7b6eae212a"],
        "agent-protocol": None,
        "tech-design": ["834655c524dca5a255ddaf1f"],
    },
    "contexts": [],
}
P["opencode-coordination"] = {
    "repo": "JF3Env/opencode-coordination", "pin": "2c9dd06f21716d8fc5885a266b119e58e78f2a0d",
    "url": "https://github.com/JF3Env/opencode-coordination",
    "coverage": {
        "task-workitem": ["9101cfa7145332b317a9353e"],
        "identity-scope": ["0b5fa995933066879753a0a5"],
        "session-context": None,
        "execution-workspace": None,
        "approval-human": ["1a1c6d9852edef2c3f970f42"],
        "result-provenance": ["01ccf2212f91bcc504af0818"],
        "memory-knowledge": None,
        "observability": ["d537234df40dcab3100b4eac"],
        "config-strategy": None,
        "runtime-integration": None,
        "agent-protocol": ["4e9888715cf937cdeac6384a"],
        "tech-design": None,
    },
    "contexts": [],
}
P["agetor"] = {
    "repo": "alamops/agetor", "pin": "897b70afb6f7671dc418c6d1053dbf8fbc3c81e0",
    "url": "https://github.com/alamops/agetor",
    "coverage": {
        "task-workitem": None,
        "identity-scope": None,
        "session-context": ["7d2249b75c4ec5bac9284bda"],
        "execution-workspace": ["e6275d13fae90b3ea49ca276"],
        "approval-human": None,
        "result-provenance": None,
        "memory-knowledge": None,
        "observability": ["74a1e19ab3d67925c43d706c"],
        "config-strategy": None,
        "runtime-integration": ["f44a67122e779c35ee472959"],
        "agent-protocol": None,
        "tech-design": ["c699464bb705742695f91592"],
    },
    "contexts": [],
}
P["lanes"] = {
    "repo": "lanes-sh/app", "pin": "7b9cb385d1100ded8a74986f81472f8856840578",
    "url": "https://github.com/lanes-sh/app",
    "coverage": {
        "task-workitem": ["fc77e9f1b10477d753e74fab"],
        "identity-scope": None,
        "session-context": None,
        "execution-workspace": ["a8434e60ad92db78fedb7af2"],
        "approval-human": None,
        "result-provenance": None,
        "memory-knowledge": ["ff178faee6ce5a1a5106b9e2"],
        "observability": None,
        "config-strategy": None,
        "runtime-integration": ["d9b7b1edd17eeefaa26756c3"],
        "agent-protocol": None,
        "tech-design": None,
    },
    "contexts": [],
}
P["mozzie"] = {
    "repo": "usemozzie/mozzie", "pin": "80f3515684722a8909fbc0c17a0526664ec0349a",
    "url": "https://github.com/usemozzie/mozzie",
    "coverage": {
        "task-workitem": ["14bb8d6ea36e18107fd51b3c"],
        "identity-scope": None,
        "session-context": None,
        "execution-workspace": ["6676d3f26c9b4f77443c5d2a"],
        "approval-human": ["3e8488d208de54fdd00a11c0"],
        "result-provenance": ["0b70106e3349d69e694526f5"],
        "memory-knowledge": None,
        "observability": None,
        "config-strategy": None,
        "runtime-integration": None,
        "agent-protocol": None,
        "tech-design": None,
    },
    "contexts": [],
}
P["mem-vault"] = {
    "repo": "songs-aaa/shared-memory-vault", "pin": "59f0b12134622c0ad93ef59ef6373cfe587deaf3",
    "url": "https://github.com/songs-aaa/shared-memory-vault",
    "coverage": {
        "task-workitem": None,
        "identity-scope": None,
        "session-context": ["151608571341f37ee2297dcb"],
        "execution-workspace": None,
        "approval-human": None,
        "result-provenance": None,
        "memory-knowledge": ["1eedaed644a280db74133572"],
        "observability": None,
        "config-strategy": None,
        "runtime-integration": None,
        "agent-protocol": None,
        "tech-design": ["de5482ebaca9a76160284089"],
    },
    "contexts": [],
}
P["python-a2a"] = {
    "repo": "themanojdesai/python-a2a", "pin": "40b969a465f85e8156793b7cfac16c5e23ed0b86",
    "url": "https://github.com/themanojdesai/python-a2a",
    "coverage": {
        "task-workitem": None,
        "identity-scope": None,
        "session-context": None,
        "execution-workspace": None,
        "approval-human": None,
        "result-provenance": None,
        "memory-knowledge": None,
        "observability": None,
        "config-strategy": ["8a03946eaf6653ada1427dc9"],
        "runtime-integration": None,
        "agent-protocol": ["5d423995e3d4b2ed0d8aab78"],
        "tech-design": None,
    },
    "contexts": [],
}
P["dmux"] = {
    "repo": "standardagents/dmux", "pin": "8cb3d926631a9349ab67f7ece41d218427ac7e24",
    "url": "https://github.com/standardagents/dmux",
    "coverage": {
        "task-workitem": None,
        "identity-scope": None,
        "session-context": None,
        "execution-workspace": ["205fcc6c54e6dcc370eeeb85"],
        "approval-human": None,
        "result-provenance": None,
        "memory-knowledge": None,
        "observability": None,
        "config-strategy": None,
        "runtime-integration": None,
        "agent-protocol": None,
        "tech-design": None,
    },
    "contexts": [],
}
P["loop-now"] = {
    "repo": "AI-for-anyone/loop-now",
    "pin": "main @ b7d6811877e6d7341ac539934ae87028df87b1e6 (collected HEAD; requested tag v0.2.0 = 8f504f61e8db628dacb52a4a00e6dc29567aa5af, collect ignores brief.repositories[].revision)",
    "url": "https://github.com/AI-for-anyone/loop-now",
    "coverage": {
        "task-workitem": ["3605745b0cae1cc75dd59c80"],
        "identity-scope": ["04f8095af68eacbb57dceb95"],
        "session-context": ["fc13fdb5c6a479f214a8e2a7"],
        "execution-workspace": ["598de2204e4d84a75a0020d4"],
        "approval-human": ["d3d21a128f2d058198f00504"],
        "result-provenance": ["0794e7e8dbb753920bae8a05"],
        "memory-knowledge": ["5d1c4de928a7b36251220b69"],
        "observability": ["033b3e9e285ecc2cfabae1c4"],
        "config-strategy": ["8c6bfd4d937cb7ce3db39c7c"],
        "runtime-integration": ["56ca86a50db2ccf35d17f401"],
        "agent-protocol": ["9dc520a2e8d7dc377efa824a"],
        "tech-design": ["d9483e0eea626b05f453e1a3"],
    },
    "contexts": [
        {"id": "CTX::loopnow-pin-deviation", "scope": "project", "kind": "constraint",
         "statement": "钉偏差（不静默接受）：请求 collect 钉 v0.2.0(8f504f61e8db628dacb52a4a00e6dc29567aa5af)，但 collect 路径完全忽略 brief.repositories[].revision（researchBriefFingerprint 归一化只留 owner/name；resolveRevision 恒用 default_branch），实际钉到 main HEAD b7d6811877e6d7341ac539934ae87028df87b1e6。本结论由 collect/test_tag_pin.py 红测实证。Evidence 有效但版本钉≠请求 tag。",
         "evidence-ref": "collect/ledger-loop-now.json repositories[].revision=b7d6811877e6d7341ac539934ae87028df87b1e6 (main)"},
        {"id": "CTX::loopnow-no-sandbox", "scope": "project", "kind": "constraint",
         "statement": "插件直接执行代码，无 sandbox；安装源须可信（README 明确「no sandbox: plugins execute code, install sources you trust」）",
         "evidence-ref": "loop-now README@v0.2.0 / plugins/SPEC.md (sealed)"},
        {"id": "CTX::loopnow-signals", "scope": "project", "kind": "constraint",
         "statement": ("sealed 后确认覆盖：tasks/workflow/Manager 协调(任务流转)、Build a team/Organize agents by project/permissions/tool access(身份 scope)、"
                       "Keep work in context/regular conversation/workspace/session(会话上下文)、working directory/LOOP_NOW_WORK_ROOT/runs on your machine(执行工作区)、"
                       "Reviewer/review/Ask me through Inbox(人工审批)、saved artifacts/delivery/messages(结果 provenance)、"
                       "Skills/project instructions(知识复用)、inspect tool calls/run timeline/model usage(可观测)、"
                       "plugins/configSchema/x-scope: project/Global settings(配置策略)、desktop app/Docker Compose/SQLite/loopctl(运行时集成)、"
                       "Inbox/subscribe to events/plugin-host-protocol/RPC(agent 协议)、Go server/SQLite/React+TypeScript+Vite/architecture(技术设计)"),
         "evidence-ref": "collect/ledger-loop-now.json (sealed)"},
    ],
}

P["multica"] = {
    "repo": "multica-ai/multica",
    "pin": "main @ 41885a6d816834663dad8e6944658e2ac8555844 (collected HEAD; requested tag v0.8.1 = b1ea927def64, collect ignores brief.repositories[].revision)",
    "url": "https://github.com/multica-ai/multica",
    "coverage": {
        "task-workitem": ["a67400762c931df62135608d"],
        "identity-scope": ["13e2a530ce5b9d6344871613"],
        "session-context": ["fcf4cce4e1d126ce88bdffec"],
        "execution-workspace": ["76fd261e3f84f3c9e33a84c6"],
        "approval-human": ["2cc46ac299adc52b807b122e"],
        "result-provenance": ["5c1fa749e640c3dec0dbd328"],
        "memory-knowledge": ["0c8c6d5548bf9d364a4fec2b"],
        "observability": ["71dfad6640e6f45a720f8a69"],
        "config-strategy": ["fb5092388de5fedd9b3c1581"],
        "runtime-integration": ["8d8aec7e4652ff51053e99ec"],
        "agent-protocol": ["8a9c13151d95b91275e847a8"],
        "tech-design": ["153a37839b2cad51bf212d2d"],
    },
    "contexts": [
        {"id": "CTX::multica-pin-deviation", "scope": "project", "kind": "constraint",
         "statement": "钉偏差（不静默接受）：请求 collect 钉 v0.8.1(b1ea927def64)，但 collect 路径完全忽略 brief.repositories[].revision（researchBriefFingerprint 归一化只留 owner/name；resolveRevision 恒用 default_branch），实际钉到 main HEAD 41885a6d81（v0.8.1 之后约 2 天）。本结论由 collect/test_tag_pin.py 红测实证。Evidence 有效但版本钉≠请求 tag；若要钉具体 release 须改编译器 collect（接入 brief revision）而非改 brief 形状。",
         "evidence-ref": "collect/ledger-multica.json repositories[].revision=41885a6d81 (main)"},
        {"id": "CTX::multica-evidence-anchored", "scope": "project", "kind": "constraint",
         "statement": "弱证据已解决（v2→v3 brief 迭代）：原 5 条 Evidence 因 keyword 路径子串误命中 docs/lark-*.md（谈媒体/配额维护）被判 native 仅因有 sealed ID；现全部 12 场景统一锚定根 README.md（canonical/英文/切题），用路径唯一 keyword 'readme.md'（不匹配 README.ja/zh，也不匹配 Dockerfile）强制选取，5 条摘录已复核为对应场景原文（review gate / assign issue / squads / diff 连 issue / 运行成本）。multica 更深能力文档在 server/internal/service/builtin_skills/multica-platform/references/*.md，但不在 docs/ 下、非 canonical，进不了 sealed ledger，如需更细证据须带外一手阅读。",
         "evidence-ref": "collect/ledger-multica.json (sealed, all README.md)"},
        {"id": "CTX::multica-signals", "scope": "project", "kind": "constraint",
         "statement": ("sealed 后确认覆盖：issues/board + assign(任务流转)、team/members/roles/access-scopes/security-model(身份与 scope)、"
                       "projects 挂载 repo+doc 上下文 + 运行内对话(会话上下文)、local daemon runtime 在你的机器(执行工作区)、"
                       "review gate + Inbox(人工审批)、diff/PR 挂回 issue(结果 provenance)、Skills 可复用 playbook(知识复用)、"
                       "Execution log 可重放 + usage analytics(可观测)、workspaces/squads/autopilots cron/Slack-Feishu-Lark 集成(配置策略)、"
                       "self-host Docker/Helm + desktop/mobile/web + 26 CLI(运行时集成)、Go backend(Chi+WebSocket)+PostgreSQL17+Next.js16+CI(技术设计)"),
         "evidence-ref": "collect/ledger-multica.json (sealed)"},
        {"id": "CTX::multica-license", "scope": "project", "kind": "constraint",
         "statement": ("授权为 Multica License（Apache-2.0 全文 + 附加条件：覆盖托管服务、商业内嵌、品牌使用）；"
                       "非纯 OSS，自托管/修改/构建允许，但商业分发与品牌需看 LICENSE/NOTICE — 采用候选须评估"),
         "evidence-ref": "multica LICENSE/NOTICE@main (sealed)"},
    ],
}

# ---------------------------------------------------------------------------
# Build bundle
# ---------------------------------------------------------------------------
graph_order = ["orca", "loop-now", "multica", "ZAgenticOPN", "herdr", "qm", "tasktrooper",
               "opencode-coordination", "agetor", "lanes", "mozzie", "mem-vault",
               "python-a2a", "dmux"]

graphs = []
scene_mapping = []
difference_entries = []
for proj in graph_order:
    info = P[proj]
    nodes = []
    slices = []
    deps = []
    for scene, cov in info["coverage"].items():
        if cov is None:
            continue
        f_id = f"F::{scene}"
        t_id = f"T::{scene}-impl"
        nodes.append({"id": f_id, "kind": "feature",
                      "statement": SCENES[scene]["start"],
                      "acceptance": SCENES[scene]["observable"], "evidence-ref": ""})
        nodes.append({"id": t_id, "kind": "capability",
                      "statement": f"{proj} 在该场景的实现能力单元",
                      "acceptance": SCENES[scene]["observable"], "evidence-ref": f"EVID::{cov[0]}"})
        s_id = f"S::{scene}"
        slices.append({
            "id": s_id,
            "members": [f_id, t_id],
            "scenario": {
                "start": SCENES[scene]["start"],
                "end": SCENES[scene]["end"],
                "observable": SCENES[scene]["observable"],
            },
            "evidence-ref": "",
        })
        scene_mapping.append({
            "slice": f"{proj}::{s_id}",
            "scene": f"SC::{scene}",
            "ruling-ref": "SCENE-SET::zopn-v1",
            "ruling-by": "zj",
        })
        # dependency: execution-workspace requires runtime-integration when both exist
        if scene == "execution-workspace" and info["coverage"].get("runtime-integration"):
            deps.append({
                "id": f"D::{proj}-exec-req-rt",
                "from": t_id, "to": f"T::runtime-integration-impl",
                "relation": "requires", "evidence-ref": "",
            })
    # also add runtime-integration T node reference for dep target consistency:
    # ensure T::runtime-integration-impl exists if referenced
    rt_present = any(s["id"] == "S::runtime-integration" for s in slices)
    rt_referenced = any(d["to"] == "T::runtime-integration-impl" for d in deps)
    if rt_referenced and not rt_present:
        # add a runtime-integration T node so dep target is in V (CHK-02)
        nodes.append({"id": "T::runtime-integration-impl", "kind": "capability",
                      "statement": f"{proj} 运行时/集成能力（被 execution 依赖）",
                      "acceptance": SCENES["runtime-integration"]["observable"],
                      "evidence-ref": ""})
    graphs.append({
        "project": proj,
        "version-pin": info["pin"],
        "nodes": nodes,
        "slice-edges": slices,
        "cross-cutting-paths": [],
        "dependency-edges": deps,
        "relation-constraints": [],
        "context-entries": info["contexts"],
        "undeclared-relations": [],
        "orphan-nodes": [],  # all nodes are in slices (or the rt helper node is referenced by dep)
    })
    # difference entries for ALL 12 scenes (native or unknown)
    for scene, cov in info["coverage"].items():
        de = {
            "id": f"DE::{proj}-{scene}",
            "scene": f"SC::{scene}",
            "project": proj,
            "slice-ref": (f"{proj}::S::{scene}" if cov is not None else ""),
            "statement": f"{proj} 在场景 {scene} 的供给状态",
        }
        if cov is not None:
            de["verdict"] = "native"
            de["evidence-refs"] = [f"EVID::{e}" for e in cov]
            de["context-refs"] = []
            de["context-verdicts"] = []
        else:
            de["verdict"] = "unknown"
            de["evidence-refs"] = []
            if proj == "loop-now":
                de["verification-plan"] = (
                    "loop-now 本轮仅做 README@v0.2.0 一手阅读，未跑 zj-research sealed 采集；"
                    "README 信号（team/identity、context、inbox 协调、workflow、plugin、observability）"
                    "待 zj-research collect 钉 sealed Evidence 后判定 native/adapted/unsupported")
            elif proj == "multica":
                de["verification-plan"] = (
                    "multica 本轮仅做 README@v0.8.1 一手阅读，未跑 zj-research sealed 采集；"
                    "README 信号密度极高（任务流转/身份scope/会话上下文/执行daemon/审批gate/结果provenance/"
                    "Skills复用/可重放日志/workspaces-squads/self-host+多端+26CLI/清晰技术栈），"
                    "待 zj-research collect 钉 sealed Evidence 后判定 native/adapted/unsupported")
            else:
                de["verification-plan"] = (
                    f"对 {info['repo']}@{info['pin']} 用判别性短语补采该维度，"
                    "或走 primary-source reading 核验；unknown≠absent")
            de["context-refs"] = []
            de["context-verdicts"] = []
        difference_entries.append(de)

# Domain-level context entries (scene-set level)
domain_contexts = [
    {"id": "CTX::zopn-single-user", "scope": "domain", "kind": "constraint",
     "statement": "ZOnePersonNetwork 目标为单人个人协同网络；真实产品边界（单人/跨设备/多项目）是 alignment item",
     "evidence-ref": "docs/reasearch/2026-11-08-research-charter.md"},
    {"id": "CTX::zopn-no-adopt-verdict", "scope": "domain", "kind": "constraint",
     "statement": "本横比仪器只产出场景×项目差异条目；采用/启动裁决属母模型 zj-open-source-capability-fit，不在本报告内",
     "evidence-ref": "SKILL.md 范围闸门 1/2"},
]

bundle = {
    "schema": "zj-graphical-cross-comparison/bundle/v1",
    "scene-set": {
        "id": "SCENE-SET::zopn-v1",
        "version-pin": "v1 (PROVISIONAL — zj draft 2026-11-09, pending ratification)",
        "source": "zj 2026-11-08 charter 模块草案 + opn-landscape 13-维度 brief（Human 给定草稿，待 ratify）",
        "derived-from-graphs": False,
        "scenes": [
            {"id": f"SC::{s}", "start": d["start"], "end": d["end"], "observable": d["observable"]}
            for s, d in SCENES.items()
        ],
        "context-entries": domain_contexts,
    },
    "graphs": graphs,
    "scene-mapping": scene_mapping,
    "equivalence-rulings": [],  # 未裁决任何场景内等价（不得自行推断语义等价）
    "optional-scene-pool-review": {
        "pool-size": 13,
        "covered": 12,
        "project-specific": 1,
        "notes": (
            "盲区核对（Human / zj）：本轮固定场景集取 12 个可观察场景，对应 opn-landscape 的 13 个模块维度；"
            "其中 ref-capability-map 是 ZAgenticOPN 参照物专属能力地图（仅其有 E），不作为通用场景，"
            "已降为 ZAgenticOPN 项目级 context-entry。agent-protocol / tech-design 保留为独立场景。"
            "盲区：仍有若干项目在若干场景为 unknown（见差异条目，多为早期一手阅读未做 sealed 采集者）；"
            "multica 与 loop-now 本轮已跑 zj-research collect 取得 12/12 sealed Evidence（multica 曾有的 Lark 子系统弱证据已通过 README 锚定 brief 修复，见 CTX::multica-evidence-anchored；两者均含钉偏差 context-entry）。"
            "未自行推断任何场景内语义等价。"),
    },
    "difference-entries": difference_entries,
    "report-sections": [
        {"n": 1, "title": "图清单与版本 pin",
         "sources": ["evidence"],
         "body": "14 个项目图，版本钉见 bundle.graphs[].version-pin；域级 context-entries 见 scene-set.context-entries（zopn-single-user / zopn-no-adopt-verdict）。"},
        {"n": 2, "title": "场景映射表与映射裁决记录",
         "sources": ["human-ruling"],
         "body": "每个项目对每个覆盖场景建一条竖切片 S::<scene>，映射到 SC::<scene>；映射裁决人=zj（Human 给定场景集）。完整映射见 bundle.scene-mapping。"},
        {"n": 3, "title": "差异条目清单",
         "sources": ["evidence"],
         "body": "12 场景 × 14 项目 = 168 条差异条目；native 绑定 sealed Evidence ID，unknown 附 verification-plan。完整清单见 bundle.difference-entries。摘要见下节指标与 report 文本。"},
        {"n": 4, "title": "可选场景集核对留痕",
         "sources": ["human-ruling"],
         "body": "见 bundle.optional-scene-pool-review.notes（zj 盲区核对）。"},
        {"n": 5, "title": "场景内语义等价裁决记录",
         "sources": ["human-ruling"],
         "body": "未裁决任何场景内语义等价：等价裁决须引用双方 acceptance 且由 Human 裁决，本轮未做，避免自行推断（如 qm 与 ZAgenticOPN 均覆盖 identity-scope 但语义互不相容，不得判等价）。"},
        {"n": 6, "title": "摘要指标（标注不参与结论）",
         "sources": ["evidence"],
         "body": "见 metrics.json；usage=display-only，not_for_conclusion=true，不得用于排序/裁决/回灌/优先级。"},
        {"n": 7, "title": "与母模型的可选回灌素材",
         "sources": ["assumption"],
         "body": "本横比只给差异条目。回灌母模型 zj-open-source-capability-fit 的素材：① orca 在 execution-workspace / runtime-integration / agent-protocol 为 native（L2 执行编排层种子，契合'以 orca 启动'）；② identity-scope / task-workitem 控制面在 orca 为 unknown，须自研语义所有权层（痛点 2 的 0→1 集中在语义层）；③ multica / loop-now 本轮已 collect 取 12/12 sealed Evidence（multica 偏 L1 多-agent 团队/权限/集成，loop-now 偏本地桌面 agent 编排），可作为执行编排层参照；multica 曾有的 5 条 Lark 子系统弱证据已通过 README 锚定 brief 修复（见 CTX::multica-evidence-anchored），两者均存在版本钉偏差（collect 忽略 brief.repositories[].revision，由 test_tag_pin.py 实证，请求 tag≠实际 HEAD）。引用前需语义复核。注意：本文件不产采用裁决。"},
        {"n": 8, "title": "完成标准自检",
         "sources": ["human-ruling"],
         "body": "第三方 Agent 可凭 bundle.difference-entries 逐条复核：每条含 scene/project/verdict/evidence-refs 或 verification-plan；来源分 evidence(原生绑定 sealed ID) / human-ruling(场景集与映射) / assumption(回灌素材)。场景集本身为 PROVISIONAL，签发前需 zj 一句话 ratify。"},
    ],
    "summary-metrics-usage": "display-only",
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print(f"wrote {OUT}")
print(f"graphs={len(graphs)} scenes={len(SCENES)} difference_entries={len(difference_entries)}")
