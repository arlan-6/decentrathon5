from integrations.llm.base import LLMClient


class OpenRouterClient(LLMClient):
    def score_text(self, text: str) -> tuple[float, str]:
        score = min(100.0, 40.0 + float(len(text)) / 8.0)
        return score, "OpenRouter stub evaluation"

