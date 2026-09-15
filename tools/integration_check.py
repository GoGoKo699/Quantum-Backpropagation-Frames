"""Read-only integration gate: tests, immutable evidence, and the same PF-02 grid.

Run in a clean full Git checkout. All generated files go under an unused runs/
directory. No historical record is rewritten and no GitHub write is performed.
"""
from __future__ import annotations
import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '8781c8fad5de5742b743178268b8e4f0e4b4f089'
FROZEN = ['research', 'provenance', 'results/PF-01', 'results/PF-02',
          'validation/bootstrap', 'validation/initialization', 'PACKAGE_MANIFEST.json',
          'qbp_frames/readout.py', 'tests/test_pf02.py']
STORED = ROOT / 'results/PF-02/remote_validation/34956367799-1/acceptance'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, timeout=30).decode()


def frozen_inventory():
    old = git('ls-tree', '-r', '--full-tree', BASELINE, '--', *FROZEN)
    current = git('ls-tree', '-r', '--full-tree', 'HEAD', '--', *FROZEN)
    if not old or old != current:
        raise RuntimeError('Frozen evidence or compiler files differ from PF-02')
    inventory = {}
    for line in old.splitlines():
        meta, name = line.split('\t', 1)
        mode, kind, expected = meta.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise RuntimeError(f'Unexpected frozen entry: {name}')
        path = ROOT / name
        if path.is_symlink():
            raise RuntimeError(f'Unexpected evidence symlink: {name}')
        data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if actual != expected:
            raise RuntimeError(f'Working-tree evidence changed: {name}')
        inventory[name] = {'git_blob': actual, 'sha256': hashlib.sha256(data).hexdigest()}
    return inventory


def compare(a, b, path='root'):
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            raise AssertionError(f'Keys changed: {path}')
        for k in a:
            compare(a[k], b[k], f'{path}.{k}')
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            raise AssertionError(f'Length changed: {path}')
        for i, (x, y) in enumerate(zip(a, b)):
            compare(x, y, f'{path}[{i}]')
    elif isinstance(a, float) or isinstance(b, float):
        if not math.isfinite(float(a)) or not math.isfinite(float(b)) or not math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12):
            raise AssertionError(f'Numeric result changed: {path}: {a} != {b}')
    elif a != b:
        raise AssertionError(f'Result changed: {path}: {a!r} != {b!r}')


def compare_csv(stored, fresh):
    with stored.open(newline='') as h:
        before = list(csv.DictReader(h))
    with fresh.open(newline='') as h:
        after = list(csv.DictReader(h))
    if len(before) != len(after):
        raise AssertionError(f'CSV row count changed: {fresh.name}')
    for i, (a, b) in enumerate(zip(before, after)):
        if a.keys() != b.keys():
            raise AssertionError('CSV columns changed')
        for key in a:
            if a[key] == b[key]:
                continue
            try:
                compare(float(a[key]), float(b[key]), f'{fresh.name}:{i}:{key}')
            except ValueError as exc:
                raise AssertionError(f'CSV categorical result changed: {i}:{key}') from exc
    return len(after)


def boundary_probes():
    # Execute the pinned old adapter with its original source-relative path.
    ns = {'__file__': str(ROOT / 'qbp_frames/parity.py'), '__name__': '_pf02_pinned_probe'}
    source = git('show', f'{BASELINE}:qbp_frames/parity.py')
    exec(compile(source, 'pinned-PF02-parity.py', 'exec'), ns)
    sys.path.insert(0, str(ROOT))
    from qbp_frames import parity
    records = []
    for k, eta in ((2, math.nextafter(1/32, 0.0)), (12, math.ldexp(1.0, -25))):
        required = 0
        ratio = (Fraction(2) - 1) / (2 * Fraction(eta))
        while 4**required < ratio:
            required += 1
        old = ns['rounds_for_relative_bound'](2.0, eta)
        new = parity.rounds_for_relative_bound(2.0, eta)
        if new != required:
            raise AssertionError('Exact-round fix failed')
        records.append({'eta_hex': eta.hex(), 'nominal_k': k,
                        'before': old, 'after': new, 'required': required})
    errors = []
    for label, function in (('before', ns['rounds_for_relative_bound']),
                            ('after', parity.rounds_for_relative_bound)):
        try:
            function(10**400, 0.1)
        except Exception as exc:
            errors.append({'version': label, 'error_type': type(exc).__name__})
        else:
            raise AssertionError('Oversized scalar was accepted')
    if errors[-1]['error_type'] != 'ValueError':
        raise AssertionError('Scalar error contract failed')
    return {'round_thresholds': records, 'oversized_scalar': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    allowed = (ROOT / 'runs').resolve()
    if out == allowed or not out.is_relative_to(allowed):
        parser.error('Use a new output directory strictly below runs/')
    out.mkdir(parents=True, exist_ok=False)
    report = {'status': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(),
              'baseline': BASELINE, 'source_commit': git('rev-parse', 'HEAD').strip(),
              'workflow_run_id': os.environ.get('GITHUB_RUN_ID'),
              'workflow_run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT'),
              'environment': {'python': platform.python_version(), 'numpy': np.__version__},
              'commands': [], 'scope': 'Integration regression only; no new scientific or cost-model claim.'}
    env = os.environ.copy()
    for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
        env[key] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'

    def run(arguments, logname):
        with (out / logname).open('w') as log:
            p = subprocess.run([sys.executable, *arguments], cwd=ROOT, env=env,
                               stdout=log, stderr=subprocess.STDOUT, timeout=300)
        report['commands'].append({'args': arguments, 'log': logname, 'returncode': p.returncode})
        if p.returncode:
            raise RuntimeError(f'Check failed: {logname}')

    try:
        clean = git('status', '--porcelain', '--untracked-files=all')
        if clean.strip():
            raise RuntimeError('Integration gate requires a clean checkout')
        before = frozen_inventory()
        (out / 'frozen-files.json').write_text(json.dumps(before, indent=2) + '\n')
        run(['tools/verify_inputs.py'], 'integrity-before.log')
        run(['-m', 'unittest', 'discover', '-s', 'tests', '-v'], 'tests.log')
        match = re.search(r'Ran (\d+) tests', (out / 'tests.log').read_text())
        if not match or int(match.group(1)) < 36 or not (out / 'tests.log').read_text().rstrip().endswith('OK'):
            raise RuntimeError('Incomplete test suite')
        report['repository_tests'] = int(match.group(1))
        run(['results/PF-01/audit.py', '--output', str(out / 'pf01-diagnostics.json')], 'pf01.log')
        run(['tools/reproduce.py', 'parity', '--output', str(out / 'parity')], 'parity.log')
        run(['tools/reproduce.py', 'matched', '--output', str(out / 'matched')], 'matched.log')
        run(['results/PF-02/acceptance.py', '--output', str(out / 'acceptance')], 'acceptance.log')
        old = json.loads((STORED / 'summary.json').read_text())
        fresh = json.loads((out / 'acceptance/summary.json').read_text())
        for obj in (old, fresh):
            obj.pop('environment', None)
        compare(old, fresh)
        rows = {name: compare_csv(STORED / name, out / 'acceptance' / name)
                for name in ('scenarios.csv', 'candidates.csv')}
        if rows != {'scenarios.csv': 144, 'candidates.csv': 4320}:
            raise RuntimeError('Acceptance coverage changed')
        report['acceptance'] = {'rows_compared': rows, 'winners': fresh['winners'],
                                'parity_wins': fresh['parity_wins'], 'matches_PF02': True,
                                'comparison_tolerance': '1e-12 relative and absolute; categories exact'}
        report['boundary_probes'] = boundary_probes()
        run(['tools/verify_inputs.py'], 'integrity-after.log')
        if frozen_inventory() != before:
            raise RuntimeError('Frozen inventory changed during tests')
        if git('status', '--porcelain', '--untracked-files=all').strip():
            raise RuntimeError('Validation modified the checkout')
        report['frozen_files_verified'] = len(before)
        report['scientific_sources_unchanged'] = True
        report['clean_checkout_before_and_after'] = True
        paths = ('qbp_frames/parity.py', 'qbp_frames/readout.py', 'tests/test_pf02.py',
                 'tests/test_pf03.py', 'tools/integration_check.py', '.github/workflows/validation.yml')
        report['source_sha256'] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
        report['status'] = 'passed'
    except Exception as exc:
        report['status'] = 'failed'
        report['error'] = f'{type(exc).__name__}: {exc}'
    finally:
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        (out / 'RUN.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))
    if report['status'] != 'passed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
