#!/usr/bin/env python3
"""摄取前的 HEAD 解析器 —— 解决 orca 等频繁发版仓库的 SHA 漂移（风险1）。

背景：编译器 resolveRevision() 只钉默认分支 HEAD、忽略 brief 的 revision/pin，
导致三元组里写死的 SHA 每次 collect/摄取都可能过期（orca 会话内漂 5 次）。
本脚本把「摄取那一刻重新解析 HEAD」固化为可执行、可复现的动作：

  用法:
    python3 resolve_head.py stablyai/orca
    python3 resolve_head.py stablyai/orca AI-for-anyone/loop-now herdrdev/herdr
    python3 resolve_head.py --check docs/../../2026-11-13-product-module-map.md

  --check 模式：解析提案三元组里每个仓库的当前 HEAD，与文档里写的 SHA 比对，
  输出 DRIFT / OK 表。DRIFT 时退出码 1，可用于 CI 或摄取前门禁。

依赖: /opt/homebrew/bin/gh（绝对路径，gh 不在默认 PATH）。只读 GitHub API。
"""
import json
import re
import subprocess
import sys

GH = "/opt/homebrew/bin/gh"


def resolve(repo):
    """返回 (default_branch, head_sha)；失败返回 (None, None)。"""
    r = subprocess.run([GH, "api", f"repos/{repo}", "--jq", ".default_branch"],
                       capture_output=True, text=True, timeout=30)
    if r.returncode != 0 or not r.stdout.strip():
        return None, None
    branch = r.stdout.strip()
    c = subprocess.run([GH, "api", f"repos/{repo}/commits/{branch}", "--jq", ".sha"],
                       capture_output=True, text=True, timeout=30)
    if c.returncode != 0 or not c.stdout.strip():
        return branch, None
    return branch, c.stdout.strip()


def check(doc_path):
    """解析文档三元组 <模块, 仓库, SHA>，比对每个仓库当前 HEAD。"""
    text = open(doc_path, encoding="utf-8").read()
    triples = re.findall(r'<([^,]+),\s*([^,]+),\s*([0-9a-f]{40})>', text)
    # 每个仓库取文档中记录的 SHA（可能有多个模块共用）
    recorded = {}
    for module, repo, sha in triples:
        recorded.setdefault(repo.strip(), set()).add(sha)
    print(f"检查 {len(recorded)} 个仓库 / {len(triples)} 条三元组\n")
    drift = False
    for repo, shas in sorted(recorded.items()):
        branch, head = resolve(repo)
        if head is None:
            print(f"  {repo:32s} RESOLVE-FAIL")
            continue
        for sha in sorted(shas):
            short = sha[:10]
            if head == sha:
                print(f"  {repo:32s} OK      ({short})")
            else:
                drift = True
                print(f"  {repo:32s} DRIFT   文档={short}  当前HEAD={head[:10]}  branch={branch}")
    print("\n结论:", "存在 DRIFT，摄取前须用当前 HEAD 回填三元组" if drift else "全部 SHA 与当前 HEAD 一致")
    sys.exit(1 if drift else 0)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    if args[0] == "--check":
        check(args[1])
        return
    for repo in args:
        branch, head = resolve(repo)
        if head:
            print(f"{repo}\t{branch}\t{head}")
        else:
            print(f"{repo}\tRESOLVE-FAIL", file=sys.stderr)


if __name__ == "__main__":
    main()
