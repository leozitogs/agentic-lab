"""Chunkers: janelas fixas e seções por título, sem corpus real."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from ragkit.chunking import fixed_chunks, split_sections, structure_chunks  # noqa: E402

DOC = """# Guide

Intro paragraph.

## Install

Run pip.

```bash
# not a heading, just a shell comment
pip install thing
```

## Empty

### Child

Child text.

````markdown
```
## also not a heading (nested fence)
```
````

## Last

Final words.
"""


class FixedChunks(unittest.TestCase):
    def test_windows_overlap_and_cover_the_text(self):
        text = "".join(chr(97 + i % 26) for i in range(2000))
        chunks = fixed_chunks("a.md", text, size=800, overlap=200)
        self.assertEqual([len(c.text) for c in chunks], [800, 800, 800])
        self.assertEqual(chunks[0].text[600:], chunks[1].text[:200])
        self.assertTrue(text.endswith(chunks[-1].text))
        self.assertEqual(chunks[0].index_text, chunks[0].text)

    def test_any_span_up_to_overlap_fits_in_one_window(self):
        text = "".join(chr(97 + (i * 7) % 26) for i in range(3001))
        chunks = fixed_chunks("a.md", text, size=100, overlap=30)
        for start in range(0, len(text) - 30):
            span = text[start:start + 30]
            self.assertTrue(any(span in c.text for c in chunks), start)

    def test_short_text_is_one_chunk_and_blank_is_none(self):
        self.assertEqual(len(fixed_chunks("a.md", "hello", 800, 200)), 1)
        self.assertEqual(fixed_chunks("a.md", "   \n  ", 800, 200), [])

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            fixed_chunks("a.md", "x", size=100, overlap=100)
        with self.assertRaises(ValueError):
            fixed_chunks("a.md", "x", size=0, overlap=0)

    def test_ids_are_unique_and_carry_the_doc(self):
        chunks = fixed_chunks("dir/a.md", "x" * 5000)
        self.assertEqual(len({c.id for c in chunks}), len(chunks))
        self.assertTrue(all(c.doc == "dir/a.md" for c in chunks))


class Sections(unittest.TestCase):
    def test_hash_lines_inside_fences_are_not_headings(self):
        paths = [" > ".join(p) for p, _ in split_sections(DOC) if p]
        self.assertEqual(paths, [
            "Guide", "Guide > Install", "Guide > Empty", "Guide > Empty > Child", "Guide > Last",
        ])

    def test_structure_chunks_skip_heading_only_sections_and_prefix_the_path(self):
        chunks = structure_chunks("guide.md", DOC)
        self.assertEqual([c.heading for c in chunks],
                         ["Guide", "Guide > Install", "Guide > Empty > Child", "Guide > Last"])
        child = chunks[2]
        self.assertTrue(child.text.startswith("### Child"))
        self.assertTrue(child.index_text.startswith("Guide > Empty > Child\n\n### Child"))
        self.assertIn("## also not a heading", child.text)

    def test_text_before_first_heading_is_kept(self):
        chunks = structure_chunks("a.md", "Preamble text.\n\n# Title\n\nBody.\n")
        self.assertEqual(chunks[0].heading, "")
        self.assertEqual(chunks[0].text, "Preamble text.")
        self.assertEqual(chunks[0].index_text, "Preamble text.")

    def test_long_sections_split_between_paragraphs(self):
        paragraphs = [f"Paragraph {i} " + "word " * 40 for i in range(10)]
        text = "# Big\n\n" + "\n\n".join(paragraphs)
        chunks = structure_chunks("big.md", text, max_chars=500)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(c.text) <= 500 for c in chunks))
        self.assertTrue(all(c.heading == "Big" for c in chunks))
        for p in paragraphs:  # nenhum parágrafo foi cortado
            self.assertTrue(any(p.strip() in c.text for c in chunks))

    def test_code_fence_with_blank_lines_stays_in_one_block(self):
        code = "```python\ndef f():\n\n    return 1\n```"
        chunks = structure_chunks("c.md", f"# T\n\n{code}\n\nAfter.\n", max_chars=1000)
        self.assertEqual(len(chunks), 1)
        self.assertIn(code, chunks[0].text)

    def test_oversized_block_is_split_between_lines(self):
        block = "\n".join(f"* item {i} " + "x" * 50 for i in range(40))
        chunks = structure_chunks("l.md", f"# List\n\n{block}\n", max_chars=400)
        self.assertTrue(all(len(c.text) <= 400 for c in chunks))
        self.assertEqual("\n".join(c.text for c in chunks).count("* item"), 40)


if __name__ == "__main__":
    unittest.main()
