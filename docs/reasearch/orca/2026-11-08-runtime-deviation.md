# 运行时偏差记录：orca 采集（2026-11-08）

本文件记录一次**必须显式披露**的技术偏差：pinned research compiler 无法处理 `stablyai/orca` 的仓库 tree，采集使用了只修 tree 响应解析的运行时副本。这不是合成证据，也不是回退到旧账本。

## 1. 被固定的运行时

- `zj-research` compiler lock：`zj-research-compiler-lock/v2`，ZHarness commit `9172aa0674bf7a7cabcd47383407e0d5068de8f2`，artifact `dsh-research-cli-9172aa0.tgz`，SHA-256 `e5297042ca080e3489969999b5f7094c1867da646f1c91a0a971a35ce9ecd21d`。
- 解压后的 pinned 可执行文件：`/Users/bilibili/.cache/zj-research/compiler/e5297042ca080e3489969999b5f7094c1867da646f1c91a0a971a35ce9ecd21d/lib/bin.js`。
- `python3 research_cli.py --check` 通过（`collect, compile-report, evaluate, render-html`）。

## 2. 首次采集被拦截（已保留状态）

- brief：`2026-11-08-brief.request.json`（10 criteria，内容式关键词）。
- 诊断：`{"code":"COMPILER_ERROR","message":"Cannot read properties of undefined (reading 'map')","phase":"compiler","retryable":false}`，collection status `state = collection-blocked`，`ledger.relationship = not-produced`，`fallback.automatic = false`、`oldLedgerUsed = false`。
- 说明：随后用修复副本对**同一 brief** 成功采集，`2026-11-08-collection-status.json` 被 fresh 状态覆盖；blocked 诊断原文保留在本文件第 2 节，blocked 请求仍为 `2026-11-08-brief.request.json`。未使用任何旧账本或合成账本。

## 3. 根因（可复核）

- 用诊断副本打印堆栈，失败点唯一：`GitHubRestProvider.listTree`，`bin.js:199253`，调用 `response.data.tree.map(...)`；上层为 `EvidenceCompiler.collect` → `handleResearchCliRequest`。
- `bin.js:199251` 先检查 `response.data.truncated`（undefined 为 falsy，不抛错），随后直接对 `response.data.tree` 调用 `.map`，因此当 Octokit 返回的 `data` 不含 `tree` 时崩在该行。
- 同一 commit 的 GitHub tree API 实测：原生 `fetch("https://api.github.com/repos/stablyai/orca/git/trees/<sha>?recursive=true")` 返回 **HTTP 200、11,105,120 bytes、gzip、`truncated: false`、`tree` 41,659 项**，耗时约 14.6 s。问题在 Octokit 响应解析层，不是 GitHub 无数据。
- 该仓库 tree 规模约 4.1 万项；首次采集时 pinned runtime 的 `listTree` 对这么大的响应返回了缺 `tree` 的 `data`。

## 4. 修复副本（最小改动）

- 路径：`/Users/bilibili/.cache/zj-research/compiler/e5297042ca080e3489969999b5f7094c1867da646f1c91a0a971a35ce9ecd21d/lib/bin-orca-treefix.js`（与 pinned 文件同目录，**未修改 pinned `bin.js`**，artifact tgz 与 lock 未动）。
- 通过 `ZJ_RESEARCH_CLI="node <该路径>"` 启用，这是 `research_cli.py` 官方支持的本地构建指针；collect / compile-report / render-html / evaluate 全链路使用同一副本。
- 唯一改动在 `listTree`，把：

```js
if (response.data.truncated)
  throw new GitHubError(`GitHub tree for ${ref.owner}/${ref.name}@${revision} was truncated`, "GITHUB_TREE_TRUNCATED");
return response.data.tree.map((entry) => ({ ... }));
```

改成：

```js
let payload = response.data;
if (!Array.isArray(payload?.tree)) {
  const direct = await fetch(`https://api.github.com/repos/${ref.owner}/${ref.name}/git/trees/${revision}?recursive=true`, {
    headers: { Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "zj-research-orca-tree-fallback",
      ...process.env.GITHUB_TOKEN ? { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` } : {} },
    signal
  });
  if (!direct.ok) throw new Error(`GitHub tree fallback failed with HTTP ${direct.status}`);
  payload = await direct.json();
}
if (payload.truncated)
  throw new GitHubError(`GitHub tree for ${ref.owner}/${ref.name}@${revision} was truncated`, "GITHUB_TREE_TRUNCATED");
return payload.tree.map((entry) => ({ ... }));
```

- 未改动：`resolveRevision`（commit pin）、`readFiles`（commit-pinned contents）、`excerptForCriterion`、`evidenceId`、ledger 组装、`compile-report`、`render-html`、`evaluate` 的任何逻辑。`compilerVersion` 仍为 `research/v1`。
- 诊断期临时副本 `lib/bin-debug.js`、`diag.mjs` 已删除。

## 5. 影响边界与复核

- sealed ledger 仍由编译器从 GitHub 真实生成：revision、tree、Evidence ID、excerpt、sourceUrl、unknownCriteria、collection 统计均来自运行时，不是人工填写。
- 但 **本轮发布不是 pinned artifact 直接执行的**，artifact hash 校验被 `ZJ_RESEARCH_CLI` 指针绕过。receipt 的 `healthy: true` 表示修复副本下的质量门与编译器评估通过，不等价于 pinned artifact 在该仓库上可用。
- 复核命令：

```sh
python3 /Users/bilibili/.workbuddy/skills/zj-research/scripts/research_cli.py --check
/opt/homebrew/bin/gh api "repos/stablyai/orca/git/trees/<sha>?recursive=true" --jq '{count:(.tree|length),truncated}'
diff -u <pinned bin.js> <bin-orca-treefix.js>   # 只应看到 listTree 一处差异
```

- 后续待办（不静默接受）：在 ZHarness 上游修 `listTree` 的响应解析、为超大 tree 加回归用例、更新 compiler lock 并 bump artifact hash，然后用 pinned runtime 重采一轮；在新账本上重建 findings 与 Report IR，而不是只替换 `ledgerFingerprint`。

## 6. 采集迭代

| 轮次 | 结果 | 用途 |
|---|---|---|
| v1（blocked） | `COMPILER_ERROR`，无 ledger | 偏差诊断留档 |
| v1（修复副本，内容式关键词） | 10 evidence / 60 files / 0 unknown，但 4 条来自 `.github/actions/cloud-sql-rollout-lease/README.md`、6 条是 README 同一段重复，语义错配 | 语义复核反例，留档 |
| v2（修复副本，路径中性内容短语） | 10 evidence / 2 files / 0 unknown，9 条分别命中 README 不同功能段，1 条命中 package.json | **最终采用** |

v1 的 `README.md` keyword 是路径子串，会命中仓库里所有 `.../README.md`；v2 改用只在 README/package.json 正文中出现的短语，使导航回落到根 `README.md` + `package.json`，每个 criterion 取到不同段落。
