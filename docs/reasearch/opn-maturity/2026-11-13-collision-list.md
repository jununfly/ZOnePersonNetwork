# keyword × tree 路径碰撞清单（2026-11-13）

由 `2026-11-13-precheck.py` 运行产出；脚本只打印 stdout，本清单为落盘记录。

## 语料（全 tree 路径）

来源：10 个目标仓的 pinned `git/trees?recursive=1`，经 `/opt/homebrew/bin/gh` 只读拉取（gh 不在 PATH，用绝对路径；token 有效、联网未被拦截）。全部 `truncated=False`。

| 仓库 | 路径数 |
|---|---|
| yc-software/qm | 2971 |
| makifbaysal/tasktrooper | 6176 |
| JF3Env/opencode-coordination | 140 |
| alamops/agetor | 1503 |
| lanes-sh/app | 44 |
| usemozzie/mozzie | 241 |
| songs-aaa/shared-memory-vault | 27 |
| themanojdesai/python-a2a | 286 |
| standardagents/dmux | 915 |
| jununfly/ZAgenticOPN | 189 |
| **TOTAL** | **12492** |

## brief 碰撞结果

- brief：`2026-11-13-brief.request.json`，`criteria=6`，`keywords=41`（均为判别性长短语）。
- **碰撞数 = 0**（无 keyword 命中非 canonical 路径子串；也没有仅命中 canonical 路径的 hint）。
- 碰撞清单：**（空）**。
- 结论：满足 Phase-3 的「碰撞为 0」前置条件。

## 对照组（不属于 brief，仅证明检测器非恒返回 0）

裸路径 keyword 若被写进 brief，会作为路径子串误钉到非 canonical 文件：

| 裸路径词 | 非 canonical 命中数 | 例 |
|---|---|---|
| `license` | 11 | `yc-software/qm:LICENSE`、`cli/LICENSE` |
| `changelog` | 1 | `JF3Env/opencode-coordination:CHANGELOG.md` |
| `dockerfile` | 12 | `qm:deploy/core/Dockerfile` |
| `makefile` | 2 | `tasktrooper:Makefile` |
| `contributing` | 7 | `qm:CONTRIBUTING.md` |
| `tests` | 202 | `qm:desktop/desk/tests/...` |
| `workflows` | 33 | `qm:.github/workflows/cicd.yml` |
| `fixtures` | 141 | `qm:cli/test/fixtures/...` |
| `spec` | 85 | `qm:scripts/dev/supervisor/specs.ts` |
| `adr` | 4 | `qm:adrs/...` |

`package.json` / `go.mod` / `pyproject.toml` / `cargo.toml` 因属 MANIFEST 白名单（canonical），对照组未计为碰撞。
对照组合计 `10/14` 会碰撞 —— 这正是本草案全部改用长短语的原因。
