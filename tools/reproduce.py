"""Rerun supplied diagnostics in an isolated copy and preserve a separate report."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import numpy as np
from verify_inputs import ROOT, verify

PACKETS = {
    'parity': ('research/parity_frames', ['validate.py']),
    'matched': ('research/matched_readout', ['validate.py']),
    'matched-full': ('research/matched_readout',
                     ['run_comparison.py', 'validate.py', 'cost_certificates.py', 'uniform_comparison.py']),
}

def file_hashes(path: Path) -> dict[str, str]:
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(path.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}

def check_report(name: str, result: dict) -> None:
    """Imported matched validator reports residuals without final assertions."""
    if name == 'parity':
        if len(result.get('checks', {})) != 8:
            raise ValueError('Unexpected number of parity check groups')
        for label, check in result['checks'].items():
            if check.get('cases', 0) <= 0:
                raise ValueError(f'No cases executed for {label}')
            for field, value in check.items():
                if field.startswith('max_'):
                    if not math.isfinite(float(value)) or abs(float(value)) > 1e-8:
                        raise ValueError(f'Residual outside wrapper tolerance: {label}.{field}={value}')
                if field in ('failures', 'rank_violations') and value != 0:
                    raise ValueError(f'Failed check: {label}.{field}')
    else:
        expected = {'group_mean', 'group_second', 'block_mean', 'block_second',
                    'walsh_aggregate', 'block_aggregate'}
        if set(result.get('checks', {})) != expected:
            raise ValueError('Unexpected matched check groups')
        for label, value in result['checks'].items():
            if not math.isfinite(float(value)) or abs(float(value)) > 1e-8:
                raise ValueError(f'Matched residual outside tolerance: {label}={value}')
            if result.get('counts', {}).get(label, 0) <= 0:
                raise ValueError(f'No matched cases for {label}')
        if result.get('stabilizer_counts') != {'1': 6, '2': 60, '3': 1080}:
            raise ValueError('Unexpected stabilizer counts')

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', choices=PACKETS)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--timeout', type=int, default=600, help='Per-script timeout in seconds')
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    verify()
    output = args.output.resolve()
    for protected in (ROOT / 'research', ROOT / 'provenance'):
        if output == protected or output.is_relative_to(protected):
            parser.error('Output cannot be inside immutable evidence directories')
    output.mkdir(parents=True, exist_ok=False)
    rel, scripts = PACKETS[args.packet]
    original = ROOT / rel
    before = file_hashes(original)
    env = os.environ.copy()
    for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
        env[key] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    report = {'packet': args.packet, 'status': 'running',
              'started_utc': datetime.now(timezone.utc).isoformat(),
              'environment': {'python': platform.python_version(), 'numpy': np.__version__,
                              'platform': platform.platform(), 'thread_limit': 1},
              'source_directory': rel, 'source_sha256': before, 'commands': [],
              'comparison_tables_regenerated': args.packet == 'matched-full',
              'limitations': 'Finite diagnostics; not independent proof, novelty review, or remote CI.'}
    started = time.perf_counter()
    try:
        with tempfile.TemporaryDirectory(prefix='qbp-reproduce-') as tmp:
            work = Path(tmp) / 'packet'
            shutil.copytree(original, work, ignore=shutil.ignore_patterns('__pycache__'))
            initial = file_hashes(work)
            for index, script in enumerate(scripts, 1):
                command = [sys.executable, script]
                log_name = f'{index:02d}-{Path(script).stem}.log'
                with (output / log_name).open('w', encoding='utf-8') as log:
                    proc = subprocess.run(command, cwd=work, env=env, stdout=log,
                                          stderr=subprocess.STDOUT, timeout=args.timeout, check=False)
                report['commands'].append({'command': ['python', script],
                                            'returncode': proc.returncode, 'log': log_name})
                if proc.returncode != 0:
                    raise RuntimeError(f'{script} exited with code {proc.returncode}; see {log_name}')
            values = json.loads((work / 'validation.json').read_text())
            check_report(args.packet, values)
            report['residual_checks'] = 'passed; finite values and residuals <= 1e-8'
            report['check_groups'] = len(values['checks'])
            report['observed_checks'] = values['checks']
            (output / 'validation.json').write_text(json.dumps(values, indent=2) + '\n')
            after = file_hashes(work)
            generated = output / 'generated'
            for name, value in after.items():
                if initial.get(name) != value and name != 'validation.json':
                    dest = generated / name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(work / name, dest)
            report['changed_in_temporary_copy'] = [n for n in after if initial.get(n) != after[n]]
        if file_hashes(original) != before:
            raise RuntimeError('Immutable source changed during execution')
        verify()
        report['status'] = 'passed'
        report['immutable_sources_unchanged'] = True
    except Exception as exc:
        report['status'] = 'failed'
        report['error'] = f'{type(exc).__name__}: {exc}'
    finally:
        report['elapsed_seconds'] = time.perf_counter() - started
        (output / 'run.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'output': str(args.output),
                      'elapsed_seconds': report['elapsed_seconds']}, indent=2))
    if report['status'] != 'passed':
        raise SystemExit(1)

if __name__ == '__main__':
    main()
