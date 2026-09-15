"""Independent identities, marginal exact distributions, and aggregate-first checks."""
import json,math
from pathlib import Path
from collections import deque
import numpy as np
from core import *

rng=np.random.default_rng(2026091532)
checks={k:0. for k in ['group_mean','group_second','block_mean','block_second','walsh_aggregate','block_aggregate']}
counts={k:0 for k in checks}

@lru_cache(None)
def stabilizers(b):
    dim=2**b
    h=np.array([[1,1],[1,-1]])/np.sqrt(2);s=np.diag([1,1j])
    generators=[local_embed(m,[i],b) for i in range(b) for m in (h,s)]
    for i in range(b):
      for j in range(b):
       if i==j:continue
       mat=np.zeros((dim,dim))
       for x in range(dim):
        y=x^((1<<(b-1-j)) if x&(1<<(b-1-i)) else 0)
        mat[y,x]=1
       generators.append(mat)
    def canon(x):
      x=x/np.linalg.norm(x);a=np.flatnonzero(abs(x)>1e-8)[0];x=x*np.conj(x[a])/abs(x[a])
      y=np.concatenate([x.real,x.imag]);y[np.abs(y)<1e-9]=0
      return tuple(np.round(y,10)),x
    e=np.zeros(dim,complex);e[0]=1
    k,e=canon(e);seen={k:e};queue=deque([e])
    while queue:
      x=queue.popleft()
      for M in generators:
        k,y=canon(M@x)
        if k not in seen: seen[k]=y;queue.append(y)
    states=np.array(list(seen.values()))
    assert len(states)=={1:6,2:60,3:1080}[b]
    return states

# Full probability comparison for grouped suffix RHT.
for n in range(2,7):
 for depth in (1,2,3):
  c=make_circuit(n,depth,rng);N=2**n
  q=rng.normal(size=N)+1j*rng.normal(size=N);q*=np.exp(-1j*np.angle(q[0]));q/=np.linalg.norm(q)
  O=make_reflection_for_response(c,q);g=2*c.T.T@q.real
  psi=c.U[:,0].astype(complex);response=O@psi
  for ids in c.groups:
   end=max(ids); a=psi.copy();b=response.copy()
   for gate in reversed(c.gates[end+1:]):a=gate.conj().T@a;b=gate.conj().T@b
   # all A_j in a sublayer are pairwise commuting; common eigenbasis via eigh of
   # a nondegenerate random weighted combination, then evaluate full probabilities.
   A=sum((1.3**k)*c.generators[j] for k,j in enumerate(ids))
   _,basis=np.linalg.eigh(A)
   pa=np.abs(basis.conj().T@(a-1j*b)/2)**2
   pb=np.abs(basis.conj().T@(a+1j*b)/2)**2
   for j in ids:
    eig=np.diag(basis.conj().T@c.generators[j]@basis).real
    # A weighted sum can have degeneracies within irrelevant spectator spaces;
    # generators are constant on these spaces for disjoint involutions.
    assert np.max(abs(basis.conj().T@c.generators[j]@basis-np.diag(eig)))<1e-9
    mean=(-2*eig)@pa+(2*eig)@pb
    second=(4*eig**2)@(pa+pb)
    checks['group_mean']=max(checks['group_mean'],float(abs(mean-g[j])))
    checks['group_second']=max(checks['group_second'],float(abs(second-4)))
    counts['group_mean']+=1;counts['group_second']+=1

# Local Clifford moment identity with measured ancilla and arbitrary external spectators.
for b in (1,2,3):
 states=stabilizers(b);dim=2**b
 for trial in range(5):
  n=b+2;N=2**n;Q=tuple(range(b))
  q=rng.normal(size=N)+1j*rng.normal(size=N);q*=np.exp(-1j*np.angle(q[0]));q/=np.linalg.norm(q)
  tau=rng.normal(size=dim);tau[0]=0;tau/=np.linalg.norm(tau)
  padded=np.zeros(N);padded[::4]=tau
  g=2*np.vdot(padded,q).real
  e=np.zeros(N);e[0]=1
  rplus=reduced(np.outer((e+q)/2,((e+q)/2).conj()),Q,n)
  rminus=reduced(np.outer((e-q)/2,((e-q)/2).conj()),Q,n)
  pp=(dim/len(states))*np.einsum('ki,ij,kj->k',states.conj(),rplus,states).real
  pm=(dim/len(states))*np.einsum('ki,ij,kj->k',states.conj(),rminus,states).real
  snapshot_columns=(dim+1)*states*states[:,0].conj()[:,None];snapshot_columns[:,0]-=1
  r=2*(snapshot_columns@tau).real
  mean=np.sum((pp-pm)*2*r)
  second=np.sum((pp+pm)*4*r*r)
  rho=reduced(np.outer(q,q.conj()),Q,n)
  u=(rho[0,0]+tau@rho@tau).real
  pred=4*(dim+1)/(dim+2)*(3+u)
  checks['block_mean']=max(checks['block_mean'],float(abs(mean-g)))
  checks['block_second']=max(checks['block_second'],float(abs(second-pred)))
  counts['block_mean']+=1;counts['block_second']+=1
  # Aggregate after many records, not one gradient reconstruction per shot.
  choice=rng.integers(len(states),size=75);sign=rng.choice([-1,1],size=75)
  mean_record=np.mean(2*sign*r[choice])
  h=np.sum(sign[:,None]*snapshot_columns[choice],axis=0)
  mean_aggregate=4*(tau@h).real/75
  checks['block_aggregate']=max(checks['block_aggregate'],float(abs(mean_record-mean_aggregate)))
  counts['block_aggregate']+=1

# Exact all-X aggregate-first identity, arbitrary records (unbiasedness separate).
for n in range(2,9):
 c=make_circuit(n,2,rng);M=257
 y=rng.integers(2**n,size=M);s=rng.choice([-1,1],size=M)
 global_f=fwht(c.T.T)
 direct=2*(global_f[:,y]@s)/M
 hist={}
 for Q in set(c.cones):
  loc=indices_on(Q,n)[y];hist[Q]=np.bincount(loc,weights=s,minlength=2**len(Q))
 aggregate=np.array([2*t@fwht(hist[Q])/M for t,Q in zip(c.taus,c.cones)])
 checks['walsh_aggregate']=max(checks['walsh_aggregate'],float(np.max(abs(direct-aggregate))))
 counts['walsh_aggregate']+=len(direct)

result=dict(seed=2026091532,checks=checks,counts=counts,stabilizer_counts={b:len(stabilizers(b)) for b in (1,2,3)})
Path(__file__).with_name('validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
