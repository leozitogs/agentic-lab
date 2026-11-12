"""Conversão de formato dos provedores, com o HTTP trocado por um stub (sem rede)."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from pikit.providers import OllamaProvider, OpenAICompatProvider, tool_calls_from_text  # noqa: E402

MESSAGES = [
    {"role": "system", "content": "sys"},
    {"role": "user", "content": "oi"},
    {"role": "assistant", "content": "", "tool_calls": [{"id": "c1", "name": "read_email",
                                                          "arguments": {"email_id": "e01"}}]},
    {"role": "tool", "tool_call_id": "c1", "name": "read_email", "content": "{...}"},
]
TOOLS = [{"name": "read_email", "description": "d", "parameters": {"type": "object", "properties": {}}}]


class Stub:
    def __init__(self, response):
        self.response, self.calls = response, []

    def __call__(self, url, payload, headers=None, timeout=300):
        self.calls.append((url, payload, headers))
        return self.response


class Ollama(unittest.TestCase):
    def test_request_and_tool_call_parsing(self):
        stub = Stub({"message": {"content": "", "tool_calls": [
            {"function": {"name": "send_email", "arguments": {"to": "a@b.example"}}}]},
            "prompt_eval_count": 10, "eval_count": 3})
        p = OllamaProvider("m", temperature=0.3, seed=2, post=stub)
        turn = p.chat(MESSAGES, TOOLS)
        url, payload, _ = stub.calls[0]
        self.assertTrue(url.endswith("/api/chat"))
        self.assertEqual(payload["options"], {"temperature": 0.3, "seed": 2})
        self.assertEqual(payload["tools"][0]["type"], "function")
        self.assertEqual(payload["messages"][2]["tool_calls"][0]["function"]["arguments"], {"email_id": "e01"})
        self.assertEqual(payload["messages"][3], {"role": "tool", "content": "{...}", "tool_name": "read_email"})
        self.assertEqual((turn.tool_calls[0].name, turn.tool_calls[0].arguments), ("send_email", {"to": "a@b.example"}))
        self.assertEqual((turn.prompt_tokens, turn.output_tokens), (10, 3))

    def test_json_mode_and_text_fallback(self):
        stub = Stub({"message": {"content": 'ok <tool_call>{"name": "list_emails", "arguments": {}}</tool_call>'}})
        p = OllamaProvider("m", post=stub)
        turn = p.chat(MESSAGES[:2], TOOLS)
        self.assertEqual([c.name for c in turn.tool_calls], ["list_emails"])
        self.assertEqual(turn.content, "ok")
        p.chat(MESSAGES[:2], None, json_mode=True)
        self.assertEqual(stub.calls[-1][1]["format"], "json")
        self.assertNotIn("tools", stub.calls[-1][1])


class OpenAICompat(unittest.TestCase):
    def test_request_and_parsing(self):
        stub = Stub({"choices": [{"message": {"content": None, "tool_calls": [
            {"id": "x", "type": "function", "function": {"name": "read_email", "arguments": '{"email_id": "e02"}'}}]}}],
            "usage": {"prompt_tokens": 7, "completion_tokens": 2}})
        p = OpenAICompatProvider("m", base_url="http://local.example/v1", api_key_env="PIKIT_TEST_NO_KEY", post=stub)
        turn = p.chat(MESSAGES, TOOLS, json_mode=True)
        url, payload, headers = stub.calls[0]
        self.assertEqual(url, "http://local.example/v1/chat/completions")
        self.assertEqual(headers, {})
        self.assertEqual(payload["messages"][2]["tool_calls"][0]["function"]["arguments"], '{"email_id": "e01"}')
        self.assertEqual(payload["messages"][3], {"role": "tool", "tool_call_id": "c1", "content": "{...}"})
        self.assertEqual(payload["response_format"], {"type": "json_object"})
        self.assertEqual(turn.tool_calls[0].arguments, {"email_id": "e02"})
        self.assertEqual(turn.content, "")


class TextCalls(unittest.TestCase):
    def test_ignores_broken_json(self):
        content, calls = tool_calls_from_text("<tool_call>{quebrado</tool_call>")
        self.assertEqual(calls, [])
        self.assertIn("quebrado", content)
