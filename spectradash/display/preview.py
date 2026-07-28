from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def font(size: int):
    path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()

def render_preview(weather: dict, output: Path) -> Path:
    image = Image.new("RGB", (1600, 1200), "white")
    draw = ImageDraw.Draw(image)
    draw.text((60, 45), weather["location"], fill="black", font=font(64))
    draw.text((60, 150), weather["current"]["icon"], fill="black", font=font(140))
    draw.text((250, 160), f'{weather["current"]["temperature"]:.0f}°', fill="black", font=font(140))
    draw.text((60, 340), weather["current"]["condition"], fill="black", font=font(38))
    y = 420
    for line in [
        f'Feels like: {weather["current"]["feels_like"]:.0f}°',
        f'Humidity: {weather["current"]["humidity"]}%',
        f'Dew point: {weather["current"]["dew_point"]:.0f}°',
        f'Wind: {weather["current"]["wind_speed"]}',
        f'Pressure: {weather["current"]["pressure"]} hPa',
        f'Sunrise: {weather["sunrise"]}',
        f'Sunset: {weather["sunset"]}',
    ]:
        draw.text((60, y), line, fill="black", font=font(34))
        y += 58
    draw.line((620, 80, 620, 1120), fill="black", width=3)
    draw.text((680, 70), "7-Day Forecast", fill="black", font=font(58))
    y = 170
    for day in weather["forecast"]:
        draw.rectangle((670, y, 1530, y + 110), outline="black", width=2)
        draw.text((700, y + 20), day["date"], fill="black", font=font(26))
        draw.text((930, y + 18), day["icon"], fill="black", font=font(36))
        draw.text((1010, y + 20), day["condition"], fill="black", font=font(26))
        draw.text((1300, y + 20), f'{day["high"]:.0f}°/{day["low"]:.0f}°', fill="black", font=font(26))
        draw.text((1300, y + 62), f'Rain {day["rain"]}%', fill="black", font=font(24))
        y += 130
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    return output
