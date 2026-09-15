import json
from pathlib import Path
import numpy as np
from core import *

def local_inner(I,a,J,b):
    both=tuple(sorted(set(I)&set(J)))
    # Both global tangents vanish outside their respective intervals.
    # Only strings supported on their intersection can contribute.
    if not both:return a[0]*b[0]
    ia=[];ib=[]
    for x in range(2**len(both)):
        aa=bb=0
        for k,site in enumerate(both):
            bit=(x>>(len(both)-1-k))&1
            aa|=bit<<(len(I)-1-I.index(site));bb|=bit<<(len(J)-1-J.index(site))
        ia.append(aa);ib.append(bb)
    return a[ia]@b[ib]

rng=np.random.default_rng(2026091531);rows=[];gram_res=0.
for n in (2,3,4,5,6):
 for depth in (1,2,3):
    c=make_circuit(n,depth,rng);P=len(c.angles)
    G=np.array([[local_inner(I,a,J,b) for J,b in zip(c.cones,c.taus)] for I,a in zip(c.cones,c.taus)])
    gram_res=max(gram_res,float(np.max(abs(G-c.T.T@c.T))))
    kappa=float(np.max(np.sum(np.abs(G),axis=1)))
    RX=walsh_second_bound_dp(c.cones,c.taus,n);RB=block_state_independent_bound(c)
    lower=.75*RB-4*kappa
    rows.append(dict(n=n,depth=depth,P=P,kappa_row_bound=kappa,RX=RX,RB=RB,
                     block_covariance_lower=lower,positive_margin=lower-RX))
    for _ in response_cases(c,rng):pass
r=dict(seed=2026091531,rows=rows,local_gram_residual=gram_res)
Path(__file__).with_name('uniform_comparison.json').write_text(json.dumps(r,indent=2))
print('Gram discrepancy',gram_res,'Minimum margin',min(x['positive_margin'] for x in rows))
for x in rows:
 if (x['n'],x['depth']) in [(3,2),(4,2),(5,3),(6,3)]:print(x)
