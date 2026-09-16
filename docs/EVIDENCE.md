# Evidence index

[Home](../README.md) · [Tutorial](TUTORIAL.md) · [Proof](THEORY.md) · [Reproduction](REPRODUCIBILITY.md)

The canonical proof route is self-contained. Original packets below are retained
for checking source identity, independent derivations, and numerical records;
their development labels are not prerequisites for reading the result.

## Exact statistical limit

**Claim.** Equal nonzero eigenvalues give exact single-copy minimax trace risk
under the real pure universally unbiased contract; at most 2r+1 effects attain
it. This is not a minimum-outcome theorem or optimal confidence law.

- Canonical: [Theorem and full proof](THEORY.md).
- Original derivations: [first proof](../results/PF-04/PROOF.md) and
  [independent proof audit and sparse attainer](../results/PF-05/PROOF_AUDIT.md).
- Numerical checks: [original diagnostic program](../results/PF-05/audit.py)
  and [recorded diagnostics](../results/PF-05/diagnostics.json).
- Maintained realization: [disjoint compiler](../qbp_frames/disjoint.py),
  [worked executable](../examples/flat_readout.py), and
  [migration/equivalence tests](../tests/test_supported.py).
- Boundaries: [model comparisons](COMPARISONS.md#which-optimality-is-proved).

## Explicit disjoint realization

**Claim.** The existing zero-angle one-layer family admits a linear-size logical
realization with full-coordinate risk 4P-8 versus the no-mask value 4P. This is
an additive variance gap, not an asymptotic end-to-end advantage.

- Canonical: [constructive proof and costs](COMPILERS.md).
- Originals: [local realization proof](../results/PF-06/PROOF.md),
  [physical-bit scanner correction](../results/PF-06/SCANNER_NOTE.md),
  [resource contract](../results/PF-06/RESOURCES.md).
- Code: [maintained disjoint module](../qbp_frames/disjoint.py),
  [original compiler](../results/PF-06/compiler.py),
  [original diagnostic grid](../results/PF-06/study.py).
- Reuse: [128-qubit compiler-only demonstration](../examples/compile_large.py)
  and [supported equivalence tests](../tests/test_supported.py).

## Overlapping-interval construction

**Claim.** Row-norm reference readout has variance at most four times the tangent
Gram trace, with an explicit width-dependent logical circuit. Its coordinate
support need not equal tangent span; generic exact minimax is not claimed.

- Canonical: [interval proof, preparation, and decoder](COMPILERS.md).
- Originals: [proof](../results/PF-07/PROOF.md),
  [resources](../results/PF-07/RESOURCES.md),
  [source-table construction](../results/PF-04/STRUCTURE.md).
- Maintained code: [intervals](../qbp_frames/intervals.py),
  [local tangent tables](../qbp_frames/local.py); original
  [compiler](../results/PF-07/compiler.py) and [study](../results/PF-07/study.py).
- Durable data: [original 30-point diagnostics and compiler cases](../data/recorded/PF-07/diagnostics.json),
  [recorded example program](../data/recorded/PF-07/example_program.json),
  [source receipt](../results/PF-07/REMOTE_VALIDATION.json).
- Tests: [maintained equivalence checks](../tests/test_supported.py) plus the
  unchanged 26-group interval diagnostic suite in full validation.

## Parity baseline and negative evidence

**Claim.** The restricted frame/Walsh algebra and covariance interpolation are
retained. Positive-round parity wins no scenario in the fixed matched-cost grid.
Neither statement is a universal circuit lower bound or a total-work advantage.

- Sources: [restricted proof](../research/parity_frames/PROOF.md),
  [audit dispositions](../results/PF-01/CLAIM_DISPOSITIONS.json),
  [negative acceptance report](../results/PF-02/REPORT.md).
- Code: [maintained parity interface](../qbp_frames/parity.py),
  [terminal compilers](../qbp_frames/readout.py),
  [fixed acceptance program](../results/PF-02/acceptance.py).
- Data: [144 scenarios](../results/PF-02/remote_validation/34956367799-1/acceptance/scenarios.csv),
  [4320 candidates](../results/PF-02/remote_validation/34956367799-1/acceptance/candidates.csv),
  [summary](../results/PF-02/remote_validation/34956367799-1/acceptance/summary.json).
- Regressions: [input and readout tests](../tests/test_pf02.py),
  [exact round-threshold tests](../tests/test_pf03.py), and the
  [unchanged integration runner](../tools/integration_check.py).

## Fixed cost analysis and unmet advantage goal

**Claim.** Existing small-point variance improvements and quantum-only operation
projections do not establish a strongest-method total-work separation.

- Interpretation: [comparisons and limitations](COMPARISONS.md).
- Original [fixed-data report](../results/PF-08/REPORT.md),
  [analysis code](../results/PF-08/compare.py), and
  [scope decision](../results/PF-08/DECISION.md).
- Durable [small comparison](../data/recorded/PF-08/small_comparison.csv),
  [scaling comparison](../data/recorded/PF-08/scaling_tradeoff.csv),
  [quantum projection](../data/recorded/PF-08/quantum_projection.json),
  [summary](../data/recorded/PF-08/summary.json), and
  [exact historical input](../data/recorded/PF-08/input_pf07_diagnostics.json).
- Provenance: [source receipt](../results/PF-08/REMOTE_VALIDATION.json) and
  [recovery map](../data/recorded/README.md). Eight unchanged analysis checks run
  on newly generated interval data in the current full gate.

## Identity, reproduction, and attribution

[INPUTS.json](../provenance/INPUTS.json) identifies both original ZIPs and their
22 extracted files. Their source hashes and all completed packets remain
unchanged. [MIGRATION.json](../maintenance/repository-polish/MIGRATION.json)
records exact SHA-256 values for preserved evidence, archived active guidance,
maintained code copies, and recovered artifact members. It supplements the
historical manifests; it does not replace them with current values.

The [current validation runner](../tools/validate.py) checks the migration map,
original manifests, inherited regressions, supported examples, and deterministic
figure regeneration. The [reproduction guide](REPRODUCIBILITY.md) lists commands,
expected coverage, and failure behavior. The [engineering record](../maintenance/repository-polish/REPORT.md)
distinguishes local tests, GitHub CI, and actual rendering inspection.

[Methods and provenance](PROVENANCE.md) describes substantive AI assistance and
source handling. [Primary sources](../literature/README.md) retain attribution
and exact audit locators. Final novelty clearance and external peer review are
not inferred from internal tests or repeated source comparisons.
