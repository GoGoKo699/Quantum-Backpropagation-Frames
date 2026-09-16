"""PF-07 interval-row reference compiler. Real full-angle Ry, big-endian sites.

Input is the CHARGED list of reversed local tangent tables, not a global matrix.
The emitted CNOT/Ry/X/H program prepares only the reference-zero branch. Suffixes
must be filled from right to left. No support union or global address list is
built; retained gate-program storage must still be counted by its consumer.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from numbers import Integral
import numpy as np


def real(value, ndim):
    raw = np.asarray(value)
    if raw.ndim != ndim or raw.dtype.kind not in 'iuf' or np.iscomplexobj(raw):
        raise ValueError('real numeric array of the requested dimension required')
    if not np.isfinite(raw).all():
        raise ValueError('finite values required')
    with np.errstate(over='raise', invalid='raise'):
        try: out = np.array(raw, dtype=np.float64, copy=True)
        except (FloatingPointError, OverflowError) as exc: raise ValueError('float64 range') from exc
    if not np.isfinite(out).all(): raise ValueError('float64 range')
    return out


def integer(value, low=0):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral) or value < low:
        raise ValueError('integer outside domain')
    return int(value)


def fwht(v):
    v = real(v, 1); N = len(v)
    if not N or N & (N-1): raise ValueError('power-of-two length required')
    with np.errstate(over='raise', invalid='raise'):
        h = 1
        while h < N:
            arr = v.reshape(-1,2*h); a=arr[:,:h].copy(); b=arr[:,h:].copy()
            arr[:,:h]=a+b; arr[:,h:]=a-b; h*=2
    return v


def ucr(controls, target, angles):
    """Complete cyclic-Gray UCR; controls indexed LSB-first in angle table.

The transform uses O(k*2^k) arithmetic, NOT an O(4^k) explicit Walsh matrix.
Every inactive-control identity is retained; no unknown response is disturbed.
"""
    controls=tuple(controls); target=integer(target)
    if any(integer(p)!=p for p in controls) or len(set(controls+(target,)))!=len(controls)+1:
        raise ValueError('distinct nonnegative sites required')
    theta=real(angles,1); m=1<<len(controls)
    if len(theta)!=m: raise ValueError('angle count')
    if not controls:
        yield ('ry',target,float(theta[0])); return
    coeff=fwht(theta)/m
    for j in range(m):
        g=j^(j>>1); nxt=((j+1)%m)^(((j+1)%m)>>1)
        yield ('ry',target,float(coeff[g]))
        bit=(g^nxt).bit_length()-1
        yield ('cx',controls[bit],target)


def exchange(p,q,theta):
    yield ('cx',p,q)
    yield from ucr((q,0),p,(0.,-theta,0.,0.))
    yield ('cx',p,q)


@dataclass
class IntervalReference:
    n: int
    starts: tuple
    ends: tuple
    tables: tuple
    groups: tuple
    ends_by_first: tuple
    first_mass: np.ndarray
    s: float

    @property
    def P(self): return len(self.tables)
    @property
    def width(self): return max(r-l for l,r in zip(self.starts,self.ends))
    @property
    def entries(self): return sum(t.size for t in self.tables)
    @property
    def incidence(self): return max(map(len,self.groups))

    @classmethod
    def from_tables(cls,n,intervals,tables):
        n=integer(n,1); intervals=list(intervals); tables=list(tables)
        if not intervals or len(intervals)!=len(tables): raise ValueError('input lengths')
        starts=[];ends=[];taus=[];groups=[[] for _ in range(n)];mu=np.zeros(n);R=list(range(1,n+1))
        for j,(interval,values) in enumerate(zip(intervals,tables)):
            sites=tuple(integer(i) for i in interval)
            if not sites or sites!=tuple(range(sites[0],sites[-1]+1)) or sites[-1]>=n:
                raise ValueError('a nonempty contiguous interval in the register is required')
            l,r=sites[0],sites[-1]+1; t=real(values,1)
            if len(t)!=(1<<(r-l)) or t[0]!=0.:
                raise ValueError('local table length and exact zero reference entry required')
            with np.errstate(over='raise',invalid='raise'):
                try: square=t*t
                except FloatingPointError as exc: raise ValueError('squared-amplitude range') from exc
            if np.any((t!=0)&(square==0)): raise ValueError('squared amplitude underflow; no silent truncation')
            starts.append(l);ends.append(r);taus.append(t)
            for a in range(l,r):
                count=1<<(r-a-1)
                groups[a].append((j,count));R[a]=max(R[a],r)
                mu[a]+=float(square[count:2*count].sum())
        s=float(mu.sum())
        if not math.isfinite(s) or s<=0: raise ValueError('positive finite total tangent mass required')
        if np.any((mu>0)&(mu/s==0)): raise ValueError('first-marker probability underflow')
        return cls(n,tuple(starts),tuple(ends),tuple(taus),tuple(tuple(g) for g in groups),tuple(R),mu,s)

    def suffix_mass(self,a):
        """One bounded temporary array; each local amplitude has ONE first site."""
        a=integer(a)
        if a>=self.n: raise ValueError('first site')
        out=np.zeros(1<<(self.ends_by_first[a]-a-1))
        for j,count in self.groups[a]:
            stride=1<<(self.ends_by_first[a]-self.ends[j])
            v=self.tables[j][count:2*count]
            out[::stride]+=v*v
        return out

    def marker_gates(self):
        yield ('x',0);yield ('cx',0,1);yield ('x',0)
        tails=np.cumsum(self.first_mass[::-1])[::-1]
        for a in range(self.n-1):
            angle=math.atan2(math.sqrt(float(tails[a+1])), math.sqrt(float(self.first_mass[a])))
            yield from exchange(a+1,a+2,angle)

    def fill_gates(self,a):
        """Known suffix state on a+1..R_a-1, conditioned on marker=1 AND ref=0."""
        if self.first_mass[a]==0: return
        h=self.suffix_mass(a); ell=self.ends_by_first[a]-a-1
        for j in range(ell):
            weights=h.reshape(1<<j,2,-1).sum(axis=2)
            angles=np.arctan2(np.sqrt(weights[:,1]),np.sqrt(weights[:,0]))
            # Previous suffix bits reversed make their usual binary index LSB-first.
            controls=tuple(range(a+j+1,a+1,-1))+(a+1,0)
            theta=np.zeros(1<<(j+2));theta[1<<j:2<<j]=angles
            yield from ucr(controls,a+j+2,theta)

    def preparation_gates(self,descending=True):
        yield from self.marker_gates()
        order=range(self.n-1,-1,-1) if descending else range(self.n)
        for a in order: yield from self.fill_gates(a)

    def gates(self):
        yield from self.preparation_gates();yield ('h',0)

    def ledger(self):
        A=[a for a in range(self.n) if self.first_mass[a]>0]
        suffix=sum((1<<(self.ends_by_first[a]-a+1))-4 for a in A)
        return {'n':self.n,'P':self.P,'w':self.width,'s':self.s,
                'local_tangent_entries':self.entries,'interval_incidence_records':sum(map(len,self.groups)),
                'max_intervals_per_site':self.incidence,'active_first_sites':len(A),
                'largest_suffix_buffer':max(1<<(self.ends_by_first[a]-a-1) for a in A),
                'cnot':6*self.n-5+suffix,'ry':4*(self.n-1)+suffix,'x':2,'h':1,
                'extra_work_qubits':0,'physical_measurement_bits':self.n+1,
                'global_support_union_materialized':False,
                'local_amplitudes_accumulated_per_mass_pass':sum(len(t)-1 for t in self.tables),
                'word_model_stream_bound':self.n+self.incidence*self.width,
                'full_program_memory':'linear in emitted gate count if retained; emitted storage is not free'}

    def row(self,bits):
        """Read n physical bits; inspect only intervals containing the first one."""
        if not isinstance(bits,str) or len(bits)!=self.n or any(b not in '01' for b in bits):
            raise ValueError('binary physical outcome string of length n required')
        a=bits.find('1')
        if a<0: return (),np.empty(0),0.
        z=bits.rfind('1')
        if z>=self.ends_by_first[a]: return (),np.empty(0),0.
        ids=[];values=[]
        for j,_ in self.groups[a]:
            if z<self.ends[j]:
                val=self.tables[j][int(bits[self.starts[j]:self.ends[j]],2)]
                if val!=0: ids.append(j);values.append(float(val))
        v=np.array(values);norm=math.hypot(*v)
        return tuple(ids),v,norm

    def score(self,b,bits):
        b=integer(b)
        if b>1: raise ValueError('reference bit')
        ids,v,norm=self.row(bits)
        return ids,(2*(-1)**b*math.sqrt(self.s))*(v/norm) if norm else v

    def add_record(self,accumulator,b,bits):
        """Sparse original-coordinate updates; no per-shot P-vector is constructed."""
        if not isinstance(accumulator,np.ndarray) or accumulator.shape!=(self.P,) or accumulator.dtype.kind!='f':
            raise ValueError('floating P-vector accumulator required')
        ids,v=self.score(b,bits)
        if ids: accumulator[np.asarray(ids,dtype=int)]+=v
        return len(ids)
