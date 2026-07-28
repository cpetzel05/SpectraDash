from __future__ import annotations

import math
import random
from datetime import datetime
from pathlib import Path
from typing import Any
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1600, 1200
P = {"black": (0,0,0), "white": (255,255,255), "yellow": (255,224,0), "red": (220,35,45), "blue": (25,90,190), "green": (0,145,90)}
THEMES = {
    # Original palettes
    "sunrise": {"primary":"red","accent":"yellow","secondary":"blue","family":"three-tone"},
    "ocean": {"primary":"blue","accent":"green","secondary":"yellow","family":"three-tone"},
    "garden": {"primary":"green","accent":"yellow","secondary":"blue","family":"three-tone"},
    "classic": {"primary":"black","accent":"red","secondary":"blue","family":"three-tone"},
    "newspaper": {"primary":"black","accent":"yellow","secondary":"red","family":"three-tone"},
    "forest": {"primary":"green","accent":"yellow","secondary":"black","family":"three-tone"},
    "night": {"primary":"blue","accent":"yellow","secondary":"green","family":"three-tone"},

    # Nostalgic Windows XP-inspired palette. This uses only the Spectra 6 inks.
    "windows-xp": {"primary":"blue","accent":"green","secondary":"yellow","family":"xp"},

    # Two-tone palettes. Secondary intentionally repeats one of the two colors.
    "two-blue-green": {"primary":"blue","accent":"green","secondary":"blue","family":"two-tone"},
    "two-red-yellow": {"primary":"red","accent":"yellow","secondary":"red","family":"two-tone"},
    "two-black-yellow": {"primary":"black","accent":"yellow","secondary":"black","family":"two-tone"},
    "two-blue-white": {"primary":"blue","accent":"white","secondary":"blue","family":"two-tone"},
    "two-green-black": {"primary":"green","accent":"black","secondary":"green","family":"two-tone"},

    # Extra three-tone palettes.
    "three-primary": {"primary":"red","accent":"yellow","secondary":"blue","family":"three-tone"},
    "three-coastal": {"primary":"blue","accent":"yellow","secondary":"white","family":"three-tone"},
    "three-meadow": {"primary":"green","accent":"yellow","secondary":"red","family":"three-tone"},
    "three-arcade": {"primary":"black","accent":"green","secondary":"yellow","family":"three-tone"},
    "three-patriot": {"primary":"blue","accent":"red","secondary":"white","family":"three-tone"},
}


@lru_cache(maxsize=96)
def font(size: int, bold: bool=False):
    paths=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
    for path in paths:
        if Path(path).exists(): return ImageFont.truetype(path,size)
    return ImageFont.load_default()


def _fit(draw, text, box, start, color, bold=True, anchor="mm"):
    x1,y1,x2,y2=box; size=start
    text=str(text)
    while size>14:
        f=font(size,bold); bb=draw.textbbox((0,0),text,font=f)
        if bb[2]-bb[0] <= x2-x1-12 and bb[3]-bb[1] <= y2-y1-8:
            draw.text(((x1+x2)//2,(y1+y2)//2),text,font=f,fill=color,anchor=anchor); return
        size-=2


def _card(draw, box, radius=22, fill=None, outline=None, width=4):
    draw.rounded_rectangle(box,radius=radius,fill=fill or P["white"],outline=outline or P["black"],width=width)


def _top_rounded_rectangle(draw, box, radius, fill):
    """Draw a rectangle with rounded top corners and a square bottom edge."""
    x1, y1, x2, y2 = map(int, box)
    width = max(1, x2 - x1 + 1)
    height = max(1, y2 - y1 + 1)
    radius = max(0, min(int(radius), width // 2, height))
    if radius == 0:
        draw.rectangle((x1, y1, x2, y2), fill=fill)
        return
    layer = Image.new("RGB", (width, height + radius), P["white"])
    mask = Image.new("L", layer.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, width - 1, height + radius - 1), radius=radius, fill=255)
    color = Image.new("RGB", layer.size, fill)
    layer.paste(color, (0, 0), mask)
    draw._image.paste(layer.crop((0, 0, width, height)), (x1, y1))


def _moon_phase_fraction(label: str, illumination: Any) -> tuple[float, bool]:
    """Return illuminated fraction and whether the bright limb is waxing."""
    try:
        fraction = max(0.0, min(1.0, float(illumination) / 100.0))
    except (TypeError, ValueError):
        fraction = 0.5
    text = str(label or "").lower()
    waxing = "waxing" in text or "first quarter" in text
    if "new moon" in text:
        fraction = 0.0
    elif "full moon" in text:
        fraction = 1.0
    elif "quarter" in text:
        fraction = 0.5
    return fraction, waxing


@lru_cache(maxsize=12)
def _lunar_surface(size: int) -> Image.Image:
    """Create one deterministic high-detail lunar texture shared by every theme.

    The texture is original procedural artwork.  It intentionally avoids an
    embedded third-party photograph so release packages remain redistributable.
    """
    size = max(64, int(size))
    rng = random.Random(0x5E1EC7A)
    surface = Image.new("L", (size, size), 184)
    px = surface.load()
    cx = cy = (size - 1) / 2.0
    radius = size * 0.455

    # Multi-scale deterministic terrain noise gives the Moon a photographic
    # texture without requiring a bundled bitmap asset.
    noise_layers = []
    for grid, amplitude in ((9, 34), (19, 20), (41, 10), (83, 5)):
        small = Image.new("L", (grid, grid))
        sp = small.load()
        for yy in range(grid):
            for xx in range(grid):
                sp[xx, yy] = rng.randrange(256)
        noise_layers.append((small.resize((size, size), Image.Resampling.BICUBIC), amplitude))

    noise_pixels = [(im.load(), amp) for im, amp in noise_layers]
    for y in range(size):
        ny = (y - cy) / radius
        for x in range(size):
            nx = (x - cx) / radius
            rr = nx * nx + ny * ny
            if rr > 1.0:
                px[x, y] = 0
                continue
            terrain = 0.0
            for npix, amp in noise_pixels:
                terrain += ((npix[x, y] - 127.5) / 127.5) * amp
            # Slight limb darkening adds depth before phase illumination.
            nz = math.sqrt(max(0.0, 1.0 - rr))
            base = 172 + terrain + 20 * nz
            px[x, y] = max(18, min(245, int(base)))

    d = ImageDraw.Draw(surface)

    # Recognizable maria shapes.  Irregular overlapping ellipses avoid the
    # synthetic "polka-dot" look of basic moon icons.
    maria = [
        (.31,.34,.18,.13,-55),(.42,.30,.12,.10,-40),(.61,.32,.16,.13,-48),
        (.69,.47,.13,.17,-52),(.55,.58,.20,.15,-43),(.36,.63,.12,.16,-36),
        (.26,.51,.10,.13,-30),(.73,.68,.08,.10,-32),(.49,.44,.07,.06,-26),
    ]
    for fx, fy, rw, rh, delta in maria:
        x = int(size * fx); y = int(size * fy)
        rx = int(size * rw); ry = int(size * rh)
        shade = max(22, min(225, 174 + delta))
        d.ellipse((x-rx, y-ry, x+rx, y+ry), fill=shade)
        # A second offset ellipse breaks perfect symmetry.
        d.ellipse((x-rx//2, y-ry//2, x+rx, y+ry//3), fill=min(235, shade+8))

    # Large named-looking basins and ray craters, followed by many tiny craters.
    major = [
        (.24,.23,.050),(.47,.18,.032),(.71,.22,.044),(.82,.39,.028),
        (.23,.53,.041),(.43,.57,.031),(.67,.70,.050),(.50,.79,.029),
        (.78,.76,.023),(.58,.43,.022),(.31,.74,.020),(.72,.55,.020),
        (.40,.40,.018),(.56,.67,.017),(.18,.68,.015),
    ]
    for fx, fy, fr in major:
        r=max(2,int(size*fr)); x=int(size*fx); y=int(size*fy)
        d.ellipse((x-r,y-r,x+r,y+r), fill=82)
        d.ellipse((x-r+max(1,r//4),y-r+max(1,r//4),x+r,y+r), outline=220, width=max(1,size//180))
        d.arc((x-r,y-r,x+r,y+r), 18, 160, fill=42, width=max(1,size//190))
        if fr >= .04:
            for a in range(0,360,30):
                length=r*3.0
                ex=x+math.cos(math.radians(a))*length
                ey=y+math.sin(math.radians(a))*length
                d.line((x,y,ex,ey), fill=205, width=max(1,size//260))

    for _ in range(max(90, size // 3)):
        angle=rng.random()*math.tau
        radial=math.sqrt(rng.random())*radius*.93
        x=int(cx+math.cos(angle)*radial); y=int(cy+math.sin(angle)*radial)
        r=rng.choice((1,1,1,2,2,3)) * max(1,size//320)
        shade=rng.randint(65,150)
        d.ellipse((x-r,y-r,x+r,y+r), fill=shade)
        if r>1:
            d.arc((x-r,y-r,x+r,y+r),200,340,fill=min(240,shade+70),width=1)

    # Mask everything to a circular lunar disc.
    mask=Image.new("L",(size,size),0)
    md=ImageDraw.Draw(mask)
    pad=int(size*.045)
    md.ellipse((pad,pad,size-pad-1,size-pad-1),fill=255)
    return Image.composite(surface, Image.new("L",(size,size),0), mask)


def _realistic_moon(draw, box, label="", illumination=50, outline=True):
    """Render the universal textured Moon with phase-accurate illumination.

    Premium LCD, Weather Station, and every other theme call this same renderer,
    so lunar geography and crater placement remain visually consistent.
    """
    x1,y1,x2,y2=map(int,box)
    size=max(12,min(x2-x1,y2-y1))
    x1+=((x2-x1)-size)//2; y1+=((y2-y1)-size)//2
    fraction,waxing=_moon_phase_fraction(label,illumination)

    scale=4 if size>=44 else 3
    hi=max(96,size*scale)
    texture=_lunar_surface(hi).copy()
    tex=texture.load()
    alpha=Image.new("L",(hi,hi),0); ap=alpha.load()
    shade=Image.new("L",(hi,hi),0); sp=shade.load()
    cx=cy=(hi-1)/2.0; radius=hi*.455

    phase_angle=math.acos(max(-1.0,min(1.0,2.0*fraction-1.0)))
    side=1.0 if waxing else -1.0
    sx=side*math.sin(phase_angle); sz=math.cos(phase_angle)
    for yy in range(hi):
        ny=(yy-cy)/radius
        for xx in range(hi):
            nx=(xx-cx)/radius; rr=nx*nx+ny*ny
            if rr>1.0: continue
            nz=math.sqrt(max(0.0,1.0-rr))
            light=nx*sx+nz*sz
            # Soft terminator and faint earthshine retain texture in the dark limb.
            lit=max(0.0,min(1.0,(light+.055)/.16))
            earthshine=0.10+0.10*nz
            illumination_level=earthshine+(1.0-earthshine)*lit
            limb=.62+.38*nz
            value=int(tex[xx,yy]*illumination_level*limb)
            sp[xx,yy]=max(8,min(248,value))
            ap[xx,yy]=255

    moon=shade.resize((size,size),Image.Resampling.LANCZOS)
    alpha=alpha.resize((size,size),Image.Resampling.LANCZOS)
    # Neutral grayscale is represented using black/white dithering so no false
    # red, yellow, blue, or green pixels appear on the six-colour panel.
    moon=moon.convert("1",dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
    final_mask=alpha.point(lambda v:255 if v>80 else 0)
    if outline:
        od=ImageDraw.Draw(moon)
        pad=max(1,int(size*.045))
        od.ellipse((pad,pad,size-pad-1,size-pad-1),outline=P["black"],width=max(1,size//30))
    draw._image.paste(moon,(x1,y1),final_mask)


def _icon(draw, kind, box, night=False, frame=0, config=None, ray_scale=1.0):
    """Draw a Spectra-palette weather icon.

    The 3D style is simulated with layered palette shapes rather than gradients,
    which keeps the artwork crisp after six-color panel quantization.
    """
    config = config or {}
    style = config.get("icon_style", "premium") if config.get("enable_3d_icons", True) else "flat"
    shadows = bool(config.get("icon_shadows", True)) and style in {"3d", "premium"}
    highlights = bool(config.get("icon_highlights", True)) and style in {"3d", "premium"}
    x1,y1,x2,y2=map(int,box); w=x2-x1; h=y2-y1; cx=(x1+x2)//2; cy=(y1+y2)//2
    shift=(frame % 3 - 1) * max(2, int(w*.018))
    outline = P["black"]
    stroke = max(3, int(min(w,h)*.025))

    def sphere(x, y, r, base, shade, light):
        if shadows:
            draw.ellipse((x-r+8,y-r+10,x+r+10,y+r+12),fill=outline)
        draw.ellipse((x-r,y-r,x+r,y+r),fill=base,outline=outline,width=stroke)
        if style in {"3d", "premium"}:
            draw.ellipse((x-r*.72,y-r*.55,x+r*.55,y+r*.72),fill=shade)
            draw.ellipse((x-r*.58,y-r*.52,x+r*.38,y+r*.43),fill=base)
            if highlights:
                draw.ellipse((x-r*.42,y-r*.42,x-r*.05,y-r*.08),fill=light)

    def cloud(px, py, scale=1.0, dark=False):
        """Layered, sculpted cloud tuned for the six-colour Spectra palette."""
        base=P["blue"] if dark else P["white"]
        shade=P["black"] if dark else P["blue"]
        warm=P["red"] if dark else P["yellow"]
        cloud_w=w*.68*scale; cloud_h=h*.34*scale
        if shadows:
            draw.ellipse((px-cloud_w*.48+10,py-cloud_h*.30+12,px+cloud_w*.52+12,py+cloud_h*.54+14),fill=P["black"])
        # Main soft body and a larger set of overlapping puffs produce a much
        # more photographic silhouette than the previous three-circle cloud.
        draw.rounded_rectangle((px-cloud_w*.48,py-cloud_h*.08,px+cloud_w*.50,py+cloud_h*.48),
                               radius=max(10,int(cloud_h*.22)),fill=base,outline=outline,width=stroke)
        puffs=[(-.38,.01,.24),(-.25,-.22,.31),(-.06,-.35,.37),(.14,-.29,.34),(.32,-.10,.28),(.42,.08,.20),
               (-.12,.02,.30),(.12,.03,.31)]
        for ox,oy,rr in puffs:
            r=cloud_h*rr*1.45
            draw.ellipse((px+cloud_w*ox-r,py+cloud_h*oy-r,px+cloud_w*ox+r,py+cloud_h*oy+r),
                         fill=base,outline=outline,width=max(2,stroke-1))
        if style in {"3d", "premium"}:
            # Deep underside plus several contour bands imitate the dimensional
            # cloud artwork used by premium LCD weather stations.
            draw.arc((px-cloud_w*.44,py-cloud_h*.02,px+cloud_w*.46,py+cloud_h*.58),4,176,
                     fill=shade,width=max(3,stroke))
            draw.arc((px-cloud_w*.34,py-cloud_h*.18,px+cloud_w*.18,py+cloud_h*.22),198,342,
                     fill=P["white"] if dark else warm,width=max(2,stroke-1))
            draw.arc((px-cloud_w*.10,py-cloud_h*.42,px+cloud_w*.38,py+cloud_h*.12),194,334,
                     fill=P["white"],width=max(2,stroke-1))
            if style == "premium":
                rng=random.Random((int(px)*131 + int(py)*17 + int(w)*7 + int(h)) & 0xffffffff)
                # Small palette puffs and short contour strokes create visible
                # texture without relying on unsupported alpha gradients.
                for i in range(28):
                    tx=px+rng.uniform(-cloud_w*.39,cloud_w*.39)
                    ty=py+rng.uniform(-cloud_h*.30,cloud_h*.34)
                    rr=rng.uniform(cloud_h*.025,cloud_h*.075)
                    col=rng.choice([base,base,P["white"],shade])
                    draw.ellipse((tx-rr,ty-rr,tx+rr,ty+rr),fill=col)
                for i in range(8):
                    yy=py+cloud_h*(.10+i*.035)
                    draw.arc((px-cloud_w*(.34-i*.018),yy-cloud_h*.10,
                              px+cloud_w*(.36-i*.012),yy+cloud_h*.14),8,172,
                             fill=shade if i%2==0 else P["black"],width=max(1,stroke//2))

    if kind in {"sun","sun-cloud"}:
        if night:
            r=min(w,h)//5
            if style == "premium":
                _realistic_moon(draw,(cx-r*1.35,cy-r*1.35,cx+r*1.35,cy+r*1.35),"Waxing crescent",38)
            else:
                sphere(cx,cy,r,P["yellow"],P["white"],P["white"])
                draw.ellipse((cx-r*.05,cy-r*.45,cx+r*.62,cy+r*.35),fill=P["white"] if style!="3d" else P["blue"])
                if style=="3d":
                    for ox,oy,rr in [(-.28,-.05,.09),(.08,.18,.07),(.18,-.18,.05)]:
                        draw.ellipse((cx+r*ox-r*rr,cy+r*oy-r*rr,cx+r*ox+r*rr,cy+r*oy+r*rr),fill=P["black"])
        else:
            r=min(w,h)//5
            angle=(frame%8)*math.pi/16
            ray_count=24 if style=="premium" else 12
            for i in range(ray_count):
                a=angle+i*(2*math.pi/ray_count)
                p1=(cx+math.cos(a)*r*1.55,cy+math.sin(a)*r*1.55)
                ray_outer=1.55+(1.0*ray_scale)
                p2=(cx+math.cos(a)*r*ray_outer,cy+math.sin(a)*r*ray_outer)
                ray_color=P["yellow"] if style=="premium" and i%2 else P["red"]
                ray_width=max(2,stroke//2) if style=="premium" and i%2 else stroke+2
                draw.line((*p1,*p2),fill=ray_color,width=ray_width)
                if highlights and i%2==0: draw.line((p1[0]-2,p1[1]-2,p2[0]-2,p2[1]-2),fill=P["yellow"],width=max(2,stroke//2))
            sphere(cx,cy,r,P["yellow"],P["red"],P["white"])

    cloud_y=cy+15
    if kind in {"cloud","sun-cloud","rain","drizzle","storm","snow","fog","ice"}:
        cloud(cx+shift,cloud_y,dark=kind=="storm")

    if kind in {"rain","drizzle","storm"}:
        drop=(frame%3)*7
        count=(7 if style=="premium" else 4) if kind!="drizzle" else (5 if style=="premium" else 3)
        for i in range(count):
            x=x1+w*(.18+i*(.64/max(1,count-1))); y=cloud_y+h*.25+drop+(i%3)*7
            length=h*(.16 if kind!="drizzle" else .11)
            if shadows: draw.line((x+4,y+5,x-5,y+length+5),fill=P["black"],width=stroke+3)
            draw.line((x,y,x-9,y+length),fill=P["blue"],width=stroke+2)
            if style=="premium":
                draw.ellipse((x-stroke*.45,y+length-stroke*.4,x+stroke*.45,y+length+stroke*.5),fill=P["blue"])
            if highlights: draw.line((x-2,y+3,x-6,y+length*.62),fill=P["white"],width=max(2,stroke//2))
    if kind=="storm" and frame%2==0:
        pts=[(cx,cloud_y+h*.22),(cx-30,cloud_y+h*.43),(cx,cloud_y+h*.41),(cx-18,cloud_y+h*.62),(cx+38,cloud_y+h*.32),(cx+4,cloud_y+h*.34)]
        if shadows: draw.polygon([(x+6,y+6) for x,y in pts],fill=P["black"])
        draw.polygon(pts,fill=P["yellow"],outline=P["red"])
    if kind=="snow":
        drift=(frame%4-2)*5
        snow_count=5 if style=="premium" else 3
        for i in range(snow_count):
            x=x1+w*(.22+i*(.56/max(1,snow_count-1)))+drift; y=cloud_y+h*.36+(i%2)*12
            for a in (0,math.pi/3,2*math.pi/3):
                dx=math.cos(a)*11; dy=math.sin(a)*11
                draw.line((x-dx,y-dy,x+dx,y+dy),fill=P["blue"],width=max(3,stroke-1))
            if highlights: draw.ellipse((x-3,y-3,x+3,y+3),fill=P["white"])
    if kind=="fog":
        for i in range(3):
            off=((frame+i)%3-1)*10
            y=cloud_y+h*(.31+i*.10)
            if shadows: draw.line((x1+w*.20+off+4,y+5,x2-w*.14+off+4,y+5),fill=P["black"],width=stroke+2)
            draw.line((x1+w*.20+off,y,x2-w*.14+off,y),fill=P["blue"],width=stroke)

def _living_scene(draw, w, box, primary, secondary, frame, style="landscape", config=None):
    config = config or {}
    x1,y1,x2,y2=box; width=x2-x1; height=y2-y1
    _card(draw,box,26,fill=P["white"])
    # Sky band and horizon provide a bold six-color illustration without gradients.
    sky=P["blue"] if w.get("is_night") else P["white"]
    draw.rounded_rectangle((x1+4,y1+4,x2-4,y2-4),radius=22,fill=sky)
    horizon=y1+int(height*.68)
    seed=int(datetime.fromisoformat(w["updated"]).timestamp()//900)
    rng=random.Random(seed)
    if w.get("is_night"):
        for _ in range(15):
            sx=rng.randint(x1+25,x2-25); sy=rng.randint(y1+20,horizon-45)
            r=rng.choice([2,3,4]); draw.ellipse((sx-r,sy-r,sx+r,sy+r),fill=P["yellow"])
        mx=x1+int(width*(.20+.05*(frame%4))); my=y1+70
        draw.ellipse((mx-42,my-42,mx+42,my+42),fill=P["yellow"],outline=P["black"],width=4)
        draw.ellipse((mx-16,my-47,mx+45,my+25),fill=P["blue"])
    else:
        sx=x1+int(width*(.15+.09*(frame%6))); sy=y1+65+int(15*math.sin(frame))
        draw.ellipse((sx-43,sy-43,sx+43,sy+43),fill=P["yellow"],outline=P["red"],width=5)
        for i in range(8):
            a=i*math.pi/4+(frame%8)*math.pi/32
            draw.line((sx+math.cos(a)*55,sy+math.sin(a)*55,sx+math.cos(a)*76,sy+math.sin(a)*76),fill=P["red"],width=5)
    # Clouds visibly drift from frame to frame.
    cloud_count=3 if w.get("cloud_cover",0)>60 else 2 if w.get("cloud_cover",0)>20 else 1
    for i in range(cloud_count):
        cx=x1+int(width*(.42+i*.22))+((frame*18+i*7)%90)-45
        cy=y1+55+i*42
        draw.rounded_rectangle((cx-70,cy,cx+80,cy+48),radius=22,fill=P["white"],outline=P["black"],width=4)
        draw.ellipse((cx-45,cy-28,cx+15,cy+37),fill=P["white"],outline=P["black"],width=4)
        draw.ellipse((cx+3,cy-37,cx+67,cy+37),fill=P["white"],outline=P["black"],width=4)
    if style=="coastal":
        draw.rectangle((x1+4,horizon,x2-4,y2-4),fill=P["blue"])
        for i in range(4):
            yy=horizon+25+i*28; shift=(frame%3)*15
            draw.arc((x1-40+shift,yy-20,x1+250+shift,yy+30),0,180,fill=P["white"],width=5)
            draw.arc((x1+230-shift,yy-20,x1+520-shift,yy+30),0,180,fill=P["white"],width=5)
    else:
        draw.polygon([(x1+4,horizon+25),(x1+width*.22,horizon-55),(x1+width*.39,horizon+20),(x1+width*.59,horizon-80),(x1+width*.82,horizon+18),(x2-4,horizon-40),(x2-4,y2-4),(x1+4,y2-4)],fill=P["green"],outline=P["black"])
        draw.polygon([(x1+width*.13,horizon+5),(x1+width*.22,horizon-55),(x1+width*.28,horizon-4)],fill=P["white"])
        draw.polygon([(x1+width*.50,horizon-24),(x1+width*.59,horizon-80),(x1+width*.67,horizon-18)],fill=P["white"])
    if config.get("scene_details", True):
        # Foreground depth: trees or shoreline posts, kept within the six-color palette.
        for i in range(5):
            tx=x1+40+i*max(90,int(width/5))+(frame*3+i*11)%28
            base=y2-8
            draw.rectangle((tx-4,base-42,tx+4,base),fill=P["black"])
            draw.polygon([(tx,base-105),(tx-32,base-36),(tx+32,base-36)],fill=P["green"],outline=P["black"])
    if config.get("seasonal_details", True):
        month=datetime.fromisoformat(w["updated"]).month
        if month in {12,1,2}:
            for i in range(10):
                px=x1+30+(i*83)%max(100,width-60); py=y2-28-(i%3)*8
                draw.ellipse((px-5,py-5,px+5,py+5),fill=P["white"],outline=P["blue"])
        elif month in {3,4,5}:
            for i in range(8):
                px=x1+35+(i*97)%max(100,width-70); py=y2-22-(i%2)*8
                draw.ellipse((px-6,py-6,px+6,py+6),fill=P["yellow"],outline=P["red"])
        elif month in {9,10,11}:
            for i in range(8):
                px=x1+45+(i*91+frame*9)%max(100,width-90); py=y1+120+(i*31)%max(100,height-170)
                draw.polygon([(px,py-7),(px+7,py),(px,py+7),(px-7,py)],fill=P["red"],outline=P["black"])
    if config.get("living_details", True):
        if w.get("is_night"):
            for i in range(5):
                fx=x1+80+(i*117+frame*23)%max(100,width-160); fy=y1+110+(i*37)%max(80,height-180)
                draw.ellipse((fx-3,fy-3,fx+3,fy+3),fill=P["yellow"])
        else:
            for i in range(3):
                bx=x1+120+i*110+(frame*8)%35; by=y1+72+i*18
                draw.arc((bx-15,by-8,bx,by+8),190,350,fill=P["black"],width=3)
                draw.arc((bx,by-8,bx+15,by+8),190,350,fill=P["black"],width=3)
    if config.get("rainbow_effects", True) and w.get("icon") in {"rain","drizzle","sun-cloud"} and frame % 4 == 0:
        rb=(x2-250,y1+35,x2-35,y1+220)
        for j,col in enumerate((P["red"],P["yellow"],P["green"],P["blue"])):
            draw.arc((rb[0]+j*8,rb[1]+j*8,rb[2]-j*8,rb[3]-j*8),180,360,fill=col,width=8)
    # Condition overlays create the e-ink animation illusion between full refreshes.
    kind=w.get("icon","sun")
    if kind in {"rain","drizzle","storm"}:
        for i in range(12):
            rx=x1+35+(i*71+frame*17)%max(80,width-70); ry=y1+145+(i*29+frame*11)%max(80,height-190)
            draw.line((rx,ry,rx-9,ry+24),fill=P["blue"],width=5)
    if kind=="snow":
        for i in range(14):
            rx=x1+25+(i*83+frame*13)%max(80,width-50); ry=y1+110+(i*41+frame*9)%max(80,height-150)
            draw.line((rx-6,ry,rx+6,ry),fill=P["blue"],width=3); draw.line((rx,ry-6,rx,ry+6),fill=P["blue"],width=3)
    if kind=="storm" and frame%2==0:
        draw.polygon([(x1+width*.70,y1+120),(x1+width*.63,y1+220),(x1+width*.70,y1+215),(x1+width*.64,y1+310),(x1+width*.82,y1+185),(x1+width*.73,y1+190)],fill=P["yellow"],outline=P["black"])
    # Current conditions overlay.
    badge=(x1+20,y2-125,x2-20,y2-20)
    draw.rounded_rectangle(badge,radius=20,fill=P["white"],outline=P["black"],width=4)
    draw.text((badge[0]+20,badge[1]+12),f'{w["temperature"]}{w["temperature_symbol"]}',font=font(48,True),fill=primary)
    draw.text((badge[0]+205,badge[1]+18),w["description"],font=font(28,True),fill=P["black"])
    draw.text((badge[0]+205,badge[1]+58),f'Feels {w["feels_like"]}{w["temperature_symbol"]}  ·  {w["wind_compass"]} {w["wind_speed"]} {w["wind_unit"]}',font=font(20),fill=P["black"])
    draw.text((badge[2]-18,badge[1]+20),f'FRAME {frame+1}',font=font(14,True),fill=secondary,anchor="ra")


def _metric(draw, box, label, value, accent, gauge=None):
    _card(draw,box,18); x1,y1,x2,y2=box
    draw.text((x1+16,y1+10),label.upper(),font=font(16,True),fill=accent)
    _fit(draw,str(value),(x1+8,y1+31,x2-8,y2-12),31,P["black"],True)
    if gauge is not None:
        frac=max(0.0,min(1.0,float(gauge)))
        draw.rounded_rectangle((x1+15,y2-13,x2-15,y2-7),radius=3,fill=P["black"])
        draw.rounded_rectangle((x1+15,y2-13,x1+15+(x2-x1-30)*frac,y2-7),radius=3,fill=accent)


def _compass(draw, box, degrees, label, primary):
    x1,y1,x2,y2=box; _card(draw,box,18)
    cx=(x1+x2)//2; cy=(y1+y2)//2+8; r=min(x2-x1,y2-y1)//2-18
    draw.ellipse((cx-r,cy-r,cx+r,cy+r),outline=P["black"],width=4)
    for name,a in [("N",-90),("E",0),("S",90),("W",180)]:
        rad=math.radians(a); draw.text((cx+math.cos(rad)*(r-16),cy+math.sin(rad)*(r-16)),name,font=font(13,True),fill=P["black"],anchor="mm")
    a=math.radians(float(degrees)-90)
    tip=(cx+math.cos(a)*(r-24),cy+math.sin(a)*(r-24)); left=(cx+math.cos(a+2.5)*18,cy+math.sin(a+2.5)*18); right=(cx+math.cos(a-2.5)*18,cy+math.sin(a-2.5)*18)
    draw.polygon([tip,left,right],fill=primary,outline=P["black"])
    draw.ellipse((cx-7,cy-7,cx+7,cy+7),fill=P["yellow"],outline=P["black"])
    draw.text((cx,y1+15),label,font=font(15,True),fill=primary,anchor="ma")


def _hourly_graph(draw, hourly, box, symbol, primary, secondary):
    x1,y1,x2,y2=box; _card(draw,box,20)
    draw.text((x1+20,y1+12),f'NEXT {len(hourly)} HOURS',font=font(19,True),fill=primary)
    graph=(x1+55,y1+65,x2-35,y2-44); gx1,gy1,gx2,gy2=graph
    temps=[h["temperature"] for h in hourly] or [0]; lo,hi=min(temps),max(temps)
    if hi==lo: hi+=1
    pts=[]
    for i,h in enumerate(hourly):
        x=gx1+(gx2-gx1)*i/max(1,len(hourly)-1); y=gy2-(h["temperature"]-lo)/(hi-lo)*(gy2-gy1); pts.append((x,y))
    if len(pts)>1: draw.line(pts,fill=primary,width=6,joint="curve")
    for i,(x,y) in enumerate(pts):
        draw.ellipse((x-7,y-7,x+7,y+7),fill=secondary,outline=P["black"],width=2)
        draw.text((x,y-26),f'{hourly[i]["temperature"]}°',font=font(15,True),fill=P["black"],anchor="mm")
        if len(hourly) <= 12 or i % 2 == 0: draw.text((x,gy2+18),hourly[i]["time"].replace(" ",""),font=font(13),fill=P["black"],anchor="mm")
        if hourly[i]["precip_probability"]>=20 and (len(hourly) <= 12 or i % 2 == 0): draw.text((x,gy2+37),f'{hourly[i]["precip_probability"]}%',font=font(13,True),fill=P["blue"],anchor="mm")



def _resolved_forecast_date_style(config: dict[str, Any]) -> str:
    """Resolve Automatic forecast date labels for the selected panel density."""
    style = str(config.get("forecast_date_style", "auto"))
    if style in {"off", "compact", "expanded"}:
        return style
    density = str(config.get("layout_density", "auto"))
    if density == "compact":
        return "compact"
    if density == "expanded":
        return "expanded"
    if density == "standard":
        return "compact"
    try:
        from .display_profiles import get_profile
        width, _ = get_profile(config.get("display_profile")).size
        return "expanded" if width >= 1200 else "compact"
    except Exception:
        return "expanded"


def _forecast_date_text(day: dict[str, Any], style: str) -> str:
    stamp = datetime.fromisoformat(str(day["date"]))
    if style == "expanded":
        return stamp.strftime("%b %-d").upper()
    if style == "compact":
        return f"{stamp.month}/{stamp.day}"
    return ""


def _forecast_day_label(day: dict[str, Any], index: int, config: dict[str, Any]) -> str:
    """Return TODAY for the first rolling forecast card when enabled."""
    if index == 0 and str(config.get("forecast_first_day_label", "today")) == "today":
        return "TODAY"
    return str(day.get("label", "")).upper()



def _lcd_panel(draw, box, radius=18, outline=None, width=3, fill=None):
    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=fill if fill is not None else P["black"],
        outline=outline or P["white"],
        width=width,
    )


def _resolved_premium_lcd_mode(weather: dict[str, Any], config: dict[str, Any]) -> str:
    """Resolve Premium LCD Light, Dark, or Automatic appearance."""
    requested = str(config.get("premium_lcd_mode", "dark"))
    if requested == "automatic":
        return "dark" if bool(weather.get("is_night")) else "light"
    return requested if requested in {"light", "dark"} else "dark"


def _render_premium_lcd(w: dict[str, Any], c: dict[str, Any], mode: str, frame: int, stamp: datetime) -> Image.Image:
    """LCD-inspired alternate layout with dedicated light and dark palettes."""
    appearance = _resolved_premium_lcd_mode(w, c)
    light_mode = appearance == "light"
    background = P["white"] if light_mode else P["black"]
    panel_fill = P["white"] if light_mode else P["black"]
    text = P["black"] if light_mode else P["white"]
    border = P["black"] if light_mode else P["white"]
    muted = P["blue"] if light_mode else P["white"]
    warm = P["red"] if light_mode else P["yellow"]
    sun_accent = P["yellow"]
    water = P["blue"]
    good = P["green"]

    img = Image.new("RGB", (WIDTH, HEIGHT), background)
    d = ImageDraw.Draw(img)

    # Top-left current conditions panel.
    _lcd_panel(d, (10, 10, 860, 525), 20, border, 3, panel_fill)
    d.text((38, 34), "CURRENT CONDITIONS", font=font(24), fill=text)
    d.text((38, 78), f'{w.get("temperature", "—")}{w.get("temperature_symbol", "°")}', font=font(108, True), fill=text)
    d.text((40, 205), f'Feels like {w.get("feels_like", w.get("temperature", "—"))}{w.get("temperature_symbol", "°")}', font=font(27), fill=text)
    d.line((38, 250, 295, 250), fill=border, width=2)
    d.text((38, 270), "HUMIDITY", font=font(17, True), fill=text)
    d.text((38, 302), f'{w.get("humidity", "—")}% ', font=font(31), fill=text)
    d.text((160, 270), "WIND", font=font(17, True), fill=text)
    d.text((160, 302), f'{w.get("wind_compass", "—")} {w.get("wind_speed", "—")} {w.get("wind_unit", "")}', font=font(27), fill=text)
    d.text((38, 357), "PRESSURE", font=font(17, True), fill=text)
    d.text((38, 389), f'{w.get("pressure", "—")} hPa', font=font(25), fill=text)
    d.text((190, 357), "VISIBILITY", font=font(17, True), fill=text)
    d.text((190, 389), f'{w.get("visibility", "—")} {w.get("visibility_unit", "")}', font=font(25), fill=text)
    _icon(d, w.get("icon", "partly-cloudy"), (300, 45, 825, 410), w.get("is_night", False), frame, {**c, "icon_style":"premium"})
    _fit(d, w.get("description", ""), (350, 390, 820, 455), 36, text, False)
    d.line((20, 465, 850, 465), fill=border, width=2)
    d.text((38, 486), f'UV {w.get("uv_index", "—")}', font=font(20, True), fill=text)
    d.text((210, 486), f'SUNRISE {w.get("sunrise", "—")}', font=font(20, True), fill=warm)
    # Fit the sunset value into a reserved column so longer localized times
    # cannot run underneath the moon artwork.
    _fit(d, f'SUNSET {w.get("sunset", "—")}', (420, 468, 606, 520), 20, warm, True)
    moon = w.get("moon", {})
    if c.get("show_moon", True):
        # Give the moon a dedicated 42 px cell with clear horizontal spacing
        # from the sunset time and from the phase description.
        _realistic_moon(d, (622, 476, 664, 518), moon.get("label", ""), moon.get("illumination", 50), outline=light_mode)
        _fit(d, str(moon.get("label", "Moon")).upper(), (676, 470, 844, 500), 16, text, True)
        _fit(d, f'{moon.get("illumination", "—")}% LIT', (676, 497, 844, 523), 15, text, False)

    # Top-right information and wind gauge.
    _lcd_panel(d, (870, 10, 1590, 525), 20, border, 3, panel_fill)
    d.text((900, 35), f'⌖ {w.get("location", "")}', font=font(34, True), fill=text)
    d.text((900, 88), stamp.strftime('%A, %B %-d, %Y').upper(), font=font(22), fill=text)
    d.text((1560, 88), stamp.strftime('%-I:%M %p'), font=font(22), fill=text, anchor='ra')
    d.line((885, 125, 1575, 125), fill=border, width=2)
    rows=[
        ("DEW POINT", f'{w.get("dew_point", "—")}{w.get("temperature_symbol", "°")}', text),
        ("PRECIP TODAY", f'{w.get("precipitation", 0)}', water),
        ("PRECIP PROB.", f'{w.get("precip_probability", w.get("daily", [{}])[0].get("precip_probability", "—"))}%', water),
    ]
    for i,(label,value,col) in enumerate(rows):
        y=160+i*82
        d.text((905,y),label,font=font(20,True),fill=text)
        d.text((1185,y),str(value),font=font(25,True),fill=col,anchor='ra')
        d.line((900,y+50,1190,y+50),fill=border,width=1)

    # Keep the section title, numeric AQI, and condition description on
    # clearly separated rows so none of the text can overlap.
    aqi_value = w.get("aqi", "—")
    aqi_label = str(w.get("aqi_label", "Unavailable")).upper()
    d.text((905, 390), "AIR QUALITY", font=font(18, True), fill=text)
    d.text((905, 420), str(aqi_value), font=font(31, True), fill=good)
    _fit(d, aqi_label, (905, 460, 1185, 500), 18, good, False)
    _compass(d,(1210,145,1565,500),w.get("wind_direction",0),f'{w.get("wind_compass","—")} {w.get("wind_speed","—")}',warm)

    # Seven large forecast cards.
    days=w.get("daily",[])[:7]
    gap=10; x0=10; y0=540; cw=(WIDTH-20-gap*6)//7; bottom=1165
    date_style=_resolved_forecast_date_style(c)
    for i,day in enumerate(days):
        x=x0+i*(cw+gap)
        today=i==0 and str(c.get("forecast_first_day_label","today"))=="today"
        card_border=warm if today else border
        _lcd_panel(d,(x,y0,x+cw,bottom),18,card_border,5 if today else 2,panel_fill)
        label=_forecast_day_label(day,i,c)
        d.text((x+cw//2,y0+35),label,font=font(25,True),fill=warm if today else text,anchor='mm')
        date=_forecast_date_text(day,"expanded" if date_style!="off" else "off")
        if date:
            d.text((x+cw//2,y0+72),date,font=font(18),fill=muted,anchor='mm')
        _icon(d,day.get("icon","cloudy"),(x+18,y0+95,x+cw-18,y0+335),False,frame+i,{**c,"icon_style":"premium"},ray_scale=.55)
        _fit(d,day.get("description",""),(x+10,y0+335,x+cw-10,y0+410),23,text,False)
        d.text((x+cw//2-8,y0+455),f'{day.get("high","—")}°',font=font(34,True),fill=warm,anchor='ra')
        d.text((x+cw//2+8,y0+455),f'{day.get("low","—")}°',font=font(34,True),fill=water,anchor='la')
        d.text((x+cw//2,y0+515),f'Rain {day.get("precip_probability","—")}% ',font=font(19),fill=water,anchor='mm')
        d.text((x+cw//2,y0+555),f'Wind {day.get("wind","—")} {w.get("wind_unit","")}',font=font(17),fill=text,anchor='mm')
    if c.get("show_weather_alerts", True) and w.get("alerts"):
        alert=w["alerts"][0]
        d.rounded_rectangle((875, 130, 1195, 220), radius=14, fill=P["red"], outline=border, width=2)
        _fit(d, alert.get("title","WEATHER ALERT").upper(), (890,142,1180,177), 20, P["white"], True)
        _fit(d, alert.get("message",""), (890,178,1180,212), 14, P["white"], False)
    d.text((800,1182),f'LAST UPDATED: {stamp.strftime("%b %-d, %Y %-I:%M %p").upper()} · {appearance.upper()} MODE',font=font(17),fill=text,anchor='ms')
    canonical=quantize_spectra(img,fast=(mode=="lite" and c.get("lite_reduced_dither",True)))
    return adapt_to_profile(canonical,c,fast=(mode=="lite" and c.get("lite_reduced_dither",True)))

def render_weather(w: dict[str,Any], c: dict[str,Any]) -> Image.Image:
    # Auto mode chooses Lite on 512 MB-class boards. Settings can override it.
    mode = c.get("performance_mode", "auto")
    if mode == "auto":
        try:
            from .system import recommended_performance_mode
            mode = recommended_performance_mode()
        except Exception:
            mode = "full"
    if mode == "lite":
        c = c.copy()
        if c.get("lite_disable_animations", True):
            c["animation_frames"] = 1
            c["living_details"] = False
            c["rainbow_effects"] = False
        c["icon_shadows"] = False
        c["icon_highlights"] = False
        c["scene_details"] = False
    img=Image.new("RGB",(WIDTH,HEIGHT),P["white"]); d=ImageDraw.Draw(img)
    theme=THEMES.get(c.get("theme"),THEMES["sunrise"]); primary=P[theme["primary"]]; accent=P[theme["accent"]]; secondary=P[theme["secondary"]]
    if c.get("auto_day_night") and w.get("is_night") and c.get("theme")!="classic": primary=P["blue"]
    frame_count=max(1,int(c.get("animation_frames",4))); stamp=datetime.fromisoformat(w["updated"]); frame=int(stamp.timestamp()//max(60,int(c.get("refresh_minutes",45))*60))%frame_count
    if c.get("layout_preset") == "premium-lcd":
        return _render_premium_lcd(w, c, mode, frame, stamp)
    d.rectangle((0,0,WIDTH,120),fill=primary)
    # Theme-specific trim. The XP-inspired palette gets its familiar blue/green/yellow rhythm,
    # while two-tone and three-tone families receive a clean ink stripe along the header.
    family=theme.get("family", "three-tone")
    if family=="xp":
        d.rectangle((0,102,WIDTH,120),fill=P["green"])
        d.rectangle((0,96,WIDTH,102),fill=P["yellow"])
    elif family=="two-tone":
        d.rectangle((0,108,WIDTH,120),fill=accent)
    else:
        d.rectangle((0,108,WIDTH//2,120),fill=accent)
        d.rectangle((WIDTH//2,108,WIDTH,120),fill=secondary)
    d.text((42,25),c.get("custom_title") or "SpectraDash",font=font(41,True),fill=P["white"] if primary!=P["white"] else P["black"])
    d.text((42,75),w["location"],font=font(24),fill=P["white"])
    updated=stamp.strftime("%a %b %-d · %-I:%M %p")
    d.text((1545,38),updated,font=font(22,True),fill=P["white"],anchor="ra")
    d.text((1545,76),f'{w["description"]} · {w["wind_compass"]} {w["wind_speed"]} {w["wind_unit"]}',font=font(18),fill=P["white"],anchor="ra")
    if c.get("living_scene",True):
        _living_scene(d,w,(30,145,760,535),primary,secondary,frame,c.get("scene_style","landscape"),c)
    else:
        _card(d,(30,145,760,535),26); _icon(d,w["icon"],(55,170,310,410),w.get("is_night",False),frame,c)
        d.text((340,178),f'{w["temperature"]}{w["temperature_symbol"]}',font=font(82,True),fill=primary); d.text((340,282),w["description"],font=font(34,True),fill=P["black"])
    # Compact instrumentation deck.
    sx=785; cw=180; gap=12; ch=92
    metrics=[
        ("Humidity",f'{w["humidity"]}%',secondary,w["humidity"]/100),
        ("Dew point",f'{w["dew_point"]}{w["temperature_symbol"]}',primary,None),
        ("AQI",f'{w["aqi"] if w["aqi"] is not None else "—"} {w["aqi_label"]}',P["green"],(w["aqi"] or 0)/300),
        ("UV index",w["uv_index"] if w["uv_index"] is not None else "—",P["red"],(w["uv_index"] or 0)/12),
        ("Pressure",f'{w["pressure"]} hPa {"↑" if w["pressure_delta"]>1 else "↓" if w["pressure_delta"]<-1 else "→"}',primary,None),
        ("Visibility",f'{w["visibility"]} {w["visibility_unit"]}',secondary,None),
        ("Cloud cover",f'{w["cloud_cover"]}%',P["blue"],w["cloud_cover"]/100),
    ]
    for i,(label,value,col,gauge) in enumerate(metrics):
        row=i//4; coln=i%4; x=sx+coln*(cw+gap); y=145+row*(ch+12); _metric(d,(x,y,x+cw,y+ch),label,value,col,gauge)
    _compass(d,(sx+3*(cw+gap),145+ch+12,sx+4*cw+3*gap,145+2*ch+12),w["wind_direction"],f'{w["wind_compass"]} {w["wind_speed"]}',primary)
    if c.get("show_hourly_graph",True): _hourly_graph(d,w["hourly"],(785,350,1570,535),w["temperature_symbol"],primary,secondary)
    # Solar strip and summary.
    d.rounded_rectangle((30,550,1570,610),radius=18,fill=P["white"],outline=P["black"],width=3)
    d.text((52,580),f'☀  Sunrise {w["sunrise"]}     Sunset {w["sunset"]}',font=font(19,True),fill=P["red"],anchor="lm")
    moon=w.get("moon",{})
    if c.get("show_moon", True):
        _realistic_moon(d,(540,557,588,605),moon.get("label",""),moon.get("illumination",50))
        moon_text=f'{moon.get("label","—")} · {moon.get("illumination","—")}% lit'
        if c.get("show_astronomy_details", True): moon_text += f' · Full {moon.get("next_full_moon","—")}'
        d.text((600,580),moon_text,font=font(18,True),fill=P["blue"],anchor="lm")
    if c.get("show_weather_summary",True): _fit(d,w.get("summary",""),(900,558,1545,603),18,P["black"],False)
    # Seven-day outlook.
    d.text((38,632),"7-DAY OUTLOOK",font=font(24,True),fill=primary)
    if c.get("show_forecast_updated", True):
        d.text((1560,634), f'Forecast updated {stamp.strftime("%b %-d, %-I:%M %p")}', font=font(16,True), fill=P["black"], anchor="ra")
    # A rolling forecast must remain chronological; weekday-start preferences apply to calendar widgets, not forecast cards.
    days=w["daily"][:7]
    date_style = _resolved_forecast_date_style(c)
    gap=10; x0=30; y0=675; cwf=(WIDTH-60-gap*6)//7
    for i,day in enumerate(days):
        x=x0+i*(cwf+gap); _card(d,(x,y0,x+cwf,1165),22)
        is_today_card = i == 0 and str(c.get("forecast_first_day_label", "today")) == "today"
        if is_today_card:
            # A restrained accent outline anchors the rolling forecast without
            # reducing contrast on monochrome or six-color e-paper panels.
            d.rounded_rectangle((x+2,y0+2,x+cwf-2,1163),radius=21,outline=primary,width=5)
        header_h = 76 if date_style == "expanded" else 54
        _top_rounded_rectangle(d,(x+3,y0+3,x+cwf-3,y0+header_h),18,primary)
        day_label = _forecast_day_label(day, i, c)
        if date_style == "expanded":
            d.text((x+cwf//2,y0+24),day_label,font=font(19,True),fill=P["white"],anchor="mm")
            d.text((x+cwf//2,y0+53),_forecast_date_text(day,date_style),font=font(17,True),fill=P["white"],anchor="mm")
        elif date_style == "compact":
            d.text((x+cwf//2,y0+28),f'{day_label} {_forecast_date_text(day,date_style)}',font=font(17,True),fill=P["white"],anchor="mm")
        else:
            d.text((x+cwf//2,y0+28),day_label,font=font(21,True),fill=P["white"],anchor="mm")
        # Forecast precipitation artwork extends below the cloud body. Keep the
        # icon group high enough that rain, snow, and storm elements never collide
        # with the high/low temperature line.
        icon_top = y0 + (46 if date_style == "expanded" else 22)
        _icon(d,day["icon"],(x+23,icon_top,x+cwf-23,icon_top+140),False,frame+i,c,ray_scale=0.55)
        d.text((x+cwf//2,y0+244),f'{day["high"]}° / {day["low"]}°',font=font(27,True),fill=P["red"],anchor="mm")
        d.text((x+cwf//2,y0+294),f'Rain {day["precip_probability"]}%',font=font(19,True),fill=P["blue"],anchor="mm")
        d.text((x+cwf//2,y0+334),f'Wind {day["wind"]} {w["wind_unit"]}',font=font(16),fill=P["black"],anchor="mm")
        d.text((x+cwf//2,y0+372),f'UV {day["uv_max"] if day["uv_max"] is not None else "—"}',font=font(16,True),fill=P["green"],anchor="mm")
        _fit(d,day["description"],(x+10,y0+395,x+cwf-10,y0+472),19,P["black"],False)
    # Plugin widgets are placed using the same 12 x 12 coordinate system as Screen Designer.
    if c.get("designer_enabled"):
        try:
            from .plugins import render_plugin, PLUGIN_ID_PREFIX
            from .system import system_info
            context = {
                "weather": w,
                "config": c,
                "system": system_info(),
                "theme": theme,
                "theme_colors": {"primary": primary, "accent": accent, "secondary": secondary},
                "palette": P.copy(),
            }
            for item in c.get("designer_layout", []):
                widget_id = str(item.get("id", ""))
                if not item.get("enabled", True) or not widget_id.startswith(PLUGIN_ID_PREFIX):
                    continue
                x = max(0, min(11, int(item.get("x", 0))))
                y = max(0, min(11, int(item.get("y", 0))))
                width = max(2, min(12 - x, int(item.get("w", 4))))
                height = max(2, min(12 - y, int(item.get("h", 3))))
                margin = 10
                box = (
                    int(x * WIDTH / 12) + margin,
                    int(y * HEIGHT / 12) + margin,
                    int((x + width) * WIDTH / 12) - margin,
                    int((y + height) * HEIGHT / 12) - margin,
                )
                render_plugin(widget_id, img, box, context)
        except Exception:
            pass
    canonical = quantize_spectra(img, fast=(mode == "lite" and c.get("lite_reduced_dither", True)))
    return adapt_to_profile(canonical, c, fast=(mode == "lite" and c.get("lite_reduced_dither", True)))


def adapt_to_profile(image: Image.Image, config: dict[str, Any], fast: bool = False) -> Image.Image:
    """Scale the canonical 1600x1200 composition to a display profile.

    The 12x12 designer grid remains resolution independent. Experimental profiles
    deliberately use a conservative whole-screen scale so contributors can test
    driver wiring before profile-specific layout refinements are accepted.
    """
    from .display_profiles import get_profile
    profile = get_profile(config.get("display_profile"))
    out = image.convert("RGB")
    if out.size != profile.size:
        out = out.resize(profile.size, Image.Resampling.LANCZOS)
    return quantize_for_colors(out, profile.colors, fast=fast)


def quantize_for_colors(image: Image.Image, colors, fast: bool = False) -> Image.Image:
    names = tuple(colors)
    if names == ("black", "white"):
        dither = Image.Dither.NONE if fast else Image.Dither.FLOYDSTEINBERG
        return image.convert("L").convert("1", dither=dither).convert("RGB")
    pal = Image.new("P", (1, 1)); flat=[]
    for name in names:
        flat.extend(P.get(name, (255,255,255)))
    flat.extend([0,0,0] * (256-len(names))); pal.putpalette(flat)
    dither = Image.Dither.NONE if fast else Image.Dither.FLOYDSTEINBERG
    return image.convert("RGB").quantize(palette=pal, dither=dither).convert("RGB")


def quantize_spectra(image:Image.Image, fast:bool=False)->Image.Image:
    pal=Image.new("P",(1,1)); flat=[]
    for k in ("black","white","yellow","red","blue","green"): flat.extend(P[k])
    flat.extend([0,0,0]*(256-6)); pal.putpalette(flat)
    dither = Image.Dither.NONE if fast else Image.Dither.FLOYDSTEINBERG
    return image.convert("RGB").quantize(palette=pal,dither=dither).convert("RGB")


def rotate_for_panel(image:Image.Image,rotation:int)->Image.Image:
    rotation=int(rotation)%360
    if rotation not in {0,90,180,270}: rotation=0
    return image.convert("RGB").rotate(-rotation, expand=True)

def render_error(message:str,config:dict[str,Any])->Image.Image:
    img=Image.new("RGB",(WIDTH,HEIGHT),P["white"]); d=ImageDraw.Draw(img)
    d.rectangle((0,0,WIDTH,130),fill=P["red"]); d.text((55,37),"SpectraDash needs attention",font=font(48,True),fill=P["white"])
    _fit(d,message,(70,220,1530,800),62,P["black"],True)
    d.text((800,1010),"Open the local web dashboard for diagnostics.",font=font(30),fill=P["blue"],anchor="mm")
    return adapt_to_profile(quantize_spectra(img), config)
