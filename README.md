# Quantum Backpropagation Frames

Research on converting known ansatz tangent queries into shared quantum
measurements for a complete classical gradient, with explicit quantum,
statistical, classical-processing, memory, and output costs.

## Current conclusion

The parity-frame algebra is retained **within its audited real-response,
phase-calibrated, conditionally unbiased frame/Walsh setting**. Its restricted
variance benchmark is not universal measurement optimality, and its phase-rank
witness is not a general gate-count lower bound.

PF-02 provides a maintained input interface and exact terminal-readout
compilers. In its 144 declared small-system cost scenarios, positive-round
parity won **zero** scenarios. Full direct masking won 96, greedy full masking
24, and no mask 24. These are outcomes of specified sufficient budgets and a
normalized work model, not measured hardware runtimes or an impossibility
result. Keep parity as a baseline, not an established flagship advantage.

PF-03 reviews these changes for integration. It adds exact round-threshold
selection, consistent scalar errors, and read-only regression CI. The audit and
repair branches remain preserved; integration does not re-audit novelty or
establish the project's end-to-end advantage goal.

## The task

At a fixed parameter point, the current real-response packet studies

```math
g=2T^{\mathsf T}q,\qquad T=U^{\mathsf T}J,\qquad
q=U^{\mathsf T}OU|0\rangle.
```

The output is all raw coordinate-gradient entries, with explicit whole-vector
error and confidence. Access, parameter normalization, unbiasedness, and
coordinatewise versus whole-vector accuracy must not be silently interchanged.
See [Scope](docs/SCOPE.md) for the project contract.

## Reader and workspace routes

| Purpose | Start here |
|---|---|
| Current evidence and limitations | [Status](docs/STATUS.md) |
| Claim dispositions | [Claim register](docs/CLAIMS.md) |
| Supported numerical API and compiler contract | [Maintained interface](qbp_frames/README.md) |
| Independent restricted-proof/source audit | [PF-01 report](results/PF-01/REPORT.md) |
| Input repair and negative cost result | [PF-02 report](results/PF-02/REPORT.md) |
| Integration review and corrections | [PF-03 report](results/PF-03/REPORT.md) |
| Reproduce tests and the same acceptance grid | [Reproducibility](REPRODUCIBILITY.md) |
| Work boundary and next decision | [Current work order](work_orders/CURRENT.md) |
| Candidate proof, unchanged as supplied | [Parity proof](research/parity_frames/PROOF.md) |
| Baselines and imported comparison evidence | [Matched-readout packet](research/matched_readout/README.md) |
| Sources and earlier directions | [Literature](literature/README.md), [research map](docs/RESEARCH_MAP.md) |
| Workspace rules | [AGENTS.md](AGENTS.md) |

## Run

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/verify_inputs.py
python -m unittest discover -s tests -v
# Clean full Git checkout required; output directory must be new.
python tools/integration_check.py --output runs/integration-01
```

Use the maintained interface:

```python
from qbp_frames import parity
```

Do not directly import the historical parity core for new input handling. Its
original invalid-input behavior is intentionally preserved for reproducibility.
The maintained interface rejects unsupported complex and nonfinite inputs. Its
realness and numerical tolerance contracts are documented in the API guide.

## Evidence and permissions

`research/`, `provenance/`, PF-01/PF-02 results, and initialization records are
preserved. `PACKAGE_MANIFEST.json` is the historical initialization snapshot,
not a current-file manifest. CI verifies the frozen history against the pinned
PF-02 commit and writes fresh logs only under `runs/`, uploaded as artifacts.
CI has read-only repository permissions and never pushes generated results.

Numerical residuals are not proofs, source-novelty certificates, or hardware
benchmarks. Earlier exploratory spectral/coherence claims are not adopted by
this integration. The project is self-contained; historical inspiration is not
a result dependency.

## License

Original code and associated documentation are available under the
[MIT License](LICENSE). Copyright (c) 2026 Ruge Lin.
See [licensing details](LICENSE_STATUS.md) for the treatment of preserved
snapshots and third-party material.

A passing check does not imply journal publication or a versioned release.
Repository setup is described in [setup](SETUP_GITHUB.md).
