"""Reference-preserving parity-phase gradient readout.

Exact ideal real-state model. Bit strings are integers; bit 0 is the least
significant bit. Dense routines are diagnostic only. NumPy is the only
non-standard-library dependency.
"""
from __future__ import annotations
from functools import lru_cache
from itertools import product
import math
import numpy as np


def fwht(a: np.ndarray) -> np.ndarray:
    a = np.array(a, dtype=float, copy=True)
    n = a.shape[-1]
    if n < 1 or n & (n - 1):
        raise ValueError('last axis must have power-of-two length')
    h = 1
    while h < n:
        v = a.reshape(*a.shape[:-1], -1, 2, h)
        p = v[..., 0, :].copy(); q = v[..., 1, :].copy()
        v[..., 0, :] = p + q; v[..., 1, :] = p - q
        h *= 2
    return a


def parity(x: int) -> int:
    return int(x).bit_count() & 1


def parity_phase(n: int, pairs: list[tuple[int, int]]) -> np.ndarray:
    N = 1 << n
    if any(a < 0 or b < 0 or a >= N or b >= N for a, b in pairs):
        raise ValueError('mask outside register')
    return np.array([(-1.) ** (sum(parity(a & x) * parity(b & x)
                                      for a, b in pairs) & 1)
                     for x in range(N)])


def edges(n: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def pair_quadratic_mask(n: int, a: int, b: int) -> int:
    mask = 0
    for k, (i, j) in enumerate(edges(n)):
        value = (((a >> i) & 1) * ((b >> j) & 1)
                 ^ ((a >> j) & 1) * ((b >> i) & 1))
        mask |= value << k
    return mask


def quadratic_phase(n: int, mask: int) -> np.ndarray:
    ee = edges(n)
    if not (0 <= mask < (1 << len(ee))):
        raise ValueError('quadratic mask outside range')
    return np.array([(-1.) ** (sum(((x >> i) & 1) * ((x >> j) & 1)
                                      for k, (i, j) in enumerate(ee)
                                      if (mask >> k) & 1) & 1)
                     for x in range(1 << n)])


def gf2_rank(rows: list[int], ncols: int) -> int:
    rows = list(map(int, rows)); rank = 0
    for col in reversed(range(ncols)):
        pivot = next((j for j in range(rank, len(rows)) if (rows[j] >> col) & 1), None)
        if pivot is None: continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for j in range(len(rows)):
            if j != rank and ((rows[j] >> col) & 1): rows[j] ^= rows[rank]
        rank += 1
    return rank


def mask_rank(n: int, mask: int) -> int:
    rows = [0] * n
    for k, (i, j) in enumerate(edges(n)):
        if (mask >> k) & 1:
            rows[i] ^= 1 << j; rows[j] ^= 1 << i
    return gf2_rank(rows, n)


def validate_inputs(T, q):
    T = np.asarray(T, dtype=float); q = np.asarray(q, dtype=float)
    if T.ndim != 2 or q.shape != (T.shape[0],): raise ValueError('shape mismatch')
    N = len(q)
    if N < 2 or N & (N-1): raise ValueError('power-of-two dimension required')
    if np.linalg.norm(T[0]) > 1e-10: raise ValueError('reference-orthogonal tangents required')
    if abs(np.linalg.norm(q)-1) > 1e-10: raise ValueError('unit real response required')
    return T, q


def measurement_moments(T, q, phase=None):
    """Enumerate all ancilla/system outcomes, not a moment-formula shortcut."""
    T, q = validate_inputs(T, q); N, P = T.shape
    if phase is None: phase = np.ones(N)
    phase = np.asarray(phase, dtype=float)
    if phase.shape != (N,) or np.max(abs(phase**2 - 1)) > 1e-12 or phase[0] != 1:
        raise ValueError('real diagonal signs fixing the reference required')
    F = fwht((phase[:, None] * T).T)
    fq = fwht(phase * q)
    p = np.stack([(1 + fq)**2, (1 - fq)**2]) / (4*N)
    z = np.stack([2*F, -2*F])
    mean = np.einsum('by,bjy->j', p, z)
    second = np.einsum('by,bjy,bky->jk', p, z, z)
    return mean, second-np.outer(mean, mean), p, z


def full_quadratic_covariance(T, q):
    T, q = validate_inputs(T, q)
    return 4 * T.T @ ((1-q*q)[:, None]*T)


def interpolated_covariance(T, q, rounds: int):
    if rounds < 0: raise ValueError('nonnegative round count required')
    C0 = measurement_moments(T, q)[1]
    Cf = full_quadratic_covariance(T, q)
    gamma = 4. ** (-rounds)
    return (1-gamma)*Cf + gamma*C0


@lru_cache(None)
def pair_mask_distribution(n: int) -> np.ndarray:
    """Exact enumeration of all 2^(2n) independently uniform parity pairs."""
    out = np.zeros(1 << (n*(n-1)//2))
    for a in range(1 << n):
        for b in range(1 << n): out[pair_quadratic_mask(n, a, b)] += 1
    return out / (1 << (2*n))


def rounds_mask_distribution(n: int, rounds: int) -> np.ndarray:
    """XOR convolution via Fourier transform, independent of covariance theorem."""
    if rounds < 0: raise ValueError('nonnegative round count required')
    p = pair_mask_distribution(n)
    out = fwht(fwht(p)**rounds) / len(p)
    if np.min(out) < -1e-12: raise ArithmeticError('negative convolution weight')
    out = np.maximum(out, 0)
    return out / out.sum()


def covariance_risk_matrix(T, rounds: int):
    """Trace covariance = q.T @ A @ q for any unit real q."""
    T = np.asarray(T, dtype=float); N, P = T.shape
    if np.linalg.norm(T[0]) > 1e-10: raise ValueError('T[0] must vanish')
    s = float(np.sum(T*T)); H = fwht(np.eye(N))/math.sqrt(N)
    S = np.sum(fwht(T.T)**2, axis=0)
    A0 = 2*s*np.eye(N) + 2*(H*S[None, :])@H.T - 4*T@T.T
    Af = 4*s*np.eye(N) - 4*np.diag(np.sum(T*T, axis=1))
    gamma = 4.**(-rounds)
    return (1-gamma)*Af + gamma*A0


def imbalance(T):
    T = np.asarray(T, dtype=float); s = float(np.sum(T*T))
    if not s: return 1.
    return float(np.max(np.sum(fwht(T.T)**2, axis=0))/s)


def risk_bound(T, rounds: int):
    s = float(np.sum(np.asarray(T)**2)); beta = imbalance(T)
    return 4*s + 2*s*(beta-1)*4.**(-rounds)


def rounds_for_relative_bound(beta: float, eta: float):
    if eta <= 0 or beta < 1-1e-12: raise ValueError('beta >= 1 and eta > 0 required')
    ratio = max(0., beta-1)/(2*eta)
    return 0 if ratio <= 1 else math.ceil(math.log(ratio, 4))


def local_shift_score(table: np.ndarray, y: int, pairs: list[tuple[int,int]]) -> float:
    """Evaluate masked Walsh score using <= 4^k lookups in the ORIGINAL table."""
    table = np.asarray(table, dtype=float)
    terms = {int(y): 1.}
    for a, b in pairs:
        new = {}
        for z, v in terms.items():
            for shift, coeff in ((0, .5), (a, .5), (b, .5), (a^b, -.5)):
                new[z^shift] = new.get(z^shift, 0.) + coeff*v
        terms = {key: value for key, value in new.items() if value != 0}
    return sum(v*table[z] for z, v in terms.items())


def local_direct_score(tau: np.ndarray, y: int, pairs):
    tau = np.asarray(tau, dtype=float); n = (len(tau)-1).bit_length()
    return float(fwht(tau*parity_phase(n, pairs))[y])


def uniform_tangent(n: int):
    t = np.ones(1 << n); t[0] = 0
    return t/np.linalg.norm(t)


def witness_variance(n: int, rank: int):
    m = 1 << n
    return 2*(m*m*(m-4)/2.**rank + 6*m-3)/(m-1)**2 - 2


def gadget_gate_count(n: int, pairs):
    return dict(cnot=2*sum(a.bit_count()+b.bit_count() for a,b in pairs),
                cz=len(pairs), clean_ancillas=2, all_to_all=True)


def simulate_gadget_basis(n: int, x: int, a: int, b: int):
    """Classical reversible gate simulation plus phase, explicit clean ancillas."""
    u=v=0
    for i in range(n):
        if (a >> i)&1: u ^= (x >> i)&1
        if (b >> i)&1: v ^= (x >> i)&1
    sign = -1 if u and v else 1
    for i in reversed(range(n)):
        if (b >> i)&1: v ^= (x >> i)&1
        if (a >> i)&1: u ^= (x >> i)&1
    return x,u,v,sign
