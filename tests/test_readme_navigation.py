"""Reader-route regressions: start from README, not the repository file browser.

The full validation suite runs these checks. Existing check_docs.py separately
checks active link destinations, anchors, math markup, and source identities.
Historical packets can contain obsolete links; they are leaves of the active
navigation graph, not sources of new reader routes.
"""
from __future__ import annotations

from collections import deque
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_docs import active_pages, destinations


def reader_pages(root: Path) -> set[Path]:
    """All active guides plus the data/figure/example provenance guides."""
    pages = set(active_pages(root))
    for directory in ("data/recorded", "figures", "examples"):
        pages.update((root / directory).glob("*.md"))
    # Engineering context is optional to readers, but remains discoverable.
    report = root / "maintenance/repository-polish/REPORT.md"
    if report.exists():
        pages.add(report)
    return {path.resolve() for path in pages}


def readme_routes(root: Path, pages: set[Path]) -> dict[str, list[str]]:
    """Return shortest local-link paths from README to guides and their assets.

    A linked directory can route through its README, but merely pointing at a
    directory does not make all its children reachable. External URLs, code
    examples, and HTML comments cannot make a local guide count as reachable.
    """
    root = root.resolve()
    entry = root / "README.md"
    if not entry.is_file():
        raise ValueError("The reading route requires a README.md")
    pages = {path.resolve() for path in pages}
    routes = {"README.md": ["README.md"]}
    queue = deque([entry])
    while queue:
        source = queue.popleft()
        source_name = source.relative_to(root).as_posix()
        text = re.sub(r"<!--.*?-->", "", source.read_text(encoding="utf-8"), flags=re.DOTALL)
        for destination in destinations(text):
            url = urlsplit(destination)
            if url.scheme or url.netloc:
                continue
            target = (source.parent / unquote(url.path)).resolve() if url.path else source
            if not target.is_relative_to(root) or not target.exists():
                continue
            candidates = [target]
            if target.is_dir():
                candidates.append(target / "README.md")
            for path in candidates:
                if not path.exists():
                    continue
                name = path.relative_to(root).as_posix()
                if name in routes:
                    continue
                routes[name] = routes[source_name] + [name]
                if path.is_file() and path in pages:
                    queue.append(path)
    return routes


class ReadmeNavigationTests(unittest.TestCase):
    def fixture(self, files: dict[str, str]):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        root = Path(folder.name)
        for name, text in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        return root, {path.resolve() for path in root.rglob("*.md")}

    def test_indirect_routes_and_assets(self):
        root, pages = self.fixture({
            "README.md": "[Learn](docs/tutorial.md#example)",
            "docs/tutorial.md": "# Example\n[Proof](proof.md)",
            "docs/proof.md": "[Data](../data.json)", "data.json": "{}",
        })
        routes = readme_routes(root, pages)
        self.assertEqual(routes["data.json"],
                         ["README.md", "docs/tutorial.md", "docs/proof.md", "data.json"])

    def test_orphan_is_not_reached_via_code_comment_or_external_url(self):
        root, pages = self.fixture({
            "README.md": "```text\n[Fake](orphan.md)\n```\n"
                         "<!-- [Hidden](orphan.md) -->\n"
                         "[External](https://example.org/orphan.md)",
            "orphan.md": "No real incoming reader link.",
        })
        self.assertNotIn("orphan.md", readme_routes(root, pages))

    def test_cycles_terminate_and_keep_shortest_route(self):
        root, pages = self.fixture({
            "README.md": "[A](a.md) [B](b.md)",
            "a.md": "[Home](README.md) [B](b.md)",
            "b.md": "[A](a.md)",
        })
        routes = readme_routes(root, pages)
        self.assertEqual(routes["b.md"], ["README.md", "b.md"])
        self.assertEqual(len(routes), 3)

    def test_directory_readme_does_not_imply_all_children_are_linked(self):
        root, pages = self.fixture({
            "README.md": "[Guide](guide/)",
            "guide/README.md": "[Linked](linked.md)",
            "guide/linked.md": "Available.", "guide/orphan.md": "Not available through prose links.",
        })
        routes = readme_routes(root, pages)
        self.assertIn("guide/linked.md", routes)
        self.assertNotIn("guide/orphan.md", routes)

    def test_escaped_paths_and_reference_links(self):
        root, pages = self.fixture({
            "README.md": "[Read][guide]\n\n[guide]: docs/a%20guide.md#section",
            "docs/a guide.md": "# Section",
        })
        self.assertIn("docs/a guide.md", readme_routes(root, pages))

    def test_every_active_repository_guide_is_reachable(self):
        pages = reader_pages(ROOT)
        routes = readme_routes(ROOT, pages)
        required = {path.relative_to(ROOT).as_posix() for path in pages}
        required.update({"LICENSE", "CITATION.cff", "examples/flat_readout.py",
                         "examples/compile_large.py", "figures/tutorial-readout.svg",
                         "figures/tutorial-readout.json", "figures/generate_tutorial.py",
                         "maintenance/repository-polish/MIGRATION.json",
                         ".github/workflows/validation.yml", "tools/validate.py"})
        missing = sorted(required - routes.keys())
        self.assertFalse(missing, "No prose-link route from README: " + ", ".join(missing))
        print(json.dumps({"readme_navigation": "passed", "required_guides": len(pages),
                          "required_destinations": len(required),
                          "maximum_link_steps": max(len(routes[name])-1 for name in required),
                          "routes": {name: routes[name] for name in sorted(required)}}, indent=2))

    def test_tutorial_prior_work_and_hopf_are_visible_from_readme(self):
        links = set(destinations((ROOT / "README.md").read_text(encoding="utf-8")))
        for target in ("docs/TUTORIAL.md", "docs/RELATED_WORK.md", "literature/README.md",
                       "docs/RESEARCH_MAP.md", "https://github.com/GoGoKo699/Hopf-QBP"):
            self.assertIn(target, links)


if __name__ == "__main__":
    unittest.main()
