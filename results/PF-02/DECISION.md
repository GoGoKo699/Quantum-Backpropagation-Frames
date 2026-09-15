# PF-02 decision

**COMPLETE WITH FINDINGS. Accept the maintained input repair and exact terminal
compiler implementations. Do not accept a parity advantage claim from this test.**

The numerical formulas on valid real inputs are unchanged. All four invalid-input
cases from PF-01 are rejected by the maintained API before coercion. The imported
research files and both source archives remain unchanged.

The two optimized full-mask compilers preserve the final measurement after their
explicit affine bitstring relabeling; they are not clean-unitary substitutions.
Their cost includes sampled-mask synthesis and relabeling. Native clean parity,
measured-uncomputation parity, and recompilation of equivalent parity masks were
all eligible, as were no mask and grouped suffix reversed tests.

In the final 144 declared cost scenarios, the winners are full direct masking
(96), full masking with greedy terminal synthesis (24), and no mask (24). No
positive-round parity prescription wins. This is a comparison of specified
sufficient budgets and priced expected work in small instances, not a lower
bound on parity performance at larger sizes or an all-method impossibility.

The three price profiles are not hardware calibrations. Classical costs are
explicit kernel/word-operation prescriptions, not CPU instruction counts.
Confidence is treated identically by a conservative whole-vector Markov bound.
Full matched global-Clifford, shallow-shadow, and routed synthesis optimization
have not been solved. The result does not settle novelty or the project's
ultimate end-to-end-advantage goal.

One next decision: review this repair branch for integration of the maintained
interface and the negative acceptance record. Retain the parity compiler as a
baseline, not as a selected flagship implementation. Any further advantage study
needs a separately justified structural regime and a matched decoder/cost model;
PF-02 does not authorize another sweep or research extension. No merge occurred.
