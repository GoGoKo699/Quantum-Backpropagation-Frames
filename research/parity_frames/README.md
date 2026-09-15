# Parity-phase frame compiler: theorem and validation packet

Date: 2026-09-15.

## What is in this packet

A constructive replacement for dense independent-CZ gradient readout: k rounds
of computing two independent random linear parities, applying one CZ between
two work ancillas, and uncomputing. The real system phase is
`(-1)^sum_l[(a_l dot x)(b_l dot x)]`.

The central derived identity is exact:

`Cov_k(q) = (1 - 4**(-k)) Cov_full_quadratic(q) + 4**(-k) Cov_all_X(q)`.

It leads to a target-dependent near-minimax covariance bound within a specified
reference-preserving real frame/Walsh measurement class. The packet also
contains a restricted phase-rank lower bound and an explicit local decoder.

This is a working research result. Neither external peer review nor literature
novelty is established. Known equatorial shadows, diagonal designs, and parity
compute/phase/uncompute operations are not presented as new primitives.

## Scope

- Complete raw classical gradient at one fixed parameter point.
- Real normalized response q, real tangent matrix T, T[0]=0.
- Exact phase-calibrated controlled objective access for response preparation.
- Independent fresh preparation and random masks for every measurement record.
- Two clean reusable work qubits, separate from the reference ancilla.
- Logical gate counts assume all-to-all connectivity; no runtime, routing,
  fault-tolerance, robustness, trainability, or quantum-advantage claim.
- The 4 tr(G) minimax result is restricted to the specified frame/Walsh class.
- The width-dependent lower bound is a real quadratic-phase RANK bound, not a
  universal CNOT lower bound. More general compilers and POVMs are not excluded.
- No previous spectral/coherence minimax theorem is audited here.

## Files

- `PROOF.md`: self-contained assumptions, lemmas, derivations, resource costs,
  and limitations.
- `core.py`: parity gadgets, exact measurement moments, covariance predictions,
  local shift-table decoder, and rank witness.
- `validate.py`: fresh exact-distribution and finite-dimensional tests.
- `validation.json`: outputs of the executed test run, including exact
  worst-response covariance for 15 non-Hopf circuit cases.
- `reference_circuit.py`: inherited small-system circuit fixture, copied byte
  for byte from the user-provided matched-audit bundle. Not a scalable production
  circuit simulator. Its other optional routines are not all rerun here.
- `SOURCES.md`: primary sources and attribution boundaries.
- `PROVENANCE.json`: input archive identity and inherited-file hashes.
- `SHA256.json`: hashes of distributed files, excluding the hash file itself.

## Reproduce

Python 3.10+ and NumPy are sufficient. From this directory:

```bash
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python validate.py
```

The code evaluates full probabilities only on small registers. The 1,024-qubit
entry is an ANALYTICAL compiler gate ledger, not a quantum simulation. Floating
point residuals are not interval-arithmetic proof certificates.

The main seed is `2026091551`. The output records Python and NumPy versions.
No Monte Carlo shot study or physical gate simulation is claimed in this packet;
the compute/phase/uncompute gate contract is checked on basis inputs, which
extends to arbitrary superpositions by linearity.

The Hopf-QBP repository was not modified.
