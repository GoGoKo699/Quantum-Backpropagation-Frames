"""Guard the GFM table stage, where backticks do NOT protect literal pipes.

A source guard, not a full Markdown renderer. Active repository tables must
spell out every cell; this deliberately rejects GFM's silent padding/truncation.
Reference: https://github.github.com/gfm/#tables-extension- (example 200).
"""
from __future__ import annotations

import re


def _lines(source: str) -> list[str]:
    source = re.sub(r"<!--.*?-->", lambda m: "\n" * m[0].count("\n"),
                    source, flags=re.DOTALL)
    result, marker = [], None
    for line in source.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if marker is not None:
            if re.fullmatch(r"\s{0,3}" + re.escape(marker[0]) +
                            "{" + str(len(marker)) + r",}\s*", line):
                marker = None
            result.append("")
        elif match:
            marker = match[1]
            result.append("")
        else:
            # Indented code cannot start a top-level GFM table.
            result.append("" if line.startswith(("    ", "\t")) else line)
    return result


def cells(line: str) -> list[str]:
    """Split the table layer before inline markup, retaining escaped cell text.

    GFM's table parser protects a pipe immediately preceded by a backslash,
    including inside a code span. It does not otherwise parse code/math here.
    """
    text = line.strip()
    dividers = [i for i, ch in enumerate(text)
                if ch == "|" and (i == 0 or text[i-1] != "\\")]
    boundaries = [-1, *dividers, len(text)]
    result = [text[a+1:b].strip() for a, b in zip(boundaries, boundaries[1:])]
    if dividers and dividers[-1] == len(text)-1:
        result.pop()
    if dividers and dividers[0] == 0:
        result.pop(0)
    return result


def tables(source: str) -> list[dict]:
    """Find pipe tables with line numbers; keep excess cells for diagnostics."""
    lines = _lines(source)
    found = []
    i = 1
    while i < len(lines):
        delimiter = cells(lines[i])
        if not ("|" in lines[i-1] and delimiter and
                all(re.fullmatch(r":?-+:?", cell) for cell in delimiter)):
            i += 1
            continue
        rows = [(i, lines[i-1], cells(lines[i-1]))]
        j = i + 1
        while j < len(lines) and lines[j].strip() and "|" in lines[j]:
            if re.match(r"^\s{0,3}(?:#{1,6}\s|>|[-+*]\s)", lines[j]):
                break
            rows.append((j+1, lines[j], cells(lines[j])))
            j += 1
        found.append({"columns": len(delimiter), "rows": rows})
        i = max(i+1, j)
    return found


def check_tables(source: str) -> int:
    """Reject lost/shifted columns and raw pipes hidden in inline code/math."""
    found, errors = tables(source), []
    for table in found:
        width = table["columns"]
        for number, raw, row in table["rows"]:
            if len(row) != width:
                errors.append(f"Line {number}: table has {len(row)} cells; expected {width}. "
                              "Escape literal pipes as \\| even inside backticks; "
                              "do not rely on silently discarded/padded cells.")
            # Also detect a hidden separator when accidental row arity matches.
            for span in re.finditer(r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)", raw):
                body = span[2]
                if any(ch == "|" and (i == 0 or body[i-1] != "\\")
                       for i, ch in enumerate(body)):
                    errors.append(f"Line {number}: unescaped pipe inside table code/math span.")
    if errors:
        raise ValueError("\n".join(errors))
    return sum(len(table["rows"]) for table in found)
