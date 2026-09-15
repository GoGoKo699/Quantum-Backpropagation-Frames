# Parity-phase compilation of shared gradient measurements

Working theorem packet, 15 September 2026. The derivations are supplied here;
numerical tests are separate. No external peer review or novelty clearance is
claimed. This packet does not re-audit earlier capped-coherence or spectral
minimax statements from the conversation.

## 1. Model

At one fixed parameter point let T be a real N by P matrix, N=2^n, with first
row zero. Let q be an unknown real unit vector and g=2 T^T q. The prepared state
is Omega(q)=(|0>|0>+|1>|q>)/sqrt(2). In the gradient application,
T=U^T J, q=U^T O U|0>, U is a real ansatz completion and O a real Hermitian-unitary
objective with phase-calibrated controlled access. Every unit real q is
realizable by a reflection O, at this fixed point. Put G=T^T T and s=tr G.
Assume s>0; s=0 is trivial.

Each shot starts with a fresh Omega(q). The frame may depend on T and independent
classical randomness, but not on the unknown q. The reference state is preserved.
The core theorems concern an all-X readout and the decoder conditionally unbiased
for every q for each chosen frame. No unrestricted-POVM optimality is claimed.
Two clean work ancillas are allowed and returned to zero. Logical circuit counts
assume all-to-all two-qubit connectivity. CNOT count is not circuit depth, wall
clock time, fault-tolerant cost, or a routed-device bound.

## 2. Representation and fixed-measurement lemmas

Write a=|0,0> and b_x=|1,x>. A real symmetric observable M has expectation
2 t^T q on Omega(q) for every real unit q iff its compression to span(a,b_x) is

    [ alpha       2 t^T ]
    [ 2 t        -alpha I ].

Proof: compare q and -q to fix the linear coefficient; the even quadratic form
must be constant on the unit sphere. Off-subspace matrix elements remain free
and can affect second moments. Equality of expectations is not operator equality.

For a fixed all-X measurement put chi_y(x)=(-1)^(x dot y). Its probabilities are
p(b,y)=(1+(-1)^b chi_y^T q)^2/(4N). Writing an arbitrary deterministic scalar
decoder as a_y+(-1)^b c_y, universal unbiasedness forces c_y=2 t^T chi_y and a_y=0.
For the latter, the even quadratic form implies N a_y=-sum_z a_z for every y;
summing forces all a_y to vanish. The decoder is therefore unique. Additional
independent postprocessing randomness only adds conditional covariance.

## 3. A reference-frame statistical benchmark

For a real orthogonal R fixing |0>, use T_R=R^T T, q_R=R^T q. The all-X record is
Z=2(-1)^b T_R^T chi_y. Let S_R(y)=||T_R^T chi_y||^2. Then

    tr Cov(Z;q) = 2s + (2/N) sum_y S_R(y) (chi_y^T q_R)^2 - ||g||^2.

At q=|0>, b=0 and y is uniform, so every frame has total covariance 4s.
A frame diagonalizing TT^T while fixing |0> gives S_R(y)=s for all y, and hence
tr Cov=4s-||g||^2. Therefore the best worst-response covariance is exactly 4s
within this frame-Walsh/conditionally-unbiased class, including random mixtures.
The eigenframe may be expensive to compute, compile, or decode.

For the identity frame define beta=max_y S_I(y)/s >=1. Then

    tr Cov_0(q) <= 2s(1+beta).

If each tangent is supported on computational strings contained in at most w
qubits, beta <= 2^w, by Cauchy-Schwarz column by column. For interval supports,
max S_I can be computed using boundary-state dynamic programming in time
polynomial in the circuit size and exponential only in w. No dense Jacobian is
required if the local tangent tables are provided by the cone compiler.

## 4. The two-parity phase gadget

Draw a,b uniformly and independently from F_2^n. Define

    D_(a,b)|x> = (-1)^[(a dot x)(b dot x)] |x>.

Compute a dot x and b dot x into two zero ancillas, CZ the ancillas, and uncompute.
Both work qubits end in zero and D_(a,b)|0>=|0>. One round uses exactly
2(|a|+|b|) CNOTs and one CZ in the displayed implementation. Expected CNOT count
is 2n; worst count is 4n. k independent rounds use 2nk expected CNOTs, k CZs,
2nk classical random bits, and the same two reusable work ancillas.

The net system unitary is diagonal, but its implementation is not restricted
to direct physical CZ edges among system qubits. Its quadratic coefficient
matrix is a b^T+b a^T over F_2 and has rank at most two. There is also a linear
phase sum_i a_i b_i x_i, which only relabels Walsh outcomes and is retained by
our physical phase implementation.

## 5. Exact covariance interpolation

Let Sigma_0(q) be the unmasked all-X covariance. Let Sigma_full(q) be the
covariance averaged over independent fair CZ choices on every system pair.
For real T,q with T[0]=0,

    Sigma_full(q) = 4 T^T diag(1-q_x^2) T.

This formula follows directly from the three surviving pairings of the four
sign indices; the all-equal term is subtracted twice. It also follows by
expanding the measurement second moment and using full quadratic masking.

Let Sigma_k(q) be the covariance for k independent two-parity rounds followed
by the corresponding unbiased masked-Walsh decoder. Then EXACTLY

    Sigma_k = (1-4^(-k)) Sigma_full + 4^(-k) Sigma_0.

Proof: the Walsh sum leaves only four-tuples x,z,u,v with x+z+u+v=0 over F_2.
Set h=x+z and delta=x+u. If h and delta are linearly dependent, the phase is one.
Otherwise (a dot h,a dot delta) and (b dot h,b dot delta) are independent uniform
two-bit strings. The exponent is their 2 by 2 determinant. Six of the sixteen
possibilities are odd and ten even, giving mean 1/4. k rounds give 4^(-k).
Independent full quadratic masks give zero in this latter case. Thus the
fourth-moment kernel is the exact affine interpolation. All means are identical,
so subtracting g g^T preserves the interpolation at covariance level.

This is not a claim that finite-k masks are a full unitary design, nor that the
variance decreases for each fixed q. Covariance differences may be indefinite.

Taking trace and using the benchmark yields

    sup_q tr Sigma_k(q) <= B_k
       := 4s + 2s (beta-1) 4^(-k).

The actual worst-response risk is nonincreasing in k: it is a convex function
of gamma=4^(-k), takes its minimum 4s at gamma=0, and is at least 4s for every
gamma because q=|0> achieves 4s. This is stronger than pointwise monotonicity,
which is not asserted.

To guarantee B_k <= 4s(1+eta), take k=0 if (beta-1)/(2eta)<=1, otherwise

    k = ceil[ log_4((beta-1)/(2eta)) ].

For width w, k=O(w+log(1/eta)). The number of complete response preparations is
unchanged per shot; the phase rounds act inside that shot and use no extra
controlled-objective query. For K independent shots, the unbiased sample mean
has MSE at most B_k/K. Markov gives the sufficient unchanged-mean guarantee
K >= B_k/(delta epsilon^2). Robust batching can instead improve confidence
dependence, but is a different, generally biased final aggregation.

## 6. Classical decoder preserving local structure

For one round,

    (-1)^(uv) = [1+(-1)^u+(-1)^v-(-1)^(u+v)]/2.

Consequently, if F_j is the original local Walsh table,

    F'_j(y) = [ F_j(y)+F_j(y+a)+F_j(y+b)-F_j(y+a+b) ]/2.

All masks are restricted to I_j in this equation. After k rounds, at most 4^k
lookups in the ORIGINAL table evaluate the score. Duplicate shifts may be
combined. Alternatively compute the local quadratic mask and a local Walsh
transform, requiring O(k w_j^2+w_j 2^(w_j)) arithmetic operations, conservatively.
The cheaper implementation can be chosen. Local supports do not grow because
the system operation is diagonal.

Thus a conservative direct-record cost is

    O(nk + sum_j min{4^k, k w_j^2+w_j 2^(w_j)})

after cone compilation and original-table preprocessing. Memory remains the
local tables, P output accumulators, the k parity masks, and small workspace.
The finite-word cost of dot products and table addresses must be retained when
w or n exceeds the assumed word size. The statement is not exponential-free
when w grows; it avoids dependence on the full 2^n state dimension.

This is a valid explicit upper implementation, NOT a claim of optimal classical
processing. More elaborate aggregate-first processing is allowed to all baselines.

## 7. A phase-rank lower bound

Let m=2^w, w>=3, and choose the single normalized tangent

    t = (sum_{x != 0}|x>)/sqrt(m-1),

padded by zeros outside its w-qubit support. It is a legitimate tangent of
psi(theta)=cos(theta)|0>+sin(theta)|t> at theta=0. Choose the valid response q=t;
then g=2. This is a statistical witness, not a quantum-hard objective instance.

For any real quadratic phase f with f(0)=0, let kappa be the binary rank of its
alternating coefficient matrix restricted to the w qubits. Let
W(y)=sum_x (-1)^(f(x)+x dot y). Direct finite-field summation gives

    E W=1, E W^2=m, E W^3=m^2/2^kappa, E W^4=m^3/2^kappa.

The Walsh score is (W-1)/sqrt(m-1). The exact scalar variance at q=t is therefore

    Var(Z) = 2 [m^2(m-4)/2^kappa + 6m - 3]/(m-1)^2 - 2.

A mask formed from at most k bilinear parity products has kappa<=2k. Since
m>=8, this implies the convenient lower bound

    Var(Z) >= m/4^k - 2.

The same bound holds after averaging any distribution of such masks, because
each mask has the same unbiased mean. To obtain worst-response variance at most
4(1+eta), necessarily

    k >= [w - log_2(6+4eta)]/2.

For fixed eta, k=Omega(w) is necessary in this bilinear-rank-limited class, while
the constructed ensemble uses w/2+O_eta(1) rounds. This matches the width
scaling, NOT the eta dependence or total elementary-gate complexity.

The restriction is essential: other real orthogonal frames, general POVMs,
complex intermediate phase constructions, and arbitrary Clifford synthesis are
not lower-bounded by counting these parity products. In particular, this is not
an Omega(nw) CNOT lower bound and not a lower bound for all shadow protocols.

## 8. Relation to prior results and scope

The reference interference, equatorial quadratic masks, diagonal-design ideas,
and parity compute/phase/uncompute techniques are established ingredients.
The claim derived in this packet is the exact fourth-moment interpolation for
this bilinear ensemble, its target-dependent covariance/cost prescription,
local shift-table decoder, and restricted rank witness. Novelty of that
combination has not been established. Do not call an unsuccessful search a
proof of novelty.

The direct independent-CZ realization has expected n(n-1)/4 system CZs. The
new implementation has 2nk expected CNOTs plus k CZs. This is a comparison to
THAT realization, not to the best possible Clifford compilation. Near-linear
unitary designs and low-depth shadow schemes are already known. The present
ensemble need not satisfy their general design conditions and their performance
cannot be inferred solely from gate counts.

No new ansatz, objective hardness assertion, hardware-noise model, inverse-metric
claim, or optimizer convergence theorem is introduced. The original Hopf-QBP
repository is unchanged. The real-response restriction must remain attached.
