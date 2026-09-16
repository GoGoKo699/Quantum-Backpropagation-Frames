# PF-04 report: information and implementation boundaries

Status: COMPLETE WITH FINDINGS; scientific scope narrowed by the results.
Baseline: 1986fe53a65062120f1be9da14c28fa48b12484d (merged main).
Branch: research/PF-04-boundary. No merge is authorized or performed.

## Main result

The proposed lower bound survives for arbitrary one-copy POVMs with a fixed,
universally unbiased finite-second-moment vector decoder:

```math
2\,\mathrm{tr}G\le\mathcal V(T)\le4\,\mathrm{tr}G.
```

The proof permits complex physical measurements, ancillas and randomized
settings; realification and compression preserve all probabilities on the real
reference family. It does not require conditional unbiasedness for each setting.
The lower bound is a direct use of an established operator moment inequality.

A sharper internally derived result closes the equal-spectrum case. If all r
nonzero eigenvalues of G are lambda, then

```math
\mathcal V(T)=\lambda\max\{2r,4(r-1)\}.
```

A finite positive-operator measurement with at most 4r+1 outcomes attains this
value. Its character construction, completeness, universal unbiasedness and
exact risk are given in PROOF.md. It is not assembled from separately measured
incompatible coordinates. The output is the original P-vector, even when the
coordinate tangents are redundant and nonorthogonal.

The construction needs a tangent-basis isometry and its classical output map.
Their computation/synthesis is not free. No efficient general compiler for this
POVM is supplied. Exact anisotropic minimax risk remains open in this packet.
The theorem is internally rederived and numerically checked, not externally
reviewed or novelty-cleared. SOURCE_AUDIT.md records the primary-source contracts.

## Same-family consequence

One disjoint layer of the existing six-rotation blocks at zero angles has
P=3n, r=P/2 and lambda=2. The all-POVM optimum is 4P-8 whereas the best
reference-preserving frame/Walsh risk is 4P. The statistical gap is additive
rather than a growing multiplicative speedup. Every raw tangent has unit norm;
this is not the earlier small-coordinate-gradient effect.

The argument extends to a fixed small-angle box: each block's singular values
remain within sqrt(220)h of sqrt(2) when its six angles have magnitudes <=h.
The permitted h<1/sqrt(110) is independent of total register size. A near-flat
spectral sandwich therefore shows that the lack of a growing variance gap is
not confined to one isolated point. This corollary does not assert optimizer
convergence or a probability distribution of trainability.

## Growing-depth implementation check

The predeclared sequence d=ceil(log2(n)/2), n=8,16,32,64,128 stays inside the
existing circuit family. A new causal-predecessor compiler finds each local
reversed tangent, then computes it by real sparse-Pauli state-vector operations
only on its light cone. It matches the independent dense fixture in small cases.
At 128 system qubits and four block layers it compiles 1,524 coordinate queries
into 94,784 scalar entries, with maximum width eight; no 2^128 state is built.

This establishes a feasible explicit local representation. It does not
establish a measurement/decoder cost separation. The retained parity recipe's
worst-width near-optimal-variance choice has k=Theta(w), and its displayed
4^k shifted table work is exponential in w just as the local Gray-character
baseline is. Block shadows already permit O(nw) readout gates and O(P) total
variance in this structure. Actual costs of synthesis, overlap evaluation,
aggregation, preprocessing and output cannot be inferred from gate order alone.

STRUCTURE.md and resources.json give the charged representations and bounds.
No new 144-case priced sweep or favorable objective search was performed.
No unrestricted circuit/decoder lower bound was established. The only such
lower bound here is Omega(L) writes/storage when materializing L tangent entries.
Tensor-network alternatives are not excluded by that representation restriction.

## Executed local evidence

study.py does not import the inherited parity formulas. Only the fixed original
matched-readout circuit fixture is imported for the small dense equivalence test,
with its SHA-256 checked first. Seed: 2026091571.

- Exact integer character first/second/third moments: ranks 1 through 16.
- 192 Born-distribution cases for flat-spectrum POVMs; 24 nonflat upper checks.
- 15 independent redundant projective-mixture decoders satisfy the general lower
  inequalities. This is diagnostic coverage, not a numerical optimization over
  every POVM.
- 24 complete full-quadratic-mask Born calculations check the established upper.
- 288 local tangent comparisons against full-state calculations through six
  qubits and three layers.
- 127 zero-angle blocks and 40 fixed-box blocks check the same-family corollary.
- Five growing-depth compiler runs, up to 128 qubits, construct only local tables.

Largest POVM risk discrepancy was 4.27e-14; maximum local tangent discrepancy was
1.12e-15. Zero-angle block spectra matched exactly in these checks. Full results,
actual environment, source hashes and limitations are in diagnostics.json. No
optimizer, approximate POVM fit, hardware timing, noisy device, or confidence
Monte Carlo was used. Floating-point checks do not prove the minimax theorem.

Local execution used provided archives because container DNS for github.com
failed; it was not a full Git checkout. Remote full-tree integration validation
is separately identified in REMOTE_VALIDATION.json after actual inspection.
Earlier source archives, maintained code, PF-01/PF-02/PF-03 results and acceptance
records are not overwritten. Main and all earlier branches stay unchanged.

## Decision

Retain the exact statistical theorem and its explicit measurement as a candidate
result needing independent proof/novelty review. Retain the compiler as a
reproducibility tool, not a positive strongest-method algorithmic claim.
PF-04 does not establish the requested implementation-cost separation. It rules
out a growing variance improvement within the stated one-copy universally
unbiased contract in the flat/near-flat regime and identifies the charged
basis-construction/decoding cost as the remaining issue.

The justified next decision is a targeted independent audit of the exact
all-POVM flat-spectrum statement and its connection to existing optimal
estimation results, before treating it as the paper's main theorem. A further
parity sweep is not recommended. No manuscript, public release, license, merge,
new ansatz or follow-on study is started by this report.
