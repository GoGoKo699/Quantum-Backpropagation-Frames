"""Check active Markdown routes, local links, MIT text and repository citation.

This checks source structure, not GitHub's visual rendering or remote URLs.
Original research packets are immutable: their outgoing historical links are
not traversed. Links *to* those packets from active pages are still checked.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
MIT = """MIT License

Copyright (c) 2026 Ruge Lin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def prose(source: str) -> str:
    """Remove fenced code, preserving line count for diagnostics."""
    lines, marker = [], None
    for line in source.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            token = match.group(1)
            if marker is None:
                marker = token
            elif token[0] == marker[0] and len(token) >= len(marker):
                marker = None
            lines.append("")
        else:
            lines.append(line if marker is None else "")
    if marker is not None:
        raise ValueError("Unclosed fenced code block")
    return "\n".join(lines)


def _escaped(text: str, position: int) -> bool:
    """Whether a delimiter is preceded by an odd number of backslashes."""
    start = position
    while start and text[start - 1] == "\\":
        start -= 1
    return (position - start) % 2 == 1


def math_fragments(source: str) -> list[tuple[int, str]]:
    """Extract rendered math, including GitHub's protected $`...`$ form.

    Ordinary code fences and inline code are excluded. Backslash-escaped dollar
    signs are literal text. This is a source guard, not a Markdown/TeX renderer.
    """
    fragments, outside, body = [], [], []
    marker, language, start_line = None, None, 0
    for number, line in enumerate(source.splitlines(), 1):
        if marker is not None:
            if re.fullmatch(r"\s{0,3}" + re.escape(marker[0]) + "{" + str(len(marker)) + r",}\s*", line):
                if language == "math":
                    fragments.append((start_line, "\n".join(body)))
                marker, language, body = None, None, []
            elif language == "math":
                body.append(line)
            outside.append("")
            continue
        opening = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if opening:
            marker, language = opening.group(1), opening.group(2).strip().lower()
            start_line = number + 1
            outside.append("")
        else:
            outside.append(line)
    if marker is not None:
        raise ValueError("Unclosed fenced code block")
    text = "\n".join(outside)

    def closing(delimiter: str, offset: int) -> int:
        while True:
            position = text.find(delimiter, offset)
            if position < 0:
                return -1
            if not _escaped(text, position):
                if delimiter != "$" or not (
                    (position and text[position - 1] == "$") or
                    text[position + 1:position + 2] == "$"
                ):
                    return position
            offset = position + len(delimiter)

    position = 0
    while position < len(text):
        if _escaped(text, position):
            position += 1
            continue
        # A protected math span must be recognized before its inner backticks
        # could be mistaken for ordinary inline code.
        if text.startswith("$`", position):
            ticks = re.match(r"`+", text[position + 1:]).group()
            begin = position + 1 + len(ticks)
            end = text.find(ticks + "$", begin)
            if end >= 0:
                fragments.append((text.count("\n", 0, position) + 1, text[begin:end]))
                position = end + len(ticks) + 1
                continue
        if text[position] == "`":
            ticks = re.match(r"`+", text[position:]).group()
            end = re.search(r"(?<!`)" + re.escape(ticks) + r"(?!`)", text[position + len(ticks):])
            if end:
                position += len(ticks) + end.end()
                continue
        delimiter = next((token for token in ("$$", "$", r"\(", r"\[") if text.startswith(token, position)), None)
        if delimiter is not None:
            end_token = {r"\(": r"\)", r"\[": r"\]"}.get(delimiter, delimiter)
            begin = position + len(delimiter)
            end = closing(end_token, begin)
            if end >= 0:
                fragments.append((text.count("\n", 0, position) + 1, text[begin:end]))
                position = end + len(end_token)
                continue
        position += 1
    return fragments


def check_math(source: str) -> int:
    fragments = math_fragments(source)
    for line, fragment in fragments:
        if "<" in fragment:
            raise ValueError(f"Line {line}: literal '<' in rendered math; use \\lt followed by a space")
        for command in re.finditer(r"\\operatorname\b", fragment):
            if not _escaped(fragment, command.start()):
                raise ValueError(f"Line {line}: unsupported \\operatorname in rendered math; use plain notation or \\mathrm")
    return len(fragments)


def heading_ids(source: str) -> set[str]:
    text = prose(source)
    result = set(re.findall(r'<a\s+(?:name|id)=[\"\']([^\"\']+)', text))
    counts: dict[str, int] = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        title = match.group(1) if match else None
        if title is None and i + 1 < len(lines) and re.fullmatch(r"\s{0,3}(?:=+|-+)\s*", lines[i + 1]):
            title = line.strip() or None
        if title is None:
            continue
        title = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", title)
        title = html.unescape(re.sub(r"<[^>]+>", "", title)).lower()
        slug = "".join(c for c in title if c in "-_ " or unicodedata.category(c)[0] in "LN")
        slug = slug.replace(" ", "-")
        index = counts.get(slug, 0)
        counts[slug] = index + 1
        result.add(slug if index == 0 else f"{slug}-{index}")
    return result


def destinations(source: str) -> list[str]:
    text = prose(source)
    # Inline code may contain Markdown examples which are not links.
    text = re.sub(r"(`+).*?\1", "", text)
    result = re.findall(r"!?\[[^\]\n]*\]\(<?([^\s<>]+?)>?(?:\s+[\"'][^\n]*?[\"'])?\)", text)
    references = {key.casefold(): value for key, value in re.findall(
        r"^\s{0,3}\[([^\]]+)\]:\s*<?([^\s>]+)>?", text, re.MULTILINE)}
    result.extend(references.values())
    for label, key in re.findall(r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]", text):
        lookup = (key or label).casefold()
        if lookup not in references:
            raise ValueError(f"Undefined Markdown reference: {lookup}")
    return result


def check_link(root: Path, source: Path, destination: str) -> None:
    url = urlsplit(destination)
    if url.scheme or url.netloc:
        return
    target = (source.parent / unquote(url.path)).resolve() if url.path else source.resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"Link escapes repository: {destination}")
    if not target.exists():
        raise ValueError(f"Missing link target: {destination}")
    fragment = unquote(url.fragment)
    if not fragment:
        return
    if target.suffix.lower() == ".md":
        if fragment not in heading_ids(target.read_text(encoding="utf-8")):
            raise ValueError(f"Missing heading anchor: {destination}")
    elif re.fullmatch(r"L\d+(?:-L\d+)?", fragment) and target.is_file():
        line = int(re.findall(r"\d+", fragment)[-1])
        if line > len(target.read_text(encoding="utf-8").splitlines()):
            raise ValueError(f"Source line anchor out of range: {destination}")


def active_pages(root: Path) -> list[Path]:
    pages = list(root.glob("*.md")) + list((root / "docs").rglob("*.md"))
    for name in ("qbp_frames/README.md", "literature/README.md", "work_orders/CURRENT.md"):
        if (root / name).exists():
            pages.append(root / name)
    pages.extend((root / "examples").glob("*.md"))
    return sorted(set(pages))


def check_citation(path: Path) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("CITATION.cff must be a YAML mapping")
    for field in ("title", "message"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"CITATION.cff requires nonempty {field}")
    if data.get("cff-version") != "1.2.0" or data.get("type", "software") not in ("software", "dataset"):
        raise ValueError("Unexpected CFF version or repository type")
    if data.get("license") != "MIT":
        raise ValueError("CITATION.cff license must be MIT")
    if data.get("repository-code") != "https://github.com/GoGoKo699/Quantum-Backpropagation-Frames":
        raise ValueError("CITATION.cff must identify this repository")
    authors = data.get("authors")
    if not isinstance(authors, list) or not authors or not all(isinstance(a, dict) for a in authors):
        raise ValueError("CITATION.cff requires authors")
    if not any(a.get("family-names") == "Lin" and a.get("given-names") == "Ruge" for a in authors):
        raise ValueError("Repository author Ruge Lin is missing")
    for field in ("doi", "date-released", "version", "preferred-citation"):
        if field in data:
            raise ValueError(f"Unreleased repository must not invent {field}")


def check(root: Path = ROOT) -> dict:
    from render_source_readings import check_source_readings

    # Normalize only whitespace, allowing standard MIT line wrapping.
    if " ".join((root / "LICENSE").read_text().split()) != " ".join(MIT.split()):
        raise ValueError("LICENSE differs from standard MIT text and approved copyright")
    check_citation(root / "CITATION.cff")
    source_readings = check_source_readings(root)
    pages, links, math_count = active_pages(root), 0, 0
    for path in pages:
        source = path.read_text(encoding="utf-8")
        try:
            text = prose(source)
            for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
                if "$" in heading or r"\(" in heading:
                    raise ValueError("Math in a heading makes navigation fragile")
            math_count += check_math(source)
            if sum(line.strip() == "$$" for line in text.splitlines()) % 2:
                raise ValueError("Unpaired display-math delimiter")
            for destination in destinations(source):
                check_link(root, path, destination)
                links += 1
        except ValueError as exc:
            raise ValueError(f"{path.relative_to(root)}: {exc}") from exc
    return {"status": "passed", "active_pages": len(pages), "links_checked": links,
            "math_fragments_checked": math_count, "source_readings": source_readings,
            "license": "MIT", "citation": "CFF 1.2.0 required fields checked",
            "scope": "Active Markdown source and local targets; no visual or external-URL claim."}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
