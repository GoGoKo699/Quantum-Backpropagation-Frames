# Quantum Backpropagation Frames

Research on **frame-based complete-gradient readout**: how known
ansatz tangents can be converted into a shared measurement, and what that
conversion costs in quantum operations, samples, classical work, and memory.

**Status: working research, not a released theorem package or an established
quantum-advantage result.** The current candidate is a parity-phase compiler with
an exact covariance-interpolation derivation, small-system validation, and a
restricted phase-rank lower bound. Novelty and superiority over the strongest
matched alternatives remain open.

The problem, assumptions, derivations, implementations, and claim boundaries
are defined within this repository. The project is organized around the cost of
turning known tangent queries into a shared measurement.

## The scientific question

At one fixed parameter point, write the complete raw coordinate gradient as

```math
g = 2 T^{\mathsf T}q,
\qquad
T = U^{\mathsf T}J,
\qquad
q = U^{\mathsf T}OU|0\rangle.
```

The ansatz and its tangent queries are known. The objective-dependent response
is obtained quantum mechanically. The task is to materialize all gradient
entries, with explicit error and confidence, without hiding cost in a frame,
classical decoder, stronger access, or a change of parameter normalization.

The current mathematical packet restricts this equation to real normalized
responses, real tangents with `T[0] = 0`, and exact phase-calibrated controlled
reflection access. Broader project assumptions remain open to explicit study.
See [Scope](docs/SCOPE.md) before changing the model.

## Current constructive candidate

Compute two random binary parities into two clean work qubits, apply one CZ
between them, and uncompute. Repeat this operation `k` times before the all-X
readout of the reference-response state. The corresponding classical decoder
uses the known tangent tables and the recorded masks.

The supplied proof derives

```math
\Sigma_k(q)
=
(1-4^{-k})\Sigma_{\mathrm{full}}(q)
+4^{-k}\Sigma_0(q).
```

Here `Sigma_0` is the ordinary all-X covariance and `Sigma_full` is the
independent full quadratic-mask covariance. The statement concerns a precisely
defined measurement and unbiased decoder, not arbitrary quantum measurements.

**Start with [the self-contained proof](research/parity_frames/PROOF.md).**
Its assumptions and qualifications are part of every claim made from it.

## Read and work from here

| Need | File |
|---|---|
| Current evidence and unresolved conclusions | [Status](docs/STATUS.md) |
| Claim-by-claim assumptions and evidence | [Claim register](docs/CLAIMS.md) |
| Exact parity construction, derivation, and diagnostic code | [Parity packet](research/parity_frames/README.md) |
| Matched readout baselines and cost accounting | [Readout audit](research/matched_readout/README.md) |
| Reproduce checks without changing imported evidence | [Reproducibility](REPRODUCIBILITY.md) |
| Next bounded research task | [Current work order](work_orders/CURRENT.md) |
| Earlier directions and their evidence boundary | [Research map](docs/RESEARCH_MAP.md) |
| Source relationships and attribution | [Literature map](literature/README.md) |
| Workspace rules | [AGENTS.md](AGENTS.md) |

## Run the startup checks

Python 3.13 and NumPy 2.3.5 are the recorded import environment. Use an isolated
Python environment; the original packet requirements remain preserved.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/verify_inputs.py
python -m unittest discover -s tests -v
python tools/reproduce.py parity --output runs/parity-audit-01
```

The runner copies a packet into an isolated temporary directory. Imported
validation JSON files are not overwritten. Each rerun records its own outputs,
logs, interpreter, dependency versions, source hashes, and return codes.
A configured CI workflow is included; no remote CI run is implied.

## Evidence boundary

The two original ZIP files and all their extracted files are preserved under
`provenance/input_archives/` and `research/`. Their manifests are checked. The original
startup results remain under `validation/bootstrap/`; initialization checks
are recorded separately under `validation/initialization/`.

A small floating-point residual is not a proof, a novelty certificate, a
hardware result, or an asymptotic benchmark. Earlier spectral/coherence claims
made during brainstorming are **not adopted as established results** by this
import. Only two evidence packets were supplied. Historical wording in those immutable
packets does not define the current project scope; see
[Origin and terminology](provenance/ORIGIN.md).

There is no selected reuse license, release tag, manuscript, or public-release
authorization. See [License status](LICENSE_STATUS.md) and
[remote setup](SETUP_GITHUB.md).
