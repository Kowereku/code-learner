import json

import httpx

from src.core.config import AI_API_KEY, AI_BASE_URL, AI_CHAT_MODEL, AI_MODEL

HEADERS = {"Authorization": f"Bearer {AI_API_KEY}"} if AI_API_KEY else {}


def chat(messages: list[dict], model: str) -> dict:
    """Send messages to the OpenAI-compatible AI provider and return its JSON answer."""
    response = httpx.post(
        f"{AI_BASE_URL}/chat/completions",
        json={
            "model": model,
            "messages": messages,
            "response_format": {"type": "json_object"},
        },
        headers=HEADERS,
        timeout=120,
    )
    response.raise_for_status()
    return json.loads(response.json()["choices"][0]["message"]["content"])


def warm_up() -> None:
    """Make the provider load both models, so the first real answers don't wait for them."""
    for model in (AI_CHAT_MODEL, AI_MODEL):
        try:
            httpx.post(
                f"{AI_BASE_URL}/chat/completions",
                json={"model": model, "messages": [{"role": "user", "content": "Hi"}], "max_tokens": 1},
                headers=HEADERS,
                timeout=180,
            )
        except httpx.HTTPError:
            pass
