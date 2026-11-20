#!/usr/bin/env python3
"""keyword x tree 路径碰撞预检 —— 2026-11-16 R3 补采 brief 专用。

纪律：docs/reasearch/2026-11-08-research-charter.md
keyword 既是路径子串 hint 又是正文匹配词；裸路径词会误钉非 canonical 文件。
采集前必须做「全 keyword x 全 tree 路径」碰撞预检，门槛=0。
tree 从 GitHub API 按当前 HEAD 实时拉取（gh 绝对路径）。
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BRIEF = os.path.join(HERE, "2026-11-16-resupply2.brief.request.json")
GH = "/opt/homebrew/bin/gh"
REPOS = ["stablyai/orca", "AI-for-anyone/loop-now", "herdrdev/herdr"]
CANON_BASENAME = re.compile(r"^(readme|agent|claude|architecture).*\.md$", re.IGNORECASE)
MANIFEST = {"package.json", "go.mod", "go.sum", "cargo.toml", "cargo.lock", "pyproject.toml", "package-lock.json", "go.work"}


def is_canonical(path):
    p = path.lower()
    if p.startswith("docs/") and p.endswith(".md"):
        return True
    base = p.rsplit("/", 1)[-1]
    return bool(CANON_BASENAME.match(base)) or base in MANIFEST


def load_tree():
    corpus, stats = [], []
    for repo in REPOS:
        r = subprocess.run([GH, "api", f"repos/{repo}"], capture_output=True, text=True, timeout=30)
        meta = json.loads(r.stdout)
        sha = meta["default_branch"]
        c = subprocess.run([GH, "api", f"repos/{repo}/commits/{sha}"], capture_output=True, text=True, timeout=30)
        sha = json.loads(c.stdout)["sha"]
        t = subprocess.run([GH, "api", f"repos/{repo}/git/trees/{sha}?recursive=1"], capture_output=True, text=True, timeout=90)
        paths = [x["path"] for x in json.loads(t.stdout).get("tree", [])]
        corpus.extend((repo, p) for p in paths)
        stats.append(f"  {repo:28s} HEAD={sha[:10]} paths={len(paths)}")
    return corpus, stats


def probe(kw, corpus):
    k = kw.lower()
    canon, noncanon = [], []
    for repo, path in corpus:
        if k in path.lower():
            (canon if is_canonical(path) else noncanon).append(f"{repo}:{path}")
    return canon, noncanon


def main():
    brief = json.load(open(BRIEF, encoding="utf-8"))
    criteria = brief["brief"]["criteria"]
    corpus, stats = load_tree()
    print("=== TREE CORPUS ===")
    for s in stats:
        print(s)
    print(f"  TOTAL = {len(corpus)}")
    print()
    collisions, canonical_only = [], 0
    for c in criteria:
        for kw in c["keywords"]:
            canon, noncanon = probe(kw, corpus)
            if noncanon:
                collisions.append((c["id"], kw, noncanon))
            elif canon:
                canonical_only += 1
    nkw = sum(len(c["keywords"]) for c in criteria)
    print(f"=== BRIEF criteria={len(criteria)} keywords={nkw} ===")
    print(f"=== COLLISIONS (keyword 命中非 canonical 路径) = {len(collisions)} ===")
    for cid, kw, hits in collisions:
        print(f"  !! [{cid}] {kw!r} -> {len(hits)} noncanon hits, e.g. {hits[:4]}")
    if not collisions:
        print("  (空) —— 全部判别性长短语均非路径子串，无误钉风险。")
    print(f"  （{canonical_only} 个 keyword 仅命中 canonical 路径，属可接受 hint）")
    print(f"=== 结论: 碰撞数={len(collisions)} (门槛=0) ===")
    sys.exit(0)


if __name__ == "__main__":
    main()
