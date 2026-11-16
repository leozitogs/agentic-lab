"""Regressões de retomada e publicação pelo entry point, sem modelo ou rede."""
import argparse
from contextlib import redirect_stdout
import io
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import run_eval
from pikit import experiment
from pikit.agent import RunResult, CONFIGS
from pikit.environment import load_all


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = pathlib.Path(self.temporary.name)
        self.results = self.root / "results"
        self.cache = self.root / "cache"
        self.patches = [
            patch.object(run_eval, "RESULTS", self.results),
            patch.object(run_eval, "CACHE", self.cache),
            patch.object(run_eval, "make_provider", return_value=object()),
            patch.object(run_eval, "environment", return_value={
                "model": "fake", "provider": "fake", "platform": "test", "python": "test",
                "ollama_version": "-", "model_details": ""}),
            patch.object(run_eval, "run_case", return_value=RunResult(final_answer="x" * 2500)),
        ]
        self.mocks = [p.start() for p in self.patches]
        for p in self.patches:
            self.addCleanup(p.stop)
        self.runner = self.mocks[-1]

    def invoke(self, *extra):
        with redirect_stdout(io.StringIO()):
            return run_eval.main(["--configs", "baseline", "--tasks", "T3", "--attacks", "A6",
                                  "--reps", "1", "--model-revision", "digest-v1", *extra])

    def journal(self):
        identity = json.loads((self.results / "results.json").read_text(encoding="utf-8"))["experiment_id"]
        return self.cache / "experiments" / identity / "runs.jsonl"

    def test_entrypoint_resume_and_full_audit(self):
        self.assertEqual(self.invoke(), 0)
        self.assertEqual(self.runner.call_count, 2)
        published = json.loads((self.results / "results.json").read_text(encoding="utf-8"))
        archive = self.results / published["audit_artifacts"]
        records = [json.loads(line) for line in (archive / "runs.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["final_answer"], "x" * 2500)
        self.assertLess(len(published["runs"][0]["final_answer"]), 2500)
        self.assertIn(published["experiment_id"], (self.results / "report.md").read_text(encoding="utf-8"))
        self.invoke()
        self.assertEqual(self.runner.call_count, 2)
        self.assertEqual(len(list(self.results.glob("experiments/*/*/manifest.json"))), 2)

    def test_fresh_and_unpinned_invocations_preserve_history(self):
        self.invoke()
        original = self.journal().read_bytes()
        self.invoke("--fresh")
        self.invoke("--model-revision", "")
        self.invoke("--model-revision", "")
        self.assertEqual(len(list(self.cache.glob("experiments/*/runs.jsonl"))), 4)
        self.assertIn(original, [p.read_bytes() for p in self.cache.glob("experiments/*/runs.jsonl")])

    def test_subset_publishes_complete_journal_and_configs_are_unique(self):
        self.invoke("--tasks", "T3,T4", "--configs", "baseline,baseline")
        self.assertEqual(self.runner.call_count, 4)
        self.invoke()
        self.assertEqual(self.runner.call_count, 4)
        published = json.loads((self.results / "results.json").read_text(encoding="utf-8"))
        self.assertEqual(published["n_runs"], 2)
        snapshot = self.results / published["audit_artifacts"] / "runs.jsonl"
        self.assertEqual(len(snapshot.read_bytes().splitlines()), 4)
        self.assertEqual(snapshot.read_bytes(), self.journal().read_bytes())

    def test_failed_and_turn_limited_cases_retry(self):
        for value in (RunResult(error="temporary"), RunResult(hit_turn_limit=True)):
            with self.subTest(value=value):
                revision = "error" if value.error else "turn-limit"
                self.runner.return_value = value
                self.invoke("--model-revision", revision)
                calls = self.runner.call_count
                self.runner.return_value = RunResult(final_answer="recovered")
                self.invoke("--model-revision", revision)
                self.assertEqual(self.runner.call_count, calls + 2)
                published = json.loads((self.results / "results.json").read_text(encoding="utf-8"))
                self.assertEqual(published["n_runs"], 2)
                self.assertTrue(all(r["final_answer"] == "recovered" for r in published["runs"]))
                # Append a later failed attempt to exercise latest-attempt precedence.
                rows = [json.loads(line) for line in self.journal().read_bytes().splitlines()]
                rows[-1]["error"] = "later failure"
                with self.journal().open("ab") as stream:
                    experiment.append_record(stream, rows[-1])
                calls = self.runner.call_count
                self.invoke("--model-revision", revision)
                self.assertEqual(self.runner.call_count, calls + 1)
                published = json.loads((self.results / "results.json").read_text(encoding="utf-8"))
                snapshot = self.results / published["audit_artifacts"] / "runs.jsonl"
                self.assertEqual(snapshot.read_bytes(), self.journal().read_bytes())
                self.assertGreater(len(snapshot.read_bytes().splitlines()), published["n_runs"])


    def test_interrupted_utf8_tail_is_preserved_and_recovered(self):
        self.invoke()
        journal = self.journal()
        original = journal.read_bytes()
        fragment = b'{"text":"\xc3'
        with journal.open("ab") as stream:
            stream.write(fragment)
        self.invoke()
        self.assertEqual(journal.read_bytes(), original)
        self.assertEqual(next(journal.parent.glob("interrupted-*.bin")).read_bytes(), fragment)

    def test_middle_corruption_and_newline_terminated_invalid_tail_fail(self):
        self.invoke()
        journal = self.journal()
        original = journal.read_bytes()
        for content in (b"broken\n" + original, original + b"broken\n"):
            journal.write_bytes(content)
            with self.assertRaisesRegex(ValueError, "corrompido"):
                self.invoke()
            self.assertEqual(journal.read_bytes(), content)

    def test_lock_prevents_simultaneous_same_experiment(self):
        self.invoke()
        with experiment.exclusive_lock(self.journal().parent / ".run.lock"):
            with self.assertRaisesRegex(RuntimeError, "Execução em uso"):
                self.invoke()

    def test_publication_lock_covers_other_identity_and_report_only(self):
        self.invoke()
        before = (self.results / "results.json").read_bytes()
        with experiment.exclusive_lock(self.results / ".publish.lock"):
            with self.assertRaisesRegex(RuntimeError, "Execução em uso"):
                self.invoke("--model-revision", "other-model")
            with self.assertRaisesRegex(RuntimeError, "Execução em uso"):
                self.invoke("--report-only")
        self.assertEqual((self.results / "results.json").read_bytes(), before)
        self.invoke("--model-revision", "other-model")
        value = json.loads((self.results / "results.json").read_text(encoding="utf-8"))
        self.invoke("--report-only")
        text = (self.results / "report.md").read_text(encoding="utf-8")
        self.assertIn(value["experiment_id"], text)
        self.assertIn(value["publication_id"], text)

    def test_legacy_report_is_byte_identical(self):
        self.results.mkdir()
        original = run_eval.KIT / "results"
        (self.results / "results.json").write_bytes((original / "results.json").read_bytes())
        self.invoke("--report-only")
        self.assertEqual((self.results / "report.md").read_bytes(),
                         (original / "report.md").read_bytes())

    def test_identity_changes_with_data_source_parameters_and_revision(self):
        kit = self.root / "kit"
        (kit / "pikit").mkdir(parents=True)
        (kit / "run_eval.py").write_text("original")
        source = kit / "pikit" / "example.py"
        source.write_text("original")
        args = argparse.Namespace(provider="ollama", host="http://localhost:11434",
                                  model="fake", model_revision="immutable-v1", temperature=0.3,
                                  fresh=False)
        inbox, tasks, attacks = load_all()

        def identify():
            return experiment.manifest(args, kit, inbox, tasks, attacks, CONFIGS, 10, "test")["experiment_id"]

        previous = identify()
        self.assertEqual(previous, identify())
        mutations = [lambda: inbox.update(extra="changed"),
                     lambda: source.write_text("changed"),
                     lambda: setattr(args, "temperature", 0.5),
                     lambda: setattr(args, "model_revision", "immutable-v2")]
        for mutate in mutations:
            mutate()
            current = identify()
            self.assertNotEqual(previous, current)
            previous = current
        for endpoint in ("http://user:password@localhost", "http://localhost?key=secret",
                         "http://localhost#secret"):
            args.host = endpoint
            with self.assertRaisesRegex(ValueError, "Endpoint"):
                identify()
