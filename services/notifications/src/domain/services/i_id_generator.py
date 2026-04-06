from abc import ABC, abstractmethod


class IIDGenerator(ABC):
    @abstractmethod
    def generate(self) -> int:
        pass
