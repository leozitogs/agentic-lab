import pathlib
import sys
import tempfile
import textwrap
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

import validate_frontmatter as vf  # noqa: E402

GOOD = """\
---
tipo: {tipo}
maturidade: draft
versao: 0.1.0
autores: [ana]
criado_em: 2026-01-10
atualizado_em: 2026-02-01
{extra}---

# Título
"""


class ValidatorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text), encoding="utf-8")
        return path

    def problems(self, rel, text):
        return [p.message for p in vf.validate_file(self.write(rel, text), self.root)]

    def test_valid_prompt_passes(self):
        self.assertEqual(self.problems("build/prompts/x.md", GOOD.format(tipo="prompt", extra="")), [])

    def test_missing_frontmatter_fails(self):
        self.assertIn("sem front-matter (ver ops/TAGS.md)", self.problems("build/prompts/x.md", "# sem\n"))

    def test_companion_files_are_exempt(self):
        self.assertEqual(self.problems("build/skills/s/examples.md", "# exemplos\n"), [])

    def test_unknown_tipo_fails(self):
        msgs = self.problems("build/prompts/x.md", GOOD.format(tipo="poema", extra=""))
        self.assertTrue(any("tipo inválido" in m for m in msgs))

    def test_wrong_home_fails(self):
        msgs = self.problems("learn/notes/x.md", GOOD.format(tipo="prompt", extra=""))
        self.assertTrue(any("deveria morar" in m for m in msgs))

    def test_bad_semver_fails(self):
        text = GOOD.format(tipo="prompt", extra="").replace("0.1.0", "v1")
        self.assertTrue(any("X.Y.Z" in m for m in self.problems("build/prompts/x.md", text)))

    def test_dates_out_of_order_fail(self):
        text = GOOD.format(tipo="prompt", extra="").replace("2026-02-01", "2025-12-31")
        self.assertIn("atualizado_em é anterior a criado_em", self.problems("build/prompts/x.md", text))

    def test_adr_needs_valid_status(self):
        self.assertIn("ADR sem campo status", self.problems("ops/decisions/a.md", GOOD.format(tipo="adr", extra="")))
        msgs = self.problems("ops/decisions/b.md", GOOD.format(tipo="adr", extra="status: talvez\n"))
        self.assertTrue(any("status de ADR inválido" in m for m in msgs))
        self.assertEqual(self.problems("ops/decisions/c.md", GOOD.format(tipo="adr", extra="status: aceito\n")), [])

    def test_template_allows_placeholder_dates(self):
        text = GOOD.format(tipo="prompt", extra="").replace("2026-01-10", "YYYY-MM-DD").replace("2026-02-01", "YYYY-MM-DD")
        self.assertEqual(self.problems("build/prompts/PROMPT-TEMPLATE.md", text), [])

    def test_score_out_of_range_fails(self):
        msgs = self.problems("build/prompts/x.md", GOOD.format(tipo="prompt", extra="nota_avaliacao: 140\n"))
        self.assertTrue(any("nota_avaliacao" in m for m in msgs))

    def test_unclosed_frontmatter_fails(self):
        msgs = self.problems("build/prompts/x.md", "---\ntipo: prompt\n")
        self.assertTrue(any("nunca fechado" in m for m in msgs))


class RepositoryTest(unittest.TestCase):
    def test_repository_is_clean(self):
        problems = [p for f in vf.collect() for p in vf.validate_file(f)]
        self.assertEqual([str(p) for p in problems], [])


if __name__ == "__main__":
    unittest.main()
