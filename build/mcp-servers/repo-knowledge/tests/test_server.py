"""Testa o servidor pelo protocolo MCP: em processo e como subprocesso stdio."""
import json
import pathlib
import sys
import unittest

import anyio
from mcp.client.client import Client, StdioServerParameters

PKG = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PKG))

from repo_knowledge_server.server import build_server  # noqa: E402


def text(result) -> str:
    return "".join(getattr(c, "text", "") for c in result.content)


class InProcessTest(unittest.TestCase):
    def run_async(self, fn):
        return anyio.run(fn)

    def test_lists_primitives(self):
        async def go():
            async with Client(build_server()) as c:
                tools = {t.name for t in (await c.list_tools()).tools}
                resources = {str(r.uri) for r in (await c.list_resources()).resources}
                templates = {t.uri_template for t in (await c.list_resource_templates()).resource_templates}
                prompts = {p.name for p in (await c.list_prompts()).prompts}
                return tools, resources, templates, prompts
        tools, resources, templates, prompts = self.run_async(go)
        self.assertEqual(tools, {"search_artifacts", "get_artifact", "list_by_tag"})
        self.assertIn("repo://prompts/index", resources)
        self.assertIn("repo://artifact/{+path}", templates)
        self.assertEqual(prompts, {"find_similar_prompt", "find_skill_for_task"})

    def test_every_tool_is_read_only(self):
        async def go():
            async with Client(build_server()) as c:
                return (await c.list_tools()).tools
        for tool in self.run_async(go):
            self.assertTrue(tool.annotations.read_only_hint, tool.name)
            self.assertFalse(tool.annotations.destructive_hint, tool.name)

    def test_search_and_get(self):
        async def go():
            async with Client(build_server()) as c:
                found = await c.call_tool("search_artifacts", {"query": "research analyst", "tipo": "prompt"})
                got = await c.call_tool("get_artifact", {"path": "build/prompts/system/research-analyst.md"})
                return found, got
        found, got = self.run_async(go)
        self.assertFalse(found.is_error)
        self.assertIn("build/prompts/system/research-analyst.md", json.dumps(found.structured_content))
        self.assertIn("You are a senior research analyst.", text(got))

    def test_traversal_is_refused(self):
        async def go():
            async with Client(build_server()) as c:
                return await c.call_tool("get_artifact", {"path": "../../../etc/passwd.md"})
        result = self.run_async(go)
        self.assertTrue(result.is_error)
        self.assertIn("access denied", text(result))

    def test_resources_and_prompts(self):
        async def go():
            async with Client(build_server()) as c:
                index = await c.read_resource("repo://prompts/index")
                art = await c.read_resource("repo://artifact/build/prompts/system/research-analyst.md")
                prompt = await c.get_prompt("find_similar_prompt", {"goal": "summarize papers"})
                return index, art, prompt
        index, art, prompt = self.run_async(go)
        self.assertIn("research-analyst.md", index.contents[0].text)
        self.assertIn("senior research analyst", art.contents[0].text)
        self.assertIn("summarize papers", prompt.messages[0].content.text)


class StdioTest(unittest.TestCase):
    """Sobe o servidor como um cliente MCP de verdade faria: subprocesso via stdio."""

    def test_stdio_roundtrip(self):
        params = StdioServerParameters(command=sys.executable, args=["-m", "repo_knowledge_server"], cwd=str(PKG))

        async def go():
            async with Client(params) as c:
                tools = await c.list_tools()
                found = await c.call_tool("search_artifacts", {"query": "MCP"})
                return tools, found
        tools, found = anyio.run(go)
        self.assertEqual(len(tools.tools), 3)
        self.assertFalse(found.is_error)


if __name__ == "__main__":
    unittest.main()
