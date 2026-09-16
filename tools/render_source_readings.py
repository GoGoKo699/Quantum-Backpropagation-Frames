"""Generate GitHub-readable copies of four byte-preserved source documents.

Only math-rendering syntax changes: operatorname becomes mathrm and literal
less-than signs become the equivalent lt command inside mathematical fences.
The four pinned sources contain no dollar-delimited inline math. Original
wording outside math, original files, and historical manifests are unchanged.

Run without arguments to regenerate the reading copies, or use --check for a
read-only identity and exact-generation check. Both work from any directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
READINGS = (
    (
        "results/PF-04/STRUCTURE.md",
        "7136645f6f9ecbf2ffc6aa3f3f24f8bdc5e7f639299dfd1d030bd7e16bdce199",
        "docs/source-readings/local-tangent-structure.md",
    ),
    (
        "results/PF-06/PROOF.md",
        "ad3389ce5a29d1f1e0ebe6c0f4db91472280608d634a1c8256ecead895d375d7",
        "docs/source-readings/disjoint-proof.md",
    ),
    (
        "results/PF-07/PROOF.md",
        "f5d243f28f2bb54c6a2301fd06de0eb69a36c5a4c57be02a8e482e31beed1045",
        "docs/source-readings/interval-proof.md",
    ),
    (
        "results/PF-08/CORE_RESULT.md",
        "8b295cfaee8eae0d50b4143faaad968f064e3a00a639c98170e8b410417f4405",
        "docs/source-readings/core-result.md",
    ),
)


def checked_path(root: Path, relative: str) -> Path:
    path = root / relative
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Invalid source-reading path: {relative}")
    return path


def render_math(source: str) -> tuple[str, dict[str, int]]:
    """Apply only the two equivalent TeX substitutions to fenced mathematics.

    Deliberately scoped to the pinned documents, not a general Markdown
    converter. Reject unsupported structural changes instead of guessing how
    a newly added source should be interpreted.
    """
    output = []
    fence = None
    mathematical = False
    counts = {"operatorname_replacements": 0, "less_than_replacements": 0}
    for line in source.splitlines(keepends=True):
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})([^\r\n]*)", line)
        if match:
            token, language = match.groups()
            if fence is None:
                fence = token
                mathematical = language.strip() == "math"
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
                mathematical = False
            output.append(line)
            continue
        if mathematical:
            line, count = re.subn(
                r"\\operatorname\{([A-Za-z][A-Za-z0-9]*)\}",
                lambda match: r"\mathrm{" + match.group(1) + "}",
                line,
            )
            counts["operatorname_replacements"] += count
            if r"\operatorname" in line:
                raise ValueError("Unrecognized operatorname syntax in a pinned source")
            counts["less_than_replacements"] += line.count("<")
            line = line.replace("<", r"\lt ")
        elif fence is None and "$" in line:
            raise ValueError("Pinned sources unexpectedly contain inline dollar math")
        output.append(line)
    if fence is not None:
        raise ValueError("Unclosed fence in a pinned source")
    return "".join(output), counts


def expected_readings(root: Path) -> list[tuple[Path, bytes, dict]]:
    """Verify all originals before computing any derived output."""
    checked = []
    for original, digest, reading in READINGS:
        path = checked_path(root, original)
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError(f"Preserved source identity mismatch: {original}")
        checked.append((original, digest, reading, raw.decode("utf-8")))
    results = []
    for original, digest, reading, source in checked:
        transformed, counts = render_math(source)
        title, separator, body = transformed.partition("\n")
        if not separator or not title.startswith("# "):
            raise ValueError(f"Expected an original document title: {original}")
        provenance = (
            "\n\n[Canonical theory](../THEORY.md) · "
            "[Constructive circuits](../COMPILERS.md) · "
            "[Evidence](../EVIDENCE.md)\n\n"
            "Reading copy with mathematical rendering syntax adjusted. "
            "The source's scientific statements and wording are preserved. "
            f"[Original source, plain view](../../{original}?plain=1).\n\n"
            "Original source SHA-256:\n\n"
            f"```text\n{digest}\n```\n\n"
            "[Deterministic generator and identity check]"
            "(../../tools/render_source_readings.py).\n"
        )
        expected = (title + provenance + body).encode("utf-8")
        summary = {
            "original": original,
            "original_sha256": digest,
            "reading": reading,
            "reading_sha256": hashlib.sha256(expected).hexdigest(),
            **counts,
        }
        results.append((checked_path(root, reading), expected, summary))
    return results


def check_source_readings(root: Path = ROOT) -> dict:
    """Read-only check of source pins and exact generated reading-copy bytes."""
    results = expected_readings(Path(root))
    for path, expected, summary in results:
        if not path.is_file() or path.read_bytes() != expected:
            raise ValueError(f"Source reading differs from deterministic rendering: {summary['reading']}")
    return {
        "status": "passed",
        "original_sources_verified": len(results),
        "reading_copies_verified": len(results),
        "scope": "Pinned source identity and exact mechanical rendering; no scientific modification.",
        "readings": [summary for _, _, summary in results],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Read-only verification; never write files")
    args = parser.parse_args()
    if not args.check:
        # All source identities are checked before the first derived write.
        for path, content, _ in expected_readings(ROOT):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    print(json.dumps(check_source_readings(ROOT), indent=2))


if __name__ == "__main__":
    main()
