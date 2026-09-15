"""Bounded repository smoke checks; not a replacement for the imported validators."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from verify_inputs import verify, checked_path
from reproduce import check_report
spec = importlib.util.spec_from_file_location('parity_packet_core', ROOT / 'research/parity_frames/core.py')
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

class RepositoryTests(unittest.TestCase):
    def test_standalone_project_framing(self):
        for name in ('README.md', 'docs/SCOPE.md', 'docs/RESEARCH_MAP.md',
                     'SETUP_GITHUB.md', 'work_orders/CURRENT.md'):
            text = (ROOT / name).read_text().lower()
            self.assertNotIn('beyond hopf', text, name)
            self.assertNotIn('non-hopf', text, name)
            self.assertNotIn('beyond the hopf', text, name)

    def test_origin_is_not_a_result_dependency(self):
        text = (ROOT / 'provenance/ORIGIN.md').read_text()
        self.assertIn('source of inspiration', text)
        self.assertIn('not a', text)
        self.assertIn('dependency', text)

    def test_repository_target_recorded(self):
        manifest = json.loads((ROOT / 'provenance/INPUTS.json').read_text())
        self.assertTrue(manifest['remote_repository_created'])
        self.assertEqual(manifest['repository'],
                         'GoGoKo699/Quantum-Backpropagation-Frames')

    def test_archive_integrity(self):
        report = verify()
        self.assertEqual(report['manifest_entries_checked'], 20)
        self.assertEqual(report['extracted_files_checked'], 22)

    def test_safe_paths(self):
        with self.assertRaises(ValueError):
            checked_path(ROOT, '../outside')

    def test_clean_parity_gadget(self):
        for a in range(4):
            for b in range(4):
                for x in range(4):
                    out = core.simulate_gadget_basis(2, x, a, b)
                    self.assertEqual(out[:3], (x, 0, 0))
                    self.assertEqual(out[3], (-1)**(core.parity(a&x)*core.parity(b&x)))

    def test_covariance_interpolation_small_ensemble(self):
        rng = np.random.default_rng(2026091552)
        T = rng.normal(size=(4, 2)); T[0] = 0
        q = rng.normal(size=4); q /= np.linalg.norm(q)
        cov = np.array([core.measurement_moments(T, q, core.quadratic_phase(2, m))[1]
                        for m in range(2)])
        for rounds in (0, 1, 2, 3):
            empirical = np.einsum('m,mij->ij', core.rounds_mask_distribution(2, rounds), cov)
            np.testing.assert_allclose(empirical, core.interpolated_covariance(T, q, rounds), atol=1e-12)

    def test_shift_decoder(self):
        t = np.array([0.0, 0.2, -0.3, 0.7])
        table = core.fwht(t)
        pairs = [(1, 3), (2, 1)]
        for y in range(4):
            self.assertAlmostEqual(core.local_shift_score(table, y, pairs),
                                   core.local_direct_score(t, y, pairs), places=12)

    def test_invalid_response_is_rejected(self):
        with self.assertRaises(ValueError):
            core.measurement_moments(np.zeros((4, 1)), np.ones(4))

    def test_report_wrapper_rejects_nan(self):
        record = json.loads((ROOT / 'research/matched_readout/validation.json').read_text())
        record['checks']['group_mean'] = float('nan')
        with self.assertRaises(ValueError):
            check_report('matched', record)

    def test_inherited_reports_match_declared_schema(self):
        for packet, path in [('parity', 'parity_frames'), ('matched', 'matched_readout')]:
            record = json.loads((ROOT / f'research/{path}/validation.json').read_text())
            check_report(packet, record)

    def test_readme_local_links(self):
        text = (ROOT / 'README.md').read_text()
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if '://' not in link:
                self.assertTrue((ROOT / link.split('#')[0]).exists(), link)

if __name__ == '__main__':
    unittest.main()
