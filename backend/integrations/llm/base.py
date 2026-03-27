from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def score_text(self, text: str) -> tuple[float, str]:
        raise NotImplementedError

