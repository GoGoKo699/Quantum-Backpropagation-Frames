# PF-01 primary-source audit

Date accessed: 2026-09-15. Scope: the supplied parity packet and its matched-measurement claims. Earlier spectral/coherent-query assertions are not audited. Sources were read through the web tool as HTML or parsed PDF; relevant PDF pages were also rendered. No local byte hash of a paper is claimed. Versions and section/equation locations below identify what was inspected.

## S1. Equatorial stabilizer measurements

Park, Teo, Jeong, *Resource-efficient shadow tomography using equatorial stabilizer measurements*, [2311.14622v4](https://arxiv.org/abs/2311.14622v4), revised 31 July 2025; Phys. Rev. Research 7, 033097.

Inspected: Section II.A Eqs. (3)-(4); Algorithm 1 and Eqs. (6)-(7); Appendix B variance analysis; Appendix G, particularly the paragraph about replacing rightmost CNOTs by X-outcome processing. PDF pages 3 and 25 were rendered.

Established content: uniform real quadratic phases and X measurements; low-Frobenius-norm observable estimation; explicit direct and nearest-neighbor implementations. Terminal linear gates can be removed with known outcome relabeling. Our full-mask endpoint and the elementary principle behind measured uncomputation are not new. The finite-round rank-two ensemble is not the uniformly sampled full ensemble; no identical finite-round interpolation theorem was located in these sections.

## S2. Diagonal-unitary designs

Nakata, Murao, *Diagonal-unitary 2-designs and their implementations by quantum circuits*, [1206.4451v5](https://arxiv.org/abs/1206.4451v5).

Inspected: phase-random constructions and Section 6, especially Propositions 2-4 and the convergence analysis in Section 6.2. This studies convergence to the complex diagonal-unitary second moment. It does not make our real finite-round ensemble a diagonal-unitary design. Markov/twirling convergence is prior methodology; the required character kernel and convergence norm must be compared, not inferred from similar circuit words.

## S3. Higher diagonal moments

Nakata, Koashi, Murao, *Generating a state t-design by diagonal quantum circuits*, [1311.1128v3](https://arxiv.org/abs/1311.1128v3), 26 May 2014; New J. Phys. 16, 053043.

Inspected: Section III.2, Theorem 1, and the construction/proof discussion in Section IV.2. The theorem characterizes all-r-subset random-phase circuits implementing a diagonal-unitary t-design. Those independent multi-qubit phases are not the rank-two bilinear updates in the packet. The packet needs a restricted four-sign identity, not this full design guarantee. Neither theorem is automatically a gate lower bound for the other's task.

## S4. Near-linear exact two-designs

Cleve, Leung, Liu, Wang, *Near-linear constructions of exact unitary 2-designs*, [1501.04592v3](https://arxiv.org/abs/1501.04592v3), 28 June 2016.

Inspected: Sections 1.1-1.3, Section 6, Appendix E. Section 1.2 includes an unconditional all-n all-Clifford construction with O(n log^2(n) loglog(n)) gates and near-linear clean workspace. Faster variants have different qualifications. Section 1.1 notes the O(n^2/log n) generic Clifford synthesis bound.

This invalidates any assertion that useful randomization universally needs quadratic gates. It does NOT, by itself, give the standard Clifford-shadow variance: unbiased reconstruction uses a second projective moment, whereas the squared score weighted by its Born probability uses a third projective moment. A two-design needs additional target-specific analysis to supply that bound. No exact finite-size cost or matching 4s guarantee is invented for this comparator.

## S5. Shallow shadows

Bertoni et al., *Shallow shadows: Expectation estimation using low-depth random Clifford circuits*, [2209.12924v3](https://arxiv.org/abs/2209.12924v3), 20 December 2024; PRL 133, 020602.

Inspected: Lemma 5, Corollary 6, Theorem 7/Eqs. (20)-(23), Theorem 9 and subsequent worst-case versus locally scrambled discussion. Theorem 7 gives the state-dependent second moment from joint Pauli probabilities. Corollary 6 supplies efficient exact computation at logarithmic measurement depth for the relevant probabilities. The paper distinguishes a typical-state norm from worst-case guarantees.

This is a mandatory architecture-level comparator. For local/Pauli-sparse derivative representations, use its actual inverse-channel and variance calculation. Low depth alone does not imply our uniform 4s endpoint. No asymptotic superiority over this framework has been established by the packet or audit.

## S6. Dual-frame optimization

Fischer, Dao, Tavernelli, Tacchino, *Dual frame optimization for informationally complete quantum measurements*, [2401.18071v2](https://arxiv.org/abs/2401.18071v2), 17 June 2024.

Inspected: Sections II.3-II.4 and III. The paper exploits redundant dual choices for an informationally complete measurement. Our fixed-basis uniqueness lemma imposes conditional unbiasedness for every response separately at each selected frame. The two statements are compatible. The lemma cannot be used to exclude ensemble-level dual optimization or target/state promises outside that restricted class.

## S7. Reversed gradient tests

Li et al., *Efficient Quantum Gradient and Higher-order Derivative Estimation via Generalized Hadamard Test*, [2408.05406v1](https://arxiv.org/abs/2408.05406v1).

Inspected: reversed-Hadamard construction and measurement-optimization discussion. Objective/generator role exchange, shorter suffix inverses, and generator grouping are established baseline ingredients. A comparator given the same controlled objective must not be charged for an unnecessary Pauli decomposition or full reversal. The imported matched packet already implements those improvements; this audit preserves them.

## S8. Clifford shadows and the correct moment order

Huang, Kueng, Preskill, *Predicting many properties of a quantum system from very few measurements*, [2002.08953v2](https://arxiv.org/abs/2002.08953v2).

Inspected: supplementary Clifford measurement discussion, Eqs. (S36), (S39)-(S43). The third-moment identity provides an immediate strong full-gradient comparator, not intrinsically one derivative per experiment.

Audit substitution: for F_j=2(|a><b_tj|+|b_tj><a|), d=2N and c=(d+1)/(d+2),

```math
\operatorname{Cov}(Z_{\rm Clifford})=12cG-\frac{gg^{\mathsf T}}{d+2}.
```

This follows by polarization of Eq. (S43): tr(F_j F_l)=8G_jl and the state-weighted symmetric product contributes 4G_jl+g_jg_l. Thus total variance<=12s, the same O(s/epsilon^2) whole-vector scale as the parity method, with different gates and decoding. Stabilizer target-overlap computation and optimized synthesis must be counted. This substitution is an audit calculation, not a separately quoted theorem.

## S9. Transvection mixing

Singal, Hsieh, *Approximate 3-designs and partial decomposition of the Clifford group representation using transvections*, [2111.13678v2](https://arxiv.org/abs/2111.13678v2).

Inspected: Scheme 1, Theorems 2-3, and the proof outline following Eq. (29). Repeated simple random Clifford updates are analyzed by a twirling spectrum, including a third-design convergence rate. This confirms that a geometric contraction from repeated low-complexity updates is not, alone, a new research principle. The update ensemble, required moments, error norm, and bias are different; no exact identification with the packet's bilinear kernel is asserted.

## S10. Quadratic-rank Fourier analysis

*Triangular cutoff threshold for the inversion walk on tournaments and the state space of restricted inversions*, [2603.01368v3](https://arxiv.org/abs/2603.01368v3).

Inspected: Lemma 3.1 and the Fourier discussion expressing eigenvalues through quadratic Gauss sums and binary ranks. The paper uses a different random update. It is context for the established rank/Gauss-sum method, not evidence that the packet's exact covariance formula was published there. The rank-witness moments were independently derived and tested in this audit.

## Search coverage and conclusion

In addition to following the supplied primary references and their mathematical locators, explicit searches included:

- `"parity" "equatorial" shadow`
- `"random" "alternating matrices" "rank two"`
- `"quantum" "parity" "covariance" "quadratic"`
- `"near-linear" "3-design" Clifford`

These returned many irrelevant hits, which were not used. Earlier broad searches also led to the transvection and quadratic-rank sources above. This is a bounded primary-source comparison, not exhaustive bibliometric, patent, or historical priority clearance.

Disposition: the primitives, full-mask endpoint, shadow moment method, and character/spectral approach are ALREADY-KNOWN ingredients. The specific 4^(-k) reference-gradient covariance interpolation plus local decoding is mathematically supported, but its novelty remains OPEN. No source examined supplies an immediately identical statement; absence of that finding is not proof of novelty. The strongest-baseline total-work advantage is also OPEN and cannot be claimed from the direct dense-CZ comparison.
