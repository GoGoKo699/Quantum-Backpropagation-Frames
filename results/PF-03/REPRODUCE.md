# Reproduce PF-03

Use a clean full checkout of the review branch and the pinned requirements:

```bash
python -m pip install -r requirements.txt
python tools/integration_check.py --output runs/pf03-review-01
```

The directory must not already exist. The runner records failures and successes
in RUN.json, never writes to a source/evidence directory, and requires the Git
objects of PF-02 commit 8781c8fad5de5742b743178268b8e4f0e4b4f089.

For a focused check only:

```bash
python -m unittest discover -s tests -p test_pf03.py -v
```

This is not equivalent to the full integration gate. The full gate also compares
all PF-02 summary values (apart from environment) and both CSV files against
results/PF-02/remote_validation/34956367799-1/acceptance/.

The exact round-selection test uses Fraction and repeated powers of four as an
independent oracle. It is not another implementation of the new bit-length
formula. The runner also executes the pinned old adapter for two before/after
probes and records actual exception types for an oversized scalar.

Old write-enabled workflows are copied unchanged to retired_workflows/ with a
.txt suffix. They are retained only as historical evidence, never invoked by
current CI. No remote commit is produced by a validation workflow.
