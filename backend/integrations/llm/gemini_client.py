from integrations.llm.base import LLMClient


class GeminiClient(LLMClient):
    def score_text(self, text: str) -> tuple[float, str]:
        score = min(100.0, 50.0 + float(len(text)) / 10.0)
        return score, "Gemini stub evaluation"

