"""Local source-table construction for the existing staggered line family.

Migrated from results/PF-04/study.py; no additional circuit family is introduced.
"""
from __future__ import annotations
import heapq
import math
import numpy as np
from .disjoint import WORDS
from .parity import _integer, _real


def parameter_count(n, depth):
    """Count full-angle coordinates in layer, generator, left-site order."""
    n = _integer(n, 'n', 2)
    depth = _integer(depth, 'depth', 1)
    return 6 * sum(len(range(layer % 2, n-1, 2)) for layer in range(depth))


def _structure(n, depth, angles):
    """Same six-generator, big-endian physical circuit family as the fixture."""
    n = _integer(n, 'n', 2)
    depth = _integer(depth, 'depth', 1)
    specs=[]
    for layer in range(depth):
        for word in WORDS:
            for left in range(layer%2,n-1,2):
                specs.append(((left,left+1),word))
    angles = _real(angles, 'angles', 1)
    if len(angles)!=len(specs): raise ValueError('angle count')
    previous=[-1]*n; predecessors=[]; supports=[]
    for j,(sites,word) in enumerate(specs):
        active=tuple(site for site,p in zip(sites,word) if p)
        supports.append(active)
        predecessors.append(tuple(previous[site] for site in active if previous[site]>=0))
        for site in active: previous[site]=j
    return specs,np.asarray(angles),supports,predecessors


def _kernel(vector, sites, word, interval):
    """Apply -i times a Pauli word with exactly one Y, using real arithmetic."""
    width=len(interval); flip=0; phase=0
    for site,p in zip(sites,word):
        if not p: continue
        b=1 << (width-1-interval.index(site))
        if p in (1,2): flip |= b
        if p in (2,3): phase |= b
    idx=np.arange(len(vector)); weights=np.fromiter((1-2*((int(x)&phase).bit_count()&1) for x in idx),float,len(idx))
    result=np.empty_like(vector); result[idx^flip]=weights*vector
    return result


def compile_local(n, depth, angles):
    """Existing staggered six-generator circuit; supply explicit full angles.

    Returns interval tables and charged visits/kernel work. This does not
    allocate a global state, but each table is exponential in interval width.
    """
    specs,angles,supports,pred=_structure(n,depth,angles)
    intervals=[]; taus=[]; visits=0; work=0
    for j,(target_sites,target_word) in enumerate(specs):
        frontier=[-x for x in pred[j]]; heapq.heapify(frontier)
        chosen=set(); active=set(supports[j])
        while frontier:
            k=-heapq.heappop(frontier)
            if k in chosen: continue
            chosen.add(k); active.update(supports[k])
            for p in pred[k]:
                if p not in chosen: heapq.heappush(frontier,-p)
        interval=tuple(range(min(active),max(active)+1)); order=sorted(chosen)
        v=np.zeros(1<<len(interval));v[0]=1
        for k in order:
            sites,word=specs[k]; theta=angles[k]
            v=math.cos(theta)*v+math.sin(theta)*_kernel(v,sites,word,interval)
        v=_kernel(v,target_sites,target_word,interval)
        for k in reversed(order):
            sites,word=specs[k];theta=angles[k]
            v=math.cos(theta)*v-math.sin(theta)*_kernel(v,sites,word,interval)
        intervals.append(interval);taus.append(v)
        visits+=len(order);work+=(2*len(order)+1)*len(v)
    return dict(n=n,depth=depth,angles=angles,intervals=intervals,taus=taus,
                visits=visits,amplitude_kernel_entries=work)


def reference_plan(local):
    """Build an interval readout from this compiler's analytically zero entries.

    The local construction has tau_j[0]=0 analytically. Check the residual before
    zeroing that entry; return its maximum so the correction remains visible.
    This helper is for compile_local output, not arbitrary interval tables.
    """
    from .intervals import IntervalReference
    taus = [_real(t, 'local tangent', 1) for t in local['taus']]
    residual = max(abs(t[0]) for t in taus)
    if residual > 1e-10:
        raise ValueError('reference-orthogonality residual exceeds 1e-10')
    for t in taus:
        t[0] = 0.
    return IntervalReference.from_tables(local['n'], local['intervals'], taus), float(residual)
