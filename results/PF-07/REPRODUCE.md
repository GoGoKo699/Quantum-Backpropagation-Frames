# Reproduce PF-07

In a full repository checkout, install the pinned requirements and use NEW
output paths:

```bash
python -m pip install -r requirements.txt
python tools/integration_check.py --output runs/integration-pf07
python results/PF-07/study.py --output runs/pf07-study
```

The complete GitHub workflow also verifies and executes PF-04, PF-05 and PF-06
before PF-07. It uses a read-only token and never commits generated evidence.
All generated results are placed below ignored runs/ and uploaded as an artifact.
A full Git checkout is required for the inherited integration gate, but not for
the standalone new study with its three hash-pinned dependency files.

The standalone delivery contains those exact dependencies, new source, local
results and the remote artifact. It is not represented as a clone of all Git
history. The new study outputs diagnostics.json and one explicit elementary
gate program example. Dense reference arrays occur only in small diagnostic
routines; the larger sequence emits gates into a counter without storing them.

Qubit site 0 is the reference; system sites are offset by one in gate tuples.
Addresses and bit strings are big-endian. Ry(theta) means exp(-i theta Y): a
hardware API using conventional R_y(phi) needs phi=2theta. The user-facing
original parameter order is the inherited circuit order, not singular axes.

Randomness: base seed 2026091607; the physical grid is independently restarted
at seed+1. No extra objectives or prices are searched to select a winner. The
large decoder probes are fabricated bit strings for testing the scanner, not
quantum outcomes or a claim of a 256-qubit state simulation.

The first local run is preserved separately in the delivery. The final packaged
source is rerun into a new directory; source hashes identify both. The current
manifest identifies final packet content. No earlier packet manifests or code
are rewritten. A final remote receipt is added after reading actual completed
job/artifact data and applies only to its stated code commit.
