"""PF-06: elementary-gate sparse readout for ONE disjoint six-rotation layer.

Real logical circuits, big-endian sites, full-angle R(theta)=exp(-i theta Y).
No quantum tangent SVD, dense global frame, or compressed quantum address is used.
Only the small diagnostic simulator materializes global amplitudes.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np

WORDS = ((2,0),(0,2),(2,1),(1,2),(2,3),(3,2))
PAULI = (np.eye(2, dtype=complex), np.array([[0,1],[1,0]], complex),
         np.array([[0,-1j],[1j,0]], complex), np.diag([1.,-1.]).astype(complex))


def real_array(value, shape=None):
    raw = np.asarray(value)
    if raw.dtype.kind not in 'iuf' or np.iscomplexobj(raw) or not np.isfinite(raw).all():
        raise ValueError('finite real numeric input required')
    if shape is not None and raw.shape != shape:
        raise ValueError(f'expected shape {shape}')
    out = raw.astype(float)
    if not np.isfinite(out).all():
        raise ValueError('outside float64 range')
    return out


def block_tangents(angles):
    """4-by-6 reversed tangents; six constant-size prefix computations."""
    angles = real_array(angles, (6,))
    prefix = np.eye(4); cols = []
    for word, theta in zip(WORDS, angles):
        Qc = -1j * np.kron(PAULI[word[0]], PAULI[word[1]])
        if np.max(abs(Qc.imag)) > 1e-14:
            raise AssertionError('generator is not real antisymmetric')
        Q = Qc.real
        cols.append(prefix.T @ Q @ prefix[:,0])
        prefix = (math.cos(theta)*np.eye(4) + math.sin(theta)*Q) @ prefix
    T = np.column_stack(cols)
    if np.max(abs(T[0])) > 1e-10 or np.max(abs(np.sum(T*T, axis=0)-1)) > 1e-10:
        raise ArithmeticError('block tangent contract failed')
    return T, prefix


def uc_rotation(controls, target, angles):
    """Gray-code UCR, exact logical decomposition; angle index uses controls LSB-first.

For 2 controls: 4 CNOTs and 4 full-angle R_y gates. No omitted diagonal gates.
"""
    controls = tuple(controls); m = 1 << len(controls)
    angles = real_array(angles, (m,))
    if len(set(controls + (target,))) != len(controls)+1:
        raise ValueError('distinct target and controls required')
    if not controls:
        return [('ry', target, float(angles[0]))]
    gray = [j ^ (j >> 1) for j in range(m)]
    coeff = [sum((-1)**((g & b).bit_count() & 1)*angles[b] for b in range(m))/m
             for g in gray]
    gates = []
    for j, alpha in enumerate(coeff):
        gates.append(('ry', target, float(alpha)))
        change = gray[j] ^ gray[(j+1) % m]
        gates.append(('cx', controls[change.bit_length()-1], target))
    return gates


def exchange_on_reference_zero(p, q, theta, ref=0):
    """Mix 10 -> cos(theta)10 + sin(theta)01 on p,q, only when ref=0."""
    return ([('cx', p, q)] + uc_rotation((q, ref), p, (0., -theta, 0., 0.))
            + [('cx', p, q)])


@dataclass
class Plan:
    angles: np.ndarray             # shape (blocks,6); output order is slot-major
    K: np.ndarray                  # blocks,3,6; active computational row queries
    row_energy: np.ndarray         # blocks,3
    s: float
    gates: list

    @property
    def blocks(self): return len(self.K)
    @property
    def n(self): return 2*self.blocks
    @property
    def P(self): return 6*self.blocks
    @property
    def r(self): return 3*self.blocks

    def counts(self):
        return {kind: sum(g[0] == kind for g in self.gates) for kind in ('cx','ry','x','h')}

    def classify(self, system_outcome):
        """Scan ALL physical bits; returns (block,type) or None. O(n) bit work."""
        if isinstance(system_outcome, bool) or not isinstance(system_outcome, (int,np.integer)):
            raise ValueError('integer outcome required')
        x = int(system_outcome)
        if not 0 <= x < 1 << self.n:
            raise ValueError('outcome outside register')
        # Convert once: repeated shifts of a growing arbitrary-size integer
        # would not implement the stated linear physical-bit scan in Python.
        bits = format(x, f'0{self.n}b')
        active = None
        for b in range(self.blocks):
            digit = 2*(bits[2*b] == '1') + (bits[2*b+1] == '1')
            if digit:
                if active is not None: return None
                active = (b, digit-1)
        if active is not None and self.row_energy[active] == 0:
            return None
        return active

    def finish(self, signed_counts, shots):
        """One final sparse output map; no P-vector is constructed per record."""
        counts = real_array(signed_counts, (self.blocks,3))
        if isinstance(shots, bool) or not isinstance(shots, (int,np.integer)) or shots < 1:
            raise ValueError('positive integer shots required')
        coef = np.zeros_like(counts)
        np.divide(2*math.sqrt(self.s)*counts, np.sqrt(self.row_energy),
                  out=coef, where=self.row_energy > 0)
        return (np.einsum('bt,btj->bj',coef,self.K)/shots).T.reshape(-1)

    def exact_risk_bound(self):
        """Logical full-rank one-layer bound; eigenvalues are computed numerically."""
        eigenvalues = np.concatenate([np.linalg.eigvalsh(k @ k.T) for k in self.K])
        return max(2*self.s, 4*self.s - 4*max(0., float(eigenvalues.min())))


def compile_plan(angles):
    angles = real_array(angles)
    if angles.ndim != 2 or angles.shape[0] < 1 or angles.shape[1] != 6:
        raise ValueError('one disjoint layer needs angles with shape (blocks,6)')
    B = len(angles)
    K = np.array([block_tangents(row)[0][1:] for row in angles])
    d = np.sum(K*K, axis=2); mass = d.sum(axis=1); s = float(mass.sum())
    if not math.isfinite(s) or s <= 0:
        raise ValueError('nonzero finite tangent mass required')
    # Reference qubit is physical site 0; the right qubit of block b is 2+2*b.
    gates = [('x',0), ('cx',0,2), ('x',0)]
    tail = np.cumsum(mass[::-1])[::-1]
    for b in range(B-1):
        theta = math.atan2(math.sqrt(float(tail[b+1])), math.sqrt(float(mass[b])))
        gates += exchange_on_reference_zero(2+2*b, 4+2*b, theta)
    # On the reference branch only, split block marker 01 into types 01,10,11.
    for b in range(B):
        left, right = 1+2*b, 2+2*b
        d1,d2,d3 = map(float,d[b])
        theta1 = math.atan2(math.sqrt(d2+d3), math.sqrt(d1))
        theta2 = -math.atan2(math.sqrt(d2), math.sqrt(d3)) if d2+d3 > 0 else 0.
        gates += uc_rotation((right,0),left,(0.,theta1,0.,0.))
        gates += uc_rotation((left,0),right,(0.,theta2,0.,0.))
    gates.append(('h',0))
    return Plan(angles.copy(),K,d,s,gates)


def apply_gate(vector, gate, qubits):
    """Small statevector diagnostic; big-endian physical site numbering."""
    v = np.asarray(vector).copy(); kind = gate[0]
    if v.shape != (1 << qubits,): raise ValueError('state size')
    if kind == 'cx':
        c,t = gate[1:]; idx = np.arange(len(v)); sel = ((idx >> (qubits-1-c)) & 1).astype(bool)
        dest = idx.copy(); dest[sel] ^= 1 << (qubits-1-t); out = np.empty_like(v); out[dest] = v
        return out
    target = gate[1]; mask = 1 << (qubits-1-target)
    idx = np.arange(len(v)); lo = idx[(idx & mask)==0]; hi = lo ^ mask
    a,b = v[lo].copy(),v[hi].copy()
    if kind == 'x': v[lo],v[hi] = b,a
    elif kind == 'h': v[lo],v[hi] = (a+b)/math.sqrt(2),(a-b)/math.sqrt(2)
    elif kind == 'ry':
        c,s = math.cos(gate[2]),math.sin(gate[2]); v[lo],v[hi] = c*a-s*b,s*a+c*b
    else: raise ValueError('unsupported gate')
    return v


def apply_circuit(vector, gates, qubits):
    for g in gates: vector = apply_gate(vector,g,qubits)
    return vector


def active_addresses(plan):
    return [digit << (plan.n-2-2*b) for b in range(plan.blocks) for digit in (1,2,3)]


def dense_tangents(plan):
    """Diagnostics only, never used in scalable compilation or decoding."""
    T = np.zeros((1 << plan.n, plan.P))
    for b in range(plan.blocks):
        for t in range(3):
            T[(t+1) << (plan.n-2-2*b), np.arange(6)*plan.blocks+b] = plan.K[b,t]
    return T


def dense_scores(plan):
    """Reference probability test only: all 2^(n+1) physical outcomes."""
    Z = np.zeros((2 << plan.n, plan.P))
    for b in range(plan.blocks):
        for t in range(3):
            if plan.row_energy[b,t] == 0: continue
            x = (t+1) << (plan.n-2-2*b)
            v = 2*math.sqrt(plan.s/plan.row_energy[b,t])*plan.K[b,t]
            ids = np.arange(6)*plan.blocks+b
            Z[x,ids] = v; Z[(1 << plan.n)+x,ids] = -v
    return Z


def reference_vector(plan):
    c = np.zeros(1 << plan.n)
    for x,d in zip(active_addresses(plan),plan.row_energy.ravel()): c[x] = math.sqrt(d/plan.s)
    return c


def risk_from_coordinates(plan, q):
    coords = real_array(q)[active_addresses(plan)]
    g = 2*np.einsum('bt,btj->bj',coords.reshape(plan.blocks,3),plan.K).T.reshape(-1)
    mass = float(coords[plan.row_energy.ravel() > 0] @ coords[plan.row_energy.ravel() > 0])
    return 2*plan.s*(1+mass) - float(g@g)
