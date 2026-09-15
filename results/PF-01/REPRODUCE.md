# Reproduce PF-01

Use a checkout of the audit branch. Python 3.13.5 and NumPy 2.3.5 were used locally. No network is required after dependency installation.

```bash
python -m pip install -r requirements.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python tools/verify_inputs.py
python -m unittest discover -s tests -v
python results/PF-01/audit.py --output runs/PF-01-new/diagnostics.json
python results/PF-01/software_probe.py --output runs/PF-01-new/software.json
python results/PF-01/resources.py --output runs/PF-01-new/resources.json
python tools/reproduce.py parity --output runs/PF-01-new/parity
python tools/reproduce.py matched --output runs/PF-01-new/matched
python tools/verify_inputs.py
```

The three audit scripts refuse to overwrite existing output files. The supplied reproduction runner uses isolated copies and preserves its output. The software probe is a diagnostic: status `issues_found` is the expected result at the audited baseline, not evidence that invalid inputs are safe. The mathematical validator raises on an invalid check and reports no pass merely because a process exits successfully.

The local source snapshot was the original uploaded starter: its nine wrapper tests passed. The remote initialized repository has twelve wrapper tests; remote CI must be consulted separately. Scientific archives are identical in both, with Git-blob and SHA-256 identities recorded in BASELINE.json. Do not describe the local directory as a full clone of the remote baseline.

The independent ensemble test stops at four system qubits. Rank/Gauss-sum witnesses use explicit vectors through eight qubits. These are finite identity diagnostics, not scalable quantum simulation, hardware timing, or an asymptotic proof. All-to-all logical resource substitutions are in resource_table.json and exclude unpriced operations as explicitly marked.

Paper source files were inspected online. Their versions and mathematical locators are recorded, but their original PDF bytes were not downloaded and have no claimed local checksum. Numeric output timestamps and rounding may vary. Audit code and recorded evidence are hashed by MANIFEST.json; imported data are governed by the original input manifests.
