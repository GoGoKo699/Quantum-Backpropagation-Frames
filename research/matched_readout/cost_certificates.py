import json
from pathlib import Path
import numpy as np
from core import *
rng=np.random.default_rng(2026091531)
rows=[];maxerr=0
for n in (2,3,4,5,6):
 for depth in (1,2,3):
  c=make_circuit(n,depth,rng)
  RX=walsh_second_bound_dp(c.cones,c.taus,n)
  direct=2*len(c.angles)+2*np.max(np.sum(fwht(c.T.T)**2,axis=0))
  maxerr=max(maxerr,abs(RX-direct))
  RB=block_state_independent_bound(c)
  RP=float(4*sum(4**len(I) for I in c.cones))
  ag=np.array([4*len(g) for g in c.groups],float)
  RR=float(sum(np.sqrt(ag))**2)
  cc=np.array(c.group_cnot,float)
  # Guarantee Pr(||error||>eps)<=delta via the common Markov conversion.
  # All coefficients below omit common 1/(delta*eps^2); integer rounding extra.
  rows.append(dict(n=n,depth=depth,P=len(c.angles),w=max(map(len,c.cones)),RX=RX,RB=RB,RP=RP,RR=RR,
                   cnot_full=2*c.total_cnot,group_a=ag.tolist(),group_cnot=cc.tolist(),
                   group_cost_C0=float(np.sum(np.sqrt(ag*cc))**2),
                   walsh_cost_C0=float(RX*2*c.total_cnot),
                   group_slope_lower=float(c.total_cnot*RR),
                   walsh_zero_initial_lower_ratio=float(c.total_cnot*RR/(RX*2*c.total_cnot))))
  # Replay RNG consumption so circuits exactly coincide with comparison.json.
  for _ in response_cases(c,rng):pass
Path(__file__).with_name('cost_certificates.json').write_text(json.dumps(dict(max_dp_brute_residual=maxerr,rows=rows),indent=2))
print('DP residual',maxerr)
for x in rows:
 if (x['n'],x['depth']) in [(3,2),(4,2),(5,3),(6,3)]:
  print({k:round(v,3) if isinstance(v,float) else v for k,v in x.items() if k not in ('group_a','group_cnot')})
print('All RX<RB and RX<RR/2?',all(r['RX']<r['RB'] and r['RX']<r['RR']/2 for r in rows))
