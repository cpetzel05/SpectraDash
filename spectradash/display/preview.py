from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PALETTE = {
    "light": ("white", "black"),
    "dark": ("#111111", "white"),
    "ocean": ("#dff5ff", "#073b4c"),
    "desert": ("#fff4d6", "#5f370e"),
    "high-contrast": ("white", "black"),
}

def _font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()

def render_preview(weather: dict, output: Path, theme: str = "light", layout: str = "weather-station") -> Path:
    bg, fg = PALETTE.get(theme, PALETTE["light"])
    image = Image.new("RGB", (1600, 1200), bg)
    draw = ImageDraw.Draw(image)
    draw.text((55, 40), "SpectraDash", fill=fg, font=_font(44, True))
    draw.text((55, 100), weather["location"], fill=fg, font=_font(56, True))
    draw.text((55, 190), f'{weather["current"]["temperature"]:.0f}°', fill=fg, font=_font(150, True))
    draw.text((330, 240), weather["current"]["condition"], fill=fg, font=_font(40))
    metrics = [
        ("Feels", f'{weather["current"]["feels_like"]:.0f}°'),
        ("Humidity", f'{weather["current"]["humidity"]}%'),
        ("Dew", f'{weather["current"]["dew_point"]:.0f}°'),
        ("Wind", f'{weather["current"]["wind_speed"]:.0f}'),
        ("AQI", str(weather["air_quality"]["us_aqi"])),
        ("UV", f'{weather["current"]["uv_index"]:.1f}'),
        ("Moon", weather["moon"]["name"]),
        ("Sun", f'{weather["sunrise"]}/{weather["sunset"]}'),
    ]
    x, y = 55, 420
    for label, value in metrics:
        draw.rounded_rectangle((x, y, x + 330, y + 115), radius=12, outline=fg, width=2)
        draw.text((x + 18, y + 14), label, fill=fg, font=_font(25, True))
        draw.text((x + 18, y + 55), value, fill=fg, font=_font(29))
        x += 355
        if x > 1200:
            x = 55
            y += 135
    y = 720
    draw.text((55, y), "7-Day Forecast", fill=fg, font=_font(40, True))
    y += 60
    for day in weather["forecast"]:
        draw.rectangle((55, y, 1545, y + 48), outline=fg, width=1)
        text = f'{day["date"]}   {day["condition"]}   {day["high"]:.0f}°/{day["low"]:.0f}°   Rain {day["rain"]}%   UV {day.get("uv_index",0):.1f}'
        draw.text((70, y + 8), text, fill=fg, font=_font(24))
        y += 52
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    return output
