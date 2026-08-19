from __future__ import annotations

from typing import Protocol


class LLMProvider(Protocol):
    """Provider boundary for model-backed reasoning."""

    def generate(self, prompt: str) -> str: ...
