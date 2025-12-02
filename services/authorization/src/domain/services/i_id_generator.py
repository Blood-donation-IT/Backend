from abc import ABC, abstractmethod

class IIDGenerator(ABC):
    @abstractmethod
    def generate(self) -> int:
        """Generates a unique identifier."""
        pass
