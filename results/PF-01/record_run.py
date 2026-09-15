"""Record an actually completed PF-01 validation run; never infer success from CI scheduling."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=Path, required=True)
    args = p.parse_args()
    directory = args.directory.resolve()
    target = ROOT / 'results/PF-01'
    if not directory.is_relative_to(target):
        p.error('Run directory must be inside this audit result directory')
    read = lambda name: json.loads((directory / name).read_text())
    before, after = read('before.json'), read('after.json')
    assert before == after and before['status'] == 'passed'
    math = read('diagnostics.json')
    assert math['status'] == 'passed' and len(math['checks']) == 17
    code_hash = hashlib.sha256((target / 'audit.py').read_bytes()).hexdigest()
    assert math['source_sha256'] == code_hash
    assert code_hash == '9600d9658964d919acc1cd9ab53928320c6ad7f5d6ad2e324d10cdc9b767e400'
    resources = read('resource_table.json')
    assert all(resources['checks'].values())
    software = read('software.json')
    log = (directory / 'repository-tests.log').read_text()
    matches = re.findall(r'Ran (\d+) tests?', log)
    assert matches and log.rstrip().endswith('OK')
    supplied = {name: read(f'{name}/run.json') for name in ('parity','matched')}
    assert all(v['status'] == 'passed' and v['immutable_sources_unchanged'] for v in supplied.values())
    record = {'status':'completed_with_findings',
              'completed_utc':datetime.now(timezone.utc).isoformat(),
              'source_commit':os.environ.get('GITHUB_SHA'),
              'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),
              'workflow_run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
              'independent_check_groups':len(math['checks']),
              'audit_code_sha256':code_hash,
              'repository_tests':int(matches[-1]),
              'archives_verified':len(before['archives']),
              'extracted_files_verified':before['extracted_files_checked'],
              'supplied_validators':{name:v['status'] for name,v in supplied.items()},
              'software_probe_status':software['status'],
              'software_cases_accepted':sum(x['accepted'] for x in software['findings']),
              'scientific_sources_unchanged':True,
              'matched_tables_regenerated':False,
              'scope':'Completed bounded diagnostics and reproductions; no external proof review, novelty clearance or hardware claim.'}
    with (directory / 'RUN.json').open('x') as f:
        f.write(json.dumps(record,indent=2)+'\n')
    (target / 'REMOTE_VALIDATION.json').write_text(json.dumps({'run_directory':str(directory.relative_to(ROOT)),**record},indent=2)+'\n')
    (target / 'resource_table.json').write_text(json.dumps(resources,indent=2)+'\n')
    files={str(path.relative_to(target)):hashlib.sha256(path.read_bytes()).hexdigest()
           for path in sorted(target.rglob('*')) if path.is_file()
           and '__pycache__' not in path.parts and path.name!='MANIFEST.json'}
    (target / 'MANIFEST.json').write_text(json.dumps({'scope':'Audit result files only; self and caches excluded. Original scientific inputs have their own manifests.','files':files},indent=2)+'\n')
    print(json.dumps(record,indent=2))

if __name__=='__main__':main()
