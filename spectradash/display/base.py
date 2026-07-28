from abc import ABC, abstractmethod
from pathlib import Path

class DisplayAdapter(ABC):
    @abstractmethod
    def show(self, image_path: Path) -> None:
        raise NotImplementedError
