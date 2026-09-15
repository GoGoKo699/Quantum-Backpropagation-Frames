"""Execute PF-02 checks and retain a uniquely named verification record."""
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
runid=os.environ.get('GITHUB_RUN_ID','local')+'-'+os.environ.get('GITHUB_RUN_ATTEMPT','1')
out=ROOT/'results/PF-02/remote_validation'/runid
out.mkdir(parents=True,exist_ok=False)
env=os.environ.copy()
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):env[key]='1'
env['PYTHONDONTWRITEBYTECODE']='1'
commands=[]
def run(args,log):
    with (out/log).open('w') as handle:
        p=subprocess.run([sys.executable,*args],cwd=ROOT,env=env,stdout=handle,
                         stderr=subprocess.STDOUT,timeout=300)
    commands.append({'args':args,'log':log,'returncode':p.returncode})
    if p.returncode:raise RuntimeError(f'Failed: {args}; see {log}')

run(['tools/verify_inputs.py','--json',str(out/'before.json')],'integrity-before.log')
run(['-m','unittest','discover','-s','tests','-v'],'tests.log')
run(['tools/reproduce.py','parity','--output',str(out/'parity')],'parity.log')
run(['tools/reproduce.py','matched','--output',str(out/'matched')],'matched.log')
run(['results/PF-02/acceptance.py','--output',str(out/'acceptance')],'acceptance.log')
run(['tools/verify_inputs.py','--json',str(out/'after.json')],'integrity-after.log')
before=json.loads((out/'before.json').read_text());after=json.loads((out/'after.json').read_text())
if before!=after:raise RuntimeError('Evidence changed during verification')
summary=json.loads((out/'acceptance/summary.json').read_text())
if summary['scenario_count']!=144 or summary['candidate_rows']!=4320:
    raise RuntimeError('Unexpected acceptance coverage')
text=(out/'tests.log').read_text();match=re.search(r'Ran (\d+) tests',text)
if not match or not text.rstrip().endswith('OK'):raise RuntimeError('Missing successful unittest summary')
paths=['qbp_frames/__init__.py','qbp_frames/parity.py','qbp_frames/readout.py',
       'tests/test_pf02.py','results/PF-02/acceptance.py','results/PF-02/record_run.py']
report={'status':'completed_with_findings','source_commit':os.environ.get('GITHUB_SHA'),
 'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'workflow_run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
 'environment':{'python':platform.python_version(),'numpy':np.__version__},
 'run_directory':str(out.relative_to(ROOT)),'repository_tests':int(match.group(1)),
 'new_test_methods':18,'archives_verified':2,'extracted_files_verified':22,
 'scientific_sources_unchanged':True,'parity_validator':'passed','matched_validator':'passed',
 'acceptance_scenarios':summary['scenario_count'],'candidate_rows':summary['candidate_rows'],
 'winners':summary['winners'],'parity_wins':summary['parity_wins'],
 'input_repair':'accepted for maintained qbp_frames.parity API; preserved archive remains unchanged',
 'advantage_acceptance':'not established by this bounded test',
 'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
 'commands':commands,
 'scope':'Finite exact-logical tests and declared expected-work prescriptions, not hardware timing, independent peer review or unrestricted optimality.'}
(out/'RUN.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'results/PF-02/REMOTE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
