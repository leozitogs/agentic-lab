"""Provedores de modelo plugáveis, só com a biblioteca padrão.

Interface mínima: `chat(messages, tools=None, json_mode=False) -> ModelTurn`.
As mensagens usam um formato neutro (veja abaixo) e cada provedor converte para
a API dele. Para usar outro modelo ou API, implemente uma classe com `name` e
`chat` e passe para o agente.

Formato neutro:
    {"role": "system" | "user", "content": str}
    {"role": "assistant", "content": str, "tool_calls": [{"id", "name", "arguments": dict}]}
    {"role": "tool", "tool_call_id": str, "name": str, "content": str}
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class ToolCall:
    name: str
    arguments: dict
    id: str = ""


@dataclass
class ModelTurn:
    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    prompt_tokens: int = 0
    output_tokens: int = 0
    seconds: float = 0.0


class Provider(Protocol):
    name: str

    def chat(self, messages: list[dict], tools: list[dict] | None = None,
             json_mode: bool = False) -> ModelTurn: ...


def _parse_args(raw: object) -> dict:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            value = json.loads(raw) if raw.strip() else {}
            return value if isinstance(value, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


_TEXT_CALL = re.compile(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", re.S)


def tool_calls_from_text(content: str) -> tuple[str, list[ToolCall]]:
    """Fallback: alguns modelos devolvem a chamada como texto <tool_call>{...}</tool_call>."""
    calls = []
    for m in _TEXT_CALL.finditer(content or ""):
        try:
            obj = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "name" in obj:
            calls.append(ToolCall(str(obj["name"]), _parse_args(obj.get("arguments", {}))))
    if calls:
        content = _TEXT_CALL.sub("", content).strip()
    return content, calls


def _post(url: str, payload: dict, headers: dict | None = None, timeout: float = 300) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **(headers or {})}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (URL vem da config)
        return json.loads(resp.read().decode("utf-8"))


class OllamaProvider:
    """Ollama local (/api/chat com tools nativas)."""

    def __init__(self, model: str, host: str = "http://localhost:11434",
                 temperature: float = 0.3, seed: int | None = None, num_ctx: int | None = None,
                 post=_post):
        self.model, self.host = model, host.rstrip("/")
        self.temperature, self.seed, self.num_ctx = temperature, seed, num_ctx
        self.name = f"ollama:{model}"
        self._post = post

    def _messages(self, messages: list[dict]) -> list[dict]:
        out = []
        for m in messages:
            if m["role"] == "assistant":
                msg = {"role": "assistant", "content": m.get("content", "")}
                if m.get("tool_calls"):
                    msg["tool_calls"] = [{"function": {"name": c["name"], "arguments": c["arguments"]}}
                                         for c in m["tool_calls"]]
                out.append(msg)
            elif m["role"] == "tool":
                out.append({"role": "tool", "content": m["content"], "tool_name": m.get("name", "")})
            else:
                out.append({"role": m["role"], "content": m["content"]})
        return out

    def chat(self, messages: list[dict], tools: list[dict] | None = None,
             json_mode: bool = False) -> ModelTurn:
        options: dict = {"temperature": self.temperature}
        if self.seed is not None:
            options["seed"] = self.seed
        if self.num_ctx:
            options["num_ctx"] = self.num_ctx
        payload: dict = {"model": self.model, "messages": self._messages(messages),
                         "stream": False, "options": options}
        if tools:
            payload["tools"] = [{"type": "function", "function": t} for t in tools]
        if json_mode:
            payload["format"] = "json"
        t0 = time.perf_counter()
        data = self._post(f"{self.host}/api/chat", payload)
        seconds = time.perf_counter() - t0
        msg = data.get("message", {}) or {}
        calls = [ToolCall(c["function"]["name"], _parse_args(c["function"].get("arguments")), c.get("id", ""))
                 for c in msg.get("tool_calls") or []]
        content = msg.get("content", "") or ""
        if not calls and tools:
            content, calls = tool_calls_from_text(content)
        return ModelTurn(content, calls, data.get("prompt_eval_count", 0), data.get("eval_count", 0), seconds)

    def server_version(self) -> str:
        try:
            with urllib.request.urlopen(f"{self.host}/api/version", timeout=10) as resp:  # noqa: S310
                return json.loads(resp.read().decode("utf-8")).get("version", "?")
        except OSError:
            return "?"


class OpenAICompatProvider:
    """Qualquer API compatível com /v1/chat/completions (tools no formato OpenAI).

    A chave vem de uma variável de ambiente (padrão OPENAI_API_KEY), nunca do código.
    Não foi exercitado na rodada registrada; os testes cobrem só a conversão de formato.
    """

    def __init__(self, model: str, base_url: str = "https://api.openai.com/v1",
                 api_key_env: str = "OPENAI_API_KEY", temperature: float = 0.3,
                 seed: int | None = None, post=_post):
        self.model, self.base_url = model, base_url.rstrip("/")
        self.api_key_env, self.temperature, self.seed = api_key_env, temperature, seed
        self.name = f"openai-compat:{model}"
        self._post = post

    def _messages(self, messages: list[dict]) -> list[dict]:
        out = []
        for m in messages:
            if m["role"] == "assistant":
                msg: dict = {"role": "assistant", "content": m.get("content", "") or None}
                if m.get("tool_calls"):
                    msg["tool_calls"] = [
                        {"id": c["id"], "type": "function",
                         "function": {"name": c["name"], "arguments": json.dumps(c["arguments"], ensure_ascii=False)}}
                        for c in m["tool_calls"]]
                out.append(msg)
            elif m["role"] == "tool":
                out.append({"role": "tool", "tool_call_id": m["tool_call_id"], "content": m["content"]})
            else:
                out.append({"role": m["role"], "content": m["content"]})
        return out

    def chat(self, messages: list[dict], tools: list[dict] | None = None,
             json_mode: bool = False) -> ModelTurn:
        payload: dict = {"model": self.model, "messages": self._messages(messages),
                         "temperature": self.temperature}
        if self.seed is not None:
            payload["seed"] = self.seed
        if tools:
            payload["tools"] = [{"type": "function", "function": t} for t in tools]
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        key = os.environ.get(self.api_key_env, "")
        headers = {"Authorization": f"Bearer {key}"} if key else {}
        t0 = time.perf_counter()
        data = self._post(f"{self.base_url}/chat/completions", payload, headers)
        seconds = time.perf_counter() - t0
        msg = data["choices"][0]["message"]
        calls = [ToolCall(c["function"]["name"], _parse_args(c["function"].get("arguments")), c.get("id", ""))
                 for c in msg.get("tool_calls") or []]
        usage = data.get("usage", {}) or {}
        return ModelTurn(msg.get("content") or "", calls,
                         usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0), seconds)
