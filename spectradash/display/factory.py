from pathlib import Path
from spectradash.display.preview import PreviewDisplay
from spectradash.display.waveshare_13in3e import Waveshare13in3EDisplay

def create_display(profile: str):
    if profile == "preview":
        return PreviewDisplay(Path("/var/lib/spectradash/last-display.png"))
    if profile == "waveshare-13in3e":
        return Waveshare13in3EDisplay()
    raise ValueError(f"Unknown display profile: {profile}")
