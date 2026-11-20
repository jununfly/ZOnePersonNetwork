# 成熟度一手材料事实清单（non-sealed primary-source reading）

> **本清单全部为 non-sealed primary-source reading**，按 charter 纪律只用于风险与验证门，不构成 canonical 能力结论。
>
> 方法：全部使用 `/opt/homebrew/bin/gh api` 按各仓库** pinned SHA**（非默认分支 HEAD）读取。LICENSE/CONTRIBUTING/CHANGELOG 经 `contents/{path}?ref={SHA}` 读取；releases/tags 经 `repos/{owner}/{repo}/releases` 与 `/tags` 读取；CI 经 `contents/.github/workflows?ref={SHA}` 列名并抽样读取内容；测试目录经 `contents/{tests,test,fixtures,spec,specs,__tests__}?ref={SHA}` 探测。API 返回 404 统一记为「未找到（路径不存在）」。
>
> **严禁项遵守声明**：本清单不给出「已成形 / 不成熟」判断、不排序、不打分、不写产品建议。分类（分池 / 待 PoC 清单）属 Human 裁决，不在本文件中发生。

---

## 1. yc-software/qm @ `605c259b28d54ee750c526b11925ddea3e0e6f59`

- `LICENSE`：MIT License（Copyright (c) 2026 QM contributors）。许可允许修改与再分发。
- `CONTRIBUTING.md`：存在。原文「we'd prefer `feature` PRs in the form of _human-written_ text… Submit changes as a PR adding a `.txt` or `.md` file to the `adrs/` folder」「Please do not have AI artificially expand…」「For bugs, just open an issue」。→ **不接受代码 PR，只接受 human-written ADR 文本贡献**；bug 走 issue。
- `CHANGELOG.md`：未找到（路径不存在）。
- `repos/.../releases`：12 条；最新 `v0.1.19`（2026-11-12），`v0.1.18`（2026-11-11），`v0.1.17`（2026-11-10）等，发版频繁。`tags` 含 `vendored-pi-ai-0.82.0-qm.*`、`vendored-pi-coding-agent-0.82.0-security.*`、`vendored-slack-socket-mode-2.0.7-qm.1` 等 vendored 标签。
- `.github/workflows/`（质量门存在）：`cicd.yml`（core-typecheck `npm run typecheck`；core-tests 分片 5；desktop sign-in tests `npm test --prefix desktop`）、`desk-native.yml`（macOS cargo fmt/clippy/test/build + swift focus 测试）、`ios-native.yml`（`swift-format lint --strict`、`xcodebuild test`）、`pgbouncer.yml`（transaction-pooling 测试）、`publish-cli.yml`（typecheck、test:pack、pin image digests）、`release-package.yml`（构建并 cosign 签名镜像）、`release.yml`、`wall-of-shame.yml`（检查 PR review report）。→ 质量门：typecheck / test / clippy / lint / build / 镜像签名齐备。
- 测试目录：`tests/` 404；`test/`（根级）存在，含 `acl-*.test.ts`、`admin-*.test.ts` 等大量 `*.test.ts`；`fixtures/`、`spec/`、`specs/`、`__tests__` 均 404。

## 2. makifbaysal/tasktrooper @ `ae5fb965c4758bbb25d2fac7f10f9bb26cb63823`

- `LICENSE`：Apache License 2.0。许可允许修改（需保留声明）。
- `CONTRIBUTING.md`：存在。含 Prerequisites（Go、Node 22+、agent CLI、`git`、`rg`）、`make setup/dev/desktop/test` 循环、Layout 说明。→ 标准 OSS 贡献流程，未见 PR 限制。
- `CHANGELOG.md`：未找到（路径不存在）。
- `repos/.../releases`：12 条；`v0.3.15`（2026-11-11）、`v0.3.14`、`v0.3.13` 同日连续发版等，发版频繁。`tags` `v0.3.4`–`v0.3.15`。
- `.github/workflows/`：`ci.yml`（`cd server && go build ./... && go vet ./... && go test ./...`；`skillvectors -check`；`desktop/runner` go build/vet/test；`desktop/ui` npm typecheck+build；`desktop` npm typecheck）、`release.yml`（构建 macOS/Windows/Linux 安装包 + updater feeds）。→ 质量门：go test / vet / typecheck / build。
- 测试目录：`tests/`、`test/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 在根级均 404（测试疑似内嵌于 `server/`）。

## 3. JF3Env/opencode-coordination @ `2c9dd06f21716d8fc5885a266b119e58e78f2a0d`

- `LICENSE`：MIT License（Copyright (c) 2026 Jonatas Fischer）。
- `CONTRIBUTING.md`：存在。规则：仅 TypeScript erasable 语法；core 不得 import host；「Every fix comes with a test that fails without it」（`npm test`）；事件 append-only、projection 确定性。→ 接受代码 PR，但要求带测试。
- `CHANGELOG.md`：存在（「# Changelog」「## Unreleased」含条目）。
- `repos/.../releases`：空。`tags`：空。
- `.github/workflows/`：`ci.yml`（`npm ci`、`npm run typecheck`、`npm test`、`npm run build`、`node scripts/gen-docs.ts --check`；`bun` smoke；`plantuml -checkonly docs/uml/src/*.puml`）。→ 质量门：typecheck / test / build / 文档生成校验。
- 测试目录：`test/`（根级）存在，含 `bridge.test.ts`、`cli.test.ts`、`ledger.test.ts`、`lifecycle.test.ts`、`plugin.test.ts`、`views.test.ts` 等；`tests/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 404。

## 4. alamops/agetor @ `897b70afb6f7671dc418c6d1053dbf8fbc3c81e0`

- `LICENSE`：MIT License（Copyright (c) 2026 Alamo Saravali）。
- `CONTRIBUTING.md`：未找到（路径不存在）。
- `CHANGELOG.md`：未找到（路径不存在）。
- `.github/workflows/`：404 → 未找到（路径不存在）。
- `repos/.../releases`：12 条；`v1.2.0`（2026-11-10）、`v1.1.1`、`v1.0.3`…`v0.1.8`。`tags` 对应存在。
- 测试目录：`tests/`、`test/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 均 404。

## 5. lanes-sh/app @ `7b9cb385d1100ded8a74986f81472f8856840578`

- `LICENSE`：未找到（路径不存在，LICENSE 与 LICENSE.md 均 404）。
- `CONTRIBUTING.md`：未找到（路径不存在）。
- `CHANGELOG.md`：未找到（路径不存在）。
- `.github/workflows/`：404 → 未找到（路径不存在）。
- `repos/.../releases`：12 条；`v0.50.0`（2026-10-31）、`v0.49.6`…`v0.47.3`。`tags` 对应存在。
- 测试目录：`tests/`、`test/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 均 404。

## 6. usemozzie/mozzie @ `80f3515684722a8909fbc0c17a0526664ec0349a`

- `LICENSE`：MIT License（Copyright (c) 2025 Mozzie Contributors）。
- `CONTRIBUTING.md`：存在（Tauri 2.0 桌面应用；Prerequisites Node≥20 / pnpm≥9 / Rust；`pnpm dev`）。→ 标准 OSS 贡献。
- `CHANGELOG.md`：未找到（路径不存在）。
- `repos/.../releases`：仅 `v0.1.8`（2026-03-12）；`tags` `v0.1.0`–`v0.1.8`。→ 发版节奏稀疏（距快照约 8 个月无新发版）。
- `.github/workflows/`：`build-test.yml`（Tauri build Windows/macOS）、`ci.yml`（`pnpm typecheck`；`cargo check`；`cargo clippy -- -D warnings`）、`release.yml`（构建 Windows/macOS + Apple 证书）。→ CI 存在，但抽样 jobs 为 typecheck / clippy / build，**未见显式 `test` / `cargo test` 步骤**。
- 测试目录：根级 `tests/`、`test/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 均 404。

## 7. songs-aaa/shared-memory-vault @ `59f0b12134622c0ad93ef59ef6373cfe587deaf3`

- `LICENSE`：MIT License（Copyright (c) 2026 shared-memory-vault contributors）。
- `CONTRIBUTING.md`：未找到（路径不存在）。
- `CHANGELOG.md`：未找到（路径不存在）。
- `.github/workflows/`：404 → 未找到（路径不存在）。
- `repos/.../releases`：空。`tags`：空。
- 测试目录：`tests/`、`test/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 均 404。

## 8. themanojdesai/python-a2a @ `40b969a465f85e8156793b7cfac16c5e23ed0b86`

- `LICENSE`：MIT License（Copyright (c) 2025 Manoj Desai）。
- `CONTRIBUTING.md`：存在（Code of Conduct、Development Setup fork/clone、`Pull Request Process`）。→ 标准代码 PR。
- `CHANGELOG.md`：未找到（路径不存在）。
- `repos/.../releases`：空。`tags`：`v0.4.6`–`v0.5.10`（12 条）。
- `.github/workflows/`：`build.yml`（`setup-python` + UV + `pytest`）、`python-tests-uv.yml`（`flake8`、`mypy`、`pytest --cov=python_a2a`）。→ 质量门：pytest / lint / 类型检查。
- 测试目录：`tests/`（根级）存在，含 `basic_test.py`、`test_client.py`、`test_discovery.py`、`test_server.py`、`test_models.py`、`unit/` 等；`test/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 404。

## 9. standardagents/dmux @ `8cb3d926631a9349ab67f7ece41d218427ac7e24`

- `LICENSE`：MIT License（Copyright (c) 2025 Justin Schroeder）。
- `CONTRIBUTING.md`：存在（「built while running dmux itself」dogfood 循环、`pnpm dev`、`pnpm run dev:doctor`）。→ 标准贡献。
- `CHANGELOG.md`：未找到（路径不存在）。
- `repos/.../releases`：12 条；`v5.11.1`（2026-08-16）、`v5.11.0`…`v5.6.0`。`tags` 对应存在。
- `.github/workflows/`：`publish.yml`（`pnpm install --frozen-lockfile`、`pnpm build`、`pnpm run build:macos-helper`、`pnpm run smoke:pack`、`npm publish --provenance --access public`）。→ 抽样仅见 build / smoke / publish，**CI 中未见显式 test 门**（仓库内有测试目录）。
- 测试目录：`tests/` 存在（子目录 `actions/`、`utils/`；`actions.devMode.test.ts`、`agentLaunch.test.ts`、`dmux.e2e.*.test.ts`、`claudeHooks.test.ts` 等大量 `*.test.ts`；含 `fixtures/`）；`test/`、`spec/`、`specs/`、`__tests__` 404。

## 10. jununfly/ZAgenticOPN @ `2ff40cc052aae12fc7a324f89691e9f194985d24`

- `LICENSE`：未找到（路径不存在，LICENSE 与 LICENSE.md 均 404）。
- `CONTRIBUTING.md`：未找到（路径不存在）。
- `CHANGELOG.md`：未找到（路径不存在）。
- `.github/workflows/`：404 → 未找到（路径不存在）。
- `repos/.../releases`：空。`tags`：空。
- 测试目录：`tests/`（根级）存在，含 `__init__.py`、`agentrq_blackbox.py`、`test_activation.py`、`test_activation_runner.py`、`test_agentrq_adapter_blackbox.py`、`test_coordination.py`、`test_proxy.py`；`test/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 404。

---

## 11. stablyai/orca @ `27eb5e2a6c5017c6fdcba4fee16bf54256550c6f`（额外 4 库之一）

- `LICENSE`：MIT License（Copyright (c) 2026 Lovecast Inc.）。
- `CONTRIBUTING.md`：位于 `.github/CONTRIBUTING.md`（存在；「Thanks for contributing to Orca」、跨平台兼容规则、安全漏洞私下报告）。→ 标准贡献。
- `CHANGELOG.md`：未找到（路径不存在）。
- `repos/.../releases`：频繁；`v1.4.258`（2026-11-13）、`v1.4.257`（2026-11-12）… 近每日级。`tags` 对应存在。
- `.github/workflows/`：60+ 个，含 `ci.yml`、`unit-tests.yml`、`e2e.yml`、`computer-e2e.yml`、`performance-contracts.yml`、`pr.yml`、`release-*.yml`、`mobile-*.yml`、`windows-*.yml`、`zcode-*-contract.yml`、`linux-wayland-gpu-sandbox.yml` 等。→ 质量门极齐备（unit / e2e / perf / 多平台 / 契约）。
- 测试目录：`tests/`（根级）存在，含 `component-fixtures/`、`e2e/`、`playwright.config.ts`、`tools/`、`AGENTS.md`；`test/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 404。

## 12. AI-for-anyone/loop-now @ `b7d6811877e6d7341ac539934ae87028df87b1e6`（额外 4 库之一；注：REPORT.md 记为 main HEAD，非请求 tag v0.2.0）

- `LICENSE`：Apache License 2.0。
- `CONTRIBUTING.md`：未找到（路径不存在）。
- `CHANGELOG.md`：存在（「# 更新日志」，含 `## v0.2.0` 等面向使用者的变更节；发布流水线取对应节作 Release 说明）。
- `repos/.../releases`：频繁；`v0.2.6`（2026-11-13）、`v0.2.5`…`v0.2.0`。`tags` `v0.1.0`、`pg-final`、`v0.2.0+`。
- `.github/workflows/`：`ci.yml`（`go vet ./cmd/... ./internal/... ./api/...`、Windows 交叉 vet、`go test -count=1 -skip '^TestStress'`、data layer stress `go test -count=3 -run '^TestStress'`）、`pages.yml`（docs 构建/部署）、`release.yml`（各平台 build+smoke、release notes 校验）。→ 质量门：go vet / go test / 跨平台 / docs。
- 测试目录：根级 `tests/`、`test/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 均 404（Go 测试内嵌于 `cmd/`、`internal/`、`api/`）。

## 13. multica-ai/multica @ `41885a6d816834663dad8e6944658e2ac8555844`（额外 4 库之一；注：REPORT.md 记为 main HEAD，非请求 tag v0.8.1）

- `LICENSE`：**「Multica License」——Apache 2.0 + 附加条件**（Part II 复现 Apache 全文，Part I 为额外条件）。→ 非标准许可证，改造/再分发须复核附加条件。
- `CONTRIBUTING.md`：存在（issue/PR 模板与要求、本地开发、隔离 worktree、共享 PostgreSQL model、testing/verification、「Contribution Terms」引用 Multica License condition 2）。→ 标准代码 PR，但受自定义许可证条款约束。
- `CHANGELOG.md`：未找到（路径不存在）。
- `repos/.../releases`：频繁；`v0.9.0`（2026-11-13）、`v0.8.2`…`v0.6.1`。`tags` 对应存在。
- `.github/workflows/`：`ci.yml`（`ci-scope decide`、`sqlc-check` 校验生成 SQL 最新、Vitest 分片、Go 测试）、`desktop-smoke.yml`、`mobile-verify.yml`（vitest typecheck/lint/test）、`openclaw-config-smoke.yml`（`go test -tags agentintegration`、`govulncheck` 在 release 中）、`ui-performance.yml`、`release.yml`（`go test --race`、`go tool govulncheck ./...`）。→ 质量门齐备，含漏洞扫描。
- 测试目录：根级 `tests/`、`test/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 均 404（测试在 `scripts/*.test.mjs` 与 Go 包内）。

## 14. herdrdev/herdr @ `ee5bfb5041bb3e4a49d591c72308aae3c81ecdde`（额外 4 库之一）

- `LICENSE`：Apache License 2.0。
- `CONTRIBUTING.md`：存在且明确「**Herdr does not accept unsolicited pull requests**」（描述曾开放 PR 门失败，改为仅接受经维护者验证的贡献）。→ 与 qm 同型的上游治理风险（PR 门受限）。
- `CHANGELOG.md`：存在（「# Changelog」「## [0.9.5] - 2026-10-14」等）。
- `repos/.../releases`：`v0.9.5`（2026-10-14）及多个 `preview-*` 标签；`tags` `v0.7.2+`。
- `.github/workflows/`：`ci.yml`（`conventional_commits.py` 校验 commit/PR、cargo-nextest 矩阵 ubuntu/macos/windows、`nix flake-check`）、`pr-gate.yml`（contributor 校验）、`preview.yml`、`release.yml`（要求已发布 preview + nix flake-check）、`distribution.yml`（docs 契约测试）、`nix.yml`、`stale-close.yml`、`website-deploy.yml`、`windows-arm64.yml`。→ 质量门：nextest / lint / conventional commits / nix / docs 契约。
- 测试目录：`tests/`（根级）存在，含 `api_ping.rs`、`cli.rs`、`detach_reattach.rs`、`live_handoff.rs`、`windows_server_security.rs`、`fixtures/`、`support/` 等；`test/`、`fixtures/`、`spec/`、`specs/`、`__tests__` 404。

---

## 缺口留痕（仅事实，非成熟度判断）

- **根 LICENSE / LICENSE.md 路径在以下仓库返回 404**：`lanes-sh/app`、`jununfly/ZAgenticOPN`（2/14）。注：仅探测 `LICENSE` 与 `LICENSE.md` 两常见名，未穷举 `LICENSE.txt` 等变体。
- **`.github/workflows` 路径在以下仓库返回 404（无 CI）**：`alamops/agetor`、`lanes-sh/app`、`songs-aaa/shared-memory-vault`、`jununfly/ZAgenticOPN`（4/14）。
- **CI 存在但抽样未见 test 门**：`usemozzie/mozzie`（`ci.yml` 仅 typecheck/clippy/build）、`standardagents/dmux`（`publish.yml` 仅 build/smoke/publish）；二者仓库内均有测试目录。
- **`CONTRIBUTING.md` 明确限制 PR**：`yc-software/qm`（仅 human-written ADR 文本，拒代码 PR）、`herdrdev/herdr`（拒未邀约 PR）。
- **`CHANGELOG.md` 存在**：`opencode-coordination`、`loop-now`、`herdr`；其余 11 仓库根级未找到。
- **`releases` 为空（无发版记录）**：`opencode-coordination`、`shared-memory-vault`、`python-a2a`、`ZAgenticOPN`；`tags` 亦空于 `shared-memory-vault`、`ZAgenticOPN`、`opencode-coordination`。
- 联网读取全程使用 `/opt/homebrew/bin/gh api`，未触发沙箱阻断（无静默丢弃/升级拦截）。
