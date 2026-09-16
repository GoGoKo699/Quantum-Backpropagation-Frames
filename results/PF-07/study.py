"""PF-07 gate checks; no earlier POVM formula is called. Reuse is hash-pinned."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import sys
import time
import numpy as np
import compiler as new

ROOT=Path(__file__).resolve().parents[2]
SEED=2026091607
CHECKS={}
SOURCES={
 'results/PF-04/study.py':'373f76105d7a07ec5604173bbab9a6e3da56dee4908510afe2e346456422df85',
 'results/PF-06/compiler.py':'456083f4545fe5832c56546793b5cffb817ed003da46522520215f5deffc5528',
 'research/matched_readout/core.py':'d6eb8552943e6d6db0fe4137ea4ed8003f2b4ccc4257c4378a12338912597a01'}


def load(path,name):
    p=ROOT/path
    if hashlib.sha256(p.read_bytes()).hexdigest()!=SOURCES[path]: raise RuntimeError('source changed: '+path)
    spec=importlib.util.spec_from_file_location(name,p);mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod;spec.loader.exec_module(mod);return mod


def check(name,residual=0.,tol=2e-9):
    if not math.isfinite(float(residual)) or residual>tol: raise AssertionError(f'{name}: {residual}')
    item=CHECKS.setdefault(name,{'cases':0,'max_residual':0.})
    item['cases']+=1;item['max_residual']=max(item['max_residual'],float(residual))


def dense(plan):
    N=1<<plan.n;T=np.zeros((N,plan.P))
    for j,(l,r,t) in enumerate(zip(plan.starts,plan.ends,plan.tables)):
        for z,value in enumerate(t):T[z<<(plan.n-r),j]=value
    return T


def table_plan(local):
    taus=[t.copy() for t in local['taus']]
    # Analytically zero by real normalization; only remove its roundoff residual.
    worst=max(abs(t[0]) for t in taus)
    if worst>1e-10:raise AssertionError('not a reference-orthogonal real circuit')
    for t in taus:t[0]=0.
    return new.IntervalReference.from_tables(local['n'],local['intervals'],taus),float(worst)


def ideal_arrays(plan):
    T=dense(plan);d=np.sum(T*T,axis=1);c=np.sqrt(d/plan.s);N=len(c)
    Z=np.zeros((2*N,plan.P));idx=d>0
    Z[:N][idx]=2*(T[idx]/c[idx,None]);Z[N:]=-Z[:N]
    return T,c,Z


def run_born(plan,q,sim,gates,T,c,Z):
    N=len(c);vac=np.zeros(N);vac[0]=1.
    inp=np.r_[vac,q]/math.sqrt(2)
    out=sim.apply_circuit(inp,gates,plan.n+1);p=abs(out)**2
    expected=np.r_[(c+q)**2,(c-q)**2]/4
    check('elementary_Born',max(abs(p-expected).max(),abs(p.sum()-1)))
    mean=p@Z;g=2*T.T@q;check('whole_raw_gradient',np.max(abs(mean-g)))
    variance=float(p@(Z*Z).sum(axis=1)-mean@mean)
    theory=2*plan.s*(1+float(q[c>0]@q[c>0]))-float(g@g)
    check('exact_trace_risk',abs(variance-theory))
    check('uniform_4s_bound',max(0.,variance-4*plan.s))
    untouched=sim.apply_circuit(np.r_[np.zeros(N),q],gates[:-1],plan.n+1)
    check('response_branch_identity',np.max(abs(untouched-np.r_[np.zeros(N),q])))
    return p,variance


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    a=parser.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    begin=time.perf_counter();rng=np.random.default_rng(SEED)
    old=load('results/PF-04/study.py','pf07_local');sim=load('results/PF-06/compiler.py','pf07_gate_sim')
    fixture=load('research/matched_readout/core.py','pf07_dense_fixture')
    # Fast Walsh compiler checked against a separate direct rotation matrix.
    for k in range(5):
      for _ in range(3):
        angles=rng.uniform(-1,1,1<<k);gates=list(new.ucr(tuple(range(k)),k,angles));n=k+1;D=1<<n
        U=np.column_stack([sim.apply_circuit(np.eye(D)[:,x],gates,n) for x in range(D)])
        expected=np.zeros_like(U)
        for x in range(D):
            pat=sum(((x>>(n-1-p))&1)<<p for p in range(k));bit=x&1;theta=angles[pat]
            expected[x,x]=math.cos(theta);expected[x^1,x]=(-1 if bit else 1)*math.sin(theta)
        check('fast_UCR_all_columns',abs(U-expected).max())
    # Synthetic mixed-width, overlap, duplicates and zeros exercise the general contract.
    synthetic=[(3,[(0,1),(1,2)],[np.array([0,1,1,1])/math.sqrt(3)]*2),
               (4,[(0,),(1,2,3),(2,3)], [np.array([0.,0.]),np.r_[0.,np.arange(1.,8.)]/12,np.array([0.,0.,1.,0.])]),
               (4,[(0,1),(0,1),(2,)], [np.array([0.,1.,-1.,0.]),np.array([0.,-1.,1.,0.]),np.array([0.,1.])])]
    for n,intervals,tables in synthetic:
        plan=new.IntervalReference.from_tables(n,intervals,tables);T,c,Z=ideal_arrays(plan);N=1<<n
        gates=list(plan.gates());v=np.zeros(2*N);v[0]=1.
        ref=sim.apply_circuit(v,gates[:-1],n+1)
        check('synthetic_reference',np.max(abs(ref-np.r_[c,np.zeros(N)])))
        for _ in range(3):
            q=rng.normal(size=N);q/=np.linalg.norm(q);run_born(plan,q,sim,gates,T,c,Z)
        expectedmu=np.zeros(n)
        for x,d in enumerate(np.sum(T*T,axis=1)):
            if x:expectedmu[n-x.bit_length()]+=d
        check('unique_first_mass',np.max(abs(expectedmu-plan.first_mass)))
        for site in range(n):
            h=plan.suffix_mass(site);pad=n-plan.ends_by_first[site];base=1<<(n-site-1)
            expected=np.sum(T[base+(np.arange(len(h))<<pad)]**2,axis=1)
            check('local_suffix_mass',np.max(abs(h-expected)))
        for x in range(N):
            ids,score=plan.score(0,format(x,f'0{n}b'));full=np.zeros(plan.P);full[list(ids)]=score
            check('sparse_score_contract',np.max(abs(full-Z[x])))
    # Complete bounded-window envelopes: count and construct without assumed sparse addresses.
    for n in range(1,7):
      for w in range(1,n+1):
        M=(n-w+2)*(1<<(w-1))-1
        number=sum((x.bit_length()-(x & -x).bit_length()+1)<=w for x in range(1,1<<n))
        check('envelope_size_formula',abs(M-number))
        intervals=[tuple(range(a,min(n,a+w))) for a in range(n)]
        tables=[]
        for interval in intervals:
            half=1<<(len(interval)-1)
            tables.append(np.r_[np.zeros(half),rng.uniform(.1,1.,half)])
        plan=new.IntervalReference.from_tables(n,intervals,tables)
        ledger=plan.ledger()
        check('full_envelope_gate_bound',max(abs(ledger['cnot']-(4*M+2*n-5)),abs(ledger['ry']-(4*M-4))))
        T,c,Z=ideal_arrays(plan);v=np.zeros(2<<n);v[0]=1.
        out=sim.apply_circuit(v,list(plan.preparation_gates()),n+1)
        check('full_envelope_preparation',np.max(abs(out-np.r_[c,np.zeros(1<<n)])))
    # Deliberately wrong order: suffix-created bits must not trigger later fillers.
    badplan=new.IntervalReference.from_tables(*synthetic[0]);T,c,Z=ideal_arrays(badplan);N=len(c)
    v=np.zeros(2*N);v[0]=1
    wrong=sim.apply_circuit(v,list(badplan.preparation_gates(descending=False)),4)
    order_error=float(np.linalg.norm(wrong-np.r_[c,np.zeros(N)]))
    if order_error<.05:raise AssertionError('wrong-order witness failed')
    check('wrong_order_counterexample')
    # Coordinate kernel: the general 4s bound can be exactly attained.
    ids=np.flatnonzero(c>0);_,_,vh=np.linalg.svd(T[ids].T,full_matrices=True)
    q=np.zeros(N);q[ids]=vh[-1];check('coordinate_null_witness',np.linalg.norm(T.T@q))
    _,risk=run_born(badplan,q,sim,list(badplan.gates()),T,c,Z)
    check('coordinate_null_saturates_4s',abs(risk-4*badplan.s))
    rng=np.random.default_rng(SEED+1)
    rows=[];max_zero=0.;saved_example=None
    for n in (3,4,5,6,8):
      for depth in (1,2,3):
       for mode in ('zero','seeded'):
        P=len(old.structure(n,depth,rng)[0]);angles=np.zeros(P) if mode=='zero' else rng.uniform(-.4,.4,P)
        local=old.compile_local(n,depth,rng,angles);plan,z0=table_plan(local);max_zero=max(max_zero,z0)
        T,c,Z=ideal_arrays(plan);N=len(c);fc=fixture.make_circuit(n,depth,rng,angles=angles)
        check('independent_dense_tangents',np.max(abs(T-fc.T)))
        gates=list(plan.gates());ledger=plan.ledger();counts=Counter(g[0] for g in gates)
        for kind in ('cx','ry','x','h'):
            field='cnot' if kind=='cx' else kind
            check('exact_gate_ledger',abs(counts[kind]-ledger[field]))
        vac=np.zeros(N);vac[0]=1;prepared=sim.apply_circuit(np.r_[vac,np.zeros(N)],gates[:-1],n+1)
        check('existing_family_reference',np.max(abs(prepared-np.r_[c,np.zeros(N)])))
        responses=[vac,T[:,0]/np.linalg.norm(T[:,0])]
        for _ in range(3):
            q=rng.normal(size=N);responses.append(q/np.linalg.norm(q))
        active=np.flatnonzero(c>0)
        R=2*plan.s*np.diag((c>0).astype(float))-4*T@T.T
        ev,evec=np.linalg.eigh(R);responses.append(evec[:,-1])
        for q in responses:p,risk=run_born(plan,q,sim,gates,T,c,Z)
        check('risk_eigen_endpoint',abs(risk-(2*plan.s+ev[-1])))
        trials=rng.multinomial(513,p/p.sum());acc=np.zeros(P);updates=0
        for outcome,count in enumerate(trials):
            b,x=divmod(outcome,N);bits=format(x,f'0{n}b');ids,v=plan.score(b,bits)
            if ids:acc[list(ids)]+=count*v;updates+=len(ids)
        check('aggregate_original_output',np.max(abs(acc/513-(trials@Z)/513)))
        # Two independent finite differences on the actual original circuit.
        q=responses[2];v=vac-q;Oin=np.eye(N)-2*np.outer(v,v)/(v@v);O=fc.U@Oin@fc.U.T
        for j in (0,P-1):
            plus=angles.copy();minus=angles.copy();plus[j]+=1e-6;minus[j]-=1e-6
            sp=fixture.make_circuit(n,depth,rng,angles=plus).U[:,0]
            sm=fixture.make_circuit(n,depth,rng,angles=minus).U[:,0]
            fd=(sp@O@sp-sm@O@sm)/(2e-6)
            check('independent_finite_difference',abs(fd-2*T[:,j]@q),2e-7)
        H=np.array([[(-1)**((x&y).bit_count()&1) for x in range(N)] for y in range(N)],float)/math.sqrt(N)
        S=np.sum((math.sqrt(N)*H@T)**2,axis=1)
        Xrisk=2*plan.s+np.linalg.eigvalsh(2*H.T@(S[:,None]*H)-4*T@T.T)[-1]
        ledger.update({'depth':depth,'angles':mode,'active_coordinate_rows_small_diagnostic':len(active),
                       'sparse_exact_risk_small':float(2*plan.s+ev[-1]),
                       'all_X_exact_risk_small':float(Xrisk),'full_mask_uniform_risk':4*plan.s,
                       'stored_program_gates_small':len(gates),'local_gate_visits':local['visits']})
        rows.append(ledger)
        if n==4 and depth==2 and mode=='seeded':saved_example={'n':n,'depth':depth,'angles':angles.tolist(),'gates':gates,'ledger':ledger}
    # Exact PF-06 counterexample, reconstructed with its fixed angles and selector.
    fc=fixture.make_circuit(4,2,rng,angles=np.linspace(-.4,.5,18))
    allowed=[(t+1)<<(4-2-2*b) for b in range(2) for t in range(3)]
    omitted=fc.T.copy();omitted[allowed]=0;j=int(np.argmax(np.linalg.norm(omitted,axis=0)))
    q=omitted[:,j]/np.linalg.norm(omitted[:,j]);local=old.compile_local(4,2,rng,np.linspace(-.4,.5,18))
    plan,_=table_plan(local);T,c,Z=ideal_arrays(plan);p,_=run_born(plan,q,sim,list(plan.gates()),T,c,Z)
    oldmissing=float(np.linalg.norm(2*fc.T.T@q));newerr=float(np.linalg.norm(p@Z-2*fc.T.T@q))
    check('PF06_missed_gradient_recovered',newerr)
    if abs(oldmissing-2.7639718921748453)>1e-10:raise AssertionError('wrong inherited witness')
    # Fixed scaling grid: compile only; count streamed gates without storing them.
    scaling=[]
    for regime in ('depth2','growing'):
      for n in (16,32,64,128,256):
        depth=2 if regime=='depth2' else math.ceil(math.log2(n)/2)
        local=old.compile_local(n,depth,rng);plan,z0=table_plan(local);max_zero=max(max_zero,z0)
        counts=Counter(g[0] for g in plan.gates());ledger=plan.ledger()
        check('streamed_scaling_gates',max(abs(counts[k]-ledger[f]) for k,f in [('cx','cnot'),('ry','ry'),('h','h'),('x','x')]))
        # Non-Born records exercise the bit scanner at scale, not a quantum simulation.
        acc=np.zeros(plan.P);maxupdates=0
        for b in range(8):
            a0=int(rng.integers(n));x=['0']*n;x[a0]='1'
            for site in range(a0+1,min(n,a0+plan.width)):
                x[site]=str(int(rng.integers(2)))
            maxupdates=max(maxupdates,plan.add_record(acc,b%2,''.join(x)))
        ledger.update({'regime':regime,'depth':depth,'local_gate_visits':local['visits'],
                       'local_amplitude_kernel_entries':local['amplitude_kernel_entries'],
                       'max_sparse_updates_in_test_records':maxupdates,'global_state_allocated':False,
                       'program_retained':False})
        scaling.append(ledger);check('finite_scalable_decoder',0. if np.isfinite(acc).all() else math.inf)
    bad=[(2,[(0,1)],[np.array([0,1,0,0],complex)]),
         (2,[(0,1)],[np.array([0,np.nan,0,0])]),(2,[(0,1)],[np.array([0,1e-200,1,0])]),
         (3,[(0,2)],[np.array([0,1,1,1])]),(2,[(0,1)],[np.array([1e-14,1,0,0])]),
         (2,[(0,1)],[np.zeros(4)])]
    for args in bad:
        try:new.IntervalReference.from_tables(*args)
        except ValueError:check('invalid_input_rejected')
        else:raise AssertionError('bad input accepted')
    data={'status':'passed','seed':SEED,'environment':{'python':platform.python_version(),'numpy':np.__version__},
          'checks':CHECKS,'small_family_points':rows,'compiler_only':scaling,
          'wrong_order_reference_error':order_error,'max_analytic_reference_roundoff_zeroed':max_zero,
          'PF06_counterexample':{'original_missed_gradient_norm':oldmissing,'new_gradient_error':newerr},
          'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path(new.__file__))},
          'inherited_source_hashes':SOURCES,'elapsed_seconds':time.perf_counter()-begin,
          'limits':'Gate/Born diagnostics at n<=8; compiler-only through n=256; no global support union, no large state, no hardware/novelty/strongest-method advantage or merge.'}
    (a.output/'diagnostics.json').write_text(json.dumps(data,indent=2)+'\n')
    (a.output/'example_program.json').write_text(json.dumps(saved_example,indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
