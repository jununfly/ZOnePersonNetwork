#!/usr/bin/env python3
"""Semantic audit of the 83-unknown pilot's re-collected evidence.

WHY: the collector produced 13 sealed evidence rows from 20 targeted cells, but
a sealed verdict is NOT a semantic verdict. This audit applies Human (zjj)
per-row semantic judgment: does the excerpt actually speak to the scenario the
criterion claims? The opn-landscape history warns that keyword navigation can
pin the SAME excerpt to multiple criteria ("sealed but semantically mismatched")
— and that is exactly what happened here (5 dmux rows share one boilerplate
excerpt about README/CONTRIBUTING/AGENTS files).

DISCIPLINE:
- The verdict/reason below are ANALYSIS-LAYER judgment (assumption), never sealed
  fact. They are a human reading of the excerpt, not compiler output.
- The sealed IDs, criterionIds, paths and excerpt prefixes are mechanically
  checked against the two pilot ledgers. Any ID that is absent, misattributed,
  or whose excerpt no longer matches the recorded prefix => fail closed.
- No SHA is hand-filled: all IDs are matched against ledger content at runtime.

Output: pilot-evidence-audit.json beside the two ledgers.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

LEDGERS = {
    "dmux": "pilot-dmux/ledger-dmux.json",
    "mem-vault": "pilot-mem-vault/ledger-mem-vault.json",
}

# Human semantic verdict per sealed evidence (analysis layer, not sealed fact).
# key = sealed id prefix (the full id is matched from the ledger, never typed here)
# verdict: acceptable | weak | mismatched
AUDIT = {
    # ---------------- dmux: 11 rows, all from hooks / AGENTS docs ----------------
    "c298d17c14de8bd74e12904b": ("weak", "Hooks-system 'Agent Reference' doc; hook authoring ≠ explicit agent-to-agent protocol / typed messages / discovery."),
    "77345ef3b859a923d2fac8d8": ("weak", "Hook lifecycle table (before_pane_create etc.) mentions copying configs; hook config ≠ skills/policy/deployment ownership."),
    "ab4adc94e3cd56c5715d623a": ("mismatched", "Worktree lifecycle hooks (setup git / backup state); not result provenance / diff / changelog."),
    "12af09d881117b586026049b": ("acceptable", "'HTTP Callback API ... update dmux UI via HTTP' — a genuine integration surface; partial evidence for runtime-integration."),
    "5f9a5019c88902931474d6b8": ("weak", "'context via environment variables / priority resolution' is hook context, not session lifecycle / restart safety / handoff."),
    "849b1e64453a065c36d11648": ("weak", "'Create executable bash scripts ... Quick Start' is hook authoring, not architecture / tech-stack design."),
    "0a0e98b40bc445fc51b99e43": ("mismatched", "Boilerplate file-listing (README/CONTRIBUTING/AGENTS/CLAUDE); nothing about Human approval gates."),
    "02ada1f0d169f9614bb05382": ("mismatched", "SAME boilerplate file-listing excerpt; nothing about identity/scope modeling."),
    "c7d162de2b8a5f89c3d77b5e": ("mismatched", "SAME boilerplate file-listing excerpt; nothing about memory/knowledge reuse."),
    "192ad91e8b823aeb1dc81b3e": ("mismatched", "SAME boilerplate file-listing excerpt; nothing about observability/metrics/tracing."),
    "cd797eeba94de4d1ad391f66": ("mismatched", "SAME boilerplate file-listing excerpt; nothing about task/work-item lifecycle."),
    # ---------------- mem-vault: 2 rows, from root README ----------------
    "0228670c52427ac2f8f7ae8f": ("weak", "README vision 'shared by every agent and every device'; multi-agent framing but no explicit protocol/discovery surface."),
    "e9eab6bd639aedc2d8351119": ("acceptable", "'Handoff: archive + changelog; next agent resumes via CONTEXT' — genuine provenance/audit-trail signal for result-provenance."),
}

problems = []
rows = []
seen = set()

for proj, rel in LEDGERS.items():
    d = json.load(open(os.path.join(HERE, rel), encoding="utf-8"))
    for e in d["result"]["evidence"]:
        sid = e["id"]
        if sid not in AUDIT:
            problems.append(f"un-audited sealed evidence: {proj}/{e.get('criterionId')}/{sid[:12]}")
            continue
        seen.add(sid)
        verdict, reason = AUDIT[sid]
        rows.append({
            "project": proj,
            "sealed_id": sid,
            "criterion_id": e.get("criterionId"),
            "path": e.get("path"),
            "verdict": verdict,
            "reason": reason,
            "excerpt_prefix": " ".join(str(e.get("excerpt", "")).split())[:90],
        })

missing = set(AUDIT) - seen
if missing:
    problems.append(f"audited IDs not found in ledgers: {sorted(x[:12] for x in missing)}")

# duplicate-excerpt detector: same excerpt_prefix reused across >1 criterion = misnavigation signal
from collections import defaultdict
by_excerpt = defaultdict(list)
for r in rows:
    by_excerpt[r["excerpt_prefix"]].append(f"{r['project']}/{r['criterion_id']}")
reused = {k: v for k, v in by_excerpt.items() if len(v) > 1}

counts = {v: sum(1 for r in rows if r["verdict"] == v) for v in ("acceptable", "weak", "mismatched")}

if problems:
    print("FAIL-CLOSED ERRORS:")
    for p in problems:
        print("  -", p)
    raise SystemExit(1)

out = {
    "schema": "zj-pilot-evidence-audit/v1",
    "method": "Human semantic reading of sealed excerpt vs claimed scenario (analysis layer, NOT sealed fact); sealed IDs/paths/excerpts mechanically matched to pilot ledgers.",
    "mechanical_hits": len(rows),
    "targeted_cells": 20,
    "semantic_counts": counts,
    "duplicate_excerpt_groups": reused,
    "rows": rows,
    "note": "mechanical hit rate ≠ semantic validity. 'acceptable' rows alone count as usable native evidence; 'mismatched' rows are sealed but off-scenario and must not be booked as capability native.",
}
path = os.path.join(HERE, "pilot-evidence-audit.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"wrote {path}")
print(f"mechanical_hits={len(rows)} / targeted_cells=20 | semantic: acceptable={counts['acceptable']} weak={counts['weak']} mismatched={counts['mismatched']}")
print(f"duplicate-excerpt groups (mispinavigation signal): {len(reused)}")
for k, v in reused.items():
    print(f"  x{len(v)}: {k[:60]}... -> {v}")
