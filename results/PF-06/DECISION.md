# PF-06 decision

**ACCEPT compiler feasibility for the disjoint one-layer family. DO NOT ACCEPT a
new strongest-method scaling advantage or a general tangent-basis compiler.**

The sparse optimal measurement from PF-05 can be implemented on the original
physical register by preparing its known reference branch. The prior presumed
need to route into a separate singular-direction register is unnecessary here.
The construction uses linear gate count, linear preprocessing/output mapping,
no extra work qubits, and no classical global state or Jacobian. Every physical
outcome is counted, including those whose decoded contribution is zero.

The zero-angle family realizes the exact flat-spectrum optimum. The same code
remains unbiased at nonzero one-layer angles; row-norm balancing gives an
explicit risk bound, not a new unequal-spectrum optimum. Basis/table computation,
full measurement-bit acquisition, classification, and output are charged.

No-mask readout already attains the same asymptotic total-work order. At the
flat point its worst-case risk is 4P versus the sparse value 4P-8. The additional
compiled gates must be repaid under an explicit cost model; a gate-only
crossover is not an end-to-end advantage. Optimized full masks, grouped suffix
tests, and aggregate-first local shadows remain legitimate alternatives.

The supplied two-layer counterexample shows that the disjoint-block selector
cannot be silently reused for overlapping layers. It is a domain boundary, not
a lower bound excluding a different compiler. Extending the construction to
that setting would be a new bounded task.

Keep the explicit compiler and the negative scaling-separation conclusion as
research evidence. No larger price search or attempt to favor parity was made.
The next substantive question is whether the known-reference route can be
constructed and decoded efficiently for overlapping tangent supports without
materializing their union or assuming an eigenbasis. Do not repeat the same
proof audit or claim that this further construction is already available.

Main, all previous branches, and all historical evidence remain unchanged.
No merge, release, license, manuscript or follow-on study is performed here.
