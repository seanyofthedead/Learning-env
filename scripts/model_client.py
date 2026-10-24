"""Tiny, tool-agnostic model client (standard library only).

Used by scripts/regenerate_cache.py and scripts/live_server.py. Nothing in the demo
needs it: the app replays app/cache.json by default.

Provider is picked from the environment:
  ANTHROPIC_API_KEY  -> Anthropic Messages API   (model: DEMO_MODEL, default claude-opus-5-5)
  OPENAI_API_KEY     -> OpenAI-compatible Chat Completions (model: DEMO_MODEL or OPENAI_MODEL,
                        required; OPENAI_BASE_URL for a compatible gateway)

Temperature: every request asks for temperature 0. Since the Anthropic API version
2026-10-21, sampling parameters are removed, and current Claude models accept only
their default sampling. This client therefore sends the older `anthropic-version:
2023-06-01` header with temperature 0, and if the model refuses the parameter it
retries once without it and reports `temperature: None` so the cache records what
actually happened.

Standard library only (urllib) on purpose: the demo laptop may have no network and no
pip, and the user asked for no extra dependencies.
"""
import json
import os
import time
import urllib.error
import urllib.request

DEFAULT_ANTHROPIC_MODEL = "claude-opus-5-5"


class ModelError(Exception):
    pass


def provider():
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    return None


def model_name():
    p = provider()
    if p == "anthropic":
        return os.environ.get("DEMO_MODEL") or DEFAULT_ANTHROPIC_MODEL
    if p == "openai":
        m = os.environ.get("DEMO_MODEL") or os.environ.get("OPENAI_MODEL")
        if not m:
            raise ModelError("Set DEMO_MODEL (or OPENAI_MODEL) to the model to use.")
        return m
    return None


def user_message(prompt, file_name, file_text):
    """How the 'attached file' is presented to the model: file first, then the prompt."""
    return f'<attached_file name="{file_name}">\n{file_text}\n</attached_file>\n\n{prompt}'


def _post(url, headers, body, timeout):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers={"content-type": "application/json", **headers},
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        raise ModelError(f"HTTP {e.code}: {detail}") from None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise ModelError(f"network error: {e}") from None


def _anthropic(text, timeout):
    base = (os.environ.get("ANTHROPIC_BASE_URL") or "https://api.anthropic.com").rstrip("/")
    headers = {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"}
    body = {"model": model_name(), "max_tokens": 4000, "temperature": 0,
            "messages": [{"role": "user", "content": text}]}
    if os.environ.get("DEMO_EFFORT"):
        body["output_config"] = {"effort": os.environ["DEMO_EFFORT"]}
    temperature = 0
    try:
        data = _post(base + "/v1/messages", headers, body, timeout)
    except ModelError as e:
        if "temperature" not in str(e).lower() and "sampling" not in str(e).lower():
            raise
        body.pop("temperature")
        temperature = None  # model accepts only its default sampling
        data = _post(base + "/v1/messages", headers, body, timeout)
    if data.get("stop_reason") == "refusal":
        raise ModelError("model declined the request (stop_reason=refusal)")
    out = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    return out.strip(), data.get("model", body["model"]), temperature


def _openai(text, timeout):
    base = (os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    headers = {"authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}
    body = {"model": model_name(), "temperature": 0,
            "messages": [{"role": "user", "content": text}]}
    data = _post(base + "/chat/completions", headers, body, timeout)
    out = data["choices"][0]["message"]["content"] or ""
    return out.strip(), data.get("model", body["model"]), 0


def generate(prompt, file_name, file_text, timeout=120):
    """Returns dict(markdown, model, temperature, latency_ms). Raises ModelError."""
    p = provider()
    if p is None:
        raise ModelError("No ANTHROPIC_API_KEY or OPENAI_API_KEY in the environment.")
    t0 = time.time()
    text = user_message(prompt, file_name, file_text)
    md, model, temp = (_anthropic if p == "anthropic" else _openai)(text, timeout)
    if not md:
        raise ModelError("empty response")
    return {"markdown": md, "model": model, "temperature": temp,
            "latency_ms": int((time.time() - t0) * 1000)}
