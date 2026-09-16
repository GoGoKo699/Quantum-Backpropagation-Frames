# Reproduce PF-05

Use Python 3.13 and the repository's pinned NumPy requirement. The independent
new diagnostic has no imports from prior proof implementations:

```bash
python results/PF-05/audit.py --output runs/pf05-audit-01
```

The output directory must not exist and cannot be inside the source packet.
The script writes diagnostics.json and fails on an assertion. It records the
actual environment, its source SHA-256, seed, case counts and residuals. The
2e-9 floating tolerance is a check threshold, not an exact-error certification.

The full read-only GitHub gate also executes tools/integration_check.py, checks
PF-04 packet hashes, runs the original PF-04 study, verifies PF-05 packet hashes,
and runs this audit. Prior proof/code/evidence paths are compared against the
pinned source commit before/after; the checkout must remain clean. Artifacts
contain the run logs and fresh generated data. No workflow pushes a branch.

MANIFEST.json hashes the completed local audit packet, excluding itself, START,
and the later remote receipt. diagnostics.json is the local reference run, not
a relabeled remote result. The remote run has its own actual versions and logs.
No full matched-cost table regeneration or new parameter sweep is part of PF-05.
