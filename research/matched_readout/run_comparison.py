import json,sys,time
from pathlib import Path
import numpy as np
from core import *
rng=np.random.default_rng(2026091531)
rows=[];checks={'walsh_mean_max':0.,'reflection_residual_max':0.,'finite_difference_max':0.,'gradient_checks':0,'fd_checks':0}
start=time.perf_counter()
for n in (2,3,4,5,6):
  for depth in (1,2,3):
    c=make_circuit(n,depth,rng)
    for name,q in response_cases(c,rng):
      wx=walsh_moments(c,q); bs=block_moments(c,q); gp=grouped_moments(c,q)
      ps=pauli_moments(c,q) if n<=5 else None
      O=make_reflection_for_response(c,q)
      checks['reflection_residual_max']=max(checks['reflection_residual_max'],float(np.max(abs(O@O-np.eye(2**n)))),float(np.max(abs(O@c.U[:,0]-c.U@q))))
      g=2*c.T.T@q
      checks['walsh_mean_max']=max(checks['walsh_mean_max'],float(np.max(abs(wx['mean']-g))))
      checks['gradient_checks']+=len(g)
      if name=='random_real':
        h=1e-6
        for j in np.unique(np.linspace(0,len(g)-1,min(5,len(g)),dtype=int)):
          ap=c.angles.copy();am=ap.copy();ap[j]+=h;am[j]-=h
          cp=make_circuit(n,depth,rng,ap);cm=make_circuit(n,depth,rng,am)
          ep=cp.U[:,0]@O@cp.U[:,0]; em=cm.U[:,0]@O@cm.U[:,0]
          err=abs((ep-em)/(2*h)-g[j]);checks['finite_difference_max']=max(checks['finite_difference_max'],float(err));checks['fd_checks']+=1
      rows.append(dict(n=n,depth=depth,P=len(g),w=max(map(len,c.cones)),response=name,gradient_norm=float(np.linalg.norm(g)),
         A_X=wx['A'],A_B=bs['A'],A_P=None if ps is None else ps['A'],A_R=gp['A'],
         groups=gp['groups'],group_variance=gp['group_variance'].tolist(),group_cnot=gp['group_cnot'].tolist(),
         ansatz_cnot=c.total_cnot,walsh_second_bound=wx['second_bound'],block_second_bound=bs['second_bound']))
    print(n,depth,len(c.angles), 'elapsed',round(time.perf_counter()-start,1),flush=True)
Path(__file__).with_name('comparison.json').write_text(json.dumps(dict(seed=2026091531,rows=rows,checks=checks),indent=2))
print(checks)
print('Block beats X:',[(r['n'],r['depth'],r['response'],round(r['A_X']/r['A_B'],3)) for r in rows if r['A_B']<r['A_X']])
