"""Prepara a pasta que o MkDocs publica.

O conteúdo do laboratório vive na raiz (learn/, build/, cases/, ops/) e não em
docs/. Este script copia os Markdown para _site_src/ mantendo a estrutura, e
troca links para arquivos que não são páginas (código, YAML, LICENSE) por links
para o arquivo no GitHub. Uso: python scripts/build_site.py && mkdocs build
"""
from __future__ import annotations

import pathlib
import posixpath
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "_site_src"
SOURCES = ("README.md", "ROADMAP.md", "learn", "build", "cases", "ops")
REPO_BLOB = "https://github.com/leozitogs/agentic-lab/blob/main/"
REPO_TREE = "https://github.com/leozitogs/agentic-lab/tree/main/"
LINK = re.compile(r"(?<!!)\]\(([^)\s#]+)(#[^)]*)?\)")
PAGE_SUFFIXES = {".md"}


def rewrite_links(text: str, rel_file: str) -> str:
    base = posixpath.dirname(rel_file)

    def fix(match: re.Match) -> str:
        target, anchor = match.group(1), match.group(2) or ""
        if re.match(r"^[a-z]+:", target) or target.startswith("/"):
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(base, target))
        if resolved.startswith(".."):
            return match.group(0)
        suffix = posixpath.splitext(resolved)[1]
        if suffix in PAGE_SUFFIXES:
            return match.group(0)
        path = ROOT / resolved
        url = (REPO_TREE if path.is_dir() and not (path / "README.md").exists() else REPO_BLOB) + resolved
        if path.is_dir() and (path / "README.md").exists():
            return match.group(0)
        return f"]({url}{anchor})"

    return LINK.sub(fix, text)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    count = 0
    for src in SOURCES:
        path = ROOT / src
        files = [path] if path.is_file() else sorted(path.rglob("*.md"))
        for file in files:
            rel = file.relative_to(ROOT).as_posix()
            dest = OUT / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(rewrite_links(file.read_text(encoding="utf-8"), rel), encoding="utf-8")
            count += 1
    (OUT / "stylesheets").mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "site" / "extra.css", OUT / "stylesheets" / "extra.css")
    print(f"{count} páginas copiadas para {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
