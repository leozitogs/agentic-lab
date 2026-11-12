"""Servidor MCP somente leitura que expõe o agentic-lab a um cliente MCP."""
from __future__ import annotations

import logging
import sys

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ResourceError, ToolError
from mcp.types import ToolAnnotations

from .catalog import AccessDenied, Catalog

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
log = logging.getLogger("repo-knowledge")

READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)
TIPOS = ("prompt", "skill", "mcp", "eval", "case", "note", "adr", "guide")


def build_server(catalog: Catalog | None = None) -> MCPServer:
    cat = catalog or Catalog()
    server = MCPServer(
        "repo-knowledge",
        version="0.2.0",
        instructions=(
            "Read-only access to the agentic-lab repository: prompts, skills, MCP servers, "
            "evaluations, cases, ADRs and study guides. Use search_artifacts first, then "
            "get_artifact for the full text. Nothing can be modified through this server."
        ),
    )

    # ---------------- tools ----------------
    @server.tool(annotations=READ_ONLY)
    def search_artifacts(query: str, tipo: str | None = None, maturidade: str | None = None,
                         tag: str | None = None, limit: int = 10) -> list[dict]:
        """Search artifacts by keywords, optionally filtered by tipo, maturidade or tag.

        tipo: prompt, skill, mcp, eval, case, note, adr or guide.
        maturidade: draft, tested, reviewed or adopted.
        """
        if tipo and tipo not in TIPOS:
            raise ToolError(f"tipo must be one of {', '.join(TIPOS)}")
        results = cat.search(query, tipo=tipo, maturidade=maturidade, tag=tag, limit=limit)
        log.info("search query=%r results=%d", query, len(results))
        return [{**a.card(), "score": round(score, 2)} for score, a in results]

    @server.tool(annotations=READ_ONLY)
    def get_artifact(path: str) -> str:
        """Return the full Markdown of an artifact, given its path relative to the repo root."""
        try:
            return cat.read(path)
        except AccessDenied as exc:
            log.warning("denied path=%r reason=%s", path, exc)
            raise ToolError(f"access denied: {exc}") from None
        except FileNotFoundError:
            raise ToolError(f"artifact not found: {path}") from None

    @server.tool(annotations=READ_ONLY)
    def list_by_tag(tag: str) -> list[dict]:
        """List every artifact that carries the given tag in its front-matter."""
        return [a.card() for a in cat.filter(tag=tag)]

    # ---------------- resources ----------------
    def _index(tipo: str):
        def read() -> str:
            return cat.index_markdown(tipo)
        return read

    for uri, tipo, title in (
        ("repo://prompts/index", "prompt", "Prompt index"),
        ("repo://skills/index", "skill", "Skill index"),
        ("repo://mcps/index", "mcp", "MCP server index"),
        ("repo://evals/index", "eval", "Evaluation index"),
        ("repo://cases/index", "case", "Case index"),
        ("repo://guides/index", "guide", "Study guide index"),
    ):
        server.resource(uri, name=f"{tipo}-index", title=title, mime_type="text/markdown")(_index(tipo))

    @server.resource("repo://artifact/{+path}", name="artifact", title="Artifact by path", mime_type="text/markdown")
    def artifact(path: str) -> str:
        """Full Markdown of one artifact."""
        try:
            return cat.read(path)
        except (AccessDenied, FileNotFoundError) as exc:
            raise ResourceError(f"cannot read {path}: {exc}") from None

    # ---------------- prompts ----------------
    @server.prompt(title="Find a prompt for a goal")
    def find_similar_prompt(goal: str) -> str:
        """Suggest existing prompts from the lab that could serve the goal."""
        return (
            f"I want to: {goal}\n\n"
            "Use the search_artifacts tool with tipo='prompt' to find candidates in the agentic-lab, "
            "read the best ones with get_artifact, and recommend at most three. For each, say why it fits, "
            "its maturity level, and what would need to change. If none fits, say so and describe what a new "
            "prompt should contain."
        )

    @server.prompt(title="Find a skill for a task")
    def find_skill_for_task(task: str) -> str:
        """Suggest skills from the lab that apply to a task."""
        return (
            f"Task: {task}\n\n"
            "Use search_artifacts with tipo='skill' and read the candidates with get_artifact. "
            "Recommend the skills that apply, in the order they should be used, and point out gaps "
            "that no existing skill covers."
        )

    return server


def main() -> None:
    catalog = Catalog()
    log.info("serving root=%s artifacts=%d", catalog.root, len(catalog.items))
    build_server(catalog).run("stdio")


if __name__ == "__main__":
    main()
