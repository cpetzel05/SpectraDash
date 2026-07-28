from PIL import ImageDraw, ImageFont

def render(image, box, context):
    draw = ImageDraw.Draw(image)
    x1, y1, x2, y2 = box
    weather = context.get("weather", {})
    accent = context.get("theme_colors", {}).get("primary", (0, 0, 255))
    draw.rounded_rectangle(box, radius=20, fill=(255,255,255), outline=(0,0,0), width=3)
    draw.text((x1+16,y1+16), "HELLO WEATHER", fill=accent)
    draw.text((x1+16,y1+52), str(weather.get("description", "Ready")), fill=(0,0,0))
