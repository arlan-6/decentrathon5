from integrations.llm.base import LLMClient


class OllamaClient(LLMClient):
    def score_text(self, text: str) -> tuple[float, str]:
        score = min(100.0, 60.0 + float(len(text)) / 12.0)
        return score, "Ollama stub evaluation"

