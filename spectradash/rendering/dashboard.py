from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from spectradash.rendering.palette import PALETTES

WIDTH, HEIGHT = 1600, 1200

def _font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()

def _metric(draw, box, label, value, colors):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=18, fill=colors["panel"], outline=colors["text"], width=2)
    draw.text((x1 + 18, y1 + 14), label, fill=colors["text"], font=_font(24, True))
    draw.text((x1 + 18, y1 + 54), value, fill=colors["text"], font=_font(30))

def render_dashboard(weather: dict, output: Path, theme: str, layout: str) -> Path:
    c = PALETTES.get(theme, PALETTES["light"])
    image = Image.new("RGB", (WIDTH, HEIGHT), c["background"])
    draw = ImageDraw.Draw(image)

    draw.text((55, 32), "SpectraDash", fill=c["accent"], font=_font(45, True))
    draw.text((55, 88), weather["location"], fill=c["text"], font=_font(58, True))

    if layout == "premium-lcd":
        draw.rounded_rectangle((40, 155, 1560, 380), radius=28, fill=c["panel"], outline=c["accent"], width=5)
    else:
        draw.rectangle((40, 155, 1560, 380), fill=c["panel"], outline=c["text"], width=3)

    draw.text((75, 180), f'{weather["current"]["temperature"]:.0f}°', fill=c["text"], font=_font(150, True))
    draw.text((360, 205), weather["current"]["condition"], fill=c["text"], font=_font(46, True))
    draw.text((360, 275), f'Feels like {weather["current"]["feels_like"]:.0f}°', fill=c["text"], font=_font(32))
    draw.text((1150, 205), f'AQI {weather["air"]["aqi"]}', fill=c["accent"], font=_font(38, True))
    draw.text((1150, 265), f'UV {weather["current"]["uv"]:.1f}', fill=c["accent"], font=_font(38, True))

    metrics = [
        ("Humidity", f'{weather["current"]["humidity"]}%'),
        ("Dew point", f'{weather["current"]["dew_point"]:.0f}°'),
        ("Wind", f'{weather["current"]["wind_speed"]:.0f}'),
        ("Gusts", f'{weather["current"]["wind_gust"]:.0f}'),
        ("Pressure", f'{weather["current"]["pressure"]:.0f} hPa'),
        ("Rain", f'{weather["forecast"][0]["rain"]}%'),
        ("Moon", weather["moon"]["name"]),
        ("Sun", f'{weather["sunrise"]}/{weather["sunset"]}'),
    ]
    x, y = 55, 410
    for label, value in metrics:
        _metric(draw, (x, y, x + 350, y + 105), label, value, c)
        x += 380
        if x > 1200:
            x = 55
            y += 125

    y = 675
    draw.text((55, y), "7-Day Forecast", fill=c["text"], font=_font(42, True))
    y += 62
    for day in weather["forecast"]:
        draw.rounded_rectangle((55, y, 1545, y + 54), radius=9, fill=c["panel"], outline=c["text"], width=1)
        text = (
            f'{day["date"]}     {day["condition"]:<18} '
            f'{day["high"]:.0f}° / {day["low"]:.0f}°     '
            f'Rain {day["rain"]}%     UV {day["uv"]:.1f}'
        )
        draw.text((75, y + 10), text, fill=c["text"], font=_font(25))
        y += 61

    draw.text((55, 1148), f'Updated {weather["updated"][:16].replace("T", " ")} · {weather["source"]}', fill=c["text"], font=_font(22))
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    return output
