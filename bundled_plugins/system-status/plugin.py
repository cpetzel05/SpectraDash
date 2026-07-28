from __future__ import annotations
from PIL import ImageDraw, ImageFont


def _font(size: int, bold: bool = False):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default()


def render(image, box, context):
    draw = ImageDraw.Draw(image)
    x1, y1, x2, y2 = box
    info = context.get("system", {})
    accent = context.get("theme_colors", {}).get("secondary", (0, 128, 0))
    draw.rounded_rectangle(box, radius=20, fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    draw.text((x1 + 16, y1 + 13), "RASPBERRY PI", font=_font(19, True), fill=accent)
    rows = [
        ("Model", str(info.get("model", "Unknown"))),
        ("CPU", str(info.get("cpu_temperature", "—"))),
        ("Memory", str(info.get("memory", "—"))),
        ("Uptime", str(info.get("uptime", "—"))),
    ]
    y = y1 + 50
    for label, value in rows:
        draw.text((x1 + 16, y), label, font=_font(16, True), fill=(0, 0, 0))
        draw.text((x2 - 16, y), value, font=_font(16), fill=(0, 0, 0), anchor="ra")
        y += 29
