"""Formato do questions.jsonl versionado e regras da validação contra o corpus."""
import json
import pathlib
import sys
import unittest

KIT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT))

from ragkit import questions  # noqa: E402
from ragkit.chunking import fixed_chunks, structure_chunks  # noqa: E402

ROWS = questions.load(KIT / "questions.jsonl")


def row(**over):
    base = {"id": "q01", "question": "How do I deploy?", "doc": "deploy.md",
            "evidence": "run the deploy command", "category": "deploy", "style": "literal"}
    base.update(over)
    return base


class VersionedSet(unittest.TestCase):
    def test_has_50_valid_questions(self):
        self.assertEqual(questions.validate_format(ROWS), [])
        self.assertEqual(len(ROWS), 50)

    def test_every_line_is_a_json_object(self):
        lines = (KIT / "questions.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertTrue(all(isinstance(json.loads(line), dict) for line in lines if line.strip()))

    def test_mix_of_styles_and_categories(self):
        styles = {r["style"] for r in ROWS}
        self.assertEqual(styles, questions.STYLES)
        paraphrases = sum(r["style"] == "parafrase" for r in ROWS)
        self.assertGreaterEqual(paraphrases, 10)
        self.assertEqual({r["category"] for r in ROWS}, questions.CATEGORIES)

    def test_error_notes_point_to_existing_ids(self):
        notes = json.loads((KIT / "error_notes.json").read_text(encoding="utf-8"))
        self.assertTrue(3 <= len(notes) <= 5)
        self.assertLessEqual(set(notes), {r["id"] for r in ROWS})


class FormatRules(unittest.TestCase):
    def check(self, *rows, count=None):
        return questions.validate_format(list(rows), expected_count=count)

    def test_valid_row(self):
        self.assertEqual(self.check(row()), [])

    def test_count(self):
        self.assertTrue(self.check(row(), count=50))

    def test_missing_and_unknown_fields(self):
        bad = row()
        del bad["evidence"]
        self.assertTrue(self.check(bad))
        self.assertTrue(self.check(row(extra="x")))

    def test_duplicate_and_malformed_ids(self):
        self.assertTrue(self.check(row(), row()))
        self.assertTrue(self.check(row(id="Q1")))

    def test_evidence_word_limits(self):
        self.assertTrue(self.check(row(evidence="too short")))
        self.assertTrue(self.check(row(evidence=" ".join(["word"] * 13))))
        self.assertEqual(self.check(row(evidence=" ".join(["word"] * 12))), [])

    def test_doc_path_category_style_and_question_mark(self):
        self.assertTrue(self.check(row(doc="/abs.md")))
        self.assertTrue(self.check(row(doc="notes.txt")))
        self.assertTrue(self.check(row(category="outra")))
        self.assertTrue(self.check(row(style="misto")))
        self.assertTrue(self.check(row(question="No question mark")))


class CorpusRules(unittest.TestCase):
    DOCS = {
        "deploy.md": "# Deploy\n\nTo publish, run the deploy command from the root.\n",
        "other.md": "# Other\n\nShared phrase here. Shared phrase here.\n\nShared phrase here. Shared phrase here.\n",
    }

    def chunkings(self, docs):
        return {"fixed": [c for p, t in docs.items() for c in fixed_chunks(p, t, 40, 30)],
                "structure": [c for p, t in docs.items() for c in structure_chunks(p, t)]}

    def validate(self, *rows, docs=None):
        docs = docs or self.DOCS
        return questions.validate_against_corpus(list(rows), docs, self.chunkings(docs))

    def test_evidence_found_after_normalization(self):
        self.assertEqual(self.validate(row(evidence="RUN the\n deploy   command")), [])

    def test_missing_doc_and_missing_evidence(self):
        self.assertIn("não existe", self.validate(row(doc="nope.md"))[0])
        self.assertIn("não aparece", self.validate(row(evidence="something else entirely"))[0])

    def test_evidence_in_another_doc_only_is_rejected(self):
        self.assertTrue(self.validate(row(evidence="Shared phrase here.")))

    def test_too_many_occurrences(self):
        problems = self.validate(row(doc="other.md", evidence="Shared phrase here."))
        self.assertTrue(any("vezes" in p for p in problems))

    def test_unreachable_in_a_chunking(self):
        long_evidence = "to publish, run the deploy command from the root"
        problems = self.validate(row(evidence=long_evidence))
        self.assertTrue(any("'fixed'" in p for p in problems), problems)
        self.assertFalse(any("'structure'" in p for p in problems), problems)


if __name__ == "__main__":
    unittest.main()
