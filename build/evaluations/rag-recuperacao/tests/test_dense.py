"""Índice denso com Chroma. Pulado se o chromadb não estiver instalado.

Usa um embedder falso e determinístico (saco de palavras com hash), então não
baixa o modelo ONNX: testa a fiação com o Chroma, não a qualidade do modelo.
"""
import hashlib
import importlib.util
import math
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

HAS_CHROMA = importlib.util.find_spec("chromadb") is not None

if HAS_CHROMA:
    from chromadb.api.types import EmbeddingFunction

    from ragkit.dense import ChromaDenseIndex
    from ragkit.text import tokenize

    class HashingEmbedder(EmbeddingFunction):
        DIM = 64

        def __init__(self):
            pass

        def __call__(self, input):
            vectors = []
            for text in input:
                vec = [0.0] * self.DIM
                for tok in tokenize(text):
                    vec[int(hashlib.md5(tok.encode()).hexdigest(), 16) % self.DIM] += 1.0
                norm = math.sqrt(sum(v * v for v in vec)) or 1.0
                vectors.append([v / norm for v in vec])
            return vectors

        @staticmethod
        def name():
            return "hashing-test"

        def get_config(self):
            return {}

        @staticmethod
        def build_from_config(config):
            return HashingEmbedder()


@unittest.skipUnless(HAS_CHROMA, "chromadb não instalado (instale requirements.txt)")
class Dense(unittest.TestCase):
    TEXTS = [
        "deploy the site to github pages",
        "configure theme colors and fonts",
        "search plugin options and index",
    ] + [f"filler document number {i} about nothing" for i in range(70)]

    def setUp(self):
        self.index = ChromaDenseIndex(self.TEXTS, embedding_function=HashingEmbedder(), batch_size=16)

    def test_all_texts_indexed_across_batches(self):
        self.assertEqual(self.index.collection.count(), len(self.TEXTS))

    def test_nearest_neighbour_is_the_matching_text(self):
        self.assertEqual(self.index.search("github pages deploy", 3)[0][0], 0)
        self.assertEqual(self.index.search("theme fonts", 3)[0][0], 1)

    def test_returns_k_indices_with_ascending_distance(self):
        hits = self.index.search("search index", 5)
        self.assertEqual(len(hits), 5)
        distances = [d for _, d in hits]
        self.assertEqual(distances, sorted(distances))
        self.assertTrue(all(isinstance(i, int) for i, _ in hits))

    def test_two_indexes_do_not_share_a_collection(self):
        other = ChromaDenseIndex(["only one text"], embedding_function=HashingEmbedder())
        self.assertEqual(other.collection.count(), 1)
        self.assertEqual(self.index.collection.count(), len(self.TEXTS))


if __name__ == "__main__":
    unittest.main()
