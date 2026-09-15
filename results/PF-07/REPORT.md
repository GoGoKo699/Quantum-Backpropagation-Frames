# PF-07: reference preparation extends to overlapping tangent intervals

Baseline: 0633ff37de69debbad93b78b146bb128be12106e.
Branch: research/PF-07-overlap-reference. Main and prior branches remain unchanged.
The final execution receipt identifies the code actually checked remotely.

## Main result

The disjoint one-layer selector is no longer necessary. Given the charged local
reversed-tangent tables of the existing alternating nearest-neighbor circuit,
we compile the row-norm reference for OVERLAPPING intervals using only
CNOT/Ry/X/H gates. The construction avoids a tangent eigenbasis, a global
support-address union and a coherently stored tangent label.

Every nonzero physical string has one first 1. Prepare a one-marker superposition
weighted by those first-site masses. Then, from RIGHT TO LEFT, fill the bounded
suffix after each marker with its required positive amplitudes. Previously
filled suffixes lie to the right of all remaining controls, so newly created
ones cannot falsely trigger later blocks. The response branch is protected by
an explicit reference-zero control and is the identity on every input.

Each reference probability is the SUM of squared contributions of all tangent
columns compatible with its address. This handles overlaps, rather than choosing
one contributing tangent or coherently adding its amplitude. Only a small
suffix array is present at a time; existing local tangent tables and any retained
circuit program remain charged. Readout is a Hadamard on the reference followed
by computational-basis measurements on all n+1 physical qubits.

The same row-norm score from PF-06 remains universally unbiased. Its exact total
variance is 2s(1+||Pi_S q||^2)-4||T^Tq||^2 <=4s, where s=tr(G) and Pi_S selects
nonzero COORDINATE rows, not tangent singular directions. At most nu original
parameter entries are updated per outcome, where nu is the number of intervals
that can cover its first 1. Full outcome scanning is O(n), not free. There is
no postselection, response tomography or change of parameter normalization.

## What this closes and what it does not

The PF-06 four-qubit/two-layer counterexample was reconstructed exactly. Its
old discarded gradient norm is 2.7639718921748453. The new elementary circuit
recovers that full gradient with local-test error 1.17e-15. Thus overlapping
light cones are not themselves an obstruction to known-reference readout.

This is not an unequal-spectrum optimum. If the coordinate row support contains
a null direction of T^T, the new readout's worst trace risk is exactly 4s. The
packet exhibits a synthetic overlap case saturating that bound. It also exhibits
a WRONG left-to-right preparation schedule with state error 0.247321261434242.
These examples distinguish the new valid compiler from tempting invalid
extensions of the earlier construction.

## Implementation and cost

The circuit uses no extra work qubits beyond the reference already supplied.
For F=sum_{positive first sectors a}4(2^{ell_a}-1), it emits 6n-5+F CNOTs,
4(n-1)+F full-angle Ry gates, two X gates and one H. The worst bound is O(n2^w).
The UCR synthesis uses a fast Walsh transform rather than a dense O(4^w)
angle matrix. Classical reference compilation costs O(L+W+nw2^w), given L local
table entries and W interval incidences. Per shot, physical bit scanning and
row evaluation cost O(n+nu w), and final output costs O(P).

For the complete fixed width-w nonvacuum envelope, M_w=(n-w+2)2^{w-1}-1,
the CNOT/Ry bounds are 4M_w+2n-5 and 4M_w-4. A standard dimension count gives a
matching O(M_w) worst-case order for EXACT preparation of all positive states
on that fixed envelope. This is not a CNOT-only, T-count, all-measurement, or
physical-gradient-family lower bound. It does not establish novelty.

At fixed depth the new compiler has linear resource scaling. Existing structured
readouts already have comparable asymptotic total work. For growing depth the
new reference circuit still pays the width exponent. No strongest-method
advantage, routed-device advantage, price winner or generic compact-tensor
representation is asserted. The matched ledger allows optimized masks, grouped
suffix tests, aggregate-first shadows and current sparse-preparation methods.

## Local execution

The provided PF-04 and PF-06 archives were extracted and their packet manifests
verified. Direct container access to github.com failed DNS; local work used a
hash-pinned source subset, not an authenticated full checkout. No historical
file was edited. The prior causal compiler supplies local tangents and the
prior small statevector engine executes elementary gates. The new preparation,
first-site aggregation and decoding were written here. No earlier POVM formula
function is called by the new checks. Independent full-state tangents and finite
differences use the separately hash-pinned original fixture.

The fixed small grid has n=3,4,5,6,8, depths 1,2,3, and zero/seeded angles:
30 circuit parameter points. It produced 191 Born/gradient/risk cases, 60 finite-
difference coordinates, 21 complete-envelope preparation checks, and independent
control/ordering/zero-row/overlap tests. All 26 groups passed in the final local
run. The source-roundoff correction is limited to the analytically zero reference
component and was at most 3.82e-16; other small amplitudes are not discarded.

The largest local mean discrepancy was 5.11e-15, trace-risk discrepancy 8.53e-13,
and finite-difference discrepancy 2.91e-10. These are floating-point diagnostics,
not interval certificates, external peer review or numerical optimization over
all measurements. The main seed is 2026091607; the main physical-grid stream is
restarted at seed+1 so auxiliary tests do not change its parameter choices.

Compiler-only checks use n=16,32,64,128,256 at fixed depth 2 and at
ceil(log2(n)/2). The largest growing-depth case has n=256, depth 4, P=3060,
w=8, 192832 local tangent entries, 96759 CNOTs and 96248 Ry gates. Its temporary
suffix-mass array has at most 128 entries; other angle/work buffers are O(2^w).
Its maximum interval incidence is 53. No global state or retained full gate
list was allocated in these scaling runs. Retaining/replaying the program in
a real implementation still requires its explicitly charged storage.

## Evidence status

The final code is rerun locally after packaging, and read-only GitHub CI checks
the entire inherited integration gate, unchanged PF-04/PF-05/PF-06 packets and
new packet hashes/diagnostics. REMOTE_VALIDATION.json identifies actual completed
runs, not assumed success. Prior negative PF-02 outcomes are preserved unchanged.
No merge, release, licensing change, manuscript or follow-on study is performed.
See DECISION.md and the source comparison for the scientific boundary.
