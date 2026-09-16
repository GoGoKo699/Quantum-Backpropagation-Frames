"""Current read-only gate; inherited integration code is preserved unchanged.

The full route requires a clean full Git clone and reruns only frozen bounded
regressions, supported examples and deterministic figures. New output goes
strictly below ignored runs/. No historical record or remote state is changed.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from check_docs import check as check_docs

ROOT = Path(__file__).resolve().parents[1]
PACKET_COUNTS = {"PF-04": 9, "PF-05": 9, "PF-06": 12, "PF-07": 11, "PF-08": 8}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, timeout=30).strip()


def verify_migration(root: Path = ROOT) -> dict:
    manifest_bytes = (root / "maintenance/repository-polish/MIGRATION.json").read_bytes()
    data = json.loads(manifest_bytes)
    files = data["preserved_files"]
    if not isinstance(files, dict) or not files:
        raise ValueError("Migration inventory has no preserved files")
    for name, expected in files.items():
        path = root / name
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Invalid preserved evidence path: {name}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Preserved evidence identity mismatch: {name}")
    for item in data.get("guidance_copies", []):
        name = item["preserved_copy"]
        path = root / name
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Invalid copied guidance path: {name}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            raise ValueError(f"Copied guidance identity mismatch: {name}")
    for item in data.get("maintained_code_copies", []):
        for prefix in ("source", "maintained"):
            name = item[f"{prefix}_path"]
            path = root / name
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError(f"Invalid maintained-code map path: {name}")
            if hashlib.sha256(path.read_bytes()).hexdigest() != item[f"{prefix}_sha256"]:
                raise ValueError(f"Maintained-code map identity mismatch: {name}")
    packets = {}
    for packet, count in PACKET_COUNTS.items():
        path = root / "results" / packet
        entries = json.loads((path / "MANIFEST.json").read_text())["sha256"]
        if len(entries) != count:
            raise ValueError(f"Original {packet} manifest coverage changed")
        for name, expected in entries.items():
            if hashlib.sha256((path / name).read_bytes()).hexdigest() != expected:
                raise ValueError(f"Original {packet} manifest identity mismatch: {name}")
        packets[packet] = count
    return {"preserved_files_verified": len(files),
            "migration_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "guidance_copies_verified": len(data.get("guidance_copies", [])),
            "maintained_code_maps_verified": len(data.get("maintained_code_copies", [])),
            "original_packet_manifests": packets}


def docs_only(paths: list[str]) -> bool:
    """Conservative classifier: executable/data/config changes always run full."""
    if not paths:
        return False
    return all(name in ("CITATION.cff", "LICENSE") or (name.endswith(".md") and (
        "/" not in name or name.startswith("docs/") or name in (
            "qbp_frames/README.md", "literature/README.md", "work_orders/CURRENT.md",
            "maintenance/repository-polish/REPORT.md"))) for name in paths)


def ci_mode() -> str:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    kind = os.environ["GITHUB_EVENT_NAME"]
    if kind == "workflow_dispatch":
        return "full"
    if kind == "pull_request":
        base = event["pull_request"]["base"]["sha"]
        head = event["pull_request"]["head"]["sha"]
        changes = git("diff", "--name-only", f"{base}...{head}").splitlines()
    elif kind == "push":
        base, head = event["before"], event["after"]
        if set(base) == {"0"}:
            return "full"
        changes = git("diff", "--name-only", base, head).splitlines()
    else:
        return "full"
    return "docs" if docs_only(changes) else "full"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("docs", "full"), default="full")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--ci-mode", action="store_true")
    args = parser.parse_args()
    if args.ci_mode:
        print(ci_mode())
        return
    if args.output is None:
        parser.error("--output is required")
    output, allowed = args.output.resolve(), (ROOT / "runs").resolve()
    if output == allowed or not output.is_relative_to(allowed):
        parser.error("Use an unused directory strictly below runs/")
    output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    report = {"status": "running", "mode": args.mode,
              "started_utc": datetime.now(timezone.utc).isoformat(),
              "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
              "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
              "python": platform.python_version(), "commands": [],
              "scope": "Existing bounded regressions; not a novelty review, new study or visual rendering test."}
    env = os.environ.copy()
    env.update({key: "1" for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "PYTHONDONTWRITEBYTECODE")})

    def run(arguments: list[str], name: str, timeout: int = 600) -> None:
        begin, logname = time.perf_counter(), f"{name}.log"
        try:
            with (output / logname).open("w") as log:
                result = subprocess.run([sys.executable, *arguments], cwd=ROOT, env=env,
                                        stdout=log, stderr=subprocess.STDOUT, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            report["commands"].append({"arguments": arguments, "log": logname,
                "returncode": None, "timeout_seconds": timeout, "elapsed_seconds": time.perf_counter() - begin})
            raise RuntimeError(f"Timed out {name}; inspect {output / logname}") from exc
        report["commands"].append({"arguments": arguments, "log": logname,
            "returncode": result.returncode, "elapsed_seconds": time.perf_counter() - begin})
        if result.returncode:
            raise RuntimeError(f"Failed {name}; inspect {output / logname}")

    try:
        report["source_commit"], report["source_tree"] = git("rev-parse", "HEAD"), git("rev-parse", "HEAD^{tree}")
        report["working_tree_clean_at_start"] = not bool(git("status", "--porcelain", "--untracked-files=all"))
        if args.mode == "full" and not report["working_tree_clean_at_start"]:
            raise RuntimeError("Full validation requires a clean checkout")
        report["documentation"] = check_docs(ROOT)
        before = verify_migration()
        report["integrity"] = before
        if args.mode == "full":
            run(["tools/integration_check.py", "--output", str(output / "integration")], "integration")
            inherited = json.loads((output / "integration/RUN.json").read_text())
            if inherited["status"] != "passed":
                raise RuntimeError("Inherited integration did not pass")
            report["repository_tests"], report["acceptance"] = inherited["repository_tests"], inherited["acceptance"]
            for packet, script in (("PF-04", "study.py"), ("PF-05", "audit.py"), ("PF-06", "study.py"), ("PF-07", "study.py")):
                run([f"results/{packet}/{script}", "--output", str(output / packet)], packet)
            run(["results/PF-08/compare.py", "--input", str(output / "PF-07/diagnostics.json"),
                 "--output", str(output / "PF-08")], "PF-08")
            report["scientific_packets"] = {}
            for packet in ("PF-04", "PF-05", "PF-06", "PF-07"):
                data = json.loads((output / packet / "diagnostics.json").read_text())
                if data["status"] != "passed":
                    raise RuntimeError(f"{packet} diagnostics did not pass")
                report["scientific_packets"][packet] = {"status": data["status"],
                    "check_groups": len(data["checks"]), "elapsed_seconds": data.get("elapsed_seconds")}
            data = json.loads((output / "PF-08/summary.json").read_text())
            if data.get("status") != "passed" or data.get("analysis_tests") != 8:
                raise RuntimeError("PF-08 fixed analysis did not pass all eight checks")
            report["scientific_packets"]["PF-08"] = {key: data[key] for key in (
                "status", "analysis_tests", "small_points", "compiler_points", "small_results", "profiles_searched", "new_circuit_cases")}
            run(["figures/generate_tutorial.py", "--output", str(output / "figures")], "figures")
            report["figures"] = {}
            for name in ("tutorial-readout.svg", "tutorial-readout.json"):
                original, generated = ROOT / "figures" / name, output / "figures" / name
                if original.read_bytes() != generated.read_bytes():
                    raise RuntimeError(f"Deterministic figure differs: {name}")
                report["figures"][name] = hashlib.sha256(generated.read_bytes()).hexdigest()
            for name in ("flat_readout.py", "compile_large.py"):
                run([f"examples/{name}"], f"example-{Path(name).stem}")
            if git("status", "--porcelain", "--untracked-files=all"):
                raise RuntimeError("Validation modified the tracked checkout")
            report["clean_checkout_before_and_after"] = True
        if verify_migration() != before:
            raise RuntimeError("Immutable identities changed during validation")
        report["status"] = "passed"
    except Exception as exc:
        report["status"], report["error"] = "failed", f"{type(exc).__name__}: {exc}"
    finally:
        report["elapsed_seconds"] = time.perf_counter() - started
        report["completed_utc"] = datetime.now(timezone.utc).isoformat()
        (output / "RUN.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
        print(json.dumps(report, indent=2, allow_nan=False))
    if report["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
