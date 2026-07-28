import shutil
from pathlib import Path
from spectradash.display.base import DisplayAdapter

class PreviewDisplay(DisplayAdapter):
    def __init__(self, output: Path):
        self.output = output

    def show(self, image_path: Path) -> None:
        self.output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(image_path, self.output)
