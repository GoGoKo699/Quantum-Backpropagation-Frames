"""PF-01 independent finite diagnostics. Does not import either research packet.

Run: python results/PF-01/audit.py --output /path/to/new/diagnostics.json
Dense exhaustive tests deliberately stop at four system qubits.
"""
from __future__ import annotations
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import itertools as it
import json
import math
from pathlib import Path
import platform
import time
import numpy as np

SEED = 2026091561
ATOL = 2e-9
checks = {}

def check(group, residual=0.0, cases=1):
    r = abs(float(residual))
    if not math.isfinite(r) or r > ATOL:
        raise AssertionError((group, r))
    d = checks.setdefault(group, {'cases': 0, 'max_abs_residual': 0.0})
    d['cases'] += cases
    d['max_abs_residual'] = max(d['max_abs_residual'], r)

def bitdot(a, b):
    return (int(a) & int(b)).bit_count() % 2

@lru_cache(None)
def chars(n):
    N = 1 << n
    return np.array([[(-1.0)**bitdot(x,y) for x in range(N)] for y in range(N)])

def signs_from_key(n, key):
    return np.array([1.-2.*((key>>x)&1) for x in range(1<<n)])

def pair_key(n, a, b):
    return sum((bitdot(a,x)*bitdot(b,x))<<x for x in range(1<<n))

def full_keys(n):
    edges = list(it.combinations(range(n),2))
    for edge_bits in it.product((0,1), repeat=len(edges)):
        yield sum((sum(c*((x>>i)&1)*((x>>j)&1)
                       for c,(i,j) in zip(edge_bits,edges))%2)<<x for x in range(1<<n))

def direct(T, q, sign=None):
    """Born probabilities from the actual (n+1)-qubit state and Hadamards."""
    N,P=T.shape; n=N.bit_length()-1
    if sign is None: sign=np.ones(N)
    e=np.eye(N)[0]; H=chars(n)/np.sqrt(N)
    state=np.concatenate((e,sign*q))/np.sqrt(2)
    H2=np.kron(np.array([[1.,1.],[1.,-1.]])/np.sqrt(2),H)
    probabilities=abs(H2@state)**2
    F=chars(n)@(sign[:,None]*T)
    scores=np.concatenate((2*F,-2*F))
    mean=probabilities@scores
    second=scores.T@(probabilities[:,None]*scores)
    return mean,second-np.outer(mean,mean),probabilities,scores

def rank_binary(A):
    A=np.array(A,dtype=np.uint8,copy=True); r=0
    for j in range(A.shape[1]):
        candidates=np.flatnonzero(A[r:,j])
        if not len(candidates): continue
        p=r+int(candidates[0]);A[[r,p]]=A[[p,r]]
        for i in range(len(A)):
            if i!=r and A[i,j]: A[i]^=A[r]
        r+=1
        if r==len(A):break
    return r

def mask_matrix(n,key):
    A=np.zeros((n,n),dtype=int)
    for i,j in it.combinations(range(n),2):
        A[i,j]=A[j,i]=((key>>(1<<i))^(key>>(1<<j))^(key>>((1<<i)|(1<<j))))&1
    return A

def moment_audit(rng):
    for n in range(1,5):
        N=1<<n; T=rng.normal(size=(N,3));T[0]=0
        t=np.ones(N);t[0]=0;t/=np.linalg.norm(t)
        qs=[np.eye(N)[0],t,rng.normal(size=N)]
        qs[-1]/=np.linalg.norm(qs[-1])
        one=Counter(pair_key(n,a,b) for a in range(N) for b in range(N))
        distributions=[Counter({0:1})]
        for k in range(1,4):
            nxt=Counter()
            for f,c in distributions[-1].items():
                for h,m in one.items(): nxt[f^h]+=c*m
            distributions.append(nxt)
        allkeys=list(full_keys(n))
        for q in qs:
            means={}; covs={}
            for f in set(distributions[-1])|set(allkeys)|{0}:
                means[f],covs[f],p,_=direct(T,q,signs_from_key(n,f))
                check('born_normalization',p.sum()-1)
                check('conditional_unbiasedness',np.max(abs(means[f]-2*T.T@q)))
            cf=sum(covs[f] for f in allkeys)/len(allkeys)
            cf_formula=4*T.T@((1-q*q)[:,None]*T)
            check('full_quadratic_covariance',np.max(abs(cf-cf_formula)))
            for k,weights in enumerate(distributions):
                mixed=sum(m*covs[f] for f,m in weights.items())/sum(weights.values())
                target=(1-4.**(-k))*cf+4.**(-k)*covs[0]
                check('parity_covariance_interpolation',np.max(abs(mixed-target)))
        # Independent exact determinant count, not covariance-formula substitution.
        for h in range(1,N):
            for d in range(1,N):
                if h==d: continue
                num=sum((-1)**(bitdot(a,h)*bitdot(b,d)+bitdot(a,d)*bitdot(b,h))
                        for a in range(N) for b in range(N))
                assert 4*num==N*N
                check('rank_two_character_exact')
        # Unique fixed-basis deterministic decoder, constraints on all q from a spanning set.
        qs=[v for e in np.eye(N) for v in (e,-e)]
        qs += [(np.eye(N)[i]+np.eye(N)[j])/np.sqrt(2) for i,j in it.combinations(range(N),2)]
        M=np.array([direct(T,q)[2] for q in qs])
        assert np.linalg.matrix_rank(M)==2*N
        check('fixed_decoder_constraint_rank')

def representation_audit(rng):
    for n in range(1,5):
        N=1<<n; T=rng.normal(size=(N,3));T[0]=0;s=np.sum(T*T)
        for _ in range(8):
            q=rng.normal(size=N);q/=np.linalg.norm(q)
            t=T[:,0];a=rng.normal();M=np.block([[np.array([[a]]),2*t[None,:]],[2*t[:,None],-a*np.eye(N)]])
            psi=np.r_[1.,q]/np.sqrt(2)
            check('restricted_observable',psi@M@psi-2*t@q)
        vals,Rsub=np.linalg.eigh((T@T.T)[1:,1:])
        R=np.eye(N);R[1:,1:]=Rsub;TR=R.T@T
        check('eigenframe_balancing',np.max(abs(np.sum((chars(n)@TR)**2,axis=1)-s)))
        for _ in range(8):
            q=rng.normal(size=N);q/=np.linalg.norm(q)
            mean,C,_,_=direct(TR,R.T@q)
            check('eigenframe_trace',np.trace(C)-(4*s-np.dot(mean,mean)))
        for _ in range(3):
            Q,_=np.linalg.qr(rng.normal(size=(N-1,N-1)));R=np.eye(N);R[1:,1:]=Q
            _,C,_,_=direct(R.T@T,np.eye(N)[0])
            check('reference_lower_bound',np.trace(C)-4*s)
    # Counterexample to removing the measurement-class restriction.
    # n=1, t=|1>, arbitrary spectral measurement of rank-two F.
    F=np.zeros((4,4));F[0,3]=F[3,0]=2
    variances=[]
    for alpha in np.linspace(0,2*np.pi,65):
        q=np.array([np.cos(alpha),np.sin(alpha)])
        psi=np.r_[1.,0.,q]/np.sqrt(2)
        v=psi@(F@F)@psi-(psi@F@psi)**2
        variances.append(v)
        check('unrestricted_counterexample_identity',v-(2-2*q[1]**2))
    return {'frame_class_worst_variance':4.,'rank_two_measurement_worst_variance':float(max(variances))}

def witness_audit(rng):
    for n in range(2,9):
        N=1<<n;t=np.r_[0.,np.ones(N-1)]/np.sqrt(N-1)
        for _ in range(24):
            A=np.triu(rng.integers(0,2,size=(n,n)),1);linear=int(rng.integers(N))
            key=sum(((sum(int(A[i,j])*((x>>i)&1)*((x>>j)&1) for i,j in it.combinations(range(n),2))+bitdot(x,linear))%2)<<x for x in range(N))
            r=rank_binary(A+A.T);W=chars(n)@signs_from_key(n,key)
            targets=[1,N,N*N/(2**r),N**3/(2**r)]
            for power,target in enumerate(targets,1):
                check('quadratic_walsh_moments', (np.mean(W**power)-target)/max(1,abs(target)))
            _,C,_,_=direct(t[:,None],t,signs_from_key(n,key))
            V=2*(N*N*(N-4)/2**r+6*N-3)/(N-1)**2-2
            check('rank_witness_variance',C[0,0]-V)
        for k in (0,1,2,3):
            for _ in range(4):
                pairs=[(int(rng.integers(N)),int(rng.integers(N))) for j in range(k)]
                key=0
                for a,b in pairs:key^=pair_key(n,a,b)
                r=rank_binary(mask_matrix(n,key))
                assert r<=2*k
                if n>=3:
                    V=2*(N*N*(N-4)/2**r+6*N-3)/(N-1)**2-2
                    assert V>=N/4**k-2-1e-9
                check('bilinear_rank_bound')

def readout_optimization_audit(rng):
    """Absorb parity uncomputation into X-basis ancilla readout.
    This is an alternative final measurement, NOT a clean unitary replacement.
    """
    for n in range(1,5):
        N=1<<n;H=np.kron(np.array([[1.,1.],[1.,-1.]])/np.sqrt(2),chars(n)/np.sqrt(N))
        for _ in range(12):
            a=int(rng.integers(N));b=int(rng.integers(N))
            q=rng.normal(size=N);q/=np.linalg.norm(q)
            T=rng.normal(size=(N,2));T[0]=0;phase=signs_from_key(n,pair_key(n,a,b))
            mean,C,p,_=direct(T,q,phase)
            state=np.r_[np.eye(N)[0],q]/np.sqrt(2)
            prob_fold=np.zeros(2*N)
            # X-measure the two work ancillas without uncomputing them.
            for u,v in it.product((0,1),repeat=2):
                character=np.array([(-1.)**(u*bitdot(a,x)+v*bitdot(b,x)) for x in range(N)])
                branch=state*np.tile(phase*character,2)/2
                probabilities=abs(H@branch)**2
                shift=(a if u else 0)^(b if v else 0)
                for anc in (0,1):
                    for y in range(N): prob_fold[anc*N+(y^shift)]+=probabilities[anc*N+y]
            check('measured_uncomputation_probability',np.max(abs(prob_fold-p)))
            # Independent clean-gadget basis contract.
            for x in range(N):
                u=v=0
                for j in range(n):
                    if (a>>j)&1:u^=(x>>j)&1
                    if (b>>j)&1:v^=(x>>j)&1
                sg=(-1)**(u*v)
                for j in reversed(range(n)):
                    if (b>>j)&1:v^=(x>>j)&1
                    if (a>>j)&1:u^=(x>>j)&1
                assert u==v==0 and sg==phase[x]
                check('clean_gadget_basis')
    for n in range(1,7):
        N=1<<n;tau=rng.normal(size=N);table=chars(n)@tau
        for _ in range(20):
            a=int(rng.integers(N));b=int(rng.integers(N));y=int(rng.integers(N))
            score=(table[y]+table[y^a]+table[y^b]-table[y^a^b])/2
            check('shift_table_identity',score-(chars(n)@(tau*signs_from_key(n,pair_key(n,a,b))))[y])

def boundary_audit():
    T=np.array([[0.],[1.]])
    q=np.array([0.,1j]);mean,C,_,_=direct(T,q)
    naive=4*T.T@((1-abs(q)**2)[:,None]*T)
    assert abs(C[0,0]-naive[0,0])>1
    qreal=np.array([0.,1.]);wrong_mean=direct(T,1j*qreal)[0]
    assert abs(wrong_mean[0]-2)>1
    # A 2-design alone does not give the usual uniform-Clifford shadow variance.
    # Qubit stabilizer MUBs are a 2-design; tensor/global dimension example in proof notes.
    return {'complex_response_covariance':float(C[0,0]),'invalid_real_formula_value':float(naive[0,0]),
            'unknown_pi_over_2_branch_phase_mean':float(wrong_mean[0]),'required_real_mean':2.}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    if args.output.exists():p.error('Refusing to overwrite output')
    started=time.perf_counter();rng=np.random.default_rng(SEED)
    moment_audit(rng);counterexample=representation_audit(rng);witness_audit(rng);readout_optimization_audit(rng)
    boundaries=boundary_audit()
    report={'status':'passed','seed':SEED,'python':platform.python_version(),'numpy':np.__version__,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'checks':checks,'class_counterexample':counterexample,'boundary_examples':boundaries,
            'elapsed_seconds':time.perf_counter()-started,
            'scope':'Independent finite diagnostics, no imported formula functions; no novelty or hardware certificate.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
