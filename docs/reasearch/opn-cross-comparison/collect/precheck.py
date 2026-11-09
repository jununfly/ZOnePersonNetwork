#!/usr/bin/env python3
"""keyword x tree 路径碰撞预检（zj-research 采集前纪律）。

规则来源：keyword 既是路径子串（命中 canonical 路径才选文件；只要存在 hint，
根 README fallback 不触发）又是正文匹配词。裸路径 keyword 会在别的文件正文被误命中
-> 语义错配。本脚本标记：哪些 keyword 作为路径子串命中了「非 canonical」路径
（误选风险），以及命中的 canonical 路径（可接受）。

canonical 路径只认：
  - docs/**/*.md
  - basename 匹配 (readme|agent|claude|architecture)*.md
  - 少数 manifest: package.json, go.mod, go.sum, Cargo.toml, Cargo.lock, pyproject.toml
"""
import json
import re
import sys

REPO = sys.argv[1] if len(sys.argv) > 1 else "multica"
BRIEF = f"brief-{REPO}.json"
TREE = f"tree-{REPO}.jsonl"

CANON_BASENAME = re.compile(r"^(readme|agent|claude|architecture).*\.md$", re.IGNORECASE)
MANIFEST = {"package.json", "go.mod", "go.sum", "cargo.toml", "cargo.lock",
            "pyproject.toml", "package-lock.json", "go.work"}


def is_canonical(path: str) -> bool:
    p = path.lower()
    if p.startswith("docs/") and p.endswith(".md"):
        return True
    base = p.rsplit("/", 1)[-1]
    if CANON_BASENAME.match(base):
        return True
    if base in MANIFEST:
        return True
    return False


def main():
    brief = json.load(open(BRIEF, encoding="utf-8"))
    criteria = brief["brief"]["criteria"]
    tree = [ln.strip() for ln in open(TREE, encoding="utf-8") if ln.strip()]
    print(f"=== repo={REPO}  tree_paths={len(tree)}  criteria={len(criteria)} ===\n")

    total_flag = 0
    for c in criteria:
        cid = c["id"]
        print(f"[{cid}]")
        any_flag = False
        for kw in c["keywords"]:
            k = kw.lower()
            canon_hits = []
            noncanon_hits = []
            for t in tree:
                tl = t.lower()
                if k in tl:
                    (canon_hits if is_canonical(t) else noncanon_hits).append(t)
            if noncanon_hits:
                any_flag = True
                total_flag += 1
                # 只列前 5 个非 canonical 命中，避免刷屏
                shown = noncanon_hits[:5]
                extra = "" if len(noncanon_hits) <= 5 else f" ...(+{len(noncanon_hits)-5})"
                print(f"  !! KW={kw!r} -> NON-CANONICAL path-substring hits ({len(noncanon_hits)}): {shown}{extra}")
            elif canon_hits:
                shown = canon_hits[:3]
                extra = "" if len(canon_hits) <= 3 else f" ...(+{len(canon_hits)-3})"
                print(f"     KW={kw!r} -> canonical hits ({len(canon_hits)}): {shown}{extra}")
            else:
                print(f"     KW={kw!r} -> no path-substring hit (pure content match only)")
        print()
    print(f"=== FLAGGED keyword-path collisions: {total_flag} ===")
    print("对策：被标记的关键词要么改成更具体的正文短语（去掉裸路径子串），")
    print("      要么确认其命中非 canonical 路径是预期（如 docs/ 下的真实文档），并在 brief 注释说明。")


if __name__ == "__main__":
    main()
