# PF-01 decision

**COMPLETE WITH FINDINGS. Retain the restricted theorem; do not promote a strongest-method advantage or novelty claim.**

## What survives

For real normalized responses, real tangents with zero reference row, calibrated controlled access, and the specified conditionally unbiased frame/Walsh readout, the supplied algebra is supported by independent rederivation and finite diagnostics. This includes the observable compression, fixed-decoder uniqueness, restricted 4 tr(G) benchmark, exact 4^(-k) covariance interpolation, local decoder, and phase-rank width witness.

## What must change in downstream use

- Reject complex or nonfinite inputs explicitly before float conversion. Current imported code can silently change the problem or return NaNs.
- Do not call the clean-gadget gate count optimal. Terminal work-qubit measurements give an equivalent final measurement with fewer CNOTs, at the cost of measurement/reset and a changed interface.
- Do not infer general measurement, gate, or hardware optimality from the restricted benchmark and bilinear-rank witness.
- Do not infer the usual shadow variance from a near-linear two-design theorem without checking the required third moment.
- Attribute the established primitives and endpoint. The exact combination remains novelty-uncleared.

## Research assessment

The current packet is a mathematically supported and useful specialization with an explicit covariance/compiler law. It is not yet an established distinct publication-level result or a demonstrated end-to-end improvement over the strongest applicable method. The direct dense-CZ comparison is insufficient; optimized Clifford, shallow, and local-block representations must retain their permitted optimizations and actual error contracts.

The absence of an identical result in this bounded literature audit does not prove novelty. Conversely, known building blocks do not by themselves prove that the entire statement is already published. The honest disposition of the exact combination is OPEN.

## One justified next step

A bounded contract-hardening and optimized-readout acceptance test on the same task and family. Correct the invalid-input interface in maintained code without altering the preserved archives, allow both clean and terminal-measurement parity implementations, and make one complete priced comparison with an optimized exact full-mask implementation and an applicable local comparator. Record whether any favorable regime remains after quantum work, samples, classical processing, resets, memory, and output are included.

This is a recommendation, not a new execution authorization. PF-01 stops here. No merge, release, license selection, manuscript, or unrelated research extension was performed.
