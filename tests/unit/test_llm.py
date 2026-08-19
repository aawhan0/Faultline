from faultline.agent.llm import LLMProvider


class FakeLLM:
    def generate(self, prompt: str) -> str:
        return f"response: {prompt}"


def test_llm_provider_contract() -> None:
    provider: LLMProvider = FakeLLM()

    result = provider.generate("diagnose this incident")

    assert result == "response: diagnose this incident"