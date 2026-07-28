from __future__ import annotations

import socket
from datetime import datetime
from pathlib import Path
from typing import Any

import psutil


def system_info() -> dict[str, Any]:
    temp = None
    thermal = Path("/sys/class/thermal/thermal_zone0/temp")
    try:
        temp = round(int(thermal.read_text().strip()) / 1000, 1)
    except Exception:
        pass
    disk = psutil.disk_usage("/")
    return {
        "hostname": socket.gethostname(), "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent, "disk_percent": disk.percent,
        "temperature_c": temp, "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
    }


def recommended_performance_mode() -> str:
    """Recommend Lite mode for low-memory boards such as the Pi Zero 2 W."""
    try:
        model = Path("/proc/device-tree/model").read_text(errors="ignore").lower()
        mem_kb = 0
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                mem_kb = int(line.split()[1]); break
        if "zero 2" in model or (mem_kb and mem_kb < 750000):
            return "lite"
    except Exception:
        pass
    return "full"
