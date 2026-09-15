"""Bounded priced acceptance sweep, not a hardware-runtime benchmark.

Exact expectations over all quadratic masks for n=2..5. Each sampled-mask
optimizer pays its synthesis work on every shot: the diagnostic's enumeration
cache is NOT free preprocessing available to the learner. The same conservative
Markov guarantee is used throughout. Unit prices are declared scenario inputs.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import sys
from collections import Counter
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from qbp_frames import parity as p
from qbp_frames import readout as r

SOURCE=ROOT/'research/matched_readout/core.py'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != 'd6eb8552943e6d6db0fe4137ea4ed8003f2b4ccc4257c4378a12338912597a01':
    raise RuntimeError('Fixture changed')
spec=importlib.util.spec_from_file_location('pf02_fixture',SOURCE)
f=importlib.util.module_from_spec(spec);sys.modules[spec.name]=f;spec.loader.exec_module(f)

PRICES={
 'gate_weighted':dict(cnot=1.,cz=1.,oneq=.1,word=.0001,measure=1.,reset=1.,memory=.0001),
 'classical_weighted':dict(cnot=1.,cz=1.,oneq=.1,word=1.,measure=1.,reset=1.,memory=.01),
 'reset_weighted':dict(cnot=1.,cz=1.,oneq=.1,word=.01,measure=20.,reset=50.,memory=.001),
}


def plan_costs(plans,price):
    """Direct, pivot, greedy and a portfolio paying for all three syntheses."""
    out={key:[] for key in ('direct','pivot','greedy','portfolio')}
    for three in plans:
        marginal=[len(x.cnots)*price['cnot']+len(x.czs)*price['cz']+
                  price['word']*(len(x.cnots)+1) for x in three]
        for x,cost in zip(three,marginal):
            out[x.method].append(cost+price['word']*x.synthesis_word_ops)
        out['portfolio'].append(min(marginal)+price['word']*sum(x.synthesis_word_ops for x in three))
    return {k:np.asarray(v) for k,v in out.items()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    eps=.1;delta=.1;denom=delta*eps*eps
    rng=np.random.default_rng(2026091566)
    masks={};compiler_stats=[]
    for n in range(2,6):
        bank=[r.portfolio(n,mask) for mask in range(1<<(n*(n-1)//2))]
        masks[n]=bank
        compiler_stats.append({'n':n,'masks':len(bank),
          'direct_mean_entangling':float(np.mean([len(x[0].czs) for x in bank])),
          'best_gate_mean_entangling':float(np.mean([min(len(y.czs)+len(y.cnots) for y in x) for x in bank])),
          'strict_gate_reductions':sum(min(len(y.czs)+len(y.cnots) for y in x)<len(x[0].czs) for x in bank),
          'scope':'Best-gate count alone; acceptance also charges all synthesis and relabeling.'})
    summary=[];allrows=[];circuits=[]
    for n in range(2,6):
      for depth in (1,2,3):
        c=f.make_circuit(n,depth,rng);P=len(c.angles)
        s=float(np.sum(c.T*c.T));beta=p.imbalance(c.T)
        RX=p.risk_bound(c.T,0)
        np.testing.assert_allclose(RX,f.walsh_second_bound_dp(c.cones,c.taus,n),atol=1e-9)
        intervals=sorted(set(c.cones));tables=sum(1<<len(I) for I in intervals)
        coeff=sum(len(t) for t in c.taus);w=max(map(len,c.cones))
        # Stated scalar-operation upper ledger, not measured Python timing.
        F_shared=sum(depth**2*len(t)+len(I)*len(t) for I,t in zip(c.cones,c.taus))
        F_beta=(2**w)*(n+P)
        F_hist=sum(len(I)*(1<<len(I)) for I in intervals)+coeff
        F_mask=coeff
        oneq_U=26*(P//6)
        memory=2*P+coeff+tables
        gate_oneq=[]
        for layer in range(depth):
            pairs=len(range(layer%2,n-1,2))
            for count in (1,1,7,7,5,5):gate_oneq += [count]*pairs
        circuits.append({'n':n,'depth':depth,'P':P,'s':s,'beta':beta,'w':w,
                         'intervals':[list(I) for I in intervals],'coefficient_words':coeff,
                         'accumulator_words':tables,'shared_preprocess_ops':F_shared,
                         'beta_preprocess_ops':F_beta,'source_angles':c.angles.tolist()})
        for profile,price in PRICES.items():
          costs=plan_costs(masks[n],price)
          for objective in (0.,10.,1000.,1e6):
            # lifecycle resets include all system/reference qubits each record
            common=objective+2*c.total_cnot*price['cnot']+(2*oneq_U+n+1)*price['oneq']
            common+=(n+1)*(price['measure']+price['reset'])
            fixed=lambda extra,final:price['word']*(F_shared+extra+final+P)+price['memory']*memory
            entries=[]
            def add(name,B,readout,extra=0,final=F_mask,rounds=0,workspace=0):
                K=math.ceil(B/denom)
                total=fixed(extra,final)+K*(common+readout)+workspace*price['memory']
                entries.append(dict(method=name,rounds=rounds,B=B,shots=K,
                                    per_record=common+readout,fixed=fixed(extra,final),
                                    expected_work=total,memory_words=memory,extra_qubits=workspace))
            add('no_mask',RX,price['word']*len(intervals),F_beta,F_hist)
            # Full-mask accumulation computes one signed coefficient per interval
            # address; all parameters sharing an interval reuse it.
            mask_decode=sum(len(I)**2+4*(1<<len(I)) for I in intervals)
            for kind,vals in costs.items():
                add('full_'+kind,4*s,float(vals.mean())+price['word']*mask_decode)
            for k in range(1,5):
                B=p.risk_bound(c.T,k)
                mask_rng=2*n*k
                aggregate=sum(2*k*len(I)**2+4*(1<<len(I)) for I in intervals)
                lookup=sum(3*4**k+2 for _ in c.cones)+sum(2*k*len(I)+k*4**k for I in intervals)
                # Direct lookup and aggregate-first are both valid; select by
                # total work including final contraction, not just per-shot work.
                K=math.ceil(B/denom)
                if K*lookup <= K*aggregate+F_mask:
                    decode=lookup;final=0
                else:decode=aggregate;final=F_mask
                clean=2*n*k*price['cnot']+k*price['cz']+price['word']*(mask_rng+decode)
                measured=n*k*price['cnot']+k*price['cz']+2*k*(price['measure']+price['reset']+price['oneq'])
                measured+=price['word']*(mask_rng+decode+2*k*n)
                add('parity_clean',B,clean,F_beta,final,k,2)
                add('parity_measured',B,measured,F_beta,final,k,2)
                # Give the same compiler options to the finite-round ensemble.
                # Linear phases are removed by a known final outcome shift.
                prob=p._ref.rounds_mask_distribution(n,k)
                conversion=k*(n*(n-1)//2+n)
                baseextra=price['word']*(mask_rng+conversion+mask_decode)
                for kind,vals in costs.items():
                    add('parity_recompiled_'+kind,B,float(prob@vals)+baseextra,F_beta,F_mask,k)
            # Applicable local comparator: commute within generator-pair groups,
            # reverse only the suffix, and allocate shots with unequal shot costs.
            groupcost=[];Bs=[]
            for a,ids in enumerate(c.groups):
                end=max(ids);paircount=len(ids)//2
                measurement_oneq=(4,2,4)[a%3]*paircount+2
                oneq=oneq_U+sum(gate_oneq[end+1:])+measurement_oneq
                cost=objective+c.group_cnot[a]*price['cnot']+oneq*price['oneq']
                cost+=(n+1)*price['reset']+(2*paircount+1)*price['measure']
                cost+=len(ids)*price['word']
                Bs.append(4*len(ids));groupcost.append(cost)
            norm=sum(math.sqrt(b*cc) for b,cc in zip(Bs,groupcost))
            Ks=[math.ceil(norm*math.sqrt(b/cc)/denom) for b,cc in zip(Bs,groupcost)]
            assert sum(b/kk for b,kk in zip(Bs,Ks)) <= denom*(1+1e-12)
            groupfixed=price['word']*(2*P)+price['memory']*(2*P)
            entries.append(dict(method='grouped_suffix_rht',rounds=0,B=None,shots=sum(Ks),
                per_record=None,fixed=groupfixed,expected_work=groupfixed+sum(kk*cc for kk,cc in zip(Ks,groupcost)),
                memory_words=2*P,extra_qubits=0,group_shots=Ks))
            winner=min(entries,key=lambda x:x['expected_work'])
            paritybest=min((x for x in entries if x['method'].startswith('parity_')),key=lambda x:x['expected_work'])
            nonparity=min((x for x in entries if not x['method'].startswith('parity_')),key=lambda x:x['expected_work'])
            row=dict(n=n,depth=depth,P=P,profile=profile,objective_cost=objective,
                     winner=winner['method'],rounds=winner['rounds'],
                     winner_work=winner['expected_work'],best_parity=paritybest['method'],
                     parity_rounds=paritybest['rounds'],parity_ratio_to_best_nonparity=paritybest['expected_work']/nonparity['expected_work'])
            summary.append(row)
            for e in entries:
                allrows.append({**{k:row[k] for k in ('n','depth','P','profile','objective_cost')},**e})
    report={'schema_version':1,'seed':2026091566,
      'environment':{'python':platform.python_version(),'numpy':np.__version__},
      'contract':{'epsilon':eps,'delta':delta,'shared_shots':'ceil(B/(delta*epsilon^2))',
       'output':'complete raw real P-entry classical gradient; unbiased mean',
       'work':'expected normalized serialized cost, not hardware seconds',
       'cost_model':'All price profiles positive. Objective price may be zero as a stress case. Common response counted per record. Individual compiler synthesis paid per sampled mask. Memory charged once as resident words; no memory-time interpretation.',
       'classical_ledger':'Explicit conservative scalar/word-operation prescriptions, not measured operation-optimal code or wall-clock timing. Gray-traversal interval aggregation (quadratic-character implementation) or shifted-table lookup selected by priced total work. Shifted lookup charges a load, multiply and add per term plus mask restriction/shift generation. Scalar kernel counts exclude Python interpreter loop overhead.',
       'randomness':'Exact ensemble mean compilation/relabel costs for all masks n=2..5; parity native gate costs are analytic expectations and may overcount degenerate rounds. Recompiling the same parity mask is also allowed.',
       'comparators':'No mask, direct/pivot/greedy/portfolio exact full masks, both parity interfaces and equivalent-mask recompilation, grouped suffix reversed tests.',
       'not_claimed':'global optimal Clifford synthesis, universal measurement optimum, hardware speedup, exact optimal sample counts, or strongest-all-method advantage.'},
      'prices':PRICES,'compiler_stats':compiler_stats,'circuits':circuits,
      'scenario_count':len(summary),'candidate_rows':len(allrows),
      'winners':dict(Counter(x['winner'] for x in summary)),
      'parity_wins':sum(x['winner'].startswith('parity_') for x in summary),
      'minimum_parity_ratio':min(x['parity_ratio_to_best_nonparity'] for x in summary),
      'maximum_parity_ratio':max(x['parity_ratio_to_best_nonparity'] for x in summary),
      'decision':'Restricted priced prescriptions only; no promotion of novelty or strongest-method advantage.'}
    (args.output/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    for filename,rows in (('scenarios.csv',summary),('candidates.csv',allrows)):
        fields=list(dict.fromkeys(k for row in rows for k in row))
        with (args.output/filename).open('w',newline='') as out:
            writer=csv.DictWriter(out,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    print(json.dumps({k:report[k] for k in ('scenario_count','candidate_rows','winners','parity_wins','minimum_parity_ratio','maximum_parity_ratio','compiler_stats')},indent=2))

if __name__=='__main__':main()
