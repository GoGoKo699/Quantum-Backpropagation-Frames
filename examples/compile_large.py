"""Reproduce an existing n=128 zero-angle disjoint compiler-only case.

Run after installation: python examples/compile_large.py
No 2^128 state, probability table, or simulated experimental data is allocated.
"""
import json
import numpy as np
from qbp_frames import disjoint


def main():
    plan = disjoint.compile_plan(np.zeros((64, 6)))
    assert plan.counts() == {"cx": 891, "ry": 764, "x": 2, "h": 1}
    assert plan.exact_risk_bound() == 1528
    assert plan.classify(1) == (63, 0)
    assert plan.classify((1 << 127) | 1) is None
    estimate = plan.finish(np.zeros((64, 3)), 1)
    assert estimate.shape == (384,)
    print(json.dumps({
        "mode": "compiler only; no Born simulation", "system_qubits": plan.n,
        "original_coordinates": plan.P, "rank_at_zero": plan.r,
        "tangent_scalars_stored": int(plan.K.size),
        "row_energy_scalars_stored": int(plan.row_energy.size),
        "program_gates_retained": len(plan.gates),
        "readout_gate_counts": plan.counts(), "physical_bits_per_record": plan.n+1,
        "flat_minimax_trace_risk": plan.exact_risk_bound(),
        "no_mask_worst_trace_risk": 4*plan.P, "full_output_length": len(estimate),
        "global_state_allocated": False, "checks": "passed"
    }, indent=2))


if __name__ == "__main__":
    main()
