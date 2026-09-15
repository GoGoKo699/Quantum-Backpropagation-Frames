# PF-01 final audit report

**Status: COMPLETE WITH FINDINGS.**

Baseline: `da0d8c771350b695206b6f06194277538833adb4`.
Audit branch: `audit/PF-01`.
Start checkpoint: `2a5d77cac017a4e2e330ed1d5b7c12ba8e492476`.
Scope: work_orders/CURRENT.md. No merge, license, publication, manuscript, or new ansatz.

## Executive decision

The parity packet's algebra survives independent rederivation on its declared real-response, phase-calibrated, conditionally unbiased frame/Walsh domain. The covariance interpolation is exact, and the phase-rank witness supports its stated width dependence. Neither is a universal measurement or gate-optimality theorem.

The software needs input-contract correction: unsupported complex inputs can be coerced to real and nonfinite values can be accepted. The original files remain untouched. These defects do not invalidate the mathematical theorem on valid inputs.

The known primitives and full-mask endpoint must remain attributed. The exact finite-round covariance/compiler combination has not been cleared as novel. A bounded source audit did not locate an identical theorem but also did not establish an end-to-end advantage over optimized, matched alternatives. The current result should be retained as an audited restricted theorem and baseline, not promoted to a publication-ready quantum-advantage claim.

## Claim dispositions

| Claim | Disposition | Reason / retained scope |
|---|---|---|
| PF-01: reference-family observable characterization | KEEP | Compression fixed by odd/even dependence on real unit q; outside-subspace entries remain free. |
| PF-02: fixed-measurement decoder uniqueness | KEEP, NARROW usage | Conditional universal unbiasedness for a chosen frame. Does not exclude other measurements, ensemble-level dual choices, or extra promises. |
| PF-03: 4 tr(G) benchmark | KEEP, NARROW usage | Exactly the reference-preserving real frame/Walsh class. An explicit rank-two measurement has worst variance 2 where this class gives 4. |
| PF-04: parity gadget | KEEP; ALREADY-KNOWN ingredients | Exact compute-phase-uncompute action and displayed clean-ancilla count. Not an optimal synthesis. Terminal measurement offers another contract and lower CNOT count. |
| PF-05: covariance interpolation | KEEP; novelty OPEN | Independent fourth-character and Born-probability derivations agree. No full-design or pointwise monotonicity claim follows. |
| PF-06: local decoder | KEEP, NARROW usage | Valid explicit upper implementation with exponential width factors. All comparators may aggregate and optimize. |
| PF-07: rank witness | KEEP, NARROW usage | Real quadratic bilinear-rank restriction; leading width dependence at fixed slack. Not an unrestricted CNOT, depth, or POVM lower bound. |
| MR-01: inherited matched audit | KEEP as finite evidence | Validator reproduced. Full matched tables were not regenerated; diagnostic objectives are not advantage instances. |
| Input guards in parity core | CORRECT in a separately reviewed patch | Complex-to-real coercion and NaN acceptance; no immutable source edited here. |
| Primitive/endpoint novelty | ALREADY-KNOWN | Interference, equatorial masks, designs, rank Fourier methods, and terminal outcome relabeling have primary precedents. |
| Novelty of exact combined result | OPEN | Bounded comparison is not a novelty certificate. |
| Strongest-method end-to-end improvement | OPEN | Correct direct-mask crossover does not settle optimized Clifford/shallow/block alternatives and decoder costs. |
| Earlier spectral/coherent minimax assertions | NOT AUDITED | No corresponding evidence packet is adopted by this work order. |

Detailed derivations are in PROOF_AUDIT.md; primary-source versions and locators in SOURCE_AUDIT.md; costs in RESOURCES.md and resource_table.json.

## Cost findings that change the comparison

1. If the gadget is the final measurement stage, measuring its work qubits in X and relabeling the system outcome halves the displayed expected CNOT count from 2nk to nk. It adds 2k measurements and resets when reusing two qubits. It is not a coherent clean-ancilla substitution. The folded measurement distribution was checked independently.
2. A fixed finite-k compiler has a slightly larger uniform variance bound than a full mask. Increasing common response cost eventually favors fewer full-mask preparations against that fixed k, even though parity uses fewer readout gates. Increasing k or optimizing the full-mask compiler changes the crossover. No blanket runtime ranking is justified.
3. Global Clifford shadows on the same rank-two derivative targets have covariance 12cG-gg^T/(2N+2), c=(2N+1)/(2N+2), and therefore the same O(s/epsilon^2) whole-vector sample scale. Eligible local block methods do too. They must not be represented as one-coordinate-at-a-time baselines.
4. A near-linear exact unitary two-design is not automatically a drop-in variance competitor: the standard shadow score's second moment uses third projective moments. The full Clifford group supplies them; a two-design theorem alone does not. Shallow methods require their actual target-dependent inverse and variance analysis.
5. Gate count, reset/readout latency, classical work, workspace, confidence, and output have been retained separately. Numerical crossovers are explicitly gate-only illustrations, not hardware runtimes or optimal-method certificates.

## Reproducibility and actual execution

The local working directory is an extracted copy of the supplied starter, not an authenticated Git checkout. The remote API supplied the authoritative baseline and branch state. The two scientific archive Git blob IDs and SHA-256 hashes match the pinned remote; local extracted scientific files match their archive entries.

Independent code `audit.py` does not import either scientific packet. It checks actual Born probabilities and explicit finite ensembles, not only the proposed interpolation function. Seed: 2026091561. Environment: Python 3.13.5, NumPy 2.3.5, one BLAS/OpenMP thread.

| Independent check | Cases | Largest residual |
|---|---:|---:|
| Born normalization / conditional mean | 3294 each | 7.8e-16 / 3.6e-15 |
| Full-mask covariance | 12 | 1.2e-13 |
| Covariance interpolation | 48 | 1.5e-12 |
| Exact determinant character | 258 | Exact integer agreement |
| Observable compression | 32 | 1.4e-15 |
| Eigenframe balancing / trace | 4 / 32 | 3.6e-14 / 1.5e-13 |
| Fixed decoder rank | 4 | Full rank in every case |
| Quadratic Walsh moments / variance | 672 / 168 | Exact moments / 4.0e-14 |
| Bilinear-rank inequality | 112 | No violations |
| Clean parity basis action | 360 | Exact agreement |
| Measured-uncomputation probabilities | 48 | Exact floating-point agreement |
| Shifted decoder identity | 120 | 2.7e-15 |

An independent rank-two measurement counterexample, a complex-response counterexample to an invalid extension, and an unknown controlled-branch phase example are included. They verify the boundaries, not failures on the theorem's stated domain.

The original starter's nine wrapper tests passed locally. These are not represented as the remote repository's twelve-test suite. The parity validator passed all eight supplied check groups in an isolated copy; the matched validator passed its six supplied residual groups. Both archives and all 22 extracted files remained unchanged. The local evidence bundle retains exact logs under reproduction/. Fresh branch-run logs, outputs, and source hashes are recorded under remote_validation/; REMOTE_VALIDATION.json identifies the actual GitHub run when it completes.

The four input-guard probes were run twice; software_probe.py preserves the executable probe. No large circuit, hardware, routing, fault-tolerance, or complete optimized-synthesis benchmark was executed. No new Monte Carlo confidence experiment was needed for this audit.

## Stop condition and next decision

PF-01 is complete: proof notes, source audit, independent diagnostics, reproducibility records, matched resource formulas, dispositions, and a decision are recorded. No source packet was rewritten and no main-branch merge is authorized.

The one recommended follow-up is a bounded **contract-hardening and optimized-readout acceptance test**: put corrected input guards in a maintained wrapper or new implementation, then compare clean and measurement-terminal parity against an optimized exact full-mask implementation and the applicable local comparator under one fully priced cost model. Accept a main-paper advantage claim only if it survives those comparisons. This follow-up is not executed or dispatched by PF-01. No new ansatz or manuscript should substitute for that missing result.
