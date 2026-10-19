import json

import httpx

from src.core.config import AI_API_KEY, AI_BASE_URL, AI_MODEL


def chat(messages: list[dict]) -> dict:
    """Send messages to the OpenAI-compatible AI provider and return its JSON answer."""
    response = httpx.post(
        f"{AI_BASE_URL}/chat/completions",
        json={
            "model": AI_MODEL,
            "messages": messages,
            "response_format": {"type": "json_object"},
        },
        headers={"Authorization": f"Bearer {AI_API_KEY}"} if AI_API_KEY else {},
        timeout=60,
    )
    response.raise_for_status()
    return json.loads(response.json()["choices"][0]["message"]["content"])
