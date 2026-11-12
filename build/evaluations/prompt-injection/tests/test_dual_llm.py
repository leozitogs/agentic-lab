"""Linguagem de plano do dual LLM: validação, substituição e execução."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from pikit.agent import Defenses  # noqa: E402
from pikit.dual_llm import PLANNER_SYSTEM, PlanError, parse_plan, run_dual_llm, substitute  # noqa: E402
from pikit.environment import load_all  # noqa: E402
from pikit.fakes import ScriptedModel  # noqa: E402
from pikit.providers import ModelTurn  # noqa: E402

INBOX, TASKS, _ = load_all()
TASK = {t["id"]: t for t in TASKS}


class Parse(unittest.TestCase):
    def test_valid(self):
        steps = parse_plan('{"steps": [{"op": "answer", "text": "oi"}]}')
        self.assertEqual(steps, [{"op": "answer", "text": "oi"}])

    def test_accepts_bare_list_and_surrounding_text(self):
        self.assertEqual(len(parse_plan('[{"op": "answer", "text": "x"}]')), 1)
        self.assertEqual(len(parse_plan('Plano: {"steps": [{"op": "answer", "text": "x"}]} fim')), 1)

    def test_rejects(self):
        for bad in ["", "não é json", '{"steps": []}', '{"steps": [{"op": "delete_all"}]}',
                    '{"steps": [{"op": "extract", "input": "E1"}]}']:
            with self.subTest(bad=bad):
                with self.assertRaises(PlanError):
                    parse_plan(bad)

    def test_prompt_formats(self):
        text = PLANNER_SYSTEM.format(**INBOX["user"])
        self.assertIn('{"op": "answer"', text)
        self.assertNotIn(INBOX["user"]["secret"], text)


class Substitute(unittest.TestCase):
    def test_forms(self):
        env = {"V1": "quinta às 15h"}
        self.assertEqual(substitute("Em {V1}.", env), "Em quinta às 15h.")
        self.assertEqual(substitute("Em {{V1}} e $V1", env), "Em quinta às 15h e quinta às 15h")
        self.assertEqual(substitute("{V9} fica", env), "{V9} fica")


class Execute(unittest.TestCase):
    def test_replans_once_then_gives_up(self):
        planner = ScriptedModel([ModelTurn("lixo"), ModelTurn("lixo de novo")])
        res = run_dual_llm(planner, planner, INBOX, TASK["T3"], Defenses(dual_llm=True))
        self.assertTrue(res.error.startswith("PlanError"))
        self.assertEqual(res.model_calls, 2)
        self.assertEqual(res.final_answer, "")

    def test_ambiguous_contact_sends_nothing(self):
        plan = ('{"steps": [{"op": "find_contact", "query": "Ana", "save": "C1"},'
                '{"op": "send_email", "to": "C1", "subject": "s", "body": "b"},'
                '{"op": "answer", "text": "ok"}]}')
        res = run_dual_llm(ScriptedModel([ModelTurn(plan)]), None, INBOX, TASK["T4"], Defenses(dual_llm=True))
        self.assertEqual(res.log.sent(), [])
        self.assertEqual([e.note for e in res.log.events if e.tool == "search_contacts"], ["ambíguo"])

    def test_select_logs_reads_and_extract_uses_extractor(self):
        plan = ('{"steps": [{"op": "select_emails", "date": "today", "save": "E1"},'
                '{"op": "extract", "input": "E1", "instruction": "resuma", "save": "V1"},'
                '{"op": "answer", "text": "Resumo: {V1}"}]}')
        extractor = ScriptedModel([ModelTurn("cinco e-mails")])
        res = run_dual_llm(ScriptedModel([ModelTurn(plan)]), extractor, INBOX, TASK["T1"], Defenses(dual_llm=True))
        reads = [e.args["email_id"] for e in res.log.events if e.tool == "read_email"]
        self.assertEqual(reads, ["e01", "e02", "e03", "e04", "e05"])
        self.assertEqual(res.final_answer, "Resumo: cinco e-mails")
        self.assertIn("Revisão do protótipo", extractor.seen[0][-1]["content"])
        self.assertEqual(res.model_calls, 2)
