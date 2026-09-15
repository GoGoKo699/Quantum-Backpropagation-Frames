"""Independent ideal-model checks. Run with single-threaded BLAS for stability."""
from __future__ import annotations
import json, math, platform, sys, time, hashlib
from pathlib import Path
import numpy as np
from core import *

ROOT=Path(__file__).resolve().parent
SEED=2026091551
rng=np.random.default_rng(SEED)
results={'seed':SEED,'python':platform.python_version(),'numpy':np.__version__,
         'scope':'real reference-response model; exact probabilities, no hardware/noise simulation',
         'checks':{},'examples':{}}

def record(name,count,**data):
    results['checks'][name]={'cases':count,**{k:float(v) if isinstance(v,(float,np.floating)) else v for k,v in data.items()}}
    print(name,results['checks'][name],flush=True)

start=time.perf_counter()
# 1. Full mask and parity-product ensembles, using explicit measurement distributions.
count=0; errmean=errfull=errinterp=0.; excess=0.
for n in range(1,6):
    N=1<<n; nmasks=1<<(n*(n-1)//2)
    phases=np.array([quadratic_phase(n,A) for A in range(nmasks)])
    for rep in range(3):
        P=min(N-1,4)
        T=rng.normal(size=(N,P));T[0]=0
        T/=np.linalg.norm(T,axis=0)
        q=rng.normal(size=N);q/=np.linalg.norm(q)
        if rep==0: q=np.eye(N)[0]
        covs=[]
        for phase in phases:
            m,C,_,_=measurement_moments(T,q,phase)
            errmean=max(errmean,float(np.max(abs(m-2*T.T@q))))
            covs.append(C)
        covs=np.array(covs)
        full=covs.mean(axis=0)
        errfull=max(errfull,float(np.max(abs(full-full_quadratic_covariance(T,q)))))
        for k in range(5):
            probs=rounds_mask_distribution(n,k)
            C=np.einsum('a,aij->ij',probs,covs)
            expected=interpolated_covariance(T,q,k)
            errinterp=max(errinterp,float(np.max(abs(C-expected))))
            excess=max(excess,float(np.trace(C)-risk_bound(T,k)))
            count+=1
record('complete_ensemble_interpolation',count,max_mean_error=errmean,
       max_full_mask_formula_error=errfull,max_covariance_error=errinterp,max_bound_violation=excess)
assert errinterp<1e-10 and errfull<1e-10 and excess<1e-10

# 2. Linear terms in parity gadgets are irrelevant to covariance but relabel outcomes.
err=0.; cases=0
for n in range(1,7):
    N=1<<n
    for rep in range(8):
        a,b=map(int,rng.integers(N,size=2));T=rng.normal(size=(N,3));T[0]=0
        T/=np.linalg.norm(T,axis=0);q=rng.normal(size=N);q/=np.linalg.norm(q)
        C1=measurement_moments(T,q,parity_phase(n,[(a,b)]))[1]
        C2=measurement_moments(T,q,quadratic_phase(n,pair_quadratic_mask(n,a,b)))[1]
        err=max(err,float(np.max(abs(C1-C2))));cases+=1
record('linear_phase_equivalence',cases,max_covariance_error=err)
assert err<1e-10

# 3. Explicit basis-state gate simulation proves clean ancilla contract on a basis.
cases=0
for n in range(1,6):
    for a in range(1<<n):
        for b in range(1<<n):
            for x in range(1<<n):
                y,u,v,s=simulate_gadget_basis(n,x,a,b)
                assert (y,u,v)==(x,0,0)
                assert s==(-1)**(parity(a&x)*parity(b&x))
                cases+=1
record('compute_phase_uncompute_basis',cases,failures=0)

# 4. Low-rank phase lower bound, independently evaluating full Fourier moments.
cases=0; err=0.; violation=0.; rank_violations=0
for w in range(2,10):
    m=1<<w;t=uniform_tangent(w)
    for k in range(6):
        for rep in range(6):
            pairs=[tuple(map(int,rng.integers(m,size=2))) for _ in range(k)]
            mask=0
            for a,b in pairs: mask^=pair_quadratic_mask(w,a,b)
            rank=mask_rank(w,mask)
            rank_violations+=int(rank>2*k)
            C=measurement_moments(t[:,None],t,parity_phase(w,pairs))[1][0,0]
            exact=witness_variance(w,rank)
            err=max(err,abs(C-exact))
            if w>=2: violation=max(violation,witness_variance(w,2*k)-C)
            cases+=1
record('phase_rank_witness',cases,max_variance_formula_error=err,
       max_lower_bound_violation=violation,rank_violations=rank_violations)
assert err<1e-8 and violation<1e-8 and rank_violations==0

# 5. Decoder uses the original local Walsh table. Several rounds and all y.
cases=0; err=0.
for w in range(1,9):
    m=1<<w
    for k in range(6):
        for rep in range(3):
            tau=rng.normal(size=m);tau[0]=0;tau/=np.linalg.norm(tau)
            F=fwht(tau);pairs=[tuple(map(int,rng.integers(m,size=2))) for _ in range(k)]
            direct=fwht(tau*parity_phase(w,pairs))
            for y in rng.choice(m,size=min(12,m),replace=False):
                ans=local_shift_score(F,int(y),pairs)
                err=max(err,abs(ans-direct[y]));cases+=1
record('shift_lookup_decoder',cases,max_error=err)
assert err<1e-9

# 6. Representation lemma and balanced-frame minimax.
cases=0; rep_err=bal_err=opt_err=0.
for n in range(1,6):
    N=1<<n
    for trial in range(4):
        P=min(N,5);T=rng.normal(size=(N,P));T[0]=0
        T/=np.linalg.norm(T,axis=0)
        t=T[:,0];alpha=rng.normal()
        compressed=np.zeros((N+1,N+1));compressed[0,0]=alpha
        compressed[0,1:]=compressed[1:,0]=2*t
        compressed[1:,1:]=-alpha*np.eye(N)
        q=rng.normal(size=N);q/=np.linalg.norm(q)
        psi=np.r_[1.,q]/math.sqrt(2)
        rep_err=max(rep_err,abs(psi@compressed@psi-2*t@q))
        _,V=np.linalg.eigh((T@T.T)[1:,1:])
        R=np.eye(N);R[1:,1:]=V
        TR=R.T@T;s=float(np.sum(T*T))
        S=np.sum(fwht(TR.T)**2,axis=0)
        bal_err=max(bal_err,float(np.max(abs(S-s))))
        risk=float(np.linalg.eigvalsh(covariance_risk_matrix(TR,0))[-1])
        opt_err=max(opt_err,abs(risk-4*s));cases+=1
record('representation_and_eigenframe',cases,max_representation_error=rep_err,
       max_balancing_error=bal_err,max_minimax_error=opt_err)
assert max(rep_err,bal_err,opt_err)<1e-9

# 7. Fixed all-X decoder uniqueness: full coefficient matrix of test states.
cases=0; min_sv=1e99
for n in range(1,5):
    N=1<<n;qs=[]
    for i in range(N): qs += [np.eye(N)[i],-np.eye(N)[i]]
    for i in range(N):
        for j in range(i+1,N):
            for sign in (-1,1): qs.append((np.eye(N)[i]+sign*np.eye(N)[j])/math.sqrt(2))
    mat=[]
    for q in qs:
        h=fwht(q)
        mat.append(np.r_[(1+h)**2,(1-h)**2]/(4*N))
    sv=np.linalg.svd(np.array(mat),compute_uv=False)
    assert (sv>1e-10).sum()==2*N
    min_sv=min(min_sv,float(sv[-1]));cases+=1
record('fixed_measurement_decoder_uniqueness',cases,minimum_nonzero_singular_value=min_sv)

# 8. Actual inherited non-Hopf ansatz, versus independent dense spectral certificate.
old=ROOT/'reference_circuit.py'
if old.exists():
    import importlib.util
    spec=importlib.util.spec_from_file_location('old_reference',old)
    oldcore=importlib.util.module_from_spec(spec);sys.modules[spec.name]=oldcore;spec.loader.exec_module(oldcore)
    examples=[]
    for n in range(2,7):
        for depth in (1,2,3):
            c=oldcore.make_circuit(n,depth,rng)
            T=c.T;s=float(np.sum(T*T)); beta=imbalance(T)
            Vs=[];bounds=[]
            for k in range(5):
                Vs.append(float(np.linalg.eigvalsh(covariance_risk_matrix(T,k))[-1]))
                bounds.append(risk_bound(T,k))
            assert all(Vs[k+1]<=Vs[k]+1e-10 for k in range(4))
            assert all(4*s-1e-9<=v<=b+1e-9 for v,b in zip(Vs,bounds))
            examples.append(dict(n=n,depth=depth,P=T.shape[1],s=s,beta=beta,
                                 worst_covariance_trace=Vs,sufficient_bounds=bounds,
                                 rounds_for_10_percent=rounds_for_relative_bound(beta,.1)))
    results['examples']['inherited_non_hopf_circuits']=examples
    record('non_hopf_worst_case_certificates',len(examples),failures=0)

# 9. Analytical/compiler resource illustration (not a statevector simulation).
w=6;n=1024;eta=.1;beta_bound=2.**w
k=rounds_for_relative_bound(beta_bound,eta)
results['examples']['large_compiler_ledger']={
    'n':n,'width_bound':w,'relative_tolerance':eta,'rounds':k,
    'expected_cnot':2*n*k,'cz':k,'worst_cnot':4*n*k,
    'expected_dense_independent_cz':n*(n-1)/4,
    'risk_factor_bound':1+4.**(-k)*(beta_bound-1)/2,
    'status':'analytic all-to-all logical gate ledger, not hardware execution'}
results['examples']['rank_witness']=[{
    'w':w,'rounds':k,'rank_only_lower_bound':witness_variance(w,2*k),
    'random_pair_variance':(1-4.**(-k))*4*(1-1/((1<<w)-1))+4.**(-k)*witness_variance(w,0)
} for w in (4,6,8,10) for k in range(6)]
results['elapsed_seconds']=time.perf_counter()-start
(ROOT/'validation.json').write_text(json.dumps(results,indent=2)+'\n')
print('RESULTS',ROOT/'validation.json',flush=True)
