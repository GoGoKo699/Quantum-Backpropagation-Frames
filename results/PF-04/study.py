"""PF-04 finite diagnostics; own POVM and causal-cone implementations.

Does not import earlier parity formulas. Dense operators are only used in
small proof checks. The growing-width compiler never constructs a full state.
"""
from __future__ import annotations
import argparse
import hashlib
import heapq
import importlib.util
import json
import math
from pathlib import Path
import platform
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / 'research/matched_readout/core.py'
EXPECTED = 'd6eb8552943e6d6db0fe4137ea4ed8003f2b4ccc4257c4378a12338912597a01'
WORDS = ((2,0),(0,2),(2,1),(1,2),(2,3),(3,2))
SEED = 2026091571


def signs(rank):
    """At most 4r characters: pairwise orthogonal, all odd triple moments zero."""
    if not isinstance(rank, int) or rank < 1:
        raise ValueError('positive integer rank required')
    lower = (rank - 1).bit_length()
    labels = np.arange(rank, dtype=np.int64) + (1 << lower)
    m = 1 << (lower + 1)
    return np.array([[(-1)**((int(y)&int(a)).bit_count()&1)
                      for a in labels] for y in range(m)], float)


def character_povm(U, V, sigma):
    """Explicit occupied-space POVM. Coordinates: a, then b_x for x=0..N-1.

U has orthonormal tangent-state columns, V orthonormal parameter columns.
The construction is mathematical; obtaining/compiling U is NOT free.
"""
    U, V, sigma = map(lambda x: np.asarray(x, float), (U,V,sigma))
    n, rank = U.shape
    if V.shape[1] != rank or sigma.shape != (rank,):
        raise ValueError('dimension mismatch')
    np.testing.assert_allclose(U.T@U, np.eye(rank), atol=1e-12)
    np.testing.assert_allclose(V.T@V, np.eye(rank), atol=1e-12)
    np.testing.assert_allclose(U[0], 0, atol=1e-12)
    chars = signs(rank)
    vec = np.column_stack((np.ones(len(chars)), chars @ U.T))
    effects = np.einsum('wi,wj->wij', vec, vec) / len(chars)
    projection = np.zeros((n+1,n+1)); projection[0,0] = 1; projection[1:,1:] = U@U.T
    effects = np.concatenate((effects, (np.eye(n+1)-projection)[None,:,:]))
    scores = np.vstack((2*(chars*sigma)@V.T, np.zeros(V.shape[0])))
    return effects, scores


def moments(effects, scores, q):
    psi = np.r_[1.,q]/math.sqrt(2.)
    p = np.einsum('a,wab,b->w', psi, effects, psi)
    if min(p) < -1e-11 or not math.isclose(float(p.sum()),1.,abs_tol=1e-11):
        raise AssertionError('not a Born distribution')
    mean = p@scores
    second = np.einsum('w,wi,wj->ij',p,scores,scores)
    return mean, second - np.outer(mean,mean)


def full_mask_moments(T,q):
    """Independently enumerate original masks, Hadamards and Born outcomes."""
    N,P=T.shape; n=(N-1).bit_length(); edges=[(i,j) for i in range(n) for j in range(i+1,n)]
    H=np.array([[(-1)**((x&y).bit_count()&1) for x in range(N)] for y in range(N)],float)
    mean=np.zeros(P); second=np.zeros((P,P))
    for mask in range(1<<len(edges)):
        phase=np.array([(-1)**sum(((mask>>k)&1)*((x>>i)&1)*((x>>j)&1)
                                 for k,(i,j) in enumerate(edges)) for x in range(N)])
        amp=H@(phase*q); score=2*(H@(phase[:,None]*T))
        prob=np.stack(((1+amp)**2,(1-amp)**2))/(4*N)
        mean += prob[0]@score - prob[1]@score
        second += np.einsum('y,yi,yj->ij',prob.sum(axis=0),score,score)
    num=1<<len(edges); mean/=num; second/=num
    return mean,second-np.outer(mean,mean)


def structure(n, depth, rng, angles=None):
    """Same six-generator, big-endian physical circuit family as the fixture."""
    specs=[]
    for layer in range(depth):
        for word in WORDS:
            for left in range(layer%2,n-1,2):
                specs.append(((left,left+1),word))
    if angles is None: angles=rng.uniform(-.7,.7,len(specs))
    if len(angles)!=len(specs): raise ValueError('angle count')
    previous=[-1]*n; predecessors=[]; supports=[]
    for j,(sites,word) in enumerate(specs):
        active=tuple(site for site,p in zip(sites,word) if p)
        supports.append(active)
        predecessors.append(tuple(previous[site] for site in active if previous[site]>=0))
        for site in active: previous[site]=j
    return specs,np.asarray(angles),supports,predecessors


def kernel(vector, sites, word, interval):
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


def compile_local(n, depth, rng, angles=None):
    specs,angles,supports,pred=structure(n,depth,rng,angles)
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
            v=math.cos(theta)*v+math.sin(theta)*kernel(v,sites,word,interval)
        v=kernel(v,target_sites,target_word,interval)
        for k in reversed(order):
            sites,word=specs[k];theta=angles[k]
            v=math.cos(theta)*v-math.sin(theta)*kernel(v,sites,word,interval)
        intervals.append(interval);taus.append(v)
        visits+=len(order);work+=(2*len(order)+1)*len(v)
    return dict(n=n,depth=depth,angles=angles,intervals=intervals,taus=taus,
                visits=visits,amplitude_kernel_entries=work)


def load_fixture():
    if hashlib.sha256(FIXTURE.read_bytes()).hexdigest()!=EXPECTED:
        raise RuntimeError('reference fixture hash mismatch')
    spec=importlib.util.spec_from_file_location('pf04_fixture',FIXTURE)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    return module


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter();rng=np.random.default_rng(SEED); checks={}
    # Exact finite sign identities (integer arithmetic, not a design assertion).
    cases=0
    for rank in range(1,17):
        c=signs(rank).astype(int); m=len(c)
        assert np.all(c.sum(axis=0)==0)
        assert np.array_equal(c.T@c,m*np.eye(rank,dtype=int))
        assert np.all(np.einsum('wi,wj,wk->ijk',c,c,c)==0)
        cases+=1
    checks['character_moments']={'cases':cases,'failures':0,'max_rank':16}
    # POVMs for rotated, redundant parameter directions, plus least-favorable responses.
    maxima=dict(completeness=0.,positivity=0.,mean=0.,risk=0.,moment_operator=0.,kadison=0.)
    cases=0; risk_table=[]
    for rank in range(1,9):
      for lam in (.25,1.,2.):
        N=1 << rank.bit_length(); P=rank+2
        U0=np.linalg.qr(rng.normal(size=(N-1,rank)))[0];U=np.vstack((np.zeros(rank),U0))
        V=np.linalg.qr(rng.normal(size=(P,rank)))[0];sig=np.full(rank,math.sqrt(lam));T=(U*sig)@V.T
        E,Z=character_povm(U,V,sig);D=N+1
        maxima['completeness']=max(maxima['completeness'],float(np.max(abs(E.sum(axis=0)-np.eye(D)))))
        maxima['positivity']=max(maxima['positivity'],float(max(0,-np.linalg.eigvalsh(E).min())))
        for j in range(P):
            M=np.einsum('w,wab->ab',Z[:,j],E);Q=np.einsum('w,wab->ab',Z[:,j]**2,E)
            wanted=np.zeros((D,D));wanted[0,1:]=2*T[:,j];wanted[1:,0]=2*T[:,j]
            maxima['moment_operator']=max(maxima['moment_operator'],float(abs(M-wanted).max()))
            maxima['kadison']=max(maxima['kadison'],float(max(0,-np.linalg.eigvalsh(Q-M@M).min())))
        responses=[np.eye(N)[0],U[:,0],-U[:,0]]
        responses += [v/np.linalg.norm(v) for v in rng.normal(size=(5,N))]
        for q in responses:
            mean,cov=moments(E,Z,q);z=U.T@q
            prediction=2*rank*lam+(2*rank-4)*lam*float(z@z)
            maxima['mean']=max(maxima['mean'],float(abs(mean-2*T.T@q).max()))
            maxima['risk']=max(maxima['risk'],abs(float(np.trace(cov))-prediction));cases+=1
        value=max(2*rank,4*(rank-1))*lam
        endpoints=[float(np.trace(moments(E,Z,q)[1])) for q in responses[:2]]
        assert math.isclose(max(endpoints),value,rel_tol=1e-11,abs_tol=1e-11)
        if lam==1.:risk_table.append({'rank':rank,'all_povm_minimax':value,'frame_walsh_minimax':4*rank,'outcomes':len(E)})
    checks['flat_spectrum_povm']={'cases':cases,'max_errors':maxima}
    # Non-flat operator means: illustrates construction but no optimality assertion.
    err=0.;cases=0
    for rank in (2,3,5):
        N=8;U=np.vstack((np.zeros(rank),np.linalg.qr(rng.normal(size=(N-1,rank)))[0]))
        V=np.eye(rank);sig=np.geomspace(1,.1,rank);T=U*sig;E,Z=character_povm(U,V,sig);s=float(sig@sig)
        for _ in range(8):
            q=rng.normal(size=N);q/=np.linalg.norm(q);z=U.T@q
            mean,cov=moments(E,Z,q)
            target=2*s*(1+float(z@z))-4*float(np.sum(sig**2*z**2))
            err=max(err,abs(float(np.trace(cov))-target),float(abs(mean-2*T.T@q).max()));cases+=1
    checks['anisotropic_upper_only']={'cases':cases,'max_error':err}
    # Unrelated redundant projective mixtures and exact operator reconstruction.
    min_gap=math.inf; min_average_gap=math.inf; residual=0.;cases=0
    for rank in (1,2,3):
      for repeat in range(5):
        N=4;D=N+1;basis=[]
        for _ in range(D+3):
            O=np.linalg.qr(rng.normal(size=(D,D)))[0]
            basis.extend(np.outer(O[:,j],O[:,j])/(D+3) for j in range(D))
        E=np.array(basis);design=E.reshape(len(E),-1).T
        T=np.zeros((N,rank));T[1:rank+1]=np.eye(rank)
        scores=[]
        for j in range(rank):
            alpha=float(rng.normal())
            M=np.diag(np.r_[alpha,np.full(N,-alpha)])
            M[0,1:]=2*T[:,j];M[1:,0]=2*T[:,j]
            z=np.linalg.lstsq(design,M.ravel(),rcond=None)[0]
            residual=max(residual,float(abs(design@z-M.ravel()).max()));scores.append(z)
        Z=np.array(scores).T
        _,cov=moments(E,Z,np.eye(N)[0]);min_gap=min(min_gap,float(np.trace(cov))-2*rank)
        av=np.mean([np.trace(moments(E,Z,sgn*np.eye(N)[i+1])[1]) for i in range(rank) for sgn in (-1,1)])
        min_average_gap=min(min_average_gap,float(av)-4*(rank-1));cases+=1
    checks['general_povm_bounds']={'cases':cases,'minimum_reference_gap':min_gap,'minimum_axis_average_gap':min_average_gap,'max_unbiased_operator_residual':residual}
    # Independently enumerate established upper bound, without using its formula.
    err=0.;cases=0
    for n in (1,2,3):
      N=1<<n
      for _ in range(4):
        T=rng.normal(size=(N,3));T[0]=0;s=float(np.sum(T*T))
        for q in (np.eye(N)[0],rng.normal(size=N)):
            q=q/np.linalg.norm(q);mean,cov=full_mask_moments(T,q)
            desired=4*T.T@np.diag(1-q*q)@T
            err=max(err,float(abs(cov-desired).max()),float(abs(mean-2*T.T@q).max()))
            assert np.trace(cov)<=4*s+1e-10;cases+=1
    checks['full_mask_born_check']={'cases':cases,'max_error':err}
    # Independent cone compiler, matched against the preserved full-state fixture.
    fixture=load_fixture();err=0.;zero=0.;norm=0.;cases=0
    for n in range(2,7):
      for depth in (1,2,3):
        local=compile_local(n,depth,rng)
        dense=fixture.make_circuit(n,depth,rng,angles=local['angles'])
        for I,tau,J,reference in zip(local['intervals'],local['taus'],dense.cones,dense.taus):
            assert I==J
            err=max(err,float(abs(tau-reference).max()));norm=max(norm,abs(float(tau@tau)-1));zero=max(zero,abs(float(tau[0])));cases+=1
    checks['local_compiler_equivalence']={'cases':cases,'max_error':err,'max_norm_error':norm,'max_reference_amplitude':zero}
    # Same physical family: one disjoint-block layer has flat spectrum at zero,
    # and uniformly near-flat spectrum in an n-independent small-angle box.
    largest_zero_error=0.; min_nearflat_margin=math.inf; flat_cases=0; box_cases=0
    for n in (2,4,8,16,32,64,128):
        st=structure(n,1,rng);loc=compile_local(n,1,rng,angles=np.zeros(len(st[0])))
        for left in range(0,n-1,2):
            columns=[]
            for I,tau in zip(loc['intervals'],loc['taus']):
                if left<=I[0] and I[-1]<=left+1:
                    vec=np.zeros(4)
                    for x,a in enumerate(tau):
                        label=sum(((x>>(len(I)-1-k))&1) << (1-(site-left)) for k,site in enumerate(I))
                        vec[label]=a
                    columns.append(vec)
            block=np.array(columns).T
            ev=np.linalg.eigvalsh(block@block.T)[1:]
            largest_zero_error=max(largest_zero_error,float(abs(ev-2).max()));flat_cases+=1
    for h in (.001,.01,.04,.08):
        for _ in range(10):
            loc=compile_local(2,1,rng,angles=rng.uniform(-h,h,6))
            block=np.zeros((4,6))
            for j,(I,tau) in enumerate(zip(loc['intervals'],loc['taus'])):
                for x,a in enumerate(tau):
                    label=sum(((x>>(len(I)-1-k))&1) << (1-site) for k,site in enumerate(I))
                    block[label,j]=a
            ev=np.linalg.eigvalsh(block@block.T)[1:]
            lower=(math.sqrt(2)-math.sqrt(220)*h)**2
            upper=(math.sqrt(2)+math.sqrt(220)*h)**2
            min_nearflat_margin=min(min_nearflat_margin,float(ev.min()-lower),float(upper-ev.max()));box_cases+=1
    assert min_nearflat_margin>=-1e-10
    checks['same_family_flat_and_open_box']={'zero_angle_blocks':flat_cases,'small_angle_blocks':box_cases,
        'max_zero_spectrum_error':largest_zero_error,'minimum_box_margin':min_nearflat_margin}
    # Chosen structural sequence, not a response-dependent acceptance sweep.
    growing=[]
    for n in (8,16,32,64,128):
        depth=math.ceil(math.log2(n)/2);local=compile_local(n,depth,rng)
        widths=[len(I) for I in local['intervals']];w=max(widths);P=len(widths);L=sum(len(t) for t in local['taus'])
        assert w<=2*depth
        assert all(abs(float(t@t)-1)<1e-10 and abs(float(t[0]))<1e-10 for t in local['taus'])
        beta_upper=(1<<w);eta=.125;k=0
        while beta_upper-1>2*eta*4**k:k+=1
        growing.append({'n':n,'depth':depth,'P':P,'w':w,'table_scalar_entries':L,
                        'local_gate_visits':local['visits'],'amplitude_kernel_entries':local['amplitude_kernel_entries'],
                        'full_state_entries_not_allocated':str(1<<n),'full_state_constructed':False,
                        'eta':eta,'beta_upper_bound':beta_upper,'conservative_parity_rounds':k,
                        'clean_parity_expected_cnot':2*n*k,'terminal_parity_expected_cnot':n*k,
                        'parity_cz':k,'direct_full_expected_cz':n*(n-1)/4,
                        'shifted_lookup_terms_per_gradient':P*4**k,
                        'gray_accumulator_entries_upper':sum(1<<len(I) for I in set(local['intervals'])),
                        'note':'Operation sizes, not total runtime or a winning-method claim. Independent centered local tables are fully materialized.'})
    checks['growing_depth_compilation']={'cases':len(growing),'largest_system':128,'max_width':max(x['w'] for x in growing),'full_state_constructed':False}
    for name,item in checks.items():
        for key,val in item.items():
            if key.startswith('max_') and isinstance(val,(int,float)) and key not in ('max_rank','max_width'):
                assert math.isfinite(val) and val<1e-9,(name,key,val)
    assert min_gap>=-1e-9 and min_average_gap>=-1e-9
    assert all(v<1e-9 for v in maxima.values())
    report={'status':'passed','seed':SEED,'environment':{'python':platform.python_version(),'numpy':np.__version__},
            'source_sha256':{str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                             'research/matched_readout/core.py':EXPECTED},
            'checks':checks,'exact_flat_spectrum_risks':risk_table,'growing_regime':growing,
            'elapsed_seconds':time.perf_counter()-started,
            'limits':'Finite logical diagnostics and local compiler operation sizes; no optimized-POVM numerical search, noise/hardware timing, external review, novelty certificate or strongest-method advantage.'}
    (args.output/'diagnostics.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
