#!/usr/bin/env python
"""Shared LLM plumbing for the Esoteric Ebb RU translation pipeline.

- Reads runtime auth from local-runtime.auth.json
- Anthropic Messages protocol against the local proxy
- Retries, disk cache, JSON-array extraction
"""
from __future__ import annotations

import json
import os
import re
import random
import threading
import time

import httpx

BASE = os.environ.get("EBRU_BASE_URL", "http://127.0.0.1:8080/v1")
AUTH_JSON = os.environ.get(
    "EBRU_AUTH_JSON",
    os.path.expanduser("~/.minimax/local-runtime.auth.json"))
CACHE_DIR = os.environ.get(
    "EBRU_CACHE_DIR",
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "work", "cache"))

os.makedirs(CACHE_DIR, exist_ok=True)

_lock = threading.Lock()


def _access_token() -> str:
    """The endpoint's token: the environment first, the local runtime second."""
    token = os.environ.get("EBRU_TOKEN")
    if token:
        return token
    with open(AUTH_JSON, encoding="utf-8") as fh:
        return json.load(fh)["auth"]["accessToken"]


TOKEN = _access_token()


def _cache_path(key: str) -> str:
    import hashlib
    h = hashlib.sha256(key.encode("utf-8")).hexdigest()[:32]
    return os.path.join(CACHE_DIR, h + ".json")


def call_llm(model: str, system: str, user: str, max_tokens: int = 8000,
             temperature: float = 0.3, timeout: float = 240.0,
             retries: int = 4, cache_key: str | None = None) -> str:
    """Single LLM call returning assistant text. Cached on disk."""
    ck = cache_key or ("%s|%s|%s" % (model, system, user))
    cp = _cache_path(ck)
    if os.path.exists(cp):
        try:
            with open(cp, encoding="utf-8") as fh:
                return json.load(fh)["text"]
        except Exception:
            pass

    body = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": user}],
        "temperature": temperature,
    }
    if system:
        body["system"] = system

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + TOKEN,
    }

    last = ""
    for attempt in range(retries):
        try:
            with httpx.Client(timeout=timeout) as client:
                r = client.post(BASE + "/messages", headers=headers, json=body)
            if r.status_code == 200:
                data = r.json()
                text = ""
                for blk in data.get("content", []):
                    if blk.get("type") == "text":
                        text = blk.get("text", "")
                        break
                if text.strip():
                    with open(cp, "w", encoding="utf-8") as fh:
                        json.dump({"text": text, "model": model}, fh, ensure_ascii=False)
                    return text
                last = "empty text: %s" % str(data)[:200]
            else:
                last = "HTTP %s: %s" % (r.status_code, r.text[:200])
        except Exception as e:
            last = "EXC %s" % e
        time.sleep(min(2 ** attempt, 20) + random.random())

    raise RuntimeError("LLM call failed after %d attempts: %s" % (retries, last))


_FENCE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$", re.M)


def extract_json_array(text: str):
    """Pull the first JSON array out of a model reply."""
    t = _FENCE.sub("", text).strip()
    try:
        v = json.loads(t)
        if isinstance(v, list):
            return v
    except Exception:
        pass
    # scan for balanced [...]
    start = t.find("[")
    while start != -1:
        depth = 0
        in_str = False
        esc = False
        for i in range(start, len(t)):
            c = t[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
                continue
            if c == '"':
                in_str = True
            elif c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    frag = t[start:i + 1]
                    try:
                        v = json.loads(frag)
                        if isinstance(v, list):
                            return v
                    except Exception:
                        break
        start = t.find("[", start + 1)
    return None


SPECIAL = re.compile(r"<[^>]*>|\{[^{}]*\}")


def extract_texts(text: str):
    """Parse a JSON array reply into a list of strings.

    The model sometimes answers with objects instead of plain strings
    ({"id": 0, "ru": "..."}); flatten those to their text field.
    """
    arr = extract_json_array(text)
    if arr is None:
        return None
    out = []
    for item in arr:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            val = None
            for k in ("ru", "text", "translation", "value", "result", "t"):
                if isinstance(item.get(k), str):
                    val = item[k]
                    break
            out.append(val if val is not None else "")
        else:
            out.append("")
    return out


def specials(text: str):
    """Multiset of inline markup/placeholders, in order."""
    return SPECIAL.findall(text or "")
