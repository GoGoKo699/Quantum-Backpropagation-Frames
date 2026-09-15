# Reproduce PF-02

From the repository root, with NumPy 2.3.5 installed:

```bash
python tools/verify_inputs.py
python -m unittest discover -s tests -v
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python results/PF-02/acceptance.py --output runs/pf02-acceptance
python tools/reproduce.py parity --output runs/pf02-parity
python tools/reproduce.py matched --output runs/pf02-matched
python tools/verify_inputs.py
```

Output directories must not already exist. The acceptance script refuses to
overwrite. It generates summary.json, scenarios.csv and candidates.csv. It uses
exact mask-ensemble expectations for two through five qubits, not Monte Carlo
sampling of mask costs. Seed 2026091566 fixes the 12 circuit parameter points.
The source parity distribution function is called internally only with these
validated small integer inputs; the maintained public interface is elsewhere.

Seeds 2026091562 through 2026091567 cover the new numerical tests. Full compiler
phase contracts enumerate one through five qubits; additional random gate-count
checks extend to 24 qubits without dense states. Complex test vectors test only
the terminal measurement equivalence, not an extension of real-gradient theory.

`record_run.py` is the bounded CI runner. It runs the entire repository test
suite, both inherited validators, this acceptance script, and before/after
input integrity. It records source hashes and actual test counts under a
unique workflow-run directory, then writes REMOTE_VALIDATION.json. It does not
alter imported evidence or execute PF-01's completed scientific audit again.
