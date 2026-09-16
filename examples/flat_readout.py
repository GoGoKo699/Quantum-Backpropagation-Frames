"""Exact two-qubit teaching example, followed by a fixed 16-record histogram.

Run after installation: python examples/flat_readout.py
No random experiment or favorable-response benchmark is performed.
"""
import json
import math
import numpy as np
from qbp_frames import disjoint


def main():
    plan = disjoint.compile_plan(np.zeros((1, 6)))
    q = np.array([math.sqrt(3)/2, .5, 0., 0.])
    reference = disjoint.reference_vector(plan)
    probabilities = np.r_[(reference+q)**2, (reference-q)**2]/4
    state = np.r_[np.array([1., 0., 0., 0.]), q]/math.sqrt(2)
    actual = disjoint.apply_circuit(state, plan.gates, plan.n+1)**2
    scores = disjoint.dense_scores(plan)
    gradient = 2*disjoint.dense_tangents(plan).T@q
    np.testing.assert_allclose(actual, probabilities, atol=2e-14, rtol=0)
    np.testing.assert_allclose(probabilities@scores, gradient, atol=2e-14, rtol=0)
    np.testing.assert_allclose(gradient, [0, 1, 0, 0, 0, 1], atol=2e-14, rtol=0)

    # Illustrative possible records, not a new Monte Carlo data set. All 16
    # experiments remain in the denominator, including six zero-score records.
    records = np.array([3, 7, 1, 1, 3, 0, 1, 0])
    bins = np.zeros((plan.blocks, 3))
    for outcome, count in enumerate(records):
        bit, system = divmod(outcome, 1 << plan.n)
        channel = plan.classify(system)
        if channel is not None:
            bins[channel] += (-1)**bit * count
    estimate = plan.finish(bins, int(records.sum()))
    np.testing.assert_allclose(estimate, (records@scores)/16, atol=2e-14, rtol=0)
    result = {
        "system_qubits": plan.n, "original_coordinates": plan.P,
        "target_gradient": gradient.tolist(),
        "physical_outcome_order": [format(i, "03b") for i in range(8)],
        "probabilities": probabilities.round(12).tolist(),
        "zero_score_probability": round(float(probabilities[[0, 4]].sum()), 12),
        "one_copy_trace_risk_at_this_response": round(disjoint.risk_from_coordinates(plan, q), 12),
        "minimax_trace_risk": plan.exact_risk_bound(),
        "no_mask_worst_trace_risk": 4*plan.P,
        "illustrative_record_counts": records.tolist(), "total_records": int(records.sum()),
        "sample_gradient": estimate.round(12).tolist(),
        "readout_gate_counts": plan.counts(), "checks": "passed"
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
