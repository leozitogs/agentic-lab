"""Download, conferência e leitura do corpus: docs/ do MkDocs na tag 1.6.1.

O corpus não é versionado no repositório. `fetch` baixa o tarball da tag para
uma pasta de cache (`.cache/rag-recuperacao/` na raiz, ignorada pelo git), confere o SHA-256 e extrai só os
arquivos `.md` de `docs/`, sem executar nada do pacote baixado.
"""
from __future__ import annotations

import hashlib
import io
import pathlib
import posixpath
import sys
import tarfile
import urllib.request

PROJECT = "mkdocs/mkdocs"
TAG = "1.6.1"
LICENSE = "BSD-2-Clause"
ARCHIVE_URL = f"https://github.com/{PROJECT}/archive/refs/tags/{TAG}.tar.gz"
ARCHIVE_NAME = f"mkdocs-{TAG}.tar.gz"
ARCHIVE_PREFIX = f"mkdocs-{TAG}/docs/"
# SHA-256 do tarball baixado em 2026-11-12.
ARCHIVE_SHA256 = "10b78edfc02bf37646d0c5b6fc7b2ee5f96b7e060207654ee187149c71b84644"
# SHA-256 do manifesto dos .md extraídos (ver `docs_manifest_sha256`). É o hash
# que garante o corpus: o GitHub gera o tarball sob demanda e, em tese, pode
# mudar a compressão sem mudar o conteúdo.
DOCS_SHA256 = "0d6e44279879d18116c43c7cb64e5959a1a4f269784d0deeeed6e9e8d248d9cc"
MAX_FILE_BYTES = 2_000_000
# Cache na raiz do repositório (.cache/ é ignorada pelo git), fora de build/: assim
# o validador de front-matter e o site não enxergam os .md baixados.
DEFAULT_CACHE = pathlib.Path(__file__).resolve().parents[4] / ".cache" / "rag-recuperacao"


class CorpusError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def docs_manifest_sha256(docs: dict[str, str]) -> str:
    """Hash estável do conjunto: caminho e SHA-256 de cada arquivo, em ordem."""
    lines = "".join(f"{path}\0{sha256_bytes(text.encode('utf-8'))}\n" for path, text in sorted(docs.items()))
    return sha256_bytes(lines.encode("utf-8"))


def _safe_rel(name: str) -> str | None:
    """Caminho relativo a docs/ se o membro for um .md seguro; senão None."""
    if not name.startswith(ARCHIVE_PREFIX) or not name.endswith(".md"):
        return None
    rel = posixpath.normpath(name[len(ARCHIVE_PREFIX):])
    if rel.startswith(("..", "/")) or "\\" in rel or ":" in rel:
        return None
    return rel


def extract_docs(archive: bytes) -> dict[str, str]:
    """Lê do tarball só os .md regulares de docs/, sem gravar nada fora do retorno."""
    docs: dict[str, str] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        for member in tar:
            rel = _safe_rel(member.name)
            if rel is None or not member.isfile() or member.size > MAX_FILE_BYTES:
                continue
            handle = tar.extractfile(member)
            if handle is not None:
                docs[rel] = handle.read().decode("utf-8").replace("\r\n", "\n")
    return docs


def write_docs(docs: dict[str, str], dest: pathlib.Path) -> None:
    for rel, text in docs.items():
        path = dest / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def load_docs(docs_dir: pathlib.Path) -> dict[str, str]:
    """Lê os .md de uma pasta, com caminhos relativos em estilo POSIX."""
    return {
        p.relative_to(docs_dir).as_posix(): p.read_text(encoding="utf-8").replace("\r\n", "\n")
        for p in sorted(docs_dir.rglob("*.md"))
    }


def fetch(cache_dir: pathlib.Path, url: str = ARCHIVE_URL, timeout: float = 60.0) -> pathlib.Path:
    """Garante o corpus em `cache_dir/mkdocs-<tag>/docs` e devolve esse caminho.

    Reaproveita o cache se o manifesto bater; senão baixa (ou reusa o tarball
    em cache), confere os hashes e extrai. Falha se o conteúdo não bater.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    docs_dir = cache_dir / f"mkdocs-{TAG}" / "docs"
    if docs_dir.is_dir() and docs_manifest_sha256(load_docs(docs_dir)) == DOCS_SHA256:
        return docs_dir

    archive_path = cache_dir / ARCHIVE_NAME
    if archive_path.is_file():
        archive = archive_path.read_bytes()
    else:
        request = urllib.request.Request(url, headers={"User-Agent": "agentic-lab-rag-kit"})
        with urllib.request.urlopen(request, timeout=timeout) as resp:  # noqa: S310 (URL fixa)
            archive = resp.read()
        archive_path.write_bytes(archive)

    archive_hash = sha256_bytes(archive)
    if archive_hash != ARCHIVE_SHA256:
        print(f"AVISO: SHA-256 do tarball difere do registrado ({archive_hash}); "
              "conferindo o conteúdo.", file=sys.stderr)
    docs = extract_docs(archive)
    manifest = docs_manifest_sha256(docs)
    if manifest != DOCS_SHA256:
        raise CorpusError(f"conteúdo de docs/ não confere: manifesto {manifest}, esperado {DOCS_SHA256}")
    write_docs(docs, docs_dir)
    return docs_dir
