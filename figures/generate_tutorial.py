"""Regenerate the analytic tutorial figure and its compact source data.

Run from any directory. No experiment or random sampling is performed.
The optional output directory permits reproduction without changing the checkout.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "figures")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    q = np.array([np.sqrt(3) / 2, 0.5, 0.0, 0.0])
    c = np.array([0.0, *([1 / np.sqrt(3)] * 3)])
    probabilities = np.array([(c + q) ** 2 / 4, (c - q) ** 2 / 4])
    rho = np.linspace(0.0, 1.0, 101)
    sparse = 12 + 4 * rho
    no_mask = 24 - 8 * rho
    assert np.isclose(probabilities.sum(), 1.0)
    assert np.isclose(probabilities[:, 0].sum(), 3 / 8)
    assert np.isclose(sparse[25], 13.0)
    assert np.isclose(no_mask[25], 22.0)

    sources = ["results/PF-05/PROOF_AUDIT.md", "results/PF-06/PROOF.md"]
    data = {
        "kind": "analytic formulas; no simulation or sampled data",
        "parameters": {"n": 2, "P": 6, "r": 3, "lambda": 2},
        "system_basis": ["00", "01", "10", "11"],
        "response": q.tolist(),
        "reference": c.tolist(),
        "probabilities_by_reference_bit": probabilities.tolist(),
        "formulas": {
            "probability": "p(b,x)=(c_x+(-1)^b q_x)^2/4",
            "rho": "squared norm of q on span{01,10,11}",
            "sparse_trace_risk": "12+4*rho",
            "no_mask_trace_risk": "24-8*rho",
        },
        "curve": [
            {"rho": float(x), "sparse": float(y), "no_mask": float(z)}
            for x, y, z in zip(rho, sparse, no_mask)
        ],
        "sources": [
            {"path": source, "sha256": hashlib.sha256((ROOT / source).read_bytes()).hexdigest()}
            for source in sources
        ],
        "generator": "figures/generate_tutorial.py",
        "matplotlib_version": matplotlib.__version__,
        "numpy_version": np.__version__,
    }
    (args.output / "tutorial-readout.json").write_text(json.dumps(data, indent=2) + "\n")

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "svg.hashsalt": "qbp-frames-analytic-tutorial-v1",
    })
    fig, axes = plt.subplots(2, 1, figsize=(7.4, 7.8), layout="constrained")
    blue, orange = "#236799", "#bd5a17"

    ax = axes[0]
    positions = np.arange(4)
    ax.bar(positions - .18, probabilities[0], .34, color=blue, label="Reference bit 0 (+ score)")
    ax.bar(positions + .18, probabilities[1], .34, color=orange, label="Reference bit 1 (− score)")
    ax.set_xticks(positions, ["00\nZero score", "01", "10", "11"])
    ax.set_ylim(0, .37)
    ax.set_ylabel("Born probability")
    ax.set_xlabel("Measured system bits")
    ax.set_title("A  Analytic probabilities for the worked response", loc="left", weight="bold", pad=12)
    ax.legend(frameon=False, fontsize=10, loc="upper right")
    ax.text(.01, .89, "00 still counts: total probability 3/8", transform=ax.transAxes, fontsize=10)
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=.15)

    ax = axes[1]
    ax.plot(rho, sparse, color=blue, linewidth=2.5, label="Sparse readout: 12 + 4ρ")
    ax.plot(rho, no_mask, color=orange, linewidth=2.5, label="No-mask readout: 24 − 8ρ")
    ax.axvline(.25, color="#777777", linestyle=":", linewidth=1)
    ax.scatter([.25], [13], color=blue, zorder=3)
    ax.scatter([.25], [22], color=orange, zorder=3)
    ax.annotate("Worked response: risk 13", (.25, 13), xytext=(.33, 12.6), fontsize=10)
    ax.annotate("Same response: risk 22", (.25, 22), xytext=(.33, 22.4), fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(10, 26)
    ax.set_xticks([0, .25, .5, .75, 1])
    ax.set_yticks([12, 16, 20, 24])
    ax.set_xlabel("Response weight in the tangent span, ρ")
    ax.set_ylabel("One-copy trace risk")
    ax.set_title("B  Analytic risks for this fixed six-coordinate model", loc="left", weight="bold", pad=12)
    ax.legend(frameon=False, fontsize=10, loc="upper right")
    ax.set_axisbelow(True)
    ax.grid(alpha=.15)
    fig.savefig(args.output / "tutorial-readout.svg", metadata={
        "Date": None,
        "Title": "Analytic probabilities and risks for the two-qubit gradient-readout example",
        "Description": "Exact formulas from the preserved sparse-measurement and one-layer proofs; no simulation.",
        "Creator": "figures/generate_tutorial.py",
    })
    plt.close(fig)
    print("wrote tutorial-readout.svg and tutorial-readout.json (analytic, no sampling)")


if __name__ == "__main__":
    main()
