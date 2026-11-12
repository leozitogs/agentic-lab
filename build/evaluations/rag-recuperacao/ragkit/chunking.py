"""Dois chunkers: por tamanho fixo (configuração A) e por estrutura (B e C)."""
from __future__ import annotations

import re
from dataclasses import dataclass

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")

Fence = tuple[str, int] | None


@dataclass(frozen=True)
class Chunk:
    id: str
    doc: str
    text: str  # trecho como está no arquivo; é aqui que a `evidence` é procurada
    index_text: str  # o que vai para o índice (B e C acrescentam o caminho de títulos)
    heading: str = ""  # caminho de títulos, ex.: "Configuration > Build directories > theme"


def fixed_chunks(doc: str, text: str, size: int = 800, overlap: int = 200) -> list[Chunk]:
    """Janelas de `size` caracteres com `overlap` de sobreposição, por documento.

    Ingênuo de propósito: corta no meio de palavras, seções e blocos de código.
    Garantia útil: qualquer trecho com até `overlap` caracteres cabe inteiro em
    pelo menos uma janela.
    """
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("exige size > 0 e 0 <= overlap < size")
    step = size - overlap
    chunks: list[Chunk] = []
    start = 0
    while start < len(text):
        piece = text[start:start + size]
        if piece.strip():
            chunks.append(Chunk(f"{doc}#fixed-{len(chunks)}", doc, piece, piece))
        if start + size >= len(text):
            break
        start += step
    return chunks


def _fence_step(line: str, fence: Fence) -> Fence:
    """Atualiza o estado de cerca de código (``` ou ~~~) depois de ler `line`."""
    match = FENCE.match(line)
    if not match:
        return fence
    marker = match.group(1)
    if fence is None:
        return (marker[0], len(marker))
    rest = line.strip()[len(marker):].strip()
    if marker[0] == fence[0] and len(marker) >= fence[1] and not rest:
        return None
    return fence


def _blocks(lines: list[str]) -> list[str]:
    """Agrupa linhas em blocos separados por linha em branco, sem quebrar cercas de código."""
    blocks: list[list[str]] = []
    current: list[str] = []
    fence: Fence = None
    for line in lines:
        fence = _fence_step(line, fence)
        if fence is None and not line.strip():
            if current:
                blocks.append(current)
                current = []
            continue
        current.append(line)
    if current:
        blocks.append(current)
    return ["\n".join(b) for b in blocks]


def _split_long(block: str, max_chars: int) -> list[str]:
    """Quebra um bloco maior que `max_chars` entre linhas (uma linha nunca é cortada)."""
    if len(block) <= max_chars:
        return [block]
    parts: list[str] = []
    current = ""
    for line in block.split("\n"):
        candidate = f"{current}\n{line}" if current else line
        if current and len(candidate) > max_chars:
            parts.append(current)
            current = line
        else:
            current = candidate
    if current:
        parts.append(current)
    return parts


def _pack(blocks: list[str], max_chars: int) -> list[str]:
    """Junta blocos consecutivos em pedaços de até `max_chars`.

    Um bloco maior que o limite (lista longa, bloco de código) é quebrado entre
    linhas como último recurso.
    """
    pieces: list[str] = []
    current = ""
    for block in (part for b in blocks for part in _split_long(b, max_chars)):
        candidate = f"{current}\n\n{block}" if current else block
        if current and len(candidate) > max_chars:
            pieces.append(current)
            current = block
        else:
            current = candidate
    if current:
        pieces.append(current)
    return pieces


def split_sections(text: str) -> list[tuple[list[str], list[str]]]:
    """Divide o Markdown em seções por título ATX (`#` a `######`).

    Devolve pares (caminho de títulos, linhas da seção, começando pelo título).
    Linhas que começam com `#` dentro de cercas de código não são títulos.
    """
    sections: list[tuple[list[str], list[str]]] = []
    stack: list[tuple[int, str]] = []
    path: list[str] = []
    current: list[str] = []
    fence: Fence = None
    for line in text.splitlines():
        in_code = fence is not None
        fence = _fence_step(line, fence)
        heading = HEADING.match(line) if not in_code and fence is None else None
        if heading:
            sections.append((path, current))
            level, title = len(heading.group(1)), heading.group(2).strip()
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            path = [t for _, t in stack]
            current = [line]
        else:
            current.append(line)
    sections.append((path, current))
    return sections


def structure_chunks(doc: str, text: str, max_chars: int = 800) -> list[Chunk]:
    """Um chunk por seção de título; seções longas são quebradas entre parágrafos.

    O texto indexado recebe o caminho de títulos na frente (ex.:
    "Configuration > Build directories > theme"), que é a informação estrutural
    que o chunk por tamanho perde. Seções só com o título são descartadas.
    """
    chunks: list[Chunk] = []
    for path, lines in split_sections(text):
        body = lines[1:] if path else lines
        if not "\n".join(body).strip():
            continue
        heading = " > ".join(path)
        prefix = f"{heading}\n\n" if heading else ""
        for piece in _pack(_blocks(lines), max_chars):
            chunks.append(Chunk(f"{doc}#sec-{len(chunks)}", doc, piece, prefix + piece, heading))
    return chunks
