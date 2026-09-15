# Project scope

## Agreed scientific goal

Develop frame-based quantum backpropagation by characterizing and compiling
shared measurements for complete classical gradients. The first positive result
may concern one concrete ansatz family with nonorthogonal tangents; arbitrary
parameterized circuits are not required.

At a fixed parameter point the requested output is the complete classical raw
gradient, with a stated confidence guarantee in whole-vector Euclidean norm:

```math
\Pr[\|\widehat g-g\|_2\le\varepsilon]\ge1-\delta.
```

Keep simultaneous coordinatewise accuracy, elementwise variance, and exact
unbiasedness explicit when comparing published backpropagation criteria.
Neither a quantum gradient state nor one directional derivative completes the
task. Changes in parameter normalization must be stated and cannot be counted
as computational improvements.

## Brainstorming versus success

Access assumptions may be explored. Every candidate must specify preparation,
controls, inverses, branch phase, quantum memory, precision, output, and what is
classically known. An assumption must not supply the gradient or an equally
expensive intermediate object for free.

The ultimate success requirement includes a provable end-to-end improvement
under matched assumptions over an applicable strong existing gradient method.
A sharp resource theorem can advance the project but does not by itself fulfill
that advantage goal. Count quantum gates, calls, fresh executions, classical
decoding, preprocessing, memory, and materialized output. Improving over an
intentionally weak implementation is insufficient.

The first deliverable is a theorem with reproducible numerical validation.
Hardware demonstration and optimizer-convergence guarantees are outside the
initial scope. PRL is a research ambition, not an acceptance prediction and not
a scientific claim to place in the repository description.

## Current packet: narrower contract

`research/parity_frames/PROOF.md` is authoritative for the candidate's model:
real unit response `q`, real `N x P` tangent matrix with zero first row, exact
calibrated controlled-objective access, independent masks and fresh response
preparation for every record, and two clean work ancillas. Logical gate counts
assume all-to-all connectivity. The reference ancilla is additional.

The minimax statement is restricted to reference-preserving real frame/Walsh
readouts with conditional unbiasedness for every response. The lower bound
counts real quadratic-phase bilinear rank; it is not a general CNOT bound or a
lower bound for all POVMs, Clifford compilers, or shadows.

## Repository boundaries

Work is confined to this repository. Do not modify other repositories as part
of its initialization or work orders.
Do not start a manuscript, publish, tag, select a license, or launch hardware
work merely because a numerical check passes. Future user instructions may
explicitly authorize those actions.
