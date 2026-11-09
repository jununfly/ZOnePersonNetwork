#!/usr/bin/env python3
"""
RED test — 事二:collect 必须把 ledger 钉到 brief 指定的 tag 解析出的 commit,
而不是默认分支 HEAD。

被测 seam(公开接口,非内部):`zj-research` collect 操作 -> sealed ledger。
观察点:ledger["repositories"][0]["revision"]["sha"]。

期望值真值源:GitHub tag ref 经 `gh api` 独立解析(不依赖被测编译器)。
这样测试不会与被测代码同构推导,也不会因重构而假绿。

背景(代码实测,非推测):
  researchBriefFingerprint 把 brief.repositories 归一化为仅 {owner,name},丢弃 revision;
  collect 仅把 candidate.repository 传给 resolveRevision;
  resolveRevision 永远 getBranch(default_branch) -> 默认分支 HEAD。
因此 brief 里的 revision 在 collect 路径是死输入。本测试把"应钉 tag"作为
期望行为固定下来;当前实现会失败(钉 HEAD),即 RED。
"""
import json
import os
import subprocess
import sys
import unittest

COLLECT_DIR = os.path.dirname(os.path.abspath(__file__))
RESEARCH_CLI = "/Users/bilibili/.workbuddy/skills/zj-research/scripts/research_cli.py"
GH = "/opt/homebrew/bin/gh"


def _gh_api(path):
    out = subprocess.check_output([GH, "api", path], text=True)
    return json.loads(out)


def _github_token():
    return subprocess.check_output([GH, "auth", "token"]).decode().strip()


def resolve_tag_commit(owner, name, tag):
    """Independent source of truth: tag ref -> commit sha (handles annotated tags)."""
    ref = _gh_api(f"repos/{owner}/{name}/git/refs/tags/{tag}")
    obj = ref["object"]
    if obj["type"] == "tag":
        tag_obj = _gh_api(f"repos/{owner}/{name}/git/tags/{obj['sha']}")
        return tag_obj["object"]["sha"]
    return obj["sha"]


def resolve_default_head(owner, name):
    repo = _gh_api(f"repos/{owner}/{name}")
    branch = repo["default_branch"]
    commit = _gh_api(f"repos/{owner}/{name}/commits/{branch}")
    return commit["sha"]


def run_collect(brief_path, ledger_out, status_out):
    env = os.environ.copy()
    env["GITHUB_TOKEN"] = _github_token()
    env["ZJ_RESEARCH_CLI_TIMEOUT_SECONDS"] = "600"
    subprocess.run(
        [sys.executable, RESEARCH_CLI, brief_path, "--output", ledger_out, "--status-output", status_out],
        check=True, env=env,
    )


def load_ledger_revision_sha(ledger_path):
    data = json.load(open(ledger_path))
    repos = data.get("result", data).get("repositories", [])
    return repos[0]["revision"]["sha"]


class TagPinTest(unittest.TestCase):
    def test_multica_collect_pins_to_tag_v0_8_1(self):
        owner, name, tag = "multica-ai", "multica", "v0.8.1"
        tag_sha = resolve_tag_commit(owner, name, tag)
        head_sha = resolve_default_head(owner, name)
        self.assertNotEqual(
            tag_sha, head_sha,
            "tag 与默认分支 HEAD 必须不同,本测试才有意义",
        )

        brief = os.path.join(COLLECT_DIR, "brief-multica.json")
        ledger = os.path.join(COLLECT_DIR, "ledger-multica-tdd.json")
        status = os.path.join(COLLECT_DIR, "status-multica-tdd.json")
        run_collect(brief, ledger, status)

        got = load_ledger_revision_sha(ledger)
        self.assertEqual(
            got, tag_sha,
            f"ledger 钉到 {got},但 tag {tag} 独立解析为 {tag_sha}。"
            f"编译器忽略了 brief 的 revision(恒钉默认分支 HEAD)。",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
