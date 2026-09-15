# Current work order

**ID:** PF-01  
**Title:** Independent parity-frame proof, novelty, and matched-cost audit  
**Status:** COMPLETE WITH FINDINGS on `audit/PF-01`; see `results/PF-01/REPORT.md` and `results/PF-01/DECISION.md`. No merge to main. Initialization did not execute this audit.

## Goal

Determine which candidate claims survive independent proof checking and whether
the exact covariance/compiler combination produces a distinct result under
matched end-to-end costs. Do not start a paper or invent another ansatz first.

## Starting evidence

Read docs/SCOPE.md and docs/CLAIMS.md; then read
research/parity_frames/PROOF.md, core.py, SOURCES.md, and validation.json.
Read the matched-readout audit, especially its grouping and aggregate-first
baselines. Verify provenance/INPUTS.json and the startup report. The immutable
archive hashes identify the starting scientific sources until a remote commit
is available. Record the actual remote baseline when one exists.

## Execute

1. Independently rederive the reference-family characterization, fixed-readout
   decoder uniqueness, the restricted 4 tr(G) benchmark, covariance interpolation,
   and the rank witness. Identify every use of realness, normalization, phase,
   conditional unbiasedness, and clean ancillas. Include small adversarial tests
   written independently of the existing formula code.
2. Check primary literature using exact versions and theorem locations. Compare
   the parity ensemble and required moments with equatorial masks, diagonal
   designs, near-linear designs, and shallow shadows. Determine whether the
   identity or an equivalent compiler is already implied. Do not use absence of
   search results as a novelty proof.
3. Compare realistic implementations under the same access and output contract.
   Include no mask, direct dense masking, the parity compiler, and the strongest
   applicable known alternative. Allow aggregation and optimized synthesis on
   all sides. Count preprocessing, work ancillas, elementary gates, decoding,
   samples, confidence, and output. Clearly separate a phase-rank lower bound
   from a gate-count or unrestricted-measurement lower bound.
4. Report a claim-by-claim KEEP / NARROW / CORRECT / ALREADY-KNOWN / OPEN
   disposition. State whether evidence supports a distinct research result,
   only a useful specialization, or a failure of a candidate statement.

## Deliverables

Use a new branch and results/PF-01/ for REPORT.md, proof notes, source audit,
reproducible diagnostics, a machine-readable resource table, and DECISION.md.
Record commands and source hashes. Leave imported packets unchanged. No merge,
publication, tag, license change, or manuscript is authorized by this work order.

## Stop condition

Stop after the dispositions, reproducible evidence, matched-cost conclusion,
and one justified next decision are recorded. Do not continue a general
coherent-query or optimizer project. A rigorous negative result is a valid
outcome; do not replace a failing comparison with a weaker baseline.
