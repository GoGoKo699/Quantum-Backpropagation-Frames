# PF-01: independent proof audit

Baseline: `da0d8c771350b695206b6f06194277538833adb4`. Audit branch: `audit/PF-01`.

This is an internal rederivation from the model and Born probabilities, with new finite diagnostics. It is not external peer review. Imported proofs and code remain unchanged. The mathematical dispositions below apply on the specified domain; software input validation is a separate finding.

## 1. Contract

Let N=2^n, T be a real N-by-P matrix with T[0,:]=0, q a real unit vector, and s=tr(T^T T)>0. The target is the full real vector g=2T^T q. Each experiment prepares (|0,0>+|1,q>)/sqrt(2). Frames may depend on T and fresh recorded classical randomness but not on q. Every chosen frame's decoder is unbiased for every admissible q, conditional on that frame. The objective is accessed with a calibrated controlled phase. One independent record uses one fresh response preparation.

At a fixed ansatz point, every q is achievable by a real reflection mapping the prepared state to the desired response. The chosen objective is then held fixed during differentiation. This is a worst-case oracle model, not an assertion that every reflection has an efficient application-specific circuit.

## 2. PF-01: observable compression (KEEP)

Restrict a real symmetric observable M to the occupied subspace spanned by a=|0,0> and b_x=|1,x>. Write its blocks as alpha, c, and B. Its expectation is

```math
\frac12\alpha+c^{\mathsf T}q+\frac12q^{\mathsf T}Bq.
```

Equality to 2t^Tq for q and -q gives c=2t. The remaining quadratic form must be the same constant on the entire unit sphere, so B=-alpha I. Conversely these blocks give the required expectation. Matrix entries coupling to unoccupied states do not affect this mean, but can affect the second moment. There is no global operator-equality claim.

## 3. PF-02: fixed-measurement uniqueness (KEEP, restricted)

Let H be the normalized Walsh matrix, chi_y its unnormalized row. The actual probabilities are

```math
p(b,y)=\frac{(1+(-1)^b\chi_y^{\mathsf T}q)^2}{4N}.
```

For a general real score a_y+(-1)^b c_y, the odd part of its mean is (1/N) sum_y c_y chi_y^Tq. Walsh invertibility fixes c_y=2t^Tchi_y. The even part requires sum_y a_y chi_y chi_y^T=-(sum_y a_y)I. Its eigenvalues give N a_y=-sum_z a_z. Summing over y forces all a_y=0. Conditional averaging of additional postprocessing randomness cannot reduce covariance below this unique score.

This does not prohibit optimized dual frames for a different, redundant measurement, ensemble-only unbiasedness, or estimation under extra promises on q. The distinction from informationally complete dual-frame optimization is substantive [S6].

## 4. PF-03: frame-class optimum (KEEP; no extension to arbitrary POVMs)

For any real orthogonal R fixing |0>, put T_R=R^T T and q_R=R^T q. Let S_R(y)=||T_R^T chi_y||^2. Summing the Born probabilities gives

```math
\operatorname{tr}\Sigma_R(q)
=2s+\frac2N\sum_y S_R(y)(\chi_y^{\mathsf T}q_R)^2-\|g\|^2.
```

At q=|0>, only the b=0 branch occurs and y is uniform; the trace covariance is exactly 4s for every allowed R. Mixtures of conditionally unbiased frames inherit this lower bound. Diagonalize TT^T on the subspace orthogonal to |0>. Every Walsh character then has squared tangent projection s. This R attains trace covariance 4s-||g||^2, proving the restricted minimax value 4s.

A counterexample prevents unrestricted interpretation. For n=1, t=|1>, directly measure F=2(|00><11|+|11><00|). On the same reference state its variance is 2-2q_1^2, with worst value 2 rather than 4. This measurement lies outside the frame/Walsh class. It does not refute the stated theorem.

The eigenframe's existence is not an efficient compiler. Finding it, synthesizing it, and decoding its outcomes must be separately charged.

## 5. PF-04 and PF-05: gadget and exact interpolation (KEEP)

For independent uniform a,b in F_2^n, computing a.x and b.x into two zero work qubits, applying CZ, and reversing the computations gives the phase (-1)^((a.x)(b.x)). Both work qubits return to zero. Its displayed CNOT count is exactly 2(|a|+|b|); expectation 2n, worst 4n. A round also uses one CZ and 2n random bits. These counts assume all-to-all connectivity and no cancellation optimization.

The polar matrix is ab^T+ba^T over F_2, of rank at most two. Diagonal products a_i b_i contribute a linear phase; dropping them requires relabeling Walsh outcomes rather than pretending the unitary is identical.

In the second moment, summing over y enforces x+z+u+v=0. Define h=x+z and Delta=x+u. For dependent h and Delta the four-sign phase is one. For independent h and Delta the exponent is the determinant of the two independent uniform pairs (a.h,a.Delta) and (b.h,b.Delta). Exactly six of the sixteen binary matrices have determinant one, hence the character expectation is 1/4. Independent rounds give 4^(-k). A full independent quadratic mask has expectation zero in this latter case.

The full-mask pairing calculation gives

```math
\Sigma_{\rm full}=4T^{\mathsf T}\operatorname{diag}(1-q_x^2)T.
```

All conditional means equal g, so the fourth-moment interpolation also holds for covariance:

```math
\Sigma_k=(1-4^{-k})\Sigma_{\rm full}+4^{-k}\Sigma_0.
```

The complete covariance, not just its trace, was independently checked. A finite-k ensemble is not asserted to be a full Haar or diagonal-unitary design. Its required character calculation is narrower than general design theorems [S2,S3,S9]. The exact 1/4 identity is an elementary character calculation; no source in the bounded audit was found stating this exact gradient/compiler combination. That is not a novelty certificate.

## 6. Variance, confidence, and width

Let beta=max_y ||T^Tchi_y||^2/s. Walsh orthogonality gives beta>=1. Cauchy-Schwarz on w-qubit-supported columns gives beta<=2^w. Hence

```math
\sup_q\operatorname{tr}\Sigma_k(q)
\le B_k=4s+2s(\beta-1)4^{-k}.
```

The worst-response trace is nonincreasing in k: as a function of gamma=4^(-k) it is convex, has its minimum 4s at gamma=0, and cannot fall below 4s because q=|0> attains that value. No pointwise matrix ordering in q follows. In particular a particular objective can have larger variance after masking.

For independent sample means, MSE<=B_k/K. Markov gives K>=B_k/(delta epsilon^2) as a sufficient whole-vector guarantee for the unchanged unbiased estimator. This is not an optimal tail bound. Robust batching is allowed with its own bias and cost contract. Masks and records must follow the declared independent sampling policy.

Choosing k from beta or its certified upper bound is valid without querying q. Computing beta can be expensive unless support structure supplies an efficient algorithm. A local-support assumption is not itself a supplied free tangent table.

## 7. PF-06: decoder (KEEP as an upper implementation)

The exact identity

```math
(-1)^{uv}=[1+(-1)^u+(-1)^v-(-1)^{u+v}]/2
```

gives four shifted original Walsh-table lookups per round, at most 4^k after k rounds. Diagonal phases preserve local support. Alternatively form the restricted quadratic mask and a local Walsh transform. The packet's minimum of these costs is a valid conservative upper bound, with finite-word address/parity costs included. It is not an optimal-decoder claim. All competitors may aggregate records, combine repeated shifts, precompute shared tables, and synthesize their measurements.

## 8. PF-07: quadratic-rank witness (KEEP; rank, not CNOT optimality)

Let m=2^w, t=q=(sum_{x!=0}|x>)/sqrt(m-1), so g=2. For a real quadratic f with f(0)=0 and polar rank r, its Walsh transform W obeys

```math
E W=1,\quad E W^2=m,\quad E W^3=m^2/2^r,\quad E W^4=m^3/2^r.
```

The last two relations follow by summing derivatives of the quadratic phase, or from the support and magnitude of its quadratic Gauss sum. They hold with linear phases retained. The resulting exact variance is

```math
2\frac{m^2(m-4)2^{-r}+6m-3}{(m-1)^2}-2.
```

For k parity products, r<=2k. For w>=3 this yields variance>=2^w/4^k-2 and the stated necessary k bound. The upper and lower bounds match the leading w dependence for fixed variance slack, not the eta dependence or total gate cost. General frames, complex intermediate circuits, arbitrary Clifford synthesis, and arbitrary POVMs are not lower-bounded by this argument. Quadratic Gauss sums and rank-based Fourier analysis are established mathematics [S10]; the witness is a task-specific use.

## 9. A cost-relevant terminal measurement substitution

For the final measurement task, coherent uncomputation is optional. After computing the two work parities and applying CZ, measure the work qubits in X. Their outcomes u,v leave the system phase D_ab times the character with label u a+v b, with Kraus magnitude 1/2. Relabel the later system-X outcome by that known label. The complete folded Born probabilities equal the clean-uncomputation scheme exactly. Across multiple diagonal rounds, the corrections add and commute.

This alternative uses expected n CNOTs and one CZ per round, rather than 2n CNOTs, plus two work measurements and resets per round when reusing two work qubits. It is not a clean-unitary substitution and has different latency/noise/resource assumptions. Terminal linear transformations absorbed into X-outcome processing are a known optimization principle [S1, Appendix G]. This audit applies that principle to the supplied gadget rather than claiming a new primitive. The independent probability test covers 48 cases.

## 10. Software and evidentiary boundaries

`software_probe.py` finds accepted NaNs in q, T, and phase, and a complex response coerced to real with a warning. These are CORRECT input-contract findings: reject unsupported complex arrays and nonfinite values before converting dtypes. No imported code was changed. The mathematical assertions above do not use these invalid inputs.

A separate complex-response example demonstrates why the stated real formula cannot be extended by replacing q_x^2 with |q_x|^2. An unknown pi/2 controlled-branch phase also changes a required mean of 2 to 0. Both are outside-contract counterexamples, not failures on the valid domain.

See diagnostics.json for all executed counts and residuals; SOURCE_AUDIT.md for references; RESOURCES.md for the matched cost decision. No earlier spectral or capped-coherence theorem was re-audited.
