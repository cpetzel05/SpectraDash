from pathlib import Path
from unittest.mock import patch

from PIL import Image

from spectradash import display


def test_display_worker_is_launched_as_package_module(tmp_path):
    completed = type("Completed", (), {
        "returncode": 0,
        "stdout": 'SPECTRADASH_RESULT={"ok": true}\n',
    })()

    image = Image.new("RGB", (1600, 1200), "white")
    with patch("spectradash.display.subprocess.run", return_value=completed) as run:
        result = display.send_to_display(image, profile_id="waveshare-13in3e")

    command = run.call_args.args[0]
    assert command[:3] == [display.sys.executable, "-m", "spectradash.hardware_worker"]
    assert command[-2:] == ["--profile", "waveshare-13in3e"]
    assert result["ok"] is True
