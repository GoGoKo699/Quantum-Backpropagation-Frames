# PF-08: final comparison and publication-scope freeze

Baseline: `a70b840c321ecfbea2f26fd40a459aef7153b068` (PF-07).
Branch: `review/PF-08-paper-scope`. Date: 2026-09-16.

## Decision

STOP exploratory expansion for the present Letter. The candidate central result
is the exact finite, single-copy, universally unbiased readout limit for a real
reference-response family, together with its sparse attaining measurement and
one explicitly charged local-circuit realization. The overlapping-interval
compiler is an extension/supporting result, not another compulsory research
program. Parity is an audited benchmark, not the presumptive flagship algorithm.

This is a scope decision, NOT a submission-readiness or novelty certificate.
The original project goal of an end-to-end improvement over a strong matched
method remains unmet. A theorem-centered paper may have independent value, but
that possibility does not retrospectively satisfy or delete the advantage goal.

## The comparison actually performed

Reanalyze the same 30 small parameter points and ten compiler-only cases already
fixed and executed in PF-07. No new angles, objectives, widths, prices or winning-
method sweeps were introduced. `compare.py` checks the source identities, grids,
normalization and finite risk data before using them. Its tests verify cost
algebra and input rejection. It does not pretend to be a new proof of PF-04/05.

On these 30 small points, the row-reference worst-response variance is below
no-mask variance in all 30 cases. It is below the full-mask value in 22 cases
and numerically equal in eight cases. The largest variance ratio relative to
either comparator is 1.5. These are finite floating-point results, with equality
classified at 1e-10 relative/absolute tolerance; they are not universal bounds
on an advantage outside the tested grid.

The ten compiler-only cases have no new global-state risk calculation. Both
reference and full masking receive the same proved sufficient coefficient
B=4P and K=ceil(4P/(delta epsilon^2)). At epsilon=delta=0.1 this is 4000P shots,
exactly the same integer count on both sides. The reference preparer may save
classical streaming but may add quantum gates. Its earlier circuit and cost
qualifications are unchanged.

## Complete cost identity, without hiding missing terms

For method j let F_j include parameter-point preprocessing and final output;
let r_j include additional quantum readout, classical streaming and any recurring
synthesis; and let C be the COMMON response preparation per experiment. Then

```math
W_S-W_F=(K_S-K_F)C+F_S-F_F+K_S r_S-K_F r_F.
```

With equal shot prescriptions, the common response cost cancels EXACTLY:

```math
W_S-W_F=F_S-F_F+K(r_S-r_F).
```

An arbitrarily expensive objective therefore cannot, by itself, make one of
these equal-budget methods preferable. Different justified budgets or different
implementation costs are needed. This is elementary cost accounting, not a new
information theorem. If K_S<K_F, an expensive common preparation can change the
ordering; the script preserves this separate affine case rather than treating
all points as identical.

## A transparent projection of the costs

The generated tables include a deliberately incomplete quantum-operation
projection using the EXISTING PF-02 gate_weighted prices: CNOT=CZ=1, one-qubit
operation=0.1, terminal measurement=1. It is NOT a total-work acceptance test.
Classical processing, compilation, memory and final-map differences stay explicit.
The common preparation remains the variable C. A direct full quadratic mask is
one valid comparator, not the strongest possible synthesis.

At n=256, depth 2, PF-07 uses 6615 CNOTs and 6104 Ry operations; direct full
masking uses 16320 expected CZs. The reference has 9120 fewer projected quantum
cost units per record. At n=256, depth 4, PF-07 uses 96759 CNOTs and 96248 Ry
operations, giving 90038.4 MORE projected units than direct full masking. Equal
terminal measurements are included and cancel. These quantities are neither
seconds nor complete wins. Optimized full-mask synthesis can improve the full-
mask comparator further. Local block shadows, grouped reversed tests, no mask,
and sparse-state preparation optimizations remain eligible.

For equal K the necessary complete comparison is whether the classical/other
per-record saving exceeds the quantum premium plus (F_S-F_F)/K. We do not fill
unknown costs with zero to announce a winner. Nor do we equate two upper-bound
complexity prescriptions with a lower bound on a competing optimal method.
At fixed width both families already have comparable asymptotic work order;
growing width leaves an exponential reference-preparation cost. Thus this final
comparison establishes no strongest-method total-work separation.

## Candidate Letter, not a collection of project episodes

The main chain is: define the measurable gradient task; prove its finite-copy
limit; give one joint measurement attaining the limit; show a charged physical
realization on the existing circuit family; distinguish statistical optimality
from computational speedup. See `docs/PAPER_SCOPE.md` for the frozen outline and
`CORE_RESULT.md` for the compact technical statement. The body is not drafted here.

Allowed completion work is limited to fixing a flaw in this exact claim,
resolving exact source equivalence and significance, producing presentation
figures from existing data, and reconciling the frozen scope with the original
unmet advantage milestone. No extra family or technology is added to rescue a
weak significance argument. Human author judgment is required before treating
this as a submission-ready contribution; internal repeated audits are not
external peer review.

## Reproducibility

The local analysis uses the mounted, SHA-256-verified PF-07 workflow artifact.
A source subset was available locally; direct git access failed DNS resolution.
No full local checkout or complete local repository test run is claimed. The
unchanged PF-07 study can be rerun separately on its original grid. Read-only CI
runs the existing complete integration gate and PF-04 through PF-07, then this
analysis on its newly generated PF-07 data. Its receipt identifies the actual
executed commit. Previous code/results and main are unchanged. No merge, release,
license change, manuscript or automatic PF-09 dispatch occurs.
