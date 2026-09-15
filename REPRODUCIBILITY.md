# Reproducibility

## Environment

The startup run records the actual Python and NumPy versions in
validation/bootstrap/. The local bootstrap environment is Python 3.13.5 and
NumPy 2.3.5. The root requirements pin NumPy 2.3.5 for the supplied experiment
records. No routed quantum hardware or external service is needed to run them.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/verify_inputs.py
python -m unittest discover -s tests -v
```

## Scientific diagnostic reruns

```bash
python tools/reproduce.py parity --output runs/parity-01
python tools/reproduce.py matched --output runs/matched-01
```

`parity` executes the complete supplied parity validator. `matched` executes
its supplied validate.py against existing imported comparison data; it does
not regenerate every comparison JSON. `matched-full` additionally regenerates
the comparison and cost tables before validation:

```bash
python tools/reproduce.py matched-full --output runs/matched-full-01
```

The full matched path includes exponential-size small-system ensembles. It is
not part of the bootstrap or default CI. Do not increase target sizes without
an explicit resource estimate. The packet code contains dense diagnostics, not
the production-scale local compiler discussed in earlier conversations.

Each invocation refuses to overwrite an existing output directory, verifies
all imports, copies the chosen packet to a temporary directory, limits BLAS
threads, logs each command, and preserves generated JSON plus before/after
hashes. It checks reported residuals as well as exit status. See run.json for
which commands actually executed.

The supplied originals and their stored JSON remain unchanged. Exact byte
agreement of fresh numerical outputs is not required across machines: elapsed
time and library-specific floating-point rounding can differ. Assertions and
recorded numerical tolerances are the relevant diagnostic conditions.

## What a pass establishes

- Archive identity, extracted-file identity, and inherited fixture equality.
- Operation of the repository wrappers and bounded smoke tests.
- For a requested scientific run, the checks actually enumerated in its JSON.

It does not establish theorem truth at all dimensions, interval-arithmetic
certification, source novelty, measurement optimality outside the stated class,
or hardware/runtime superiority.

## CI

The included workflow runs import integrity, repository tests, and the parity
validator on Python 3.13. Local validation is not a remote CI run. Remote CI outcomes must be read from
GitHub for the actual pushed commit.
