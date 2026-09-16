# Research map

This is a reconstruction of the scientific route from the supplied conversation,
not a transcript, not an archival record of every intermediate calculation,
and not fresh verification of earlier claims.

1. **Signed-overlap interface.** arXiv:2604.07639 motivated reading many useful
   signed overlaps from a common quantum response. Replacing test vectors by
   ansatz tangents connects this interface to gradients.
2. **Nonorthogonal tangent queries.** The transformed Jacobian need not be
   orthogonal if its queries can be decoded efficiently. Measurement count,
   decoder cost, signal scale, and whole-vector error must be separated.
3. **Pair rotations, response tomography, and coherence.** Earlier exploration
   studied low total tangent norm, a small-signal regime, spectral truncation,
   and coherent refinement. No corresponding self-contained evidence packet
   is supplied here. These directions remain background, not dependencies of
   the parity theorem.
4. **Local circuit decoder.** Ordinary inverse circuits leave small reversed
   tangents for shallow nearest-neighbor preparations. Local Walsh tables,
   grouped suffix reversed tests, local-Pauli shadows, and rank-two block
   shadows were compared on matched diagnostic instances.
5. **Representation choice.** Different observables have the same expectation
   on the reference family but different covariance and compilation cost.
   The supplied matched-readout audit preserves the implemented comparison.
6. **Parity-frame compiler.** The current proof packet gives a concrete phase
   circuit, exact covariance interpolation, local decoder, and a restricted
   phase-rank witness. This is the main candidate for the next independent
   proof and novelty audit.

## Decisions that should not be lost

- Do not use parameter shift as the only baseline when grouped reverse tests,
  aggregate-first shadows, or classical adjoints are applicable.
- Do not charge a comparator for a Pauli decomposition while giving our method
  free controlled access to the whole objective.
- Do not interpret absolute error on a small gradient as resolved information.
- Do not call known equatorial readout, tomography refinement, or parity
  compute-phase-uncompute primitives new.
- Do not confuse dense diagnostic code with the scalable local decoder.
- Do not infer practical speedup from a count of settings or oracle queries.

The current question is how much work it takes to turn known tangent geometry
into a near-optimal shared measurement with a complete classical output.
Background inspiration is recorded separately in `provenance/ORIGIN.md`; it
is not a premise of the current results.
