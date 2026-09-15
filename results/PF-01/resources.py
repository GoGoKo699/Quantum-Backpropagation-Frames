"""Generate PF-01 matched contracts and explicitly limited logical-cost illustrations."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

def ratio(beta: float, rounds: int) -> float:
    """B_k / (4 tr G), for tr G > 0."""
    if beta < 1 or rounds < 0:
        raise ValueError('Invalid beta or round count')
    return 1 + (beta - 1) / (2 * 4**rounds)

def ledger(n: int, beta: float, rounds: int, measured: bool = False) -> dict:
    return {'method': 'parity_measured' if measured else 'parity_clean',
            'n': n, 'rounds': rounds, 'variance_ratio_to_4s': ratio(beta, rounds),
            'expected_cnot': n * rounds * (1 if measured else 2),
            'cz': rounds, 'extra_measurements': 2 * rounds if measured else 0,
            'extra_resets_with_two_reused_ancillas': 2 * rounds if measured else 0,
            'work_ancillas': 2 if rounds else 0}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        p.error('Refusing to overwrite output')
    methods = [
        {'method': 'no_mask', 'B': '2*s*(1+beta)', 'readout_two_qubit_gates': '0',
         'ancillas_extra_to_reference': '0', 'processing': 'local Walsh compilation; shared interval histograms; final tangent contractions',
         'status': 'exact known implementation; baseline must always be allowed'},
        {'method': 'dense_independent_CZ_direct', 'B': '4*s',
         'readout_two_qubit_gates': 'expected n*(n-1)/4 CZ', 'ancillas_extra_to_reference': '0',
         'processing': 'n*(n-1)/2 random bits; local restricted masks and lookup/FWHT or aggregate moments',
         'status': 'known exact equatorial-mask endpoint; not an optimal gate lower bound'},
        {'method': 'dense_CZ_optimized', 'B': '4*s',
         'readout_two_qubit_gates': 'compile same sampled diagonal Clifford; allow O(n^2/log n) generic Clifford synthesis; constants instance-dependent',
         'ancillas_extra_to_reference': 'implementation-dependent',
         'processing': 'charge synthesis and any final linear outcome relabeling; do not charge the direct dense count after optimization',
         'status': 'eligible strong comparator; no implemented finite-size optimized synthesis in this audit'},
        {'method': 'parity_clean', 'B': '4*s+2*s*(beta-1)*4^(-k)',
         'readout_two_qubit_gates': 'expected 2*n*k CNOT plus k CZ; worst 4*n*k CNOT plus k CZ',
         'ancillas_extra_to_reference': '2 clean reusable work qubits',
         'processing': '2*n*k random bits; O(n*k+sum_j min(4^k,k*w_j^2+w_j*2^w_j)) conservative direct-record upper bound; aggregation permitted',
         'status': 'candidate exact clean-unitary implementation; not optimal synthesis'},
        {'method': 'parity_measured_uncomputation', 'B': 'same as parity_clean',
         'readout_two_qubit_gates': 'expected n*k CNOT plus k CZ; worst 2*n*k CNOT plus k CZ',
         'ancillas_extra_to_reference': '2 reused with 2*k X measurements and resets, or 2*k disposable work qubits',
         'processing': 'same tangent decoder plus known outcome shift sum(u_l*a_l+v_l*b_l)',
         'status': 'audit-derived equivalent final measurement; NOT a clean unitary substitution; reset/readout latency must be charged'},
        {'method': 'global_Clifford_shadow_rank_two_targets', 'B': '12*(2*N+1)/(2*N+2)*s',
         'exact_covariance': '12*c*G - g*g^T/(2*N+2), c=(2*N+1)/(2*N+2)',
         'readout_two_qubit_gates': 'allow O((n+1)^2/log(n+1)) optimized all-to-all Clifford synthesis',
         'ancillas_extra_to_reference': 'no work ancilla intrinsically required; compilation-dependent',
         'processing': 'stabilizer-tableau sampling and target overlaps, not full density matrix; sparse tangents give a concrete polynomial-in-P,exponential-in-width decoder',
         'status': 'known matched-access full-vector competitor with same O(s/epsilon^2) sample scaling'},
        {'method': 'local_rank_two_block_Clifford', 'B': '32*s for two partitions with coverage >=1/2',
         'readout_two_qubit_gates': 'O(n*w) direct block compilation when blocks have <=2*w qubits; allow better synthesis',
         'ancillas_extra_to_reference': '0',
         'processing': 'block snapshots: accumulate only required zero-column entries, then tangent contractions; charge 2^O(w) work',
         'status': 'eligible for the local-support family; known moment identities plus source-packet block construction; not for arbitrary T'},
        {'method': 'near_linear_exact_unitary_2design', 'B': None,
         'readout_two_qubit_gates': 'O(n*log^2(n)*loglog(n)) all-Clifford unconditional construction; other variants exist',
         'ancillas_extra_to_reference': 'near-linear clean workspace in cited construction',
         'processing': 'design sampling/basis arithmetic and target decoder must be charged',
         'status': 'not automatically a drop-in shadow-variance comparator: second moments of scores require third projective moments; additional analysis OPEN'},
        {'method': 'shallow_shadows', 'B': 'derive from Theorem 7 for the actual target operators; do not substitute a typical-state norm',
         'readout_two_qubit_gates': 'O(n*d_m) for declared measurement depth d_m',
         'ancillas_extra_to_reference': 'implementation-dependent',
         'processing': 'inverse-channel and joint-Pauli probabilities; exactly computable in poly(n) at d_m=O(log n) for specified sparse-Pauli targets',
         'status': 'strong eligible architecture; no uniform 4*s inference from low depth alone'},
    ]
    illustrations = []
    for n,w in [(32,2),(128,6),(1024,6),(1024,12)]:
        beta = float(2**w); eta = .1
        k = max(0, math.ceil(math.log((beta-1)/(2*eta),4)))
        dense = n*(n-1)/4
        for measured in (False,True):
            row = ledger(n,beta,k,measured)
            r = row['variance_ratio_to_4s']
            extra = row['expected_cnot']+row['cz']
            crossover = (dense-r*extra)/(r-1)
            row.update(width_bound=w, beta_assumption=beta, eta=eta,
                       dense_expected_cz=dense,
                       dense_crossover_response_gate_units=max(0.,crossover),
                       crossover_positive=bool(crossover>0),
                       interpretation='Below a positive crossover the parity prescription wins this gate-only comparison; above it dense wins. No classical or reset time priced.')
            illustrations.append(row)
    choices = []
    n=1024;beta=64.
    for response in (0.,1e3,1e5,1e7,1e9):
        for reset_measure_price in (0.,1000.):
            candidates = [('no_mask',0,ratio(beta,0)*response)]
            candidates.append(('dense_direct',None,response+n*(n-1)/4))
            for k in range(1,13):
                for measured in (False,True):
                    r=ratio(beta,k); gate=n*k*(1 if measured else 2)+k
                    terminal=4*k*reset_measure_price if measured else 0
                    candidates.append(('parity_measured' if measured else 'parity_clean',k,r*(response+gate+terminal)))
            best=min(candidates,key=lambda x:x[2])
            choices.append({'response_gate_units':response,'price_per_extra_measurement_or_reset':reset_measure_price,
                            'best_among_displayed_only':best[0], 'rounds':best[1],
                            'work_divided_by_4s_over_delta_epsilon_squared':best[2]})
    report = {'schema_version':1,
              'contract': {'output':'materialized P-entry raw real gradient',
                           'accuracy':'Pr(||g_hat-g||_2<=epsilon)>=1-delta',
                           'sufficient_records':'ceil(B/(delta*epsilon^2)) for the unchanged unbiased independent sample mean',
                           'shared_response_cost':'C_resp=cost of fresh Omega, including forward, controlled objective, reverse and common readout',
                           'total_work':'F_m + K_m*(C_resp+Q_m+weight_C*C_m+weight_M*M_m+weight_R*R_m)+final_decode+P output',
                           'cost_units':'quantum gates, classical work, measurements and resets remain separate unless explicit prices are supplied',
                           'geometric_inputs':'s and beta are known certified quantities or explicit bounds; beta computation may be exponential in width',
                           'not_claimed':'runtime optimality, optimal confidence dependence, a free frame/decoder or a quantum-hard application'},
              'methods':methods,
              'gate_only_illustrations_NOT_total_runtime':illustrations,
              'restricted_prescription_choices_NOT_all_method_optima':choices,
              'checks':{'beta_one_no_mask_suffices':ratio(1.,0)==ratio(1.,8)==1.,
                        'measured_uncompute_halves_expected_CNOT':all(ledger(n,2.,3,True)['expected_cnot']*2==ledger(n,2.,3,False)['expected_cnot'] for n in (1,8,128)),
                        'all_near_optimal_bounds_satisfied':all(x['variance_ratio_to_4s']<=1.1 for x in illustrations)}}
    assert all(report['checks'].values())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'checks':report['checks'],'illustrations':illustrations,'choices':choices},indent=2))

if __name__=='__main__':main()
