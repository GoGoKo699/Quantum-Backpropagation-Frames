# PF-03 integration decision

**Recommendation: integrate the repaired baseline after the read-only integration
gate passes. Do not promote a parity-advantage or novelty claim. No merge is
performed by this work order.**

The merge candidate includes PF-01 and PF-02 history, their original logs, the
maintained real/finite API, and the exact terminal-readout compilers. PF-03 fixes
two scalar-helper boundary behaviors and makes current status/CI match the
actual accumulated evidence. Estimator mathematics and the cost model are not
changed. The source branches remain preserved.

Acceptance requires the full gate, not only a green unit-test job: frozen-tree
identity, 36 test methods, supplied diagnostics and validators, and unchanged
144-scenario/4320-row PF-02 acceptance output. The reviewed run receipt identifies
the executed commit. A later code change requires a new run; a receipt for an
older commit does not claim verification of later code.

The inherited 96 full-direct, 24 full-greedy and 24 no-mask winners remain the
research record. Zero positive-round parity wins is not erased, reinterpreted
as a success, or generalized into a no-go theorem.

Once the gate is verified, open an unmerged pull request to main. The next
operational decision is authorization to merge that reviewed candidate. A new
advantage study requires a separately justified work order; it is not started
by this integration review.
