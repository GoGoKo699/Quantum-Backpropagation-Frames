"""Independent contract and compiler tests for the maintained PF-02 interface."""
import unittest
import warnings
import numpy as np
from qbp_frames import parity as p
from qbp_frames import readout as r


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.T=np.array([[0.,0.],[.3,.2],[.1,-.4],[.8,.5]])
        self.q=np.array([.5,.5,.5,.5])

    def test_original_four_probes_rejected(self):
        T=self.T.copy(); T[1,0]=np.nan
        q=self.q.copy(); q[1]=np.nan
        phase=np.ones(4); phase[1]=np.nan
        for a,b,c in ((T,self.q,None),(self.T,q,None),
                       (self.T,self.q,phase),(self.T,self.q.astype(complex),None)):
            with self.subTest():
                with warnings.catch_warnings(record=True) as w:
                    with self.assertRaises(ValueError): p.measurement_moments(a,b,c)
                    self.assertEqual(len(w),0)

    def test_nonfinite_and_complex_all_array_positions(self):
        for bad in (np.nan,np.inf,-np.inf):
            for slot in ('T','q','phase'):
                args={'T':self.T.copy(),'q':self.q.copy(),'phase':np.ones(4)}
                args[slot].flat[1]=bad
                with self.subTest(bad=bad,slot=slot), self.assertRaises(ValueError):
                    p.measurement_moments(**args)
        for slot in ('T','q','phase'):
            args={'T':self.T,'q':self.q,'phase':np.ones(4)}
            args[slot]=args[slot].astype(complex)
            with self.assertRaises(ValueError): p.measurement_moments(**args)

    def test_no_coerced_strings_objects_or_bools(self):
        for a in (self.T.astype(str),self.T.astype(object),self.T.astype(bool)):
            with self.assertRaises(ValueError): p.validate_inputs(a,self.q)
        with self.assertRaises(ValueError): p.fwht([[1],[1,2]])

    def test_shapes_and_geometry(self):
        for T,q in ((np.zeros((3,2)),np.ones(3)/np.sqrt(3)),
                    (np.zeros((4,0)),self.q),(self.T,np.ones((4,1))),
                    (self.T,self.q*2),(self.T[:,:1].T,self.q),
                    (self.T+1,self.q)):
            with self.subTest(),self.assertRaises(ValueError): p.validate_inputs(T,q)

    def test_exact_sign_contract(self):
        for phase in ([1,1,0,1],[-1,1,1,1],[1,1,1+1e-13,1],[1,1]):
            with self.assertRaises(ValueError): p.measurement_moments(self.T,self.q,phase)

    def test_round_contract_all_entry_points(self):
        for rounds in (-1,1.2,True,np.nan,np.inf,1+0j,'1'):
            for f in (lambda:p.interpolated_covariance(self.T,self.q,rounds),
                      lambda:p.risk_bound(self.T,rounds),
                      lambda:p.covariance_risk_matrix(self.T,rounds)):
                with self.subTest(rounds=rounds),self.assertRaises(ValueError): f()

    def test_beta_eta_and_extreme_finite_scalars(self):
        for beta,eta in ((np.nan,.1),(np.inf,.1),(2,np.nan),(2,0),(.9,.1),(True,.1)):
            with self.assertRaises(ValueError): p.rounds_for_relative_bound(beta,eta)
        self.assertEqual(p.rounds_for_relative_bound(1,.1),0)
        self.assertGreater(p.rounds_for_relative_bound(1e308,1e-300),0)

    def test_local_masks_and_addresses(self):
        for pairs in ([(-1,0)],[(4,0)],[(1.2,0)],[(True,0)],[(1,)],None):
            with self.subTest(pairs=pairs),self.assertRaises(ValueError): p.parity_phase(2,pairs)
        for y in (-1,4,1.2,True):
            with self.assertRaises(ValueError): p.local_shift_score(np.ones(4),y,[(1,2)])
        with self.assertRaises(ValueError): p.quadratic_phase(2,2)
        with self.assertRaises(ValueError): p.parity_phase(0,[])

    def test_risk_functions_guard_tangents(self):
        for T in (self.T.astype(complex),np.full((4,2),np.nan)):
            for f in (p.imbalance,lambda a:p.risk_bound(a,2),lambda a:p.covariance_risk_matrix(a,2)):
                with self.assertRaises(ValueError): f(T)

    def test_numeric_overflow_is_not_success(self):
        T=self.T*1e308
        with self.assertRaises(ValueError): p.risk_bound(T,0)
        with self.assertRaises(ValueError): p.fwht([1e308,1e308])

    def test_valid_input_equivalence(self):
        rng=np.random.default_rng(2026091562)
        for n in range(1,6):
            for P in (1,3):
                T=rng.normal(size=(1<<n,P));T[0]=0
                q=rng.normal(size=1<<n);q/=np.linalg.norm(q)
                phase=p.parity_phase(n,[(1,(1<<n)-1)])
                for f in ('measurement_moments','full_quadratic_covariance'):
                    args=(T,q,phase) if f=='measurement_moments' else (T,q)
                    a=getattr(p,f)(*args);b=getattr(p._ref,f)(*args)
                    for x,y in zip(a,b) if isinstance(a,tuple) else [(a,b)]:
                        np.testing.assert_array_equal(x,y)
                for k in range(4):
                    np.testing.assert_array_equal(p.interpolated_covariance(T,q,k),
                                                   p._ref.interpolated_covariance(T,q,k))
                np.testing.assert_array_equal(p.covariance_risk_matrix(T,2),p._ref.covariance_risk_matrix(T,2))
                self.assertEqual(p.imbalance(T),p._ref.imbalance(T))
                self.assertEqual(p.risk_bound(T,2),p._ref.risk_bound(T,2))

    def test_no_input_mutation_and_shift_equivalence(self):
        T=self.T.copy();q=self.q.copy();p.measurement_moments(T,q)
        np.testing.assert_array_equal(T,self.T);np.testing.assert_array_equal(q,self.q)
        tau=np.array([0.,.2,-.4,.1]);table=p.fwht(tau)
        for y in range(4):
            self.assertAlmostEqual(p.local_direct_score(tau,y,[(1,3),(2,1)]),
                                   p.local_shift_score(table,y,[(1,3),(2,1)]))


class CompilerTests(unittest.TestCase):
    def test_exhaustive_phase_contract(self):
        for n in range(1,6):
            for mask in range(1<<(n*(n-1)//2)):
                phase=p.quadratic_phase(n,mask)
                for plan in (r.pivot(n,mask),r.greedy(n,mask)):
                    for x in range(1<<n):
                        self.assertEqual(plan.phase(x),phase[x]*(-1)**((plan.offset&x).bit_count()&1))

    def test_folded_born_distributions(self):
        rng=np.random.default_rng(2026091563)
        for n in range(1,6):
            for _ in range(8):
                N=1<<n;mask=int(rng.integers(1<<(n*(n-1)//2)))
                state=rng.normal(size=2*N)+1j*rng.normal(size=2*N)
                state=state.reshape(2,N);state/=np.linalg.norm(state)
                H=np.array([[(-1)**((x&y).bit_count()&1) for x in range(N)] for y in range(N)])/np.sqrt(N)
                Hanc=np.array([[1,1],[1,-1]])/np.sqrt(2)
                ideal=np.abs(Hanc@(state*p.quadratic_phase(n,mask))@H)**2
                for plan in r.portfolio(n,mask):
                    actual=np.zeros_like(state)
                    for x in range(N):actual[:,plan.address(x)]=state[:,x]*plan.phase(x)
                    prob=np.abs(Hanc@actual@H)**2
                    folded=np.zeros_like(prob)
                    for y in range(N):folded[:,plan.outcome(y)]+=prob[:,y]
                    np.testing.assert_allclose(folded,ideal,atol=2e-14,rtol=0)

    def test_terminal_parity_folded_born(self):
        rng=np.random.default_rng(2026091564)
        for n in range(1,5):
            N=1<<n
            H=np.array([[(-1)**((x&y).bit_count()&1) for x in range(N)] for y in range(N)])/np.sqrt(N)
            Hanc=np.array([[1,1],[1,-1]])/np.sqrt(2)
            for _ in range(8):
                a,b=map(int,rng.integers(N,size=2))
                state=rng.normal(size=(2,N))+1j*rng.normal(size=(2,N));state/=np.linalg.norm(state)
                work=np.zeros((2,N,4),complex)
                for x in range(N):
                    u=(a&x).bit_count()&1;v=(b&x).bit_count()&1
                    work[:,x,u+2*v]=state[:,x]*(-1)**(u*v)
                Hwork=np.kron(Hanc,Hanc)
                work=work@Hwork
                folded=np.zeros((2,N))
                for uv in range(4):
                    prob=np.abs(Hanc@work[:,:,uv]@H)**2
                    shift=(a if uv&1 else 0)^(b if uv&2 else 0)
                    for y in range(N):folded[:,y^shift]+=prob[:,y]
                ideal=np.abs(Hanc@(state*p.parity_phase(n,[(a,b)]))@H)**2
                np.testing.assert_allclose(folded,ideal,atol=2e-14,rtol=0)

    def test_greedy_does_not_increase_gate_count(self):
        rng=np.random.default_rng(2026091565)
        for n in (3,6,12,24):
            for _ in range(10):
                mask=sum(int(bit)<<i for i,bit in enumerate(rng.integers(2,size=n*(n-1)//2)))
                a,b=r.direct(n,mask),r.greedy(n,mask)
                self.assertLessEqual(len(b.cnots)+len(b.czs),len(a.czs))

    def test_gray_character(self):
        rng=np.random.default_rng(2026091567)
        for n in range(1,9):
            for _ in range(8):
                mask=sum(int(bit)<<i for i,bit in enumerate(rng.integers(2,size=n*(n-1)//2)))
                y=int(rng.integers(1<<n))
                expected=p.quadratic_phase(n,mask)*np.array([(-1)**((x&y).bit_count()&1) for x in range(1<<n)])
                np.testing.assert_array_equal(r.quadratic_character(n,mask,y),expected)

    def test_compiler_invalid_inputs(self):
        for f in (r.direct,r.greedy,r.pivot):
            for n,mask in ((0,0),(2,-1),(2,2),(2,True),(2,1.0)):
                with self.assertRaises(ValueError):f(n,mask)

if __name__=='__main__':unittest.main()
