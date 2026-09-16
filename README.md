# Quantum Backpropagation Frames

Finite-copy measurement limits and explicit readout circuits for complete
classical quantum gradients, with quantum and classical costs kept separate.

## Current research focus

**Exploratory expansion is frozen for the candidate Letter.** The central result
is the exact real-response, single-copy, universally unbiased gradient-readout
limit when the nonzero tangent sensitivities are equal, together with its sparse
attaining measurement and an explicit local-circuit realization.

```math
\mathcal V(T)=\lambda\max\{2r,4(r-1)\},
\qquad g(q)=2T^{\mathsf T}q.
```

The measurement uses at most 2r+1 outcomes. Circuit implementation is supplied
for the existing local family rather than assumed as free basis access.
An overlapping-interval extension supplies bounded-risk readout with explicit
width-dependent cost. These are internally checked results, not externally
reviewed novelty claims. Statistical optimality is not a runtime advantage.

The original end-to-end improvement milestone remains unmet. The preserved
PF-02 comparison has zero positive-round parity winners. This repository does
not present a failed comparison as a success or a universal impossibility.

## Reading routes

| Purpose | Document |
|---|---|
| Fixed question, main-paper content and stopping rule | [Paper scope](docs/PAPER_SCOPE.md) |
| Compact technical result and assumptions | [Core result](results/PF-08/CORE_RESULT.md) |
| Last cost comparison and decision | [PF-08 report](results/PF-08/REPORT.md) |
| Full exact-limit proof and independent internal audit | [PF-04](results/PF-04/PROOF.md), [PF-05](results/PF-05/REPORT.md) |
| Explicit optimal-readout implementation | [PF-06](results/PF-06/PROOF.md) |
| Overlapping interval implementation | [PF-07](results/PF-07/PROOF.md) |
| Original scope and current status | [Scope](docs/SCOPE.md), [status](docs/STATUS.md) |
| Maintained numerical API and original repair evidence | [API](qbp_frames/README.md), [PF-02](results/PF-02/REPORT.md) |
| Work boundary | [Current work order](work_orders/CURRENT.md) |
| Reproduction and workspace instructions | [Reproducibility](REPRODUCIBILITY.md), [AGENTS.md](AGENTS.md) |

## Checks

```bash
python -m pip install -r requirements.txt
python tools/verify_inputs.py
python -m unittest discover -s tests -v
# Clean full checkout required; outputs must be new.
python tools/integration_check.py --output runs/integration
python results/PF-07/study.py --output runs/pf07-fixed
python results/PF-08/compare.py --input runs/pf07-fixed/diagnostics.json --output runs/pf08-final
```

Current CI is read-only and publishes run-specific artifacts. Prior scientific
packets and their negative results are preserved. PACKAGE_MANIFEST.json remains
the historical initialization snapshot, not a current tree inventory. New
numerical work should use the maintained API where applicable, not assume that
historical fixture code provides a validated public interface.

No new research phase follows automatically from an interesting open question.
Only correction and publication-critical assessment of the frozen contribution
remain in scope. No manuscript, merge, public release or license selection is
implied. See [license status](LICENSE_STATUS.md).
