from integrations.llm.base import LLMClient
from integrations.llm.ollama_client import OllamaClient


class AIService:
    def __init__(self, client: LLMClient | None = None) -> None:
        self.client = client or OllamaClient()

    def evaluate(self, text: str) -> tuple[float, str]:
        return self.client.score_text(text=text)

