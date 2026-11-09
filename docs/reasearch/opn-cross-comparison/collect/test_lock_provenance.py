#!/usr/bin/env python3
"""TDD guard for cutting the ZHarness dependency from the zj-research compiler lock.

Background:
- The research compiler artifact is `@deepseek-ai/dsh-research-compiler-artifact`
  (dsh = DeepSeek Harness), vendored into jununfly/ZHarness as a build source.
- At runtime `research_cli.artifact_command` reads ONLY `artifact` (filename) +
  `sha256` from the lock and loads the bundled local tgz; the lock's top-level
  `repository`/`commit` fields are dead metadata and were misattributed as the
  "version source" (ZHarness). This test enforces the cut:
    事一: re-identify the artifact by its real upstream identity; ZHarness is
          provenance metadata, never a version pin.
    事三 (naming): the artifact filename must not embed a ZHarness commit hash.
It also proves the loader still resolves the renamed artifact (sha256 intact),
so the cut is non-regressive.
"""

import json
import sys
import unittest
from pathlib import Path

SKILL = Path("/Users/bilibili/.workbuddy/skills/zj-research")
sys.path.insert(0, str(SKILL / "scripts"))
import research_cli as rc  # noqa: E402

ARTIFACTS = SKILL / "artifacts"
LOCK = ARTIFACTS / "compiler-lock.json"


class LockProvenanceTest(unittest.TestCase):
    def setUp(self):
        self.lock = json.loads(LOCK.read_text(encoding="utf-8"))

    def test_no_top_level_zharness_identity(self):
        # 事一/事三: ZHarness must no longer appear as the version identity.
        self.assertNotIn(
            "repository",
            self.lock,
            "top-level 'repository' must be removed from the lock (move under provenance)",
        )
        self.assertNotIn(
            "commit",
            self.lock,
            "top-level 'commit' must be removed from the lock (move under provenance)",
        )

    def test_artifact_name_has_no_commit_hash(self):
        name = self.lock["artifact"]
        self.assertNotRegex(
            name,
            r"[0-9a-f]{7,40}",
            "artifact filename must not embed a ZHarness commit hash",
        )

    def test_provenance_labels_zharness_as_metadata_only(self):
        prov = self.lock.get("provenance")
        self.assertIsInstance(prov, dict, "lock must carry a 'provenance' block")
        self.assertIn("upstream", prov)
        self.assertIn("@deepseek-ai/dsh-research-compiler-artifact", prov["upstream"])
        bs = prov.get("buildSource")
        self.assertIsInstance(bs, dict, "provenance.buildSource must record the build source")
        self.assertEqual(bs.get("repository"), "https://github.com/jununfly/ZHarness")
        self.assertEqual(
            bs.get("role"),
            "build-source-metadata",
            "ZHarness must be labeled metadata, never a version pin",
        )
        self.assertNotIn("version", bs, "buildSource must not be treated as a version")

    def test_loader_resolves_renamed_artifact(self):
        # Non-regression: the loader still finds + verifies the artifact after rename.
        cmd = rc.artifact_command("research", rc.PROTOCOL)
        self.assertEqual(cmd[0], "node")
        self.assertTrue(Path(cmd[1]).is_file(), "resolved executable must exist")
        actual = rc.file_sha256(ARTIFACTS / self.lock["artifact"])
        self.assertEqual(
            actual,
            self.lock["sha256"],
            "artifact sha256 must match the lock (rename must not change bytes)",
        )


if __name__ == "__main__":
    unittest.main()
