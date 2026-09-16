"""Regression checks for validation boundaries, especially false passes."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_docs import check_link, destinations, heading_ids, prose
from validate import docs_only
import validate


class ValidationTests(unittest.TestCase):
    def test_docs_classification_never_skips_science_or_workflow_changes(self):
        self.assertTrue(docs_only(["README.md", "docs/TUTORIAL.md", "CITATION.cff"]))
        for path in ("qbp_frames/disjoint.py", "results/PF-08/REPORT.md",
                     "figures/tutorial-readout.json", ".github/workflows/validation.yml",
                     "requirements.txt", "maintenance/repository-polish/MIGRATION.json"):
            self.assertFalse(docs_only(["README.md", path]), path)
        self.assertFalse(docs_only([]))

    def test_real_anchor_required_and_encoded_paths_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "README.md"
            source.write_text("# Home\n")
            (root / "target file.md").write_text("# First\n## Exact risk\n## Exact risk\n")
            check_link(root, source, "target%20file.md#exact-risk-1")
            check_link(root, source, "#home")
            for destination in ("target%20file.md#missing", "absent.md", "../outside.md"):
                with self.assertRaises(ValueError, msg=destination):
                    check_link(root, source, destination)

    def test_code_examples_do_not_create_fake_links_or_headings(self):
        source = "# Actual\n```md\n# Not a heading\n[no](absent.md)\n```\n`[no](fake.md)`\n[yes](target.md)\n"
        self.assertEqual(destinations(source), ["target.md"])
        self.assertEqual(heading_ids(source), {"actual"})
        with self.assertRaises(ValueError):
            prose("```python\nprint(1)\n")

    def test_missing_reference_definition_fails(self):
        with self.assertRaises(ValueError):
            destinations("[Proof][missing]")
        self.assertEqual(destinations("[Proof][source]\n[source]: proof.md#result\n"), ["proof.md#result"])

    def test_migration_hashes_reject_changed_evidence_and_copied_guidance(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(validate, "PACKET_COUNTS", {}):
            root = Path(tmp)
            record = root / "maintenance/repository-polish"
            record.mkdir(parents=True)
            original = root / "proof.md"
            copy = root / "guidance.md"
            original.write_bytes(b"original proof\n")
            copy.write_bytes(b"original guidance\n")
            data = {"preserved_files": {"proof.md": hashlib.sha256(original.read_bytes()).hexdigest()},
                    "guidance_copies": [{"preserved_copy": "guidance.md", "sha256": hashlib.sha256(copy.read_bytes()).hexdigest()}]}
            (record / "MIGRATION.json").write_text(json.dumps(data))
            self.assertEqual(validate.verify_migration(root)["guidance_copies_verified"], 1)
            copy.write_bytes(b"changed guidance\n")
            with self.assertRaisesRegex(ValueError, "Copied guidance identity"):
                validate.verify_migration(root)
            copy.write_bytes(b"original guidance\n")
            original.write_bytes(b"changed proof\n")
            with self.assertRaisesRegex(ValueError, "Preserved evidence identity"):
                validate.verify_migration(root)


if __name__ == "__main__":
    unittest.main()
