from __future__ import annotations
from datetime import datetime
from PIL import ImageDraw, ImageFont

QUOTES = [
    "Sunshine is the best medicine.",
    "Every cloud has a silver lining.",
    "A calm sky begins with a calm mind.",
    "Weather changes. Good design endures.",
]


def _font(size: int, bold: bool = False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def render(image, box, context):
    draw = ImageDraw.Draw(image)
    x1, y1, x2, y2 = box
    theme = context.get("theme_colors", {})
    accent = theme.get("primary", (0, 0, 255))
    draw.rounded_rectangle(box, radius=20, fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    draw.rectangle((x1 + 3, y1 + 3, x2 - 3, y1 + 48), fill=accent)
    draw.text((x1 + 15, y1 + 14), "DAILY THOUGHT", font=_font(18, True), fill=(255, 255, 255))
    quote = QUOTES[datetime.now().timetuple().tm_yday % len(QUOTES)]
    words = quote.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textbbox((0, 0), trial, font=_font(22, True))[2] > max(100, x2 - x1 - 34):
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    y = y1 + 70
    for line in lines[:4]:
        draw.text((x1 + 17, y), line, font=_font(22, True), fill=(0, 0, 0))
        y += 31
