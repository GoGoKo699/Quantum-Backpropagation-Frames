"""Integration regressions; no new ansatz or cost sweep."""
from fractions import Fraction
import math
from pathlib import Path
import random
import unittest
import numpy as np
from qbp_frames import parity

ROOT = Path(__file__).resolve().parents[1]


def exact_rounds(beta, eta):
    """Independent rational oracle, deliberately using repeated multiplication."""
    ratio = (Fraction(float(beta)) - 1) / (2 * Fraction(float(eta)))
    power, count = Fraction(1), 0
    while power < ratio:
        power *= 4
        count += 1
    return count


class IntegrationTests(unittest.TestCase):
    def test_thresholds_and_neighbors(self):
        for k in range(537):
            eta = math.ldexp(1.0, -1 - 2*k)
            for e in (eta, math.nextafter(eta, 0.0), math.nextafter(eta, math.inf)):
                with self.subTest(k=k, eta=e.hex()):
                    self.assertEqual(parity.rounds_for_relative_bound(2.0, e), exact_rounds(2.0, e))

    def test_binary64_extremes(self):
        betas = (1.0, math.nextafter(1.0, 2.0), 2.0, 64.0, float.fromhex('0x1.fffffffffffffp+1023'))
        etas = (float.fromhex('0x0.0000000000001p-1022'), 1e-300, 0.1, 1.0, 1e308)
        for b in betas:
            for e in etas:
                self.assertEqual(parity.rounds_for_relative_bound(b, e), exact_rounds(b, e))

    def test_random_exact_minimality(self):
        rng = random.Random(2026091568)
        for _ in range(500):
            beta = 1.0 + math.ldexp(rng.uniform(0.5, 1.0), rng.randrange(-52, 1024))
            eta = math.ldexp(rng.uniform(0.5, 1.0), rng.randrange(-1072, 1024))
            self.assertEqual(parity.rounds_for_relative_bound(beta, eta), exact_rounds(beta, eta))

    def test_oversized_scalars_raise_value_error(self):
        for b, e in ((10**400, 0.1), (2.0, 10**400)):
            with self.assertRaises(ValueError):
                parity.rounds_for_relative_bound(b, e)

    def test_original_estimators_unchanged(self):
        rng = np.random.default_rng(2026091568)
        for n in range(1,5):
            t = rng.normal(size=(1 << n, 3)); t[0] = 0
            q = rng.normal(size=1 << n); q /= np.linalg.norm(q)
            for k in range(5):
                np.testing.assert_array_equal(parity.interpolated_covariance(t, q, k),
                                              parity._ref.interpolated_covariance(t, q, k))
            zero = np.zeros_like(t)
            self.assertEqual(parity.risk_bound(zero, 0), 0.0)

    def test_active_ci_is_read_only_and_complete(self):
        paths = sorted((ROOT / '.github/workflows').glob('*.yml'))
        self.assertEqual([p.name for p in paths], ['validation.yml'])
        text = paths[0].read_text()
        self.assertIn('contents: read', text)
        self.assertNotIn('contents: write', text)
        self.assertNotIn('git push', text)
        self.assertNotIn('pull_request_target', text)
        self.assertIn('pull_request:', text)
        self.assertIn('tools/integration_check.py', text)
        self.assertIn('actions/upload-artifact@', text)


if __name__ == '__main__':
    unittest.main()
