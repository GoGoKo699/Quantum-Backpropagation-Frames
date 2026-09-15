"""Reproduce input-contract defects without modifying the imported implementation."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import warnings
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'research/parity_frames/core.py'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite output')
    spec = importlib.util.spec_from_file_location('pf01_guard_probe_target', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    T = np.array([[0.], [1.]])
    q = np.array([0., 1.])
    cases = [
        ('nan_response', T, np.array([np.nan, 0.]), None),
        ('complex_response_silently_coerced', T, np.array([0., 1.+1.j]), None),
        ('nan_internal_tangent', np.array([[0.], [np.nan]]), q, None),
        ('nan_phase', T, q, np.array([1., np.nan])),
    ]
    findings = []
    for label, tangent, response, phase in cases:
        finding = {'case': label}
        with warnings.catch_warnings(record=True) as messages:
            warnings.simplefilter('always')
            try:
                result = module.measurement_moments(tangent, response, phase)
                finding.update(accepted=True, mean_finite=bool(np.all(np.isfinite(result[0]))))
            except Exception as exc:
                finding.update(accepted=False, exception=f'{type(exc).__name__}: {exc}')
            finding['warnings'] = [str(item.message) for item in messages]
        findings.append(finding)
    report = {'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'status': 'issues_found' if any(f['accepted'] for f in findings) else 'rejected',
              'findings': findings,
              'scope': 'Input guard defects, not counterexamples to valid-domain mathematics. Imported code unchanged.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
