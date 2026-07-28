from __future__ import annotations
import sys
import time
from pathlib import Path
from PIL import Image
from spectradash.display.base import DisplayAdapter

DRIVER_DIR = Path("/opt/waveshare-13in3e/python/lib")
STAMP = Path("/var/lib/spectradash/last-physical-refresh.txt")
MIN_REFRESH_SECONDS = 180

class Waveshare13in3EDisplay(DisplayAdapter):
    def _driver(self):
        if not DRIVER_DIR.exists():
            raise RuntimeError(
                "Waveshare driver is not installed. Run "
                "sudo scripts/install-waveshare-driver.sh"
            )
        sys.path.insert(0, str(DRIVER_DIR))
        import epd13in3E
        return epd13in3E

    def _check_interval(self):
        if not STAMP.exists():
            return
        elapsed = time.time() - float(STAMP.read_text().strip())
        if elapsed < MIN_REFRESH_SECONDS:
            remaining = int(MIN_REFRESH_SECONDS - elapsed)
            raise RuntimeError(f"Physical refresh locked for another {remaining} seconds.")

    def show(self, image_path: Path) -> None:
        self._check_interval()
        driver = self._driver()
        epd = driver.EPD()
        image = Image.open(image_path).convert("RGB")
        if image.size != (driver.EPD_WIDTH, driver.EPD_HEIGHT):
            image = image.resize((driver.EPD_WIDTH, driver.EPD_HEIGHT))
        try:
            epd.Init()
            epd.display(epd.getbuffer(image))
            STAMP.parent.mkdir(parents=True, exist_ok=True)
            STAMP.write_text(str(time.time()))
        finally:
            epd.sleep()
