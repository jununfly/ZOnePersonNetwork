#!/usr/bin/env python3
"""Generate the two targeted re-collection briefs for the 83-unknown pilot.

Q5b (zj 2026-11-23): only the unknown-scene criteria are re-collected, with
path-unique keyword anchoring ('readme.md' matches the root README.md only,
not README.ja.md / README.zh.md) — the lesson from opn-landscape's weak-evidence
incident where a colliding keyword pinned evidence to the wrong canonical file.

Repo identities are copied from SoT (bundle.json verification-plans), NOT guessed:
  dmux       = standardagents/dmux @ 8cb3d926631a9349ab67f7ece41d218427ac7e24
  mem-vault  = songs-aaa/shared-memory-vault @ 59f0b12134622c0ad93ef59ef6373cfe587deaf3
The `revision` field is deliberately the SoT version-pin SHA (the compiler
ignores repositories[].revision anyway — see baseline §6.3).

Unknown scenes are derived mechanically from bundle.json difference-entries
(verdict=unknown), so the briefs cannot drift from what is actually missing.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLE = os.path.join(HERE, "..", "bundle.json")
TEMPLATE = os.path.join(HERE, "brief-multica.json")

# project -> (owner, name, SoT version-pin SHA). Copied from bundle verification-plans.
REPOS = {
    "dmux": ("standardagents", "dmux", "8cb3d926631a9349ab67f7ece41d218427ac7e24"),
    "mem-vault": ("songs-aaa", "shared-memory-vault", "59f0b12134622c0ad93ef59ef6373cfe587deaf3"),
}

# Path-unique keyword + scene-discriminating phrases. 'readme.md' pins the root
# README.md; the rest are candidate body phrases for excerptForCriterion. Kept
# generic (not multica-specific) so they apply to both small README-centric repos.
SCENE_KW = {
    "task-workitem": ["readme.md", "issue board", "work item", "track tasks"],
    "identity-scope": ["readme.md", "roles and access scopes", "security model", "owner"],
    "session-context": ["readme.md", "context", "session", "handoff", "continuity"],
    "execution-workspace": ["readme.md", "runtime", "sandbox", "local daemon", "execution"],
    "approval-human": ["readme.md", "approval", "human approval", "review", "you decide"],
    "result-provenance": ["readme.md", "provenance", "changelog", "diff", "commit"],
    "memory-knowledge": ["readme.md", "playbook", "knowledge", "reuse", "memory"],
    "observability": ["readme.md", "execution log", "metrics", "tracing", "observability"],
    "config-strategy": ["readme.md", "configuration", "policy", "access scopes", "config"],
    "runtime-integration": ["readme.md", "self-host", "CLI", "API", "integration"],
    "agent-protocol": ["readme.md", "daemon", "protocol", "agent", "MCP"],
    "tech-design": ["readme.md", "architecture", "SQLite", "PostgreSQL", "Go", "Markdown"],
}

def main():
    b = json.load(open(BUNDLE, encoding="utf-8"))
    tpl = json.load(open(TEMPLATE, encoding="utf-8"))
    q_by_id = {c["id"]: c["question"] for c in tpl["brief"]["criteria"]}

    for proj, (owner, name, pin) in REPOS.items():
        # mechanically derive this project's unknown scenes from the SoT
        unknown_ids = sorted({
            de["scene"].replace("SC::", "")
            for de in b["difference-entries"]
            if de["project"] == proj and de["verdict"] == "unknown"
        })
        criteria = []
        for scene in unknown_ids:
            cid = f"mod-{scene}"
            if cid not in q_by_id:
                raise SystemExit(f"no question template for {cid} (scene {scene})")
            if scene not in SCENE_KW:
                raise SystemExit(f"no keyword set for scene {scene}")
            criteria.append({
                "id": cid,
                "question": q_by_id[cid],
                "critical": True,
                "keywords": SCENE_KW[scene],
            })
        brief = dict(tpl["brief"])  # shallow copy; replace the four varying fields
        brief["topic"] = (
            f"Targeted re-collection for {owner}/{name} (SoT pin {pin[:8]}…, compiler "
            f"resolves default-branch HEAD) to fill {len(criteria)} unknown scenario cells "
            f"in the ZOnePersonNetwork cross-comparison. ONLY unknown-scene criteria; "
            f"path-unique keyword 'readme.md' anchors the root README. Commit-pinned. "
            f"No adoption ranking."
        )
        brief["repositories"] = [{"owner": owner, "name": name, "revision": pin}]
        brief["criteria"] = criteria
        out = {"protocol": tpl["protocol"], "operation": "collect", "brief": brief}
        path = os.path.join(HERE, f"brief-pilot-{proj}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"{proj}: {len(criteria)} criteria -> {path}")

if __name__ == "__main__":
    main()
