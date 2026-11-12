"""Testa a própria régua: as checagens precisam aprovar uma saída boa e
reprovar uma saída ruim conhecida, sem chamar modelo nenhum."""
import pathlib
import sys
import unittest

SUITE = pathlib.Path(__file__).resolve().parent.parent / "build" / "evaluations" / "research-analyst"
sys.path.insert(0, str(SUITE))

import checks  # noqa: E402
import prompt  # noqa: E402

GOOD = (SUITE / "fixtures" / "reference_good.txt").read_text(encoding="utf-8")
BAD = (SUITE / "fixtures" / "reference_bad.txt").read_text(encoding="utf-8")
CTX = {"vars": {"sources": "rag-study-a, rag-study-b, finetune-cost-note"}}


class ChecksOnReferenceOutputs(unittest.TestCase):
    def test_good_output_passes_every_check(self):
        for fn in (checks.has_structure, checks.only_given_sources, checks.names_disagreements,
                   checks.actionable_next_steps, checks.under_word_limit):
            with self.subTest(check=fn.__name__):
                self.assertTrue(fn(GOOD, CTX)["pass"], fn(GOOD, CTX)["reason"])

    def test_bad_output_is_caught(self):
        self.assertFalse(checks.has_structure(BAD, CTX)["pass"])          # seções fora de ordem
        self.assertFalse(checks.only_given_sources(BAD, CTX)["pass"])     # "Smith et al." inventado
        self.assertFalse(checks.names_disagreements(BAD, CTX)["pass"])    # "None."
        self.assertFalse(checks.actionable_next_steps(BAD, CTX)["pass"])  # um passo vago

    def test_word_limit(self):
        self.assertFalse(checks.under_word_limit("palavra " * 700, CTX)["pass"])

    def test_clarification(self):
        self.assertTrue(checks.asks_clarification("Could you share the question and the sources?", CTX)["pass"])
        self.assertFalse(checks.asks_clarification(GOOD, CTX)["pass"])


class PromptAssembly(unittest.TestCase):
    def test_system_prompt_comes_from_the_prompt_doc(self):
        self.assertTrue(prompt.system_prompt().startswith("You are a senior research analyst."))

    def test_every_fixture_used_by_the_suite_exists(self):
        config = (SUITE / "promptfooconfig.yaml").read_text(encoding="utf-8")
        for line in config.splitlines():
            if line.strip().startswith("sources:") and '"' not in line:
                for name in line.split(":", 1)[1].split(","):
                    self.assertTrue((SUITE / "fixtures" / f"{name.strip()}.txt").exists(), name)

    def test_empty_input_is_explicit(self):
        msg = prompt.user_message("", "")
        self.assertIn("(no question provided)", msg)
        self.assertIn("(no sources provided)", msg)


if __name__ == "__main__":
    unittest.main()
