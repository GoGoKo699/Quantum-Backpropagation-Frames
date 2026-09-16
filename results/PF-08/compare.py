"""Close the fixed PF-07 comparison; no new circuits, prices or winner search.

Consumes a verified PF-07 diagnostic record. Quantum-only cost crossovers are
explicitly projections, NOT total-work rankings. Complete costs remain affine
in the common response, compilation, streaming and output costs.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import unittest

PF07_HASHES = {
    'study.py': '43f5ca1d30d0ce390fa04505c69f6e5a301c409d4c67a3921b8d60e413795faf',
    'compiler.py': 'e72813edd9883240e9f1efe903aafc7dee86404eaae9ea2349501174738b6efa'}
BASELINE = 'a70b840c321ecfbea2f26fd40a459aef7153b068'


def relation(a: float, b: float) -> str:
    if math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-10):
        return 'equal_within_tolerance'
    return 'lower' if a < b else 'higher'


def affine_difference(ks: int, kf: int, fs: float, ff: float,
                      rs: float, rf: float) -> tuple[float, float]:
    """W_s-W_f = slope*C + intercept; F includes final output costs."""
    return ks-kf, fs-ff+ks*rs-kf*rf


def quantum_readout(row: dict) -> dict[str, float]:
    """Projection of PF-02 gate_weighted prices. NO classical or compile cost.

Uses emitted PF-07 gates (not optimal synthesis) and a valid direct full mask
(not optimal masking). n+1 final measurement operations are counted on all sides.
The common response circuit is the FREE VARIABLE C, not omitted or set to zero.
"""
    n = row['n']
    product = 1.1*(n+1)  # 0.1 per H, 1 per measurement (existing price profile)
    return {'reference': row['cnot']+0.1*(row['ry']+3)+(n+1),
            'no_mask': product,
            'full_direct': product+n*(n-1)/4}


def crossing(bs: float, bf: float, qs: float, qf: float) -> dict:
    """Continuous K~B crossover of quantum-only projection, not a confidence optimum."""
    slope = bs-bf
    intercept = bs*qs-bf*qf
    if math.isclose(slope, 0, rel_tol=0, abs_tol=1e-9*max(bs,bf)):
        return {'type': 'response_cost_cancels', 'reference_minus_comparator': intercept}
    value = -intercept/slope
    return {'type': 'reference_below_projection_when_C_greater' if slope<0 else
            'reference_below_projection_when_C_less', 'C_boundary': value}


def validate(data: dict) -> None:
    if data.get('status') != 'passed' or data.get('seed') != 2026091607:
        raise ValueError('Wrong or unsuccessful PF-07 input')
    if data.get('source_hashes') != PF07_HASHES:
        raise ValueError('PF-07 code hash does not match frozen baseline')
    rows = data['small_family_points']
    expected = {(n,d,a) for n in (3,4,5,6,8) for d in (1,2,3)
                for a in ('zero','seeded')}
    actual = {(x['n'],x['depth'],x['angles']) for x in rows}
    if len(rows)!=30 or actual!=expected:
        raise ValueError('Small grid changed')
    large=data['compiler_only']
    if len(large)!=10 or {(x['n'],x['regime']) for x in large} != {
            (n,r) for n in (16,32,64,128,256) for r in ('depth2','growing')}:
        raise ValueError('Compiler grid changed')
    for r in rows+large:
        if not math.isclose(r['s'],r['P'],rel_tol=1e-12,abs_tol=1e-12):
            raise ValueError('Raw-coordinate normalization changed')
    for r in rows:
        for k in ('sparse_exact_risk_small','all_X_exact_risk_small','s'):
            if not math.isfinite(r[k]) or r[k]<=0: raise ValueError('Invalid risk')
        if r['sparse_exact_risk_small']>4*r['s']+1e-8:
            raise ValueError('Frozen 4s bound not reproduced')
    for r in large:
        if r['global_state_allocated'] or r['program_retained']:
            raise ValueError('Unexpected scaling implementation')


class AlgebraChecks(unittest.TestCase):
    def test_equal_budget_cancellation(self):
        self.assertEqual(affine_difference(100,100,8,3,20,10),(0,1005))
    def test_different_budget_sign(self):
        a,b=affine_difference(50,100,0,0,30,10)
        self.assertEqual((a,b),(-50,500)); self.assertEqual(a*10+b,0)
    def test_flat_ratio(self):
        for r in range(1,65):
            optimum=max(2*r,4*(r-1)); self.assertTrue(2*r<=optimum<=4*r)
            if r>=3:self.assertAlmostEqual(4*r/optimum,r/(r-1))
    def test_full_mask_mean(self):
        for n in range(1,5):
            e=n*(n-1)//2
            self.assertEqual(sum(i.bit_count() for i in range(1<<e))/(1<<e),n*(n-1)/4)
    def test_reject_nonfinite(self):
        corrupt=json.loads(json.dumps(self.data))
        corrupt['small_family_points'][0]['sparse_exact_risk_small']=float('nan')
        with self.assertRaises(ValueError):validate(corrupt)
    def test_equal_crossing_not_divide_zero(self):
        self.assertEqual(crossing(12,12,8,4)['type'],'response_cost_cancels')
    def test_counterexample_to_quantum_only_ranking(self):
        # A cheap quantum readout can lose after legitimate classical work is added.
        self.assertLess(100*4,100*8)
        self.assertGreater(100*(4+100),100*(8+1))
    def test_known_readout_projection(self):
        out=quantum_readout({'n':3,'cnot':17,'ry':12})
        self.assertAlmostEqual(out['reference'],22.5)
        self.assertAlmostEqual(out['no_mask'],4.4)
        self.assertAlmostEqual(out['full_direct'],5.9)


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();data=json.loads(a.input.read_text());validate(data)
    a.output.mkdir(parents=True,exist_ok=False)
    AlgebraChecks.data=data
    with (a.output/'tests.log').open('w') as log:
        result=unittest.TextTestRunner(stream=log,verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(AlgebraChecks))
    if not result.wasSuccessful():raise RuntimeError('Algebra checks failed')
    rows=[];projections=[]
    for r in data['small_family_points']:
        bs=r['sparse_exact_risk_small'];bx=r['all_X_exact_risk_small'];bf=4*r['s']
        row={k:r[k] for k in ('n','depth','angles','P','w')}
        row.update(reference_variance=bs,no_mask_variance=bx,full_mask_variance=bf,
                   reference_vs_full=relation(bs,bf),reference_vs_no_mask=relation(bs,bx),
                   no_mask_over_reference=bx/bs,full_over_reference=bf/bs)
        rows.append(row)
        q=quantum_readout(r)
        projections.append({'case':{k:r[k] for k in ('n','depth','angles')},
            'quantum_cost_projection':q,
            'versus_no_mask':crossing(bs,bx,q['reference'],q['no_mask']),
            'versus_full_direct':crossing(bs,bf,q['reference'],q['full_direct']),
            'not_total_work':True})
    scaling=[]
    for r in data['compiler_only']:
        q=quantum_readout(r)
        # Same validated conservative B=4P prescription: EXACT equal integer budgets.
        k=4000*r['P']  # epsilon=delta=0.1; (delta epsilon^2)^(-1)=1000
        row={z:r[z] for z in ('regime','n','depth','P','w','cnot','ry',
            'local_tangent_entries','word_model_stream_bound','max_intervals_per_site')}
        row.update(shots_reference_and_full=k,direct_full_expected_CZ=r['n']*(r['n']-1)/4,
          additional_quantum_projection=q['reference']-q['full_direct'],
          response_cost_difference_coefficient=0,
          required_classical_saving_per_record=q['reference']-q['full_direct'],
          extra_fixed_cost_term='+(F_reference-F_full)/K; F includes final output',
          oneq_price=0.1,entangling_price=1.0,
          actual_stream_operations_not_benchmarked=True)
        scaling.append(row)
    summary={'status':'passed','baseline':BASELINE,'input_sha256':hashlib.sha256(a.input.read_bytes()).hexdigest(),
        'input_source_hashes':data['source_hashes'],'environment':{'python':platform.python_version()},
        'analysis_tests':result.testsRun,'small_points':len(rows),'compiler_points':len(scaling),
        'small_results':{
            'reference_lower_than_no_mask':sum(r['reference_vs_no_mask']=='lower' for r in rows),
            'reference_lower_than_full':sum(r['reference_vs_full']=='lower' for r in rows),
            'reference_equal_to_full_numerically':sum(r['reference_vs_full']=='equal_within_tolerance' for r in rows),
            'reference_larger_than_full':sum(r['reference_vs_full']=='higher' for r in rows),
            'maximum_no_mask_over_reference':max(r['no_mask_over_reference'] for r in rows),
            'maximum_full_over_reference':max(r['full_over_reference'] for r in rows)},
        'equal_budget_cases':len(scaling),'profiles_searched':0,'new_circuit_cases':0,
        'quantum_projection_note':'Existing PF-02 gate_weighted gate/measurement prices only. Classical costs, memory and compilation remain explicit variables; no total winner is selected.',
        'total_work_decision':'No strongest-method end-to-end advantage established. Quantum-only crossovers are not acceptance wins.',
        'scope_decision':'FREEZE exploratory expansion; exact finite real globally-unbiased theorem plus attaining measurement and existing local realization are the candidate Letter core.',
        'not_submission_ready':['Exact-result novelty not cleared','Human expert significance/assumption review pending','Original end-to-end advantage milestone remains unmet'],
        'evidence_boundary':'Reanalysis of fixed verified PF-07 output, not a new gate simulator or proof audit. Existing diagnostics may be rerun separately.',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    for name,records in [('small_comparison.csv',rows),('scaling_tradeoff.csv',scaling)]:
        with (a.output/name).open('w',newline='') as h:
            w=csv.DictWriter(h,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    (a.output/'quantum_projection.json').write_text(json.dumps(projections,indent=2)+'\n')
    (a.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
