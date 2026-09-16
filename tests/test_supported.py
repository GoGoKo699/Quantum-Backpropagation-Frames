"""Maintained-package migration equivalence and public contract regressions."""
import hashlib
import importlib.util
from pathlib import Path
import sys
import unittest
import warnings
import numpy as np
from qbp_frames import disjoint, intervals, local, parity

ROOT = Path(__file__).resolve().parents[1]


def fixture(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT/relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class MigrationEquivalence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old_disjoint = fixture('results/PF-06/compiler.py', '_supported_pf06')
        cls.old_intervals = fixture('results/PF-07/compiler.py', '_supported_pf07')
        cls.old_local = fixture('results/PF-04/study.py', '_supported_pf04')

    def test_packaged_parity_kernel_identity(self):
        expected = (ROOT/'research/parity_frames/core.py').read_bytes()
        actual = (ROOT/'qbp_frames/_parity_reference.py').read_bytes()
        self.assertEqual(actual, expected)
        self.assertEqual(hashlib.sha256(actual).hexdigest(), parity._SHA)

    def test_disjoint_nonzero_and_flat_equivalence(self):
        for angles in (np.zeros((1,6)), np.linspace(-.4,.4,12).reshape(2,6)):
            maintained = disjoint.compile_plan(angles)
            original = self.old_disjoint.compile_plan(angles)
            for attribute in ('angles', 'K', 'row_energy'):
                np.testing.assert_array_equal(getattr(maintained, attribute), getattr(original, attribute))
            self.assertEqual(maintained.gates, original.gates)
            self.assertEqual(maintained.exact_risk_bound(), original.exact_risk_bound())
            for name in ('dense_tangents', 'dense_scores', 'reference_vector'):
                np.testing.assert_array_equal(getattr(disjoint,name)(maintained),
                                              getattr(self.old_disjoint,name)(original))
            counts=np.zeros((maintained.blocks,3)); counts[0,0]=3
            np.testing.assert_array_equal(maintained.finish(counts,7), original.finish(counts,7))
            q=np.zeros(1<<maintained.n);q[0]=1.
            self.assertEqual(disjoint.risk_from_coordinates(maintained,q),
                             self.old_disjoint.risk_from_coordinates(original,q))
            state=np.r_[q,q]/np.sqrt(2)
            np.testing.assert_array_equal(disjoint.apply_circuit(state,maintained.gates,maintained.n+1),
                self.old_disjoint.apply_circuit(state,original.gates,original.n+1))

    def test_interval_equivalence_and_streamed_scores(self):
        args=(3,[(0,1),(1,2)], [np.array([0.,1.,1.,1.])/np.sqrt(3)]*2)
        maintained=intervals.IntervalReference.from_tables(*args)
        original=self.old_intervals.IntervalReference.from_tables(*args)
        self.assertEqual(list(maintained.gates()), list(original.gates()))
        self.assertEqual(maintained.ledger(), original.ledger())
        accumulator=np.zeros(maintained.P)
        expected=np.zeros(maintained.P)
        for x in range(8):
            for bit in (0,1):
                bits=format(x,'03b')
                ids,score=maintained.score(bit,bits)
                old_ids,old_score=original.score(bit,bits)
                self.assertEqual(ids,old_ids)
                np.testing.assert_array_equal(score,old_score)
                maintained.add_record(accumulator,bit,bits)
                if ids: expected[list(ids)]+=score
        np.testing.assert_array_equal(maintained.finish(accumulator,16),expected/16)

    def test_source_table_equivalence(self):
        for n,depth in ((2,1),(4,2),(5,3)):
            angles=np.linspace(-.4,.5,local.parameter_count(n,depth))
            maintained=local.compile_local(n,depth,angles)
            original=self.old_local.compile_local(n,depth,np.random.default_rng(1),angles)
            for field in ('intervals','visits','amplitude_kernel_entries'):
                self.assertEqual(maintained[field],original[field])
            for a,b in zip(maintained['taus'],original['taus']):
                np.testing.assert_array_equal(a,b)
            plan,residual=local.reference_plan(maintained)
            self.assertLessEqual(residual,1e-10)
            self.assertEqual(plan.P,len(angles))
            self.assertTrue(all(t[0]==0 for t in plan.tables))

    def test_flat_example_unbiased_including_zero_outcomes(self):
        plan=disjoint.compile_plan(np.zeros((1,6)))
        q=np.array([np.sqrt(3)/2,.5,0,0]);c=disjoint.reference_vector(plan)
        prob=np.r_[(c+q)**2,(c-q)**2]/4
        Z=disjoint.dense_scores(plan)
        np.testing.assert_allclose(prob@Z,[0,1,0,0,0,1],atol=2e-14,rtol=0)
        self.assertAlmostEqual(prob[[0,4]].sum(),3/8)
        self.assertAlmostEqual(disjoint.risk_from_coordinates(plan,q),13)
        self.assertEqual(plan.exact_risk_bound(),16)
        self.assertGreater(np.linalg.norm((prob@Z)/(1-3/8)-prob@Z),.5)


class SupportedContracts(unittest.TestCase):
    def assert_invalid(self, function):
        with warnings.catch_warnings(record=True) as emitted:
            with self.assertRaises(ValueError): function()
            self.assertEqual(emitted,[])

    def test_disjoint_shapes_real_and_finite(self):
        for bad in (np.zeros((0,6)),np.zeros((1,5)),np.zeros((1,6),complex),
                    np.zeros((1,6),bool),np.full((1,6),np.nan),[['x']*6],[[0],[0,1]]):
            self.assert_invalid(lambda:disjoint.compile_plan(bad))
        plan=disjoint.compile_plan(np.zeros((1,6)))
        for q in ([1,1,0,0],[1,0],np.array([1,0,0,0],complex),[np.inf,0,0,0]):
            self.assert_invalid(lambda:disjoint.risk_from_coordinates(plan,q))

    def test_count_contract_and_inactive_denominator(self):
        plan=disjoint.compile_plan(np.zeros((1,6)))
        for shots in (0,-1,True,1.,np.nan,2**53+1):
            self.assert_invalid(lambda:plan.finish([[0,0,0]],shots))
        for counts in ([[1.5,0,0]],[[2,0,0]],[[np.nan,0,0]],[[1+0j,0,0]],
                       [[1e308,1e308,1e308]],[[0,0]]):
            self.assert_invalid(lambda:plan.finish(counts,1))
        np.testing.assert_array_equal(plan.finish([[0,0,0]],3),np.zeros(6))
        for outcome in (-1,4,True,1.,np.nan):
            self.assert_invalid(lambda:plan.classify(outcome))

    def test_signed_count_exact_integer_boundary(self):
        plan=disjoint.compile_plan(np.zeros((1,6)))
        limit=2**53
        invalid=(
            [[limit+1,0,0]], [[limit+1,0.,0]],
            [[-(limit+1),0,0]], np.array([[limit+1,0,0]],dtype=np.int64),
            [[limit,1,0]], [[-limit,-1,0]],
            np.array([[limit,1,0]],dtype=np.float64),
        )
        for counts in invalid:
            self.assert_invalid(lambda:plan.finish(counts,limit))
        # Both endpoints and a total exactly on the boundary remain accepted.
        np.testing.assert_array_equal(plan.finish([[limit,0,0]],limit),
                                      plan.finish([[1,0,0]],1))
        np.testing.assert_array_equal(plan.finish([[-limit,0,0]],limit),
                                      plan.finish([[-1,0,0]],1))
        self.assertTrue(np.isfinite(plan.finish([[limit-1,1,0]],limit)).all())

    def test_real_gate_contracts(self):
        for gate in (('ry',0,np.nan),('x',True),('cx',0,0),('cx',0,2),('z',0),([],0)):
            self.assert_invalid(lambda:disjoint.apply_gate([1,0,0,0],gate,2))
        self.assert_invalid(lambda:disjoint.apply_gate(np.array([1,0],complex),('h',0),1))
        self.assert_invalid(lambda:disjoint.apply_gate([1e308,1e308],('h',0),1))
        for controls,target in (((True,),1),((-1,),1),((0,),0)):
            self.assert_invalid(lambda:disjoint.uc_rotation(controls,target,[0,0]))
        self.assert_invalid(lambda:disjoint.uc_rotation((0,),1,[1e308,1e308]))
        self.assert_invalid(lambda:disjoint.exchange_on_reference_zero(1,1,.2))
        self.assert_invalid(lambda:disjoint.apply_circuit([1,0],[],True))

    def test_interval_numeric_contracts(self):
        for table in ([0,1e-200,1,0],[0,1e308,1,0],[0,1,complex(0),0],
                      [0,np.nan,0,0],[1e-14,1,0,0],[0,0,0,0]):
            self.assert_invalid(lambda:intervals.IntervalReference.from_tables(2,[(0,1)],[table]))
        for interval in ((0,2),(-1,0),(True,),(1,0)):
            self.assert_invalid(lambda:intervals.IntervalReference.from_tables(3,[interval],[[0,1,1,1]]))
        self.assert_invalid(lambda:intervals.IntervalReference.from_tables(True,[(0,)],[[0,1]]))
        self.assert_invalid(lambda:intervals.IntervalReference.from_tables(2,None,None))
        self.assert_invalid(lambda:intervals.fwht([1e308,1e308]))

    def test_interval_record_contracts(self):
        plan=intervals.IntervalReference.from_tables(2,[(0,1)],[[0,1,0,0]])
        for bit,bits in ((True,'01'),(2,'01'),(0,'2'),(0,1),(0,'001')):
            self.assert_invalid(lambda:plan.score(bit,bits))
        for accumulator in (np.zeros(2),np.zeros(1,dtype=int),np.zeros(1,dtype=np.float32),
                            np.array([np.nan]),np.array([0j])):
            self.assert_invalid(lambda:plan.add_record(accumulator,0,'01'))
        frozen=np.zeros(1);frozen.flags.writeable=False
        self.assert_invalid(lambda:plan.add_record(frozen,0,'01'))
        self.assert_invalid(lambda:plan.finish([0],True))
        self.assert_invalid(lambda:plan.finish([0],0))
        for site in (-1,2,True):
            self.assert_invalid(lambda:list(plan.fill_gates(site)))
        # Sparse updates need not scan unrelated coordinates; finalization
        # validates the complete output once, including untouched entries.
        sparse=intervals.IntervalReference.from_tables(2,[(0,),(1,)],[[0,1],[0,1]])
        invalid=np.array([np.nan,0.])
        sparse.add_record(invalid,0,'01')
        self.assert_invalid(lambda:sparse.finish(invalid,1))

    def test_local_family_contracts(self):
        for n,depth in ((True,1),(1,1),(2,0),(2,1.5)):
            self.assert_invalid(lambda:local.compile_local(n,depth,np.zeros(6)))
        for angles in (np.zeros(5),np.zeros(6,complex),np.full(6,np.nan),np.zeros((1,6))):
            self.assert_invalid(lambda:local.compile_local(2,1,angles))


if __name__ == '__main__':
    unittest.main()
