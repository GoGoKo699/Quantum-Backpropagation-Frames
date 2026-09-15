"""PF-05 bounded independent POVM audit. Does not import PF-04 formula code.

NumPy + standard library only. Explicit effects and Born probabilities check
premises, not a numerical search over every POVM. No source files are rewritten.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import time
import numpy as np

SEED = 2026091581
TOL = 2e-9


def close(a, b, label):
    err = float(np.max(np.abs(np.asarray(a) - np.asarray(b)), initial=0))
    if not math.isfinite(err) or err > TOL:
        raise AssertionError(f'{label}: {err}')
    return err


def group():
    return {'cases': 0, 'max_residual': 0.0}


def record(g, *errors):
    g['cases'] += 1
    g['max_residual'] = max(g['max_residual'], *errors)


def orthogonal(rng, n, r, complex_=False):
    a = rng.normal(size=(n, r))
    if complex_:
        a = a + 1j*rng.normal(size=(n, r))
    return np.linalg.qr(a, mode='reduced')[0]


def basis(rng, r, extra=2):
    n = 1 << r.bit_length()  # n > r, leaving a genuine response nuisance direction
    U = np.zeros((n, r))
    U[1:] = orthogonal(rng, n-1, r)
    V = orthogonal(rng, r+extra, r)
    return U, V


def sparse_measurement(U, V, lam):
    """2r active effects + one complementary effect; direct effect construction."""
    n, r = U.shape
    d = n+1
    a = np.eye(d)[0]
    B = np.vstack((np.zeros((1, r)), U))
    effects, scores = [], []
    for i in range(r):
        for sign in (-1, 1):
            v = (a + sign*np.sqrt(r)*B[:, i])/np.sqrt(2*r)
            effects.append(np.outer(v, v))
            scores.append(sign*2*np.sqrt(r*lam)*V[:, i])
    effects.append(np.eye(d)-np.outer(a, a)-B@B.T)
    scores.append(np.zeros(V.shape[0]))
    return np.array(effects), np.array(scores)


def character_measurement(U, V, lam):
    """Independent binary-character version, for comparison with the supplied POVM."""
    n, r = U.shape
    ell = (r-1).bit_length()
    m = 1 << (ell+1)
    labels = [1 << ell | i for i in range(r)]
    C = np.array([[1-2*((y & L).bit_count() & 1) for L in labels] for y in range(m)])
    a = np.eye(n+1)[0]
    B = np.vstack((np.zeros((1,r)), U))
    vectors = (a[None,:] + C@B.T)/np.sqrt(m)
    E = np.einsum('wa,wb->wab', vectors, vectors)
    E = np.concatenate((E, (np.eye(n+1)-np.outer(a,a)-B@B.T)[None,:,:]))
    Z = np.vstack((2*np.sqrt(lam)*C@V.T, np.zeros(V.shape[0])))
    return E, Z


def born(E, Z, q):
    psi = np.r_[1., q]/np.sqrt(2.)
    p_complex = np.einsum('a,wab,b->w', psi.conj(), E, psi)
    close(p_complex.imag, 0., 'real Born probabilities')
    p = p_complex.real
    if p.min() < -TOL:
        raise AssertionError('negative Born probability')
    close(p.sum(), 1., 'probability normalization')
    mu = p@Z
    covariance = Z.T@(p[:,None]*Z)-np.outer(mu,mu)
    return p, mu, covariance


def target_operator(T):
    n,p = T.shape
    M = np.zeros((p,n+1,n+1))
    M[:,0,1:] = 2*T.T
    M[:,1:,0] = 2*T.T
    return M


def test_attainers(rng):
    g=group(); op=group(); comparison=group(); table=[]
    for r in range(1,17):
        for lam in (0.5, 1., 2.):
            U,V = basis(rng,r)
            n=U.shape[0]; T=np.sqrt(lam)*U@V.T
            E,Z=sparse_measurement(U,V,lam)
            F,W=character_measurement(U,V,lam)
            aerr=close(E.sum(axis=0),np.eye(n+1),'sparse completeness')
            mineig=min(float(np.linalg.eigvalsh(e).min()) for e in E)
            if mineig < -TOL: raise AssertionError('effect not positive')
            merr=close(np.einsum('wj,wab->jab',Z,E),target_operator(T),'operator unbiasedness')
            record(op,aerr,max(0.,-mineig),merr)
            e0=np.eye(n)[0]
            qlist=[e0,U[:,0],-U[:,0]]
            direction=rng.normal(size=r);direction/=np.linalg.norm(direction)
            for weight in (.1,.5,.9):
                qlist.append(np.sqrt(weight)*U@direction+np.sqrt(1-weight)*e0)
            for _ in range(2):
                q=rng.normal(size=n);q/=np.linalg.norm(q);qlist.append(q)
            for q in qlist:
                _,mu,cov=born(E,Z,q)
                z=U.T@q; h=float(z@z)
                ideal=2*r*lam+(2*r-4)*lam*h
                record(g,close(mu,2*T.T@q,'sparse mean'),close(np.trace(cov),ideal,'sparse risk'))
                _,mu2,cov2=born(F,W,q)
                record(comparison,close(mu2,mu,'character mean'),close(np.trace(cov2),np.trace(cov),'equal trace risk'))
            r0=float(np.trace(born(E,Z,e0)[2])); r1=float(np.trace(born(E,Z,U[:,0])[2]))
            close(max(r0,r1),lam*max(2*r,4*(r-1)),'attained minimax')
            if lam==1:
                table.append({'rank':r,'minimax_risk':max(r0,r1),'sparse_outcomes':len(E),
                              'character_outcomes':len(F),'frame_walsh_risk':4*r})
    return {'sparse_Born':g,'sparse_operator_contract':op,'character_comparison':comparison},table


def test_nuisance_and_nulls(rng):
    g=group(); contrast=[]
    for r in range(1,9):
        U,V=basis(rng,r,extra=3); E,Z=sparse_measurement(U,V,1.)
        n=U.shape[0]; q=np.sqrt(.25)*U[:,0]+np.sqrt(.75)*np.eye(n)[0]
        p,mu,cov=born(E,Z,q)
        expected_prob=(1+.25)/2
        # The unused sector is an outcome, not uncounted failed postselection.
        record(g,close(p[:-1].sum(),expected_prob,'active probability'))
        conditional=(p[:-1]@Z[:-1])/p[:-1].sum()
        close(conditional,mu/expected_prob,'conditional bias factor')
        if np.linalg.norm(conditional-mu)<.1: raise AssertionError('postselection bias not detected')
        null=np.linalg.svd(V.T,full_matrices=True)[2][r]
        E2=np.repeat(E/2,2,axis=0)
        Z2=np.repeat(Z,2,axis=0)+np.tile([1.,-1.],len(E))[:,None]*null
        _,mu2,C2=born(E2,Z2,q)
        projected=Z2@V@V.T
        _,mup,Cp=born(E2,projected,q)
        record(g,close(mu2,mu,'null noise mean'),close(np.trace(C2)-np.trace(cov),1.,'null risk increment'),
               close(mup,mu,'projected mean'),close(Cp,cov,'projected covariance'))
        contrast.append({'rank':r,'active_probability':float(p[:-1].sum()),
                         'renormalized_bias_norm':float(np.linalg.norm(conditional-mu))})
    return g,contrast


def test_general_measurements(rng):
    g=group(); gaps=[]; realify=group()
    for n in (2,3,4,5):
        for r in (1,n-1):
            for _ in range(2):
                U=np.zeros((n,r));U[1:]=orthogonal(rng,n-1,r)
                d=n+1; m=3*d*d
                A=orthogonal(rng,m,d,complex_=True)
                Ec=np.einsum('wa,wb->wab',A.conj(),A)
                E=Ec.real
                T=U
                targets=target_operator(T)
                Z=np.linalg.lstsq(E.reshape(m,-1).T,targets.reshape(r,-1).T,rcond=1e-12)[0]
                residual=close(np.einsum('wj,wab->jab',Z,E),targets,'general unbiased operators')
                e0=np.eye(n)[0]
                _,_,C0=born(E,Z,e0)
                axes=[np.trace(born(E,Z,sign*U[:,i])[2]) for i in range(r) for sign in (-1.,1.)]
                gap0=float(np.trace(C0)-2*r)
                gap1=float(np.mean(axes)-4*(r-1))
                if min(gap0,gap1)<-TOL: raise AssertionError('lower-bound violation')
                # Refine each real effect, retaining the score. Explicitly check both Cauchy inequalities.
                ref_vectors=[]; ref_scores=[]
                for e,z in zip(E,Z):
                    lam,Q=np.linalg.eigh(e)
                    if lam.min()<-TOL:raise AssertionError('realification not PSD')
                    for value,vector in zip(lam,Q.T):
                        if value>1e-12:
                            ref_vectors.append(np.sqrt(value)*vector);ref_scores.append(z)
                R=np.array(ref_vectors); S=np.array(ref_scores)
                x=R[:,0]; y=R[:,1:]@U; norms=np.sum(S*S,axis=1)
                lhs=float(np.sum(x*np.sum(S*y,axis=1)))
                aa=float(np.sum(norms*x*x));bb=float(np.sum(norms*np.sum(y*y,axis=1)))
                err=close(lhs,2*r,'rank-one cross moment')
                if min(aa-4*r,bb-4*r*r)<-TOL:raise AssertionError('Cauchy premise failed')
                for j in range(r):
                    Qj=np.einsum('w,wab->ab',Z[:,j]**2,E)
                    if np.linalg.eigvalsh(Qj-targets[j]@targets[j]).min()<-TOL:
                        raise AssertionError('operator moment inequality failed')
                q=rng.normal(size=n);q/=np.linalg.norm(q)
                p0,m0,c0=born(Ec,Z,q);p1,m1,c1=born(E,Z,q)
                record(realify,close(p0,p1,'realified probabilities'),close(m0,m1,'realified mean'),close(c0,c1,'realified moments'))
                record(g,residual,err)
                gaps.append({'N':n,'rank':r,'reference_lower_slack':gap0,'axis_average_lower_slack':gap1})
    return g,realify,gaps


def test_dilation():
    g=group()
    for r in range(1,33):
        # Outcome rows: (i,-), (i,+). Column zero = reference, then r tangent basis vectors.
        W=np.zeros((2*r,r+1))
        for i in range(r):
            for k,sgn in enumerate((-1.,1.)):
                W[2*i+k,0]=1/np.sqrt(2*r)
                W[2*i+k,i+1]=sgn/np.sqrt(2)
        record(g,close(W.T@W,np.eye(r+1),'Naimark isometry'))
    return g


def test_boundary_contrasts(rng):
    g=group(); cases=[]
    for r in (1,2,3,5):
        U,V=basis(rng,r); E,Z=sparse_measurement(U,V,1.)
        # Outside real-response contract: same mean estimates Re q, not the real risk formula.
        q=1j*U[:,0]
        _,mu,C=born(E,Z,q)
        record(g,close(mu,0.,'imaginary response mean'),close(np.trace(C),4*r,'imaginary response risk'))
        # Convexifying the parameter family changes variance, even though first moments remain valid.
        ps=[]
        for i in range(r):
            for sgn in (-1.,1.):ps.append(born(E,Z,sgn*U[:,i])[0])
        pm=np.mean(ps,axis=0); mm=pm@Z
        Cm=Z.T@(pm[:,None]*Z)-np.outer(mm,mm)
        record(g,close(np.trace(Cm),4*r,'mixture risk'))
        cases.append({'rank':r,'pure_real_minimax':max(2*r,4*(r-1)),
                      'imaginary_response_risk':float(np.trace(C)),
                      'axis_mixture_risk':float(np.trace(Cm)),
                      'biased_zero_worst_MSE':4.})
    # Same optimal trace does not mean identical coordinate covariance.
    U=np.zeros((4,3));U[1:]=np.eye(3);V=np.eye(3)
    E,Z=sparse_measurement(U,V,1.);F,W=character_measurement(U,V,1.)
    q=np.r_[0.,np.ones(3)/np.sqrt(3)]
    _,_,c=born(E,Z,q);_,_,d=born(F,W,q)
    record(g,close(np.trace(c),np.trace(d),'trace not matrix objective'))
    if np.linalg.norm(c-d)<.5:raise AssertionError('covariance distinction absent')
    return g,cases,{'sparse_covariance':c.tolist(),'character_covariance':d.tolist()}


def test_local_fisher(rng):
    g=group(); example=None
    for r in (2,3,5):
        n=r+2;d=n+1
        U=np.eye(n)[:,1:r+1];q=U[:,0]
        psi=np.r_[1.,q]/np.sqrt(2)
        tangent=np.linalg.svd(q[None,:],full_matrices=True)[2][1:].T
        psi_d=np.vstack((np.zeros((1,n-1)),tangent))/np.sqrt(2)
        O=orthogonal(rng,d,d)
        amplitudes=O@psi; da=O@psi_d
        p=amplitudes**2; derivatives=2*amplitudes[:,None]*da
        if p.min()<1e-12:raise AssertionError('unexpected singular measurement probabilities')
        fisher=derivatives.T@(derivatives/p[:,None])
        J=2*U.T@tangent
        local_score=(2*U.T@q)[None,:]+(derivatives/p[:,None])@np.linalg.solve(fisher,J.T)
        mu=p@local_score
        cov=local_score.T@(p[:,None]*local_score)-np.outer(mu,mu)
        record(g,close(fisher,2*np.eye(n-1),'real-model Fisher matrix'),
               close(mu,2*U.T@q,'local unbiased mean'),close(derivatives.T@local_score,J.T,'local unbiased derivative'),
               close(np.trace(cov),2*(r-1),'local risk not global minimax'))
        qalt=-q; palt=(O@np.r_[1.,qalt]/np.sqrt(2))**2
        bias=float(np.linalg.norm(palt@local_score-2*U.T@qalt))
        if bias<.1:raise AssertionError('local decoder unexpectedly globally unbiased')
        if r==3:example={'rank':r,'pointwise_local_risk':float(np.trace(cov)),
                         'global_unbiased_minimax':8.,'opposite_point_bias':bias}
    return g,example


def test_block_stability(rng):
    g=group(); h=.015
    I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
    A=[np.kron(a,b) for a,b in ((Y,I),(I,Y),(Y,X),(X,Y),(Y,Z),(Z,Y))]
    e=np.eye(4)[:,0]
    zero=np.column_stack([(-1j*a@e).real for a in A])
    close(np.linalg.svd(zero,compute_uv=False)[:3],np.sqrt(2)*np.ones(3),'zero block spectrum')
    min_margin=float('inf')
    for _ in range(40):
        angles=rng.uniform(-h,h,6); prefix=np.eye(4,dtype=complex);cols=[]
        for angle,a in zip(angles,A):
            cols.append(-1j*prefix.conj().T@a@prefix@e)
            prefix=(np.cos(angle)*np.eye(4)-1j*np.sin(angle)*a)@prefix
        T=np.column_stack(cols)
        change=np.linalg.norm(T.real-zero,2)
        bound=np.sqrt(220)*h
        if change>bound+TOL:raise AssertionError('small-angle perturbation bound')
        sing=np.linalg.svd(T.real,compute_uv=False)[:3]
        margin=min(sing.min()-(np.sqrt(2)-bound),(np.sqrt(2)+bound)-sing.max())
        if margin<-TOL:raise AssertionError('small-angle spectrum')
        min_margin=min(min_margin,float(margin))
        record(g,close(T.imag,0.,'real block'),close(T[0],0.,'zero reference row'))
    g['minimum_singular_bound_margin']=min_margin
    return g


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(); out=args.output.resolve()
    here=Path(__file__).resolve().parent
    if out==here or out.is_relative_to(here):
        parser.error('Generated output must be outside the source packet')
    out.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter();rng=np.random.default_rng(SEED)
    report={'status':'running','seed':SEED,'environment':{'python':platform.python_version(),'numpy':np.__version__},
            'audit_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'imports_prior_formula_code':False,'tolerance':TOL,'checks':{}}
    try:
        checks,table=test_attainers(rng);report['checks'].update(checks);report['exact_risk_table']=table
        a,b=test_nuisance_and_nulls(rng);report['checks']['nuisance_and_null_outputs']=a;report['renormalization_contrasts']=b
        a,b,c=test_general_measurements(rng);report['checks']['arbitrary_redundant_POVMs']=a;report['checks']['complex_effect_realification']=b;report['lower_bound_slacks']=c
        report['checks']['explicit_dilation']=test_dilation()
        a,b,c=test_boundary_contrasts(rng);report['checks']['contract_boundaries']=a;report['out_of_contract']=b;report['nonunique_optimal_covariances']=c
        a,b=test_local_fisher(rng);report['checks']['local_Fisher_contrast']=a;report['local_not_global']=b
        report['checks']['same_family_stability']=test_block_stability(rng)
        report['status']='passed'
    except Exception as exc:
        report['status']='failed';report['error']=f'{type(exc).__name__}: {exc}'
    report['elapsed_seconds']=time.perf_counter()-started
    report['limits']='Independent finite checks, not optimization over all POVMs, an interval proof, external peer review, novelty clearance, hardware implementation or advantage benchmark.'
    (out/'diagnostics.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps(report,indent=2,allow_nan=False))
    if report['status']!='passed':raise SystemExit(1)

if __name__=='__main__':main()
