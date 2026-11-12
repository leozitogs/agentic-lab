"""recall@k, MRR e bootstrap com casos de resultado conhecido."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from ragkit.metrics import (bootstrap_ci, first_hit_rank, mrr_at_k,  # noqa: E402
                            paired_bootstrap_diff, recall_at_k)


class FirstHit(unittest.TestCase):
    def test_match_ignores_case_and_whitespace(self):
        ranked = ["nothing here", "Set the\n  CANONICAL   url of", "set the canonical url of the site"]
        self.assertEqual(first_hit_rank(ranked, "set the canonical URL"), 2)

    def test_no_hit(self):
        self.assertIsNone(first_hit_rank(["a", "b"], "c"))
        self.assertIsNone(first_hit_rank([], "c"))


class RecallAndMRR(unittest.TestCase):
    RANKS = [1, 3, None, 2, 10]

    def test_recall_at_k(self):
        self.assertEqual(recall_at_k(self.RANKS, 1), 1 / 5)
        self.assertEqual(recall_at_k(self.RANKS, 3), 3 / 5)
        self.assertEqual(recall_at_k(self.RANKS, 5), 3 / 5)
        self.assertEqual(recall_at_k(self.RANKS, 10), 4 / 5)

    def test_mrr(self):
        expected = (1 + 1 / 3 + 0 + 1 / 2 + 1 / 10) / 5
        self.assertAlmostEqual(mrr_at_k(self.RANKS, 10), expected)
        # com corte em 5 a pergunta achada na posição 10 vale zero
        self.assertAlmostEqual(mrr_at_k(self.RANKS, 5), (1 + 1 / 3 + 1 / 2) / 5)

    def test_extremes(self):
        self.assertEqual(recall_at_k([1, 1], 1), 1.0)
        self.assertEqual(mrr_at_k([1, 1]), 1.0)
        self.assertEqual(recall_at_k([None, None], 10), 0.0)
        self.assertEqual(mrr_at_k([None]), 0.0)
        self.assertEqual(recall_at_k([], 5), 0.0)
        self.assertEqual(mrr_at_k([]), 0.0)


class Bootstrap(unittest.TestCase):
    def test_constant_values_give_a_point_interval(self):
        self.assertEqual(bootstrap_ci([1.0] * 20), (1.0, 1.0))

    def test_interval_contains_the_mean_and_is_reproducible(self):
        values = [1.0] * 30 + [0.0] * 20
        lo, hi = bootstrap_ci(values)
        self.assertLess(lo, 0.6)
        self.assertGreater(hi, 0.6)
        self.assertEqual((lo, hi), bootstrap_ci(values))

    def test_paired_difference(self):
        diff, lo, hi = paired_bootstrap_diff([1.0, 1.0, 0.0, 1.0], [0.0, 1.0, 0.0, 0.0])
        self.assertEqual(diff, 0.5)
        self.assertLessEqual(lo, diff)
        self.assertGreaterEqual(hi, diff)
        with self.assertRaises(ValueError):
            paired_bootstrap_diff([1.0], [1.0, 0.0])


if __name__ == "__main__":
    unittest.main()
