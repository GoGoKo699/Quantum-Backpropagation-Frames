# Literature and attribution map

Start with the imported [source notes](../research/parity_frames/SOURCES.md)
and the attribution section of the [matched audit](../research/matched_readout/README.md).
Those notes identify what previous work was credited with during the source
packet's preparation. The repository bootstrap did not reopen or independently
verify those articles.

## Priority for the next audit

| Topic | Source identified in the supplied material | Question to verify |
|---|---|---|
| Stream-to-oracle and signed-overlap motivation | arXiv:2604.07639 | What access and readout guarantees are actually used here? |
| Real equatorial shadows | arXiv:2311.14622 | Does its ensemble or moment analysis already imply the parity interpolation? |
| Diagonal designs | arXiv:1206.4451; arXiv:1311.1128 | Which moments are needed, and which existing constructions reproduce them? |
| Near-linear designs | arXiv:1501.04592 | Is the direct dense-CZ comparator unnecessarily costly? |
| Shallow shadows | arXiv:2209.12924 | Compare total gate, decoding, and sample costs under matched structure. |
| Dual-frame optimization | arXiv:2401.18071 | Distinguish decoder redundancy from conditional unbiasedness in our restricted family. |
| Reversed gradient tests | arXiv:2408.05406 | Permit grouping and shorter suffixes in the baseline. |
| Established gradient criteria | arXiv:2306.14962; arXiv:2305.13362 | Keep output norm, bias, memory, and coherent resources explicit. |
| Coherent tomography background | arXiv:2207.08800; arXiv:2405.14765 | Earlier exploration only; not a dependency to assume proven by the current tests. |

For each new novelty entry, record the exact version, theorem/section, access
model, output, error guarantee, and computational ledger. Distinguish a result
quoted from a source from a new derivation combining known results. A search
that finds no match is not a novelty certificate.
