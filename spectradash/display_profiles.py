from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class DisplayProfile:
    id: str
    name: str
    manufacturer: str
    width: int
    height: int
    colors: tuple[str, ...]
    driver_module: str | None
    driver_root: str | None
    verified: bool
    density: str
    supports_partial_refresh: bool = False
    notes: str = ""

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    @property
    def status(self) -> str:
        return "verified" if self.verified else "experimental"

    def to_dict(self) -> dict:
        result = asdict(self)
        result["colors"] = list(self.colors)
        result["status"] = self.status
        return result


PROFILES: dict[str, DisplayProfile] = {
    "waveshare-13in3e": DisplayProfile(
        id="waveshare-13in3e", name='13.3" Spectra 6 (E)', manufacturer="Waveshare",
        width=1600, height=1200, colors=("black", "white", "yellow", "red", "blue", "green"),
        driver_module="epd13in3E", driver_root="E-paper_Separate_Program/13.3inch_e-Paper_E/RaspberryPi/python",
        verified=True, density="expanded", notes="Verified on EL133UF1 hardware.",
    ),
    "waveshare-7in3e": DisplayProfile(
        id="waveshare-7in3e", name='7.3" Spectra 6 (E)', manufacturer="Waveshare",
        width=800, height=480, colors=("black", "white", "yellow", "red", "blue", "green"),
        driver_module="epd7in3e", driver_root="E-paper_Separate_Program/7.3inch_e-Paper_E/RaspberryPi/python",
        verified=False, density="standard", notes="Software-rendered and driver-mapped; community hardware testing required.",
    ),
    "waveshare-7in5v2-bw": DisplayProfile(
        id="waveshare-7in5v2-bw", name='7.5" V2 black/white', manufacturer="Waveshare",
        width=800, height=480, colors=("black", "white"), driver_module="epd7in5_V2",
        driver_root="RaspberryPi_JetsonNano/python", verified=False, density="standard",
        supports_partial_refresh=False, notes="Monochrome preview verified; physical driver path may vary by Waveshare checkout.",
    ),
    "waveshare-5in65f": DisplayProfile(
        id="waveshare-5in65f", name='5.65" seven-color (F)', manufacturer="Waveshare",
        width=600, height=448, colors=("black", "white", "yellow", "red", "blue", "green", "orange"),
        driver_module="epd5in65f", driver_root="RaspberryPi_JetsonNano/python", verified=False,
        density="compact", notes="Software-rendered preview only until community hardware validation.",
    ),
    "waveshare-4in2v2-bw": DisplayProfile(
        id="waveshare-4in2v2-bw", name='4.2" V2 black/white', manufacturer="Waveshare",
        width=400, height=300, colors=("black", "white"), driver_module="epd4in2_V2",
        driver_root="RaspberryPi_JetsonNano/python", verified=False, density="compact",
        supports_partial_refresh=True, notes="Compact mode; physical refresh behavior needs community testing.",
    ),
    "preview-1024x600": DisplayProfile(
        id="preview-1024x600", name="Generic 1024 x 600 preview", manufacturer="Generic",
        width=1024, height=600, colors=("black", "white", "yellow", "red", "blue", "green"),
        driver_module=None, driver_root=None, verified=False, density="standard",
        notes="Browser/software preview only; no physical driver.",
    ),
}

DEFAULT_PROFILE_ID = "waveshare-13in3e"


def get_profile(profile_id: str | None) -> DisplayProfile:
    return PROFILES.get(str(profile_id), PROFILES[DEFAULT_PROFILE_ID])


def list_profiles() -> Iterable[DisplayProfile]:
    return PROFILES.values()
