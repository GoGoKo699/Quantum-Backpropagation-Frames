"""Matched ideal-model gradient readout comparison.
Full-angle Pauli rotations, big-endian qubit indexing; no hardware model.
"""
from __future__ import annotations
import itertools, math
from dataclasses import dataclass
from functools import lru_cache
import numpy as np
from numpy.typing import NDArray

PAULI = [np.eye(2,dtype=complex), np.array([[0,1],[1,0]],complex),
         np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.]).astype(complex)]
WORDS = [(2,0),(0,2),(2,1),(1,2),(2,3),(3,2)]

def fwht(a):
    out=np.array(a,copy=True)
    n=out.shape[-1]
    if n<1 or n&(n-1): raise ValueError('last dimension must be power of two')
    h=1
    while h<n:
        v=out.reshape(*out.shape[:-1],-1,2,h)
        l=v[...,0,:].copy(); r=v[...,1,:].copy()
        v[...,0,:]=l+r; v[...,1,:]=l-r
        h*=2
    return out

def kron_all(ops):
    out=np.array([[1.]],complex)
    for a in ops: out=np.kron(out,a)
    return out

def local_embed(a,sites,n):
    sites=tuple(sites)
    others=tuple(i for i in range(n) if i not in sites)
    order=sites+others
    b=np.kron(a,np.eye(2**len(others)))
    perm=np.argsort(order)
    return b.reshape([2]*(2*n)).transpose(tuple(perm)+tuple(perm+n)).reshape(2**n,2**n)

@dataclass
class Circuit:
    n:int
    depth:int
    angles:NDArray
    U:NDArray
    T:NDArray
    B:list
    cones:list
    taus:list
    groups:list
    group_cnot:list
    generators:list
    gates:list
    total_cnot:int


def make_circuit(n,depth,rng,angles=None):
    # Each disjoint physical block has the same six generator positions.
    # Schedule each generator position across the disjoint blocks before moving on.
    specs=[]; groups=[]; measure_charges=[]
    for layer in range(depth):
        pairs=[(k,k+1) for k in range(layer%2,n-1,2)]
        layer_groups=[]
        for word in WORDS:
            ids=[]
            for pair in pairs:
                ids.append(len(specs)); specs.append((pair,word))
            if ids: layer_groups.append(ids)
        # Consecutive pairs of generator types commute. Jointly measure them.
        # (YI,IY): product Y basis; (YX,XY) and (YZ,ZY): one-CNOT Bell basis.
        for k in range(0,len(layer_groups),2):
            groups.append(layer_groups[k]+layer_groups[k+1])
            measure_charges.append(0 if k==0 else len(pairs))
    P=len(specs); N=2**n
    if angles is None: angles=rng.uniform(-.7,.7,P)
    angles=np.array(angles,float)
    if angles.shape!=(P,):raise ValueError('angle count')
    prefix=np.eye(N,dtype=complex)
    Bs=[];ts=[];cones=[];taus=[];As=[];gates=[];charges=[]
    for j,((pair,word),theta) in enumerate(zip(specs,angles)):
        Alocal=np.kron(PAULI[word[0]],PAULI[word[1]])
        A=local_embed(Alocal,pair,n)
        B=prefix.conj().T@A@prefix
        t=(-1j*B[:,0]).real
        # Backward light cone, using actual nonidentity supports, not padded block.
        support=set(pair[k] for k in range(2) if word[k])
        for prevpair,prevword in reversed(specs[:j]):
            prev=set(prevpair[k] for k in range(2) if prevword[k])
            if support&prev: support |= prev
        # Use interval hull for partitions/histograms.
        sites=tuple(range(min(support),max(support)+1))
        idx=[]
        for x in range(2**len(sites)):
            full=sum(((x>>(len(sites)-1-a))&1)<<(n-1-site) for a,site in enumerate(sites))
            idx.append(full)
        tau=t[idx]
        assert abs(np.linalg.norm(tau)-1)<1e-10
        Uj=np.cos(theta)*np.eye(N)-1j*np.sin(theta)*A
        Bs.append(B);ts.append(t);cones.append(sites);taus.append(tau)
        As.append(A);gates.append(Uj);charges.append(2 if sum(p!=0 for p in word)==2 else 0)
        prefix=Uj@prefix
    total=sum(charges)
    groupcost=[]
    for group,measurement_cnot in zip(groups,measure_charges):
        end=max(group)
        suffix=sum(charges[end+1:])
        groupcost.append(total+suffix+measurement_cnot)
    return Circuit(n,depth,angles,prefix.real,np.array(ts).T,Bs,cones,taus,
                   groups,groupcost,As,gates,total)

def indices_on(sites,n):
    return np.array([sum(((x>>(n-1-k))&1)<<(len(sites)-1-i)
                         for i,k in enumerate(sites)) for x in range(2**n)])

def reduced(rho,sites,n):
    rest=tuple(i for i in range(n) if i not in sites)
    order=tuple(sites)+rest
    a=rho.reshape([2]*(2*n)).transpose(order+tuple(i+n for i in order))
    a=a.reshape(2**len(sites),2**len(rest),2**len(sites),2**len(rest))
    return np.einsum('arbr->ab',a)

def partitions(n,w):
    # two staggered partitions of lengths <=2w, using infinite-grid boundaries
    parts=[]
    for offset in (0,w):
        blocks=[]
        start=offset
        while start>0: start-=2*w
        while start<n:
            lo=max(0,start); hi=min(n,start+2*w)
            if hi>lo:blocks.append(tuple(range(lo,hi)))
            start+=2*w
        parts.append(blocks)
    return parts


def walsh_moments(c,q):
    N=2**c.n; f=fwht(c.T.T)
    fq=fwht(q)
    p=np.stack([np.abs(1+fq)**2,np.abs(1-fq)**2])/(4*N)
    z=np.stack([2*f,-2*f]) # 2,P,N
    mean=np.einsum('by,bjy->j',p,z)
    second=np.einsum('by,bjy->j',p,z*z)
    g=2*c.T.T@q.real
    assert np.max(abs(mean-g))<1e-10
    return dict(mean=mean,second=second,variance=second-g*g,
                A=float(np.sum(second-g*g)),f=f,p=p,
                second_bound=float(2*len(g)+2*np.max(np.sum(f*f,axis=0))))


def block_moments(c,q,parts=None):
    P=c.T.shape[1]; n=c.n
    w=max(map(len,c.cones))
    if parts is None: parts=partitions(n,w)
    rho=np.outer(q,q.conj()); g=2*c.T.T@q.real
    second=np.zeros(P); covers=[]; operators={}
    for j,sites in enumerate(c.cones):
        covered=[]
        for s,blocks in enumerate(parts):
            for ib,Q in enumerate(blocks):
                if set(sites)<=set(Q):covered.append((s,ib,Q));break
        pj=len(covered)/len(parts)
        assert pj>0
        for s,ib,Q in covered:
            m=2**len(Q); tau=np.zeros(m)
            pos=[Q.index(k) for k in sites]
            for x,val in enumerate(c.taus[j]):
                y=sum(((x>>(len(sites)-1-a))&1)<<(len(Q)-1-b) for a,b in enumerate(pos))
                tau[y]=val
            rq=reduced(rho,Q,n)
            v=float(rq[0,0].real+(tau@rq@tau).real)
            alpha=(m+1)/(m+2)
            second[j] += (4/pj**2)/len(parts)*alpha*(3+v)
            operators[s,ib,j]=tau
        covers.append(covered)
    return dict(A=float(np.sum(second-g*g)),second=second,variance=second-g*g,
                partitions=parts,covers=covers,operators=operators,
                second_bound=float(sum(16/ (len(x)/len(parts)) for x in covers)))


@lru_cache(None)
def pauli_ensemble(n):
    if n>5:raise ValueError('Exact Pauli ensemble intentionally limited to five qubits')
    eig=[];sh=[]
    for a in PAULI[1:]:
        _,v=np.linalg.eigh(a)
        for k in range(2):
            s=v[:,k];r=np.outer(s,s.conj())
            eig.append(s);sh.append(3*r-np.eye(2))
    ss=np.array([[1]],complex); ssnap=np.array([[[1]]],complex)
    for _ in range(n):
        ss=np.array([np.kron(v,u) for v in ss for u in eig])
        ssnap=np.array([np.kron(v,u) for v in ssnap for u in sh])
    return ss,ssnap


def pauli_moments(c,q):
    states,snaps=pauli_ensemble(c.n); n=c.n; g=2*c.T.T@q.real
    score=np.einsum('jab,kba->kj',np.array(c.B),snaps,optimize=True).real
    # ancilla Y=s: unnormalized system vector (|0> - i*s*q)/2.
    zero=np.zeros(len(q));zero[0]=1
    vectors=np.stack([zero-1j*q,zero+1j*q])/2
    probs=np.abs(states.conj()@vectors.T)**2/(3**n)
    mean=np.sum(probs[:,0,None]*(-2*score)+probs[:,1,None]*(2*score),axis=0)
    second=np.sum((probs[:,0]+probs[:,1])[:,None]*4*score**2,axis=0)
    assert abs(probs.sum()-1)<1e-10
    assert np.max(abs(mean-g))<1e-9
    return dict(A=float(np.sum(second-g*g)),mean=mean,second=second,variance=second-g*g)


def grouped_moments(c,q):
    g=2*c.T.T@q.real
    a=np.array([np.sum(np.maximum(0.,4-g[ids]**2)) for ids in c.groups])
    return dict(group_variance=a,A=float(np.sum(np.sqrt(a))**2),
                group_cnot=np.array(c.group_cnot),groups=len(a))


def group_cost(c,q,objective_cost=0,arithmetic_weight=0):
    gm=grouped_moments(c,q)
    cost=objective_cost+gm['group_cnot']+arithmetic_weight*np.array([len(x) for x in c.groups])
    return float(np.sum(np.sqrt(gm['group_variance']*cost))**2)


def response_cases(c,rng):
    N=2**c.n
    v=rng.normal(size=N); v/=np.linalg.norm(v)
    # This response construction merely defines accessible reflection test instances.
    # It is not claimed classically hard.
    yield 'random_real',v
    f=fwht(c.T.T)
    # Largest-error response for all-X among real unit q: matrix-free spectral map,
    # expressed densely only in the tiny validation Hilbert space.
    H=fwht(np.eye(N))/np.sqrt(N)
    riskmat=2*(H*np.sum(f*f,axis=0)[None,:])@H-4*c.T@c.T.T
    _,vec=np.linalg.eigh((riskmat+riskmat.T)/2)
    yield 'walsh_worst_real',vec[:,-1]
    j=int(rng.integers(c.T.shape[1]));yield 'tangent',c.T[:,j]
    z=np.zeros(N);z[0]=1;yield 'zero_response',z


def make_reflection_for_response(c,q):
    if abs(q[0].imag)>1e-12:raise ValueError('reflection requires real reference overlap')
    e=np.zeros_like(q);e[0]=1
    if np.linalg.norm(e-q)<1e-12:R=np.eye(len(q))
    else:
        v=e-q;R=np.eye(len(q))-2*np.outer(v,v.conj())/np.vdot(v,v)
    return c.U@R@c.U.T

def walsh_second_bound_dp(cones,taus,n):
    """Exact max_y sum_j f_j(y_Ij)^2 via 1D interval dynamic programming.
    Returns an objective-independent bound on the total second moment.
    """
    w=max(map(len,cones));ending=[[] for _ in range(n)]
    for Q,tau in zip(cones,taus):
        if Q!=tuple(range(Q[0],Q[-1]+1)):raise ValueError('intervals required')
        ending[Q[-1]].append((len(Q),fwht(tau)**2))
    dp={0:0.}
    for bitpos in range(n):
        ndp={}
        for state,value in dp.items():
            for bit in (0,1):
                full=(state<<1)|bit
                add=sum(table[full&((1<<k)-1)] for k,table in ending[bitpos])
                nextstate=full&((1<<max(w-1,0))-1)
                nv=value+float(add)
                if nextstate not in ndp or nv>ndp[nextstate]:ndp[nextstate]=nv
        dp=ndp
    maximum=max(dp.values())
    return 2*len(taus)+2*maximum


def block_state_independent_bound(c):
    w=max(map(len,c.cones));parts=partitions(c.n,w);R=0.
    for I in c.cones:
        qs=[]
        for blocks in parts:
            for Q in blocks:
                if set(I)<=set(Q):qs.append(Q);break
        p=len(qs)/len(parts)
        R+=sum(16*(2**len(Q)+1)/(2**len(Q)+2) for Q in qs)/(len(parts)*p*p)
    return R
