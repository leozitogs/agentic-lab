import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from repo_knowledge_server.catalog import AccessDenied, Catalog  # noqa: E402

DOC = """---
tipo: {tipo}
maturidade: {mat}
versao: 0.1.0
autores: [ana]
criado_em: 2026-01-01
atualizado_em: 2026-01-01
tags: [{tags}]
---

# {title}

## Objetivo

{goal}
"""


def make_repo(root: pathlib.Path) -> None:
    files = {
        "build/prompts/system/summarizer.md": DOC.format(tipo="prompt", mat="tested", tags="sintese, pesquisa", title="Summarizer", goal="Resumir artigos científicos com citações."),
        "build/skills/triage/SKILL.md": DOC.format(tipo="skill", mat="draft", tags="suporte", title="Triage", goal="Classificar tickets de suporte por urgência."),
        "learn/notes/nota.md": DOC.format(tipo="note", mat="draft", tags="", title="Nota sobre avaliação", goal="Avaliação de prompts com rubrica."),
        "build/skills/triage/examples.md": "# exemplos sem front-matter\n",
        "build/.hidden/secret.md": DOC.format(tipo="prompt", mat="draft", tags="", title="Oculto", goal="não deve aparecer"),
        "README.md": "# raiz\n",
        "segredo.txt": "não é markdown\n",
    }
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


class CatalogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        make_repo(self.root)
        self.cat = Catalog(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_indexes_only_artifacts_with_frontmatter(self):
        self.assertEqual(sorted(self.cat.items), ["build/prompts/system/summarizer.md", "build/skills/triage/SKILL.md", "learn/notes/nota.md"])

    def test_title_and_summary_come_from_the_document(self):
        a = self.cat.items["build/prompts/system/summarizer.md"]
        self.assertEqual(a.title, "Summarizer")
        self.assertEqual(a.summary, "Resumir artigos científicos com citações.")
        self.assertEqual(a.tags, ("sintese", "pesquisa"))

    def test_search_ranks_title_matches_first_and_ignores_accents(self):
        results = self.cat.search("avaliacao")
        self.assertEqual(results[0][1].path, "learn/notes/nota.md")
        self.assertEqual(self.cat.search("SUMMARIZER")[0][1].path, "build/prompts/system/summarizer.md")

    def test_search_filters(self):
        self.assertEqual([a.path for _, a in self.cat.search("tickets", tipo="prompt")], [])
        self.assertEqual(len(self.cat.search("tickets", tipo="skill")), 1)
        self.assertEqual(self.cat.search("   "), [])

    def test_filter_by_tag_is_case_and_accent_insensitive(self):
        self.assertEqual([a.path for a in self.cat.filter(tag="Síntese")], ["build/prompts/system/summarizer.md"])

    def test_read_allows_repo_markdown(self):
        self.assertIn("Summarizer", self.cat.read("build/prompts/system/summarizer.md"))
        self.assertIn("raiz", self.cat.read("README.md"))

    def test_read_blocks_unsafe_paths(self):
        for bad in ["../etc/passwd.md", "/etc/passwd.md", "C:/Windows/x.md", "build/../../x.md",
                    "build/.hidden/secret.md", "segredo.txt", "", "build/x\x00.md", "outra/pasta/x.md"]:
            with self.subTest(path=bad), self.assertRaises(AccessDenied):
                self.cat.read(bad)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            self.cat.read("build/prompts/nao-existe.md")

    def test_index_markdown(self):
        md = self.cat.index_markdown("prompt")
        self.assertIn("[Summarizer](repo://artifact/build/prompts/system/summarizer.md)", md)
        self.assertIn("Nenhum artefato", self.cat.index_markdown("case"))


class RealRepositoryTest(unittest.TestCase):
    def test_real_repo_has_expected_artifacts(self):
        cat = Catalog()
        self.assertIn("build/prompts/system/research-analyst.md", cat.items)
        self.assertIn("build/mcp-servers/repo-knowledge/README.md", cat.items)
        self.assertTrue(cat.search("research analyst", tipo="prompt"))


if __name__ == "__main__":
    unittest.main()
