import httpx
import pytest

from faultline.agent.ollama import OllamaProvider


def test_ollama_provider_generates_text(monkeypatch) -> None:
    captured = {}

    def fake_post(url, **kwargs):
        captured["url"] = url
        captured["kwargs"] = kwargs

        request = httpx.Request("POST", url)

        return httpx.Response(
            200,
            json={"response": "Database connection pool exhausted."},
            request=request,
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    provider = OllamaProvider()

    result = provider.generate("Diagnose this incident.")

    assert result == "Database connection pool exhausted."
    assert captured["url"] == "http://localhost:11434/api/generate"
    assert captured["kwargs"]["json"]["model"] == "qwen2.5:3b"
    assert captured["kwargs"]["json"]["stream"] is False


def test_ollama_provider_rejects_http_errors(monkeypatch) -> None:
    def fake_post(url, **kwargs):
        request = httpx.Request("POST", url)

        return httpx.Response(
            500,
            text="server error",
            request=request,
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    provider = OllamaProvider()

    with pytest.raises(httpx.HTTPStatusError):
        provider.generate("Diagnose this incident.")


def test_ollama_provider_rejects_missing_response(monkeypatch) -> None:
    def fake_post(url, **kwargs):
        request = httpx.Request("POST", url)

        return httpx.Response(
            200,
            json={"model": "qwen2.5:3b"},
            request=request,
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    provider = OllamaProvider()

    with pytest.raises(ValueError, match="missing 'response'"):
        provider.generate("Diagnose this incident.")