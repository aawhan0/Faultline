from __future__ import annotations

import httpx

from faultline.agent.llm import LLMProvider


class OllamaProvider(LLMProvider):
    """LLM provider backed by a local Ollama server."""

    def __init__(
        self,
        model: str = "qwen2.5:3b",
        base_url: str = "http://localhost:11434",
        timeout: float = 120.0,
        temperature: float = 0.0,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                },
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        if "response" not in data:
            raise ValueError("Ollama response missing 'response' field.")

        return data["response"]
