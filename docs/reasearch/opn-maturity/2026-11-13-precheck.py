#!/usr/bin/env python3
"""keyword x tree 路径碰撞预检 —— 2026-11-13 成熟度 brief 草案专用。

纪律来源：docs/reasearch/2026-11-08-research-charter.md
  keyword 既是「路径子串 hint」又是「正文匹配词」。裸路径 keyword（如
  LICENSE / tests / workflows / fixtures）会作为路径子串命中别的非 canonical
  文件，把采集误钉到错误文件。采集前必须做「全 keyword x 全 tree 路径」碰撞预检。

canonical 路径（沿用 opn-cross-comparison/collect/precheck.py 的规则）：
  - docs/**/*.md
  - basename 匹配 (readme|agent|claude|architecture)*.md
  - manifest: package.json / go.mod / go.sum / Cargo.toml / Cargo.lock /
              pyproject.toml / package-lock.json / go.work

tree 语料：10 个 pinned 目标仓的 git/trees?recursive=1，经 /opt/homebrew/bin/gh
只读拉取（绝对定位，gh 不在 PATH 时仍可用）。gh 不可用/失败时回退到仓库内缓存的
docs/reasearch/opn-cross-comparison/collect/tree-*.jsonl。

本脚本只打印到 stdout，不写任何文件；碰撞清单由对话侧用 Write 工具落盘。
用法：python3 2026-11-13-precheck.py
"""
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BRIEF = os.path.join(HERE, "2026-11-13-brief.request.json")
GH = "/opt/homebrew/bin/gh"
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CACHED_TREES = os.path.join(
    REPO_ROOT, "docs", "reasearch", "opn-cross-comparison", "collect", "tree-*.jsonl"
)

# 10 个目标仓，pin 与 2026-11-08-module-matrix.md 一致
REPOS = [
    ("yc-software", "qm", "605c259b"),
    ("makifbaysal", "tasktrooper", "ae5fb965"),
    ("JF3Env", "opencode-coordination", "2c9dd06f"),
    ("alamops", "agetor", "897b70af"),
    ("lanes-sh", "app", "7b9cb385"),
    ("usemozzie", "mozzie", "80f35156"),
    ("songs-aaa", "shared-memory-vault", "59f0b121"),
    ("themanojdesai", "python-a2a", "40b969a4"),
    ("standardagents", "dmux", "8cb3d926"),
    ("jununfly", "ZAgenticOPN", "2ff40cc0"),
]

# 对照组：成熟 brief 容易被误用的裸路径词（不属于 brief，仅证明检测器有效）
NAKED_CONTROL = [
    "license", "changelog", "dockerfile", "makefile", "contributing",
    "tests", "workflows", "fixtures", "package.json", "go.mod",
    "pyproject.toml", "cargo.toml", "spec", "adr",
]

CANON_BASENAME = re.compile(r"^(readme|agent|claude|architecture).*\.md$", re.IGNORECASE)
MANIFEST = {
    "package.json", "go.mod", "go.sum", "cargo.toml", "cargo.lock",
    "pyproject.toml", "package-lock.json", "go.work",
}


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


def load_tree():
    """返回 (corpus, stats)。corpus: [(repo_label, path)]; stats: 可读摘要行列表。"""
    corpus = []
    stats = []
    gh_ok = os.path.exists(GH)
    if gh_ok:
        for owner, name, pin in REPOS:
            label = f"{owner}/{name}"
            try:
                r = subprocess.run(
                    [GH, "api", f"repos/{owner}/{name}/git/trees/{pin}?recursive=1"],
                    capture_output=True, text=True, timeout=30,
                )
                data = json.loads(r.stdout)
                paths = [t["path"] for t in data.get("tree", [])]
                corpus.extend((label, p) for p in paths)
                stats.append(
                    f"  {label:32s} paths={len(paths):5d} "
                    f"truncated={data.get('truncated', False)}  src=gh(pinned)"
                )
            except Exception as e:  # noqa: BLE001 - 诊断用，回退缓存
                gh_ok = False
                stats.append(f"  {label:32s} gh FAILED ({str(e)[:60]})")
                break
    if not gh_ok:
        corpus = []
        stats = []
        for fp in sorted(glob.glob(CACHED_TREES)):
            with open(fp, encoding="utf-8") as fh:
                paths = [ln.strip() for ln in fh if ln.strip()]
            label = os.path.basename(fp)
            corpus.extend((label, p) for p in paths)
            stats.append(f"  {label:32s} paths={len(paths):5d}  src=cached(non-target)")
    return corpus, stats


def probe(keyword, corpus):
    """返回 (canonical_hits, noncanonical_hits) 两个 'repo:path' 列表。"""
    k = keyword.lower()
    canon, noncanon = [], []
    for repo, path in corpus:
        if k in path.lower():
            (canon if is_canonical(path) else noncanon).append(f"{repo}:{path}")
    return canon, noncanon


def main():
    with open(BRIEF, encoding="utf-8") as fh:
        brief = json.load(fh)
    criteria = brief["brief"]["criteria"]

    corpus, stats = load_tree()
    print("=== TREE CORPUS (全 tree 路径) ===")
    for s in stats:
        print(s)
    print(f"  TOTAL paths = {len(corpus)}")
    print()

    total_kw = 0
    canonical_only = 0
    collisions = []  # (criterion_id, keyword, noncanonical_hits)
    for c in criteria:
        for kw in c["keywords"]:
            total_kw += 1
            canon, noncanon = probe(kw, corpus)
            if noncanon:
                collisions.append((c["id"], kw, noncanon))
            elif canon:
                canonical_only += 1

    print(f"=== BRIEF: criteria={len(criteria)}  keywords={total_kw} ===")
    print(f"=== COLLISIONS (keyword 命中非 canonical 路径子串 / 误钉风险) = {len(collisions)} ===")
    if collisions:
        for cid, kw, hits in collisions:
            sample = hits[:5]
            more = "" if len(hits) <= 5 else f" ...(+{len(hits) - 5})"
            print(f"  !! [{cid}] KW={kw!r} -> {len(hits)} non-canonical hits: {sample}{more}")
    else:
        print("  (空) —— 全部判别性长短语均非路径子串，无误钉风险。")
    print(f"  （另有 {canonical_only} 个 keyword 仅命中 canonical 路径，属可接受的文件 hint）")
    print()

    ctrl = 0
    print("=== 对照组：裸路径 keyword 自测（不属于 brief，仅证明检测器非恒返回 0） ===")
    for kw in NAKED_CONTROL:
        canon, noncanon = probe(kw, corpus)
        if noncanon:
            ctrl += 1
            print(f"  [{kw!r}] 会碰撞: {len(noncanon)} 条非 canonical 命中, 例 {noncanon[:3]}")
    print(f"  control collisions = {ctrl}/{len(NAKED_CONTROL)}")
    print()
    print(f"=== 结论: brief 碰撞数 = {len(collisions)} (Phase-3 门槛要求 = 0) ===")
    sys.exit(0)


if __name__ == "__main__":
    main()
