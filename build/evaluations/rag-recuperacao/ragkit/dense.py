"""Busca densa com Chroma (configuração C).

Embedder padrão do Chroma: all-MiniLM-L6-v2 exportado para ONNX e rodado com
onnxruntime, sem PyTorch. O modelo (~80 MB) é baixado uma vez para
~/.cache/chroma/onnx_models na primeira execução.
"""
from __future__ import annotations

import itertools
from collections.abc import Sequence

import chromadb
from chromadb.config import Settings

_counter = itertools.count()


def default_embedding_function():
    """O mesmo modelo do `DefaultEmbeddingFunction` do Chroma, instanciado uma vez.

    `DefaultEmbeddingFunction` cria um `ONNXMiniLM_L6_V2` novo a cada chamada e,
    com isso, uma sessão ONNX nova por consulta (cerca de 130 ms a mais em cada
    uma). Usar a classe direto mantém a sessão em cache. O tokenizador do Chroma
    trunca e preenche toda entrada para 256 tokens.
    """
    from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2

    return ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"])


class ChromaDenseIndex:
    """Coleção em memória (EphemeralClient), distância cosseno, top-k por consulta."""

    def __init__(self, texts: Sequence[str], embedding_function=None, batch_size: int = 64):
        self.embedding_function = embedding_function or default_embedding_function()
        self.client = chromadb.EphemeralClient(settings=Settings(anonymized_telemetry=False))
        self.collection = self.client.create_collection(
            name=f"ragkit-{next(_counter)}",
            embedding_function=self.embedding_function,
            configuration={"hnsw": {"space": "cosine"}},
        )
        for start in range(0, len(texts), batch_size):
            batch = list(texts[start:start + batch_size])
            ids = [str(i) for i in range(start, start + len(batch))]
            self.collection.add(ids=ids, documents=batch)

    def search(self, query: str, k: int = 10) -> list[tuple[int, float]]:
        """Os `k` vizinhos mais próximos: (índice do chunk, distância cosseno)."""
        res = self.collection.query(query_texts=[query], n_results=k, include=["distances"])
        return [(int(i), float(d)) for i, d in zip(res["ids"][0], res["distances"][0])]
