"""Regressions for literal ket/absolute-value pipes in GitHub Markdown tables."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_table_cells import cells, check_tables, tables


class TableCellTests(unittest.TestCase):
    def test_ket_inside_backticks_is_not_a_protected_separator(self):
        with self.assertRaisesRegex(ValueError, "expected 3"):
            check_tables("| Parameter | Gate | Tangent |\n|---|---|---|\n| t | YI | `|10⟩` |")

    def test_escaped_ket_retains_three_cells(self):
        text = "| Parameter | Gate | Tangent |\n|---|---|---|\n| t | YI | `\\|10⟩` |"
        self.assertEqual(check_tables(text), 2)
        self.assertEqual(tables(text)[0]["rows"][1][2][2], r"`\|10⟩`")

    def test_pipe_in_protected_math_still_needs_table_escape(self):
        with self.assertRaises(ValueError):
            check_tables("| Object | Meaning |\n|---|---|\n| $`|x|`$ | magnitude |")
        self.assertEqual(check_tables(
            r"| Object | Meaning |" + "\n|---|---|\n" + r"| $`\lvert x\rvert`$ | magnitude |"), 2)

    def test_extra_or_missing_cells_are_not_silently_discarded(self):
        for body in ("| a | b | c |", "| a |"):
            with self.subTest(body=body), self.assertRaises(ValueError):
                check_tables("| A | B |\n|---|---|\n" + body)
        self.assertEqual(check_tables("| A | B |\n|---|---|\n| a | |"), 2)

    def test_headers_and_backtick_delimiter_widths(self):
        with self.assertRaises(ValueError):
            check_tables("| A | B | C |\n|---|---|\n| a | b |")
        self.assertEqual(check_tables("A | B\n:--- | ---:\n``a ` \\| b`` | c"), 2)
        # A raw pipe must not silently turn one code span into two cells.
        with self.assertRaises(ValueError):
            check_tables("A | B\n---|---\n`a|b`")

    def test_code_fences_comments_and_non_table_kets_are_ignored(self):
        bad = "| A | B |\n|---|---|\n| `|x⟩` | b |"
        for text in ("```md\n" + bad + "\n```", "~~~~\n" + bad + "\n~~~~",
                     "<!--\n" + bad + "\n-->", "A paragraph with `|x⟩` and $|q⟩$."):
            with self.subTest(text=text):
                self.assertEqual(check_tables(text), 0)

    def test_actual_tutorial_keeps_all_six_tangents(self):
        source = (ROOT / "docs/TUTORIAL.md").read_text(encoding="utf-8")
        matching = [t for t in tables(source)
                    if "Tangent at zero angles" in t["rows"][0][2]]
        self.assertEqual(len(matching), 1)
        rows = matching[0]["rows"][1:]
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(len(row) == 3 for _, _, row in rows))
        values = [row[2].strip("`").replace(r"\|", "|") for _, _, row in rows]
        self.assertEqual(values, ["|10⟩", "|01⟩", "|11⟩", "|11⟩", "|10⟩", "|01⟩"])

    def test_all_active_reader_tables(self):
        from check_docs import active_pages
        pages = active_pages(ROOT)
        errors, count = [], 0
        for path in pages:
            try:
                count += check_tables(path.read_text(encoding="utf-8"))
            except ValueError as exc:
                errors.append(f"{path.relative_to(ROOT)}: {exc}")
        self.assertFalse(errors, "\n".join(errors))
        self.assertGreater(count, 6)
        print(f"Checked {count} table header/body rows across {len(pages)} active pages.", file=sys.stderr)


if __name__ == "__main__":
    unittest.main()
