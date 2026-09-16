"""Independent gate/Born and bounded scaling checks for the PF-06 compiler.
No previous POVM formula implementation is imported. Dense fixture only tests
small existing circuits. The scalable compiler allocates only block tables.
"""
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
import compiler as c

ROOT = Path(__file__).resolve().parents[2]
SEED = 2026091591
FIXTURE_SHA = 'd6eb8552943e6d6db0fe4137ea4ed8003f2b4ccc4257c4378a12338912597a01'
CHECKS = {}


def record(name, residual=0., tolerance=2e-9):
    if not math.isfinite(float(residual)) or residual > tolerance:
        raise AssertionError(f'{name}: {residual} exceeds {tolerance}')
    entry = CHECKS.setdefault(name, {'cases':0, 'max_residual':0.})
    entry['cases'] += 1
    entry['max_residual'] = max(entry['max_residual'],float(residual))


def load_fixture():
    path = ROOT/'research/matched_readout/core.py'
    if hashlib.sha256(path.read_bytes()).hexdigest() != FIXTURE_SHA:
        raise RuntimeError('fixture identity mismatch')
    spec=importlib.util.spec_from_file_location('pf06_fixture',path)
    mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    return mod


def explicit_uc(controls,target,angles,n):
    U=np.zeros((1<<n,1<<n))
    for x in range(1<<n):
        pat=sum(((x>>(n-1-p))&1)<<i for i,p in enumerate(controls))
        a=angles[pat];bit=(x>>(n-1-target))&1
        U[x,x]=math.cos(a)
        U[x^(1<<(n-1-target)),x]=(-1 if bit else 1)*math.sin(a)
    return U


def all_x_bound(plan):
    H=np.array([[(-1)**((x&y).bit_count()&1) for x in range(4)] for y in range(4)])
    # Maximization separates over disjoint blocks; no global Walsh table.
    return 2*plan.s+2*sum(np.sum((H[:,1:]@k)**2,axis=1).max() for k in plan.K)


def end_to_end_rows(B,plan):
    """Symbolic resources, no invented hardware pricing or acceptance winners."""
    counts=plan.counts(); P=plan.P
    assert counts == {'cx':14*B-5,'ry':12*B-4,'x':2,'h':1}
    return {'blocks':B,'n':2*B,'P':P,'rank_at_zero':3*B,
            'stored_tangent_scalars':int(plan.K.size),'row_energies':int(plan.row_energy.size),
            'readout_gates':counts,'physical_measurements':2*B+1,'extra_work_qubits':0,
            'worst_outcome_block_scan':B,'signed_count_bins':3*B,
            'output_scalars':P,'final_contraction_multiplies':18*B,'final_contraction_additions':12*B,
            'other_final_multiplications':3*B,'other_final_divisions':9*B,'other_final_square_roots':3*B+1,
            'all_X_flat_variance':4*P,'sparse_flat_variance':4*P-8,
            'flat_max_variance_ratio':(4*P)/(4*P-8),
            'CNOT_only_common_response_crossover':(3*B-1)*(14*B-5),
            'notes':'Counts for explicit arbitrary-angle logical gates, not optimal synthesis or seconds. No global state allocated.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    a=parser.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    rng=np.random.default_rng(SEED);start=time.perf_counter();fixture=load_fixture()
    # Independent UCR matrices, all computational inputs including inactive controls.
    for k in (0,1,2,3):
      for _ in range(6):
        n=k+1;ctrl=tuple(range(k));theta=rng.uniform(-2,2,1<<k)
        gates=c.uc_rotation(ctrl,k,theta);E=np.eye(1<<n)
        matrix=np.column_stack([c.apply_circuit(E[:,x],gates,n) for x in range(1<<n)])
        record('uniformly_controlled_rotation',np.max(abs(matrix-explicit_uc(ctrl,k,theta,n))))
    # Controlled exchange: direct truth action, not the UCR equations.
    for angle in (0.,.2,-.7,math.pi/2):
        gates=c.exchange_on_reference_zero(1,2,angle)
        matrix=np.column_stack([c.apply_circuit(np.eye(8)[:,i],gates,3) for i in range(8)])
        wanted=np.eye(8);wanted[2,2]=wanted[1,1]=math.cos(angle)
        wanted[1,2]=math.sin(angle);wanted[2,1]=-math.sin(angle)
        record('controlled_exchange',np.max(abs(matrix-wanted)))
    rows=[];small=[]
    for B in range(1,5):
      settings=[('zero',np.zeros((B,6)))]
      for width in (.04,.4):
        for repeat in range(2): settings.append((f'box{width}-{repeat}',rng.uniform(-width,width,(B,6))))
      for label,angles in settings:
        plan=c.compile_plan(angles);N=1<<plan.n;T=c.dense_tangents(plan)
        # Compare block-only compiler with the old global derivative calculation.
        fc=fixture.make_circuit(plan.n,1,rng,angles=angles.T.ravel())
        record('existing_family_tangents',np.max(abs(T-fc.T)))
        # Conditional preparation must preserve the ENTIRE response branch.
        e=np.zeros(2*N);e[0]=1
        prepared=c.apply_circuit(e,plan.gates[:-1],plan.n+1)
        ref=c.reference_vector(plan)
        record('reference_preparation',np.max(abs(prepared-np.r_[ref,np.zeros(N)])))
        Z=c.dense_scores(plan);active=np.array(c.active_addresses(plan));d=plan.row_energy.ravel()
        responses=[np.eye(N)[0],np.eye(N)[active[0]],T[:,0]/np.linalg.norm(T[:,0])]
        if B>1: responses.append(np.eye(N)[active[0]|active[-1]])
        for _ in range(3):
            q=rng.normal(size=N);responses.append(q/np.linalg.norm(q))
        for q in responses:
            only_response=np.r_[np.zeros(N),q]
            untouched=c.apply_circuit(only_response,plan.gates[:-1],plan.n+1)
            record('response_branch_identity',np.max(abs(untouched-only_response)))
            inp=np.r_[np.eye(N)[0],q]/math.sqrt(2)
            out=c.apply_circuit(inp,plan.gates,plan.n+1);prob=out*out
            ideal=np.r_[(ref+q)**2,(ref-q)**2]/4
            record('gate_Born_distribution',max(abs(prob-ideal).max(),abs(prob.sum()-1)))
            mean=prob@Z;second=prob@(Z*Z).sum(axis=1);risk=second-mean@mean
            record('whole_gradient_mean',np.max(abs(mean-2*T.T@q)))
            record('trace_risk_identity',abs(float(risk)-c.risk_from_coordinates(plan,q)))
            record('risk_upper_bound',max(0.,float(risk)-plan.exact_risk_bound()))
        # The diagonal reference measurement is a valid complete POVM on occupied space.
        E=np.zeros((2*len(active)+1,N+1,N+1));scores=[]
        for i,x in enumerate(active):
          for j,sig in enumerate((1,-1)):
            v=np.zeros(N+1);v[0]=math.sqrt(d[i]/plan.s);v[x+1]=sig
            E[2*i+j]=np.outer(v,v)/2
        E[-1]=np.eye(N+1)-E[:-1].sum(axis=0)
        record('occupied_POVM',max(abs(E.sum(axis=0)-np.eye(N+1)).max(),max(0.,-np.linalg.eigvalsh(E).min())))
        # Aggregated decoder: valid comparison on exactly the same sampled records.
        q=responses[-1];prob=np.r_[(ref+q)**2,(ref-q)**2]/4
        shots=1000;events=rng.multinomial(shots,prob/prob.sum());hist=np.zeros((B,3))
        for value,count in enumerate(events):
            bit,x=divmod(value,N);ch=plan.classify(x)
            if ch is not None: hist[ch]+=(-1)**bit*count
        record('aggregate_decoder',np.max(abs(plan.finish(hist,shots)-(events@Z)/shots)))
        # Finite differences do not reuse the reverse tangent compiler.
        O=np.eye(N)-2*np.outer((np.eye(N)[0]-responses[-1]),(np.eye(N)[0]-responses[-1]))/np.linalg.norm(np.eye(N)[0]-responses[-1])**2
        O=fc.U@O@fc.U.T
        ids=range(plan.P) if B==1 else (0,plan.P//2,plan.P-1)
        h=1e-6
        for j in ids:
            aa=angles.T.ravel().copy();bb=aa.copy();aa[j]+=h;bb[j]-=h
            pa=fixture.make_circuit(plan.n,1,rng,angles=aa).U[:,0]
            pb=fixture.make_circuit(plan.n,1,rng,angles=bb).U[:,0]
            fd=(pa@O@pa-pb@O@pb)/(2*h)
            record('finite_differences',abs(fd-2*T[:,j]@responses[-1]),2e-7)
        small.append({'blocks':B,'angles':label,'s':plan.s,'sparse_variance_bound':plan.exact_risk_bound(),
                      'all_X_variance_bound':float(all_x_bound(plan)),
                      'full_mask_variance_bound':4*plan.s,
                      'grouped_three_setting_bound':12*plan.P,
                      'optimal_at_zero_only':label=='zero'})
        if label=='zero':
            eigen=np.linalg.eigvalsh(plan.K[0]@plan.K[0].T)
            record('zero_flat_optimum',max(abs(eigen-2).max(),abs(plan.exact_risk_bound()-(4*plan.P-8)),abs(all_x_bound(plan)-4*plan.P)))
    # Additional POVM structural test without large occupied-space matrices.
    for B in (1,2,4,8,16,32,64,128,256):
        plan=c.compile_plan(np.zeros((B,6)));row=end_to_end_rows(B,plan);rows.append(row)
        record('scalable_compiler',max(abs(plan.s-plan.P),abs(np.sum(plan.row_energy/plan.s)-1)))
    # Counterexample to silently applying this support rule after an overlapping layer.
    fc=fixture.make_circuit(4,2,rng,angles=np.linspace(-.4,.5,18))
    one=c.compile_plan(np.zeros((2,6)));active=c.active_addresses(one)
    omitted=fc.T.copy();omitted[active]=0
    j=int(np.argmax(np.linalg.norm(omitted,axis=0)));q=omitted[:,j]/np.linalg.norm(omitted[:,j])
    missing=float(np.linalg.norm(2*fc.T.T@q))
    if missing < .1: raise AssertionError('overlap witness unexpectedly zero')
    boundary={'n':4,'depth':2,'P':18,'coordinate':j,'missing_gradient_norm':missing,
              'explanation':'A two-layer tangent lies outside the exactly-one-active-disjoint-block sector. This compiler is not valid for it.'}
    record('overlap_scope_counterexample')
    # Existing-family only input contract, deliberate malformed inputs.
    bad=[np.zeros((1,5)),np.zeros((2,1,6)),np.ones((1,6),complex),np.full((1,6),np.nan)]
    for value in bad:
        try:c.compile_plan(value)
        except ValueError: record('invalid_domain_rejected')
        else:raise AssertionError('invalid input accepted')
    # Bounded finite-shot risk check, nonzero signal; assessment, not tail certification.
    plan=c.compile_plan(np.zeros((2,6)));N=1<<plan.n;q=np.eye(N)[c.active_addresses(plan)[0]]
    prob=np.r_[(c.reference_vector(plan)+q)**2,(c.reference_vector(plan)-q)**2]/4
    Z=c.dense_scores(plan);g=2*c.dense_tangents(plan).T@q;mc=[]
    for K in (64,256,1024):
        estimates=rng.multinomial(K,prob/prob.sum(),size=5000)@Z/K
        errors=np.sum((estimates-g)**2,axis=1);expected=c.risk_from_coordinates(plan,q)/K
        observed=float(errors.mean());se=float(errors.std(ddof=1)/math.sqrt(len(errors)))
        mc.append({'shots':K,'replicates':5000,'gradient_norm':float(np.linalg.norm(g)),
                   'predicted_MSE':expected,'observed_MSE':observed,'standard_error':se})
        record('finite_shot_MSE',max(0.,abs(observed-expected)-6*se),1e-8)
    data={'status':'passed','seed':SEED,'environment':{'python':platform.python_version(),'numpy':np.__version__},
          'checks':CHECKS,'small_parameter_cases':small,'compiler_scaling':rows,'overlap_boundary':boundary,
          'finite_shot_checks':mc,'elapsed_seconds':time.perf_counter()-start,
          'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path(c.__file__))},
          'fixture_sha256':FIXTURE_SHA,
          'limits':'Real logical one-layer implementation. No general tangent-basis compiler, noise/hardware timing, price-winner search, novelty clearance or merge.'}
    (a.output/'diagnostics.json').write_text(json.dumps(data,indent=2)+'\n')
    (a.output/'example_plan.json').write_text(json.dumps({'angles':plan.angles.tolist(),'gates':plan.gates,'counts':plan.counts()},indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
