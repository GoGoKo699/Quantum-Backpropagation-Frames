"""Record only completed initialization checks, then remove transfer fragments."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil

ROOT = Path(__file__).resolve().parents[1]
V = ROOT / 'validation/initialization'
reports = {name: json.loads((V / name / 'run.json').read_text())
           for name in ('parity', 'matched')}
if any(r['status'] != 'passed' or not r['immutable_sources_unchanged']
       for r in reports.values()):
    raise RuntimeError('Validator checks are incomplete')
log = (V / 'repository-tests.log').read_text()
if 'Ran 12 tests' not in log or not log.rstrip().endswith('OK'):
    raise RuntimeError('Repository tests are incomplete')
integrity = json.loads((V / 'integrity.json').read_text())
if integrity['status'] != 'passed' or integrity['extracted_files_checked'] != 22:
    raise RuntimeError('Input verification is incomplete')
record = {
    'status': 'completed',
    'completed_utc': datetime.now(timezone.utc).isoformat(),
    'repository': 'GoGoKo699/Quantum-Backpropagation-Frames',
    'source_commit': os.environ.get('GITHUB_SHA', 'local-dry-run'),
    'workflow_run_id': os.environ.get('GITHUB_RUN_ID'),
    'repository_tests': 12,
    'parity_validator': reports['parity']['status'],
    'matched_validator': reports['matched']['status'],
    'original_archives_verified': 2,
    'extracted_files_verified': 22,
    'scientific_sources_unchanged': True,
    'scope': 'Initialization and standalone framing only; no new scientific audit.',
    'work_order': 'PF-01 remains READY; not executed by initialization.'
}
(ROOT / 'provenance/REMOTE_INITIALIZED.json').write_text(
    json.dumps(record, indent=2) + '\n')
(V / 'REPORT.md').write_text('''# Repository initialization verification

The private repository was initialized with standalone framing. Current scope,
claims, and workflow rules do not depend on the historical source of inspiration.
Immutable evidence and original bootstrap records were preserved exactly.

## Checks completed in this run

- Both original archive SHA-256 hashes and all 22 extracted files verified.
- All 12 repository tests passed.
- The supplied parity validator passed in an isolated temporary copy.
- The supplied matched-readout validator passed in an isolated temporary copy.
- Both validators left the imported scientific sources unchanged.

The logs, environment, source hashes, command status, and residual checks are
recorded alongside this report. The source commit and workflow run identifier
are in `provenance/REMOTE_INITIALIZED.json`.

## Boundary

The full matched-comparison tables were not regenerated. No new proof, novelty,
hardware, or asymptotic audit was performed. PF-01 remains READY. No license,
release, publication, or change to another repository is implied.

The one-time import workflow is inert after initialization because its READY
marker and transfer files have been removed. The ordinary validation workflow
is maintained separately.
''')
shutil.rmtree(ROOT / '.bootstrap')
files = {}
for p in sorted(ROOT.rglob('*')):
    if not p.is_file():
        continue
    rel = p.relative_to(ROOT)
    if any(x in rel.parts for x in ('.git', '__pycache__', '.venv', 'runs')):
        continue
    if rel.as_posix() == 'PACKAGE_MANIFEST.json':
        continue
    files[rel.as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
(ROOT / 'PACKAGE_MANIFEST.json').write_text(json.dumps({
    'schema_version': 1,
    'scope': 'Post-initialization files; self, .git, caches, environments, and runs excluded.',
    'files': files
}, indent=2) + '\n')
print(json.dumps(record, indent=2))
