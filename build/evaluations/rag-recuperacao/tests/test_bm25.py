"""BM25 e tokenizador num corpus sintético minúsculo."""
import math
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from ragkit.bm25 import BM25Index  # noqa: E402
from ragkit.text import normalize, tokenize  # noqa: E402

CORPUS = [
    "Deploy the site to GitHub Pages with gh-deploy.",
    "Set site_name in the configuration file.",
    "The theme controls colors and fonts of the theme.",
    "Plugins extend the build. Search is a plugin.",
]


class Tokenizer(unittest.TestCase):
    def test_lowercase_stopwords_and_punctuation(self):
        self.assertEqual(tokenize("How do I Deploy THE site?"), ["deploy", "site"])

    def test_identifiers_keep_whole_and_parts(self):
        self.assertEqual(tokenize("site_name"), ["site_name", "site", "name"])
        self.assertEqual(tokenize("__init__"), ["init"])

    def test_no_stemming(self):
        self.assertNotEqual(tokenize("excluded"), tokenize("exclude"))

    def test_normalize(self):
        self.assertEqual(normalize("  Foo\n\tBAR  baz "), "foo bar baz")


class BM25(unittest.TestCase):
    def setUp(self):
        self.index = BM25Index(CORPUS)

    def test_best_match_comes_first(self):
        self.assertEqual(self.index.search("deploy to github", 1)[0][0], 0)
        self.assertEqual(self.index.search("site name configuration", 1)[0][0], 1)
        self.assertEqual(self.index.search("search plugin", 1)[0][0], 3)

    def test_unknown_terms_return_nothing(self):
        self.assertEqual(self.index.search("kubernetes helm", 5), [])

    def test_k_limits_results_and_scores_are_descending(self):
        hits = self.index.search("site theme plugin", 2)
        self.assertEqual(len(hits), 2)
        self.assertGreaterEqual(hits[0][1], hits[1][1])

    def test_idf_matches_lucene_formula_and_is_positive(self):
        n = len(CORPUS)
        self.assertAlmostEqual(self.index.idf["theme"], math.log(1 + (n - 1 + 0.5) / (1 + 0.5)))
        self.assertTrue(all(v > 0 for v in self.index.idf.values()))

    def test_term_frequency_saturates(self):
        index = BM25Index(["theme", "theme theme theme theme theme theme"], b=0.0)
        s1, s6 = index.scores("theme")[0], index.scores("theme")[1]
        self.assertGreater(s6, s1)
        self.assertLess(s6, s1 * (index.k1 + 1))  # teto de (k1 + 1) * idf

    def test_ties_break_by_corpus_order(self):
        index = BM25Index(["alpha beta", "alpha beta", "gamma"])
        self.assertEqual([i for i, _ in index.search("alpha", 2)], [0, 1])

    def test_repeated_query_terms_count_once(self):
        self.assertEqual(self.index.scores("theme"), self.index.scores("theme theme theme"))

    def test_empty_corpus(self):
        self.assertEqual(BM25Index([]).search("anything", 3), [])


if __name__ == "__main__":
    unittest.main()
