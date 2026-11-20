# sealed 补采受阻记录：无法按三元组指定 SHA 钉 commit（2026-11-16）

> ## ✅ 终态（2026-11-16 当日已处置，本记录作为根因留档）
> zj 裁决选 **A**（重 pin 到 HEAD + 真实 collect），已执行完毕。三条风险全部处置：
> 1. **SHA 漂移** → 建 `resolve_head.py --check` 解析器，实测 13 仓库中 4 个漂移（orca/agetor/tasktrooper/qm），固化为摄取前门禁；三元组 SHA 与 Evidence ID 溯源解耦。
> 2. **缺格 sealed** → 三轮定向 + 路径导航补采，8/9 格拿到 sealed 证据；仅 orca-M6 诚实保留 unknown（orca 文档无可密封可观测声明）。见 `2026-11-16-resupply.findings.md`。
> 3. **工具链限制** → 确认为外部编译器不可改；本记录即根因留档，配合解析器规避，未静默改 SHA。
>
> 下方「待 zj 裁决的替代路径」为当时的决策输入，**已选定 A**，不再是未决项。

## 触发
zj 在 R3 拍板选 B：对 orca / loop-now / herdr 的 M5（执行与工作区隔离）/ M6（可观测与回放）/ M12（技术设计与部署）补采 sealed Evidence，再定①实现源。三元组已精确到 40 位 pinned SHA。

## 结论：sealed collect 无法钉到指定 SHA（结构性限制，非配置问题）

### 实锤 1 — 受控实验
- brief 指定 `stablyai/orca pin=27eb5e2a6c5017c6fdcba4fee16bf54256550c6f`。
- 适配器握手通过（`zj-research-cli/v1: collect, compile-report, evaluate, render-html`）。
- collect 成功产出 ledger（`/tmp/zj-pin-probe/ledger.json`）。
- **ledger 实际 revision.sha = `54563fec0a35fab9860c772183d48c9d96ffd6bf`（当前 main HEAD），不是 brief 指定的 `27eb5e2a…`。**

### 实锤 2 — 编译器源码
`~/.cache/zj-research/compiler/e5297042…/lib/bin.js` 的 `resolveRevision(ref, signal)`：
```
repos.get({owner, repo}) -> repository.data.default_branch
getBranch({owner, repo, branch: default_branch}) -> commit2.data.commit.sha
```
永远钉默认分支 HEAD。**brief 的 `revision` / `pin` 字段完全不参与**（`"pin"` token 计数 = 0）。无环境变量/字段可覆盖。

### 实锤 3 — 三仓库 HEAD 漂移状态（pinned SHA 均真实存在）
| 仓库 | 默认分支 | 当前 HEAD | 三元组 SHA | 既有 ledger SHA |
|---|---|---|---|---|
| stablyai/orca | main | `54563fec` | `27eb5e2a` | `4f06ffd6`（11-08 既有 v2） |
| AI-for-anyone/loop-now | main | `1e04ed00` | `b7d68118` | 无 sealed ledger（仅 tree 缓存） |
| herdrdev/herdr | master | `ee5bfb50` | `ee5bfb50` | `ee5bfb50`（11-08 既有 v2） |

三份 SHA（三元组 / 当前 HEAD / 既有 ledger）在 orca 上互不相同；herdr 三者恰好一致（HEAD 未漂移）。

### 实锤 4 — 既有 ledger 不够用
- orca 既有 ledger pin `4f06ffd6` ≠ 三元组 `27eb5e2a`，criteria 是 11-08 那轮（product-scope / orchestration / review-provenance…），非为 M5/M6/M12 设计。
- herdr 既有 ledger pin 与三元组一致，criteria 亦为 11-08 那轮。
- 按 charter「结论层作废、事实层留作素材」，事实层可引用，但**不能冒充为针对 M5/M6/M12 的新补采证据**；且旧 brief fingerprint 与新问题不匹配。

## 因此
「按三元组指定 SHA 补采 sealed Evidence」在当前编译器下**物理不可行**。若强行 collect，得到的是当前 HEAD 的证据，与三元组 SHA 不符——等于静默技术偏差，按纪律必须隔离并上报，不得接受。

## 待 zj 裁决的替代路径（不替你选）
- **A. 重 pin 三元组到当前 HEAD**：把三元组 SHA 从历史 commit 改成当前 HEAD（orca 54563fec / loop-now 1e04ed00 / herdr ee5bfb50 不变），再 collect。代价：三元组语义从「当时的版本」变成「现在的最新版」，需接受版本漂移。
- **B. 接受既有 sealed 事实层 + 标注覆盖缺口**：不重采，直接引用 orca@4f06ffd6 / herdr@ee5bfb50 既有 sealed Evidence 中相关条目（如 herdr 的 persistence-detach / detection-evidence / install-surface），loop-now 保持 unknown；在提案里显式标「契约源 pin 与三元组不一致」。代价：M5/M6/M12 证据不完整，loop-now 无证。
- **C. 修编译器支持 pin**：改 `resolveRevision` 优先读 brief 的 revision（需要改第三方编译器 artifact，超出本项目边界，且违反 zj-research「纯协议适配层、不捆绑编译器」架构）。不推荐。
- **D. 降级为非 sealed 一手阅读**：用 gh api 按三元组 SHA 读实现/文档，标 non-sealed，只作风险与验证门（charter 第 8 节先例）。代价：不满足「sealed 证据」原要求，但能精准按 SHA 定位。

## 证据链
- 受控实验产物：`/tmp/zj-pin-probe/{brief.json,ledger.json,status.json}`（临时目录，未入仓）。
- 校验命令见本文件「实锤」各节；全部使用绝对路径 `/opt/homebrew/bin/gh` 与缓存编译器 `e5297042…`。
- 未 commit / push。
