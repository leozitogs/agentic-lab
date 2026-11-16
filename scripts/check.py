"""Executa o núcleo offline e, opcionalmente, os componentes instalados."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def checks(site: bool = False, mcp: bool = False) -> list[tuple[Path, list[str]]]:
    commands = [(ROOT, ["scripts/validate_frontmatter.py"]),
                (ROOT, ["-m", "unittest", "discover", "-s", "tests", "-v"])]
    for kit in ("rag-recuperacao", "prompt-injection"):
        commands.append((ROOT / "build" / "evaluations" / kit,
                         ["-m", "unittest", "discover", "-s", "tests", "-v"]))
    commands.append((ROOT / "build/evaluations/rag-recuperacao", ["validate_questions.py"]))
    if mcp:
        commands.append((ROOT / "build/mcp-servers/repo-knowledge",
                         ["-m", "unittest", "discover", "-s", "tests", "-v"]))
    if site:
        commands.extend([(ROOT, ["scripts/build_site.py"]), (ROOT, ["-m", "mkdocs", "build", "--strict"])])
    return commands


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", action="store_true", help="Requer site/requirements.txt instalado")
    parser.add_argument("--mcp", action="store_true", help="Requer repo-knowledge instalado")
    args = parser.parse_args(argv)
    for directory, arguments in checks(args.site, args.mcp):
        print(f"\n[{directory.relative_to(ROOT) or '.'}] python {' '.join(arguments)}", flush=True)
        result = subprocess.run([sys.executable, *arguments], cwd=directory)
        if result.returncode:
            return result.returncode
    print("\nVerificações concluídas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
