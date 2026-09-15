# Claim register

This register distinguishes available derivations, inherited computation,
fresh computation, and unestablished conclusions. The packet proof is a
working derivation, not independent review. Fresh startup checks are described
in `../validation/bootstrap/REPORT.md`.

| ID | Claim / question | Available evidence | Boundary |
|---|---|---|---|
| PF-01 | Reference-restricted observable characterization | `research/parity_frames/PROOF.md`, section 2; finite checks | Real symmetric observables on the specified reference family; not operator equality everywhere. |
| PF-02 | Unique universally conditionally unbiased decoder for fixed all-X readout | Proof section 2; full-rank finite constraint checks | Does not exclude optimizing a richer measurement or dropping conditional unbiasedness. |
| PF-03 | Worst-response total covariance benchmark `4 tr(G)` | Proof section 3; eigenframe checks | Only the stated reference-preserving real frame/Walsh class, not arbitrary POVMs. |
| PF-04 | Compute-phase-uncompute parity gadget | Proof section 4; reversible basis-input checks | Two clean work ancillas; all-to-all logical gate ledger. |
| PF-05 | Exact covariance interpolation with coefficient `4**(-k)` | Proof section 5; complete small ensemble moments | Real normalized response; new independent parity masks per record. |
| PF-06 | Local shifted-Walsh decoder and explicit costs | Proof section 6; lookup versus direct-score tests | Exponential local-width factors remain; no optimal-decoder claim. |
| PF-07 | Width-dependent lower bound | Proof section 7; quadratic-rank witness | A bilinear-rank bound for real quadratic phase masks, not an unrestricted gate or measurement bound. |
| MR-01 | Matched comparison of four readout implementations | `research/matched_readout/` code and JSON records | Diagnostic instances are classically easy; finite examples are not a quantum-advantage demonstration. |
| OPEN-01 | Novelty of covariance/compiler combination | Literature pointers available | Not cleared. Audit exact statements against primary sources. |
| OPEN-02 | Advantage over strongest matched compiler/shadow implementation | Resource ledger and selected baselines available | Not established. Near-linear designs, shallow shadows, and optimized compilation must be allowed. |
| OPEN-03 | General or routed hardware optimality | None in supplied packets | Do not infer from the phase-rank witness or logical counts. |
| OPEN-04 | Earlier spectral and capped-coherence minimax results | Conversation-level assertions, no corresponding proof/code packet supplied | Not adopted or revalidated in this repository. |

A diagnostic success may strengthen computational evidence for a premise. It
must not automatically promote OPEN entries or expand the theorem class.
Record negative findings and known-method equivalences as carefully as positive
results. A future patch to an imported proof must preserve the original source
and a claim-to-change map.
