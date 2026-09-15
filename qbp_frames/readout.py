"""Exact terminal CZ compilers; output relabeling is part of the contract.

No globally optimal synthesis claim. The two constructed alternatives are a
quadratic-form pivot elimination and a greedy CNOT congruence reduction.
They implement L*D_f up to a known Z character. An X-outcome is relabeled by
L.T and that character. These plans are NOT coherent D_f substitutions.
All-to-all CNOT/CZ primitives; bit 0 is the least significant address bit.
"""
from __future__ import annotations
from dataclasses import dataclass
from .parity import _integer


def edge_list(n):
    return [(i,j) for i in range(n) for j in range(i+1,n)]


def _inputs(n, mask):
    n, mask = _integer(n, 'n', 1), _integer(mask, 'mask')
    if mask >= 1 << (n*(n-1)//2):
        raise ValueError('Quadratic mask outside register')
    return n, mask


def _rows(n, mask):
    rows = [0]*n
    for k,(i,j) in enumerate(edge_list(n)):
        if (mask >> k)&1:
            rows[i] ^= 1 << j
            rows[j] ^= 1 << i
    return rows


def _edges(rows):
    return [(i,j) for i,row in enumerate(rows) for j in range(i+1,len(rows))
            if (row >> j)&1]


def _transpose(value, gates):
    for c,t in reversed(gates):
        if (value >> t)&1:
            value ^= 1 << c
    return value


@dataclass(frozen=True)
class Plan:
    n: int
    method: str
    cnots: tuple
    czs: tuple
    offset: int
    synthesis_word_ops: int

    def address(self, x):
        x = _integer(x, 'address')
        if x >= 1 << self.n:
            raise ValueError('Address outside register')
        for c,t in self.cnots:
            if (x >> c)&1:
                x ^= 1 << t
        return x

    def outcome(self, y):
        y = _integer(y, 'outcome')
        if y >= 1 << self.n:
            raise ValueError('Outcome outside register')
        return _transpose(y, self.cnots) ^ self.offset

    def phase(self, x):
        y = self.address(x)
        return -1 if sum(((y >> i)&1)*((y >> j)&1) for i,j in self.czs)&1 else 1

    def ledger(self):
        return {'cnot':len(self.cnots), 'cz':len(self.czs), 'work_qubits':0,
                'extra_measurements':0, 'resets':0,
                'synthesis_word_ops':self.synthesis_word_ops,
                'relabel_word_ops':len(self.cnots)+1,
                'mask_storage_bits':self.n*(self.n-1)//2,
                'terminal_only':True}


def direct(n, mask):
    n, mask = _inputs(n, mask)
    rows = _rows(n, mask)
    return Plan(n, 'direct', (), tuple(_edges(rows)), 0, n*(n-1)//2)


def pivot(n, mask):
    n, mask = _inputs(n, mask)
    rows = _rows(n, mask)
    active = set(range(n)); gates=[]; pairs=[]; linear=0
    ops=n*(n-1)//2
    while True:
        ee=[(i,j) for i in active for j in active if i<j and (rows[i]>>j)&1]
        ops += len(active)**2
        if not ee:
            break
        i,j=min(ee,key=lambda ij:(rows[ij[0]].bit_count()+rows[ij[1]].bit_count(),ij))
        rest=active-{i,j}
        aa=[v for v in sorted(rest) if (rows[i]>>v)&1]
        bb=[v for v in sorted(rest) if (rows[j]>>v)&1]
        gates.extend((v,i) for v in bb)
        gates.extend((v,j) for v in aa)
        pairs.append((i,j))
        # f = y_i*y_j + f_rest + (sum aa x)*(sum bb x).
        for a in aa:
            for b in bb:
                if a==b:
                    linear ^= 1<<a
                else:
                    rows[a] ^= 1<<b; rows[b] ^= 1<<a
                ops += 3
        for v in rest:
            rows[v] &= ~((1<<i)|(1<<j))
        rows[i]=rows[j]=0
        active=rest
        ops += n + len(aa)+len(bb)
    return Plan(n, 'pivot', tuple(gates), tuple(pairs), linear, ops)


def greedy(n, mask):
    n, mask = _inputs(n, mask)
    rows = _rows(n, mask); gates=[]; linear=0
    ops=n*(n-1)//2
    while True:
        best=None
        for c in range(n):
            for t in range(n):
                if c==t:
                    continue
                keep=((1<<n)-1)^((1<<c)|(1<<t))
                drop=(rows[c]&keep).bit_count()-((rows[c]^rows[t])&keep).bit_count()
                ops += 7
                if drop>1 and (best is None or drop>best[0]):
                    best=(drop,c,t)
        if best is None:
            break
        _,c,t=best
        # Substitute old x_t = new x_t + new x_c in the phase polynomial.
        if ((linear>>t)&1) ^ ((rows[c]>>t)&1):
            linear ^= 1<<c
        change=rows[t]&~((1<<c)|(1<<t))
        rows[c] ^= change
        for j in range(n):
            if (change>>j)&1:
                rows[j] ^= 1<<c
        gates.append((c,t)); ops += 2*n+5
    return Plan(n,'greedy',tuple(gates),tuple(_edges(rows)),
                _transpose(linear,gates),ops)


def portfolio(n, mask):
    """Return alternatives, not an assertion of globally optimal synthesis."""
    return (direct(n,mask), pivot(n,mask), greedy(n,mask))


def quadratic_character(n, mask, y):
    """All signed characters by Gray traversal, O(2^n+n^2) word kernels.

Used only on local blocks by the streaming decoder. It avoids evaluating a
quadratic polynomial separately at every local basis address.
    """
    import numpy as np
    n, mask = _inputs(n, mask)
    y = _integer(y, 'outcome')
    if y >= 1 << n:
        raise ValueError('Outcome outside register')
    rows = _rows(n, mask)
    out = np.empty(1 << n, dtype=np.int8)
    x=0; sign=1; out[0]=1
    for step in range(1,1 << n):
        bit=(step & -step).bit_length()-1
        flip=((rows[bit]&x).bit_count()&1)^((y>>bit)&1)
        if flip:
            sign=-sign
        x ^= 1 << bit
        out[x]=sign
    return out
