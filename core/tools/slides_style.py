#!/mnt/workspace/.venv/bin/python3
# slides_style.py — CSS helpers: colors, gradients, rotation, geometry, download

import math, pathlib, urllib.request

_THEME = {
    "DARK1": (0,0,0), "DARK2": (32,18,77), "TEXT1": (0,0,0), "TEXT2": (32,18,77),
    "LIGHT1": (255,255,255), "LIGHT2": (232,232,232),
    "BACKGROUND1": (255,255,255), "BACKGROUND2": (232,232,232),
    "ACCENT1": (103,78,167), "ACCENT2": (213,166,189), "ACCENT3": (100,180,100),
    "ACCENT4": (200,150,50), "ACCENT5": (50,150,200), "ACCENT6": (200,100,50),
}


def _rgb(color: dict, alpha: float = 1.0) -> str | None:
    rgb = color.get("rgbColor", {})
    if rgb:
        r, g, b = (round(rgb.get(k, 0) * 255) for k in ("red", "green", "blue"))
    else:
        tc = color.get("themeColor", "")
        if tc not in _THEME:
            return None
        r, g, b = _THEME[tc]
    return f"rgba({r},{g},{b},{alpha:.2f})" if alpha < 1 else f"rgb({r},{g},{b})"


def _fill_color(solid_fill: dict) -> str | None:
    return _rgb(solid_fill.get("color", {}), solid_fill.get("alpha", 1.0))


def _gradient_css(gradient: dict) -> str | None:
    stops = gradient.get("gradientStops", [])
    if not stops:
        return None
    css_angle = (90 - gradient.get("angle", 0)) % 360
    parts = [f"{(_rgb(s.get('color',{}), s.get('alpha',1.0)) or 'transparent')} {round(s.get('position',0)*100)}%"
             for s in stops]
    return f"linear-gradient({css_angle:.0f}deg, {', '.join(parts)})"


def rotation_deg(transform: dict) -> float:
    return math.degrees(math.atan2(transform.get("shearY", 0) or 0,
                                   transform.get("scaleX", 1.0) or 1.0))


def eff_scale(transform: dict) -> tuple[float, float]:
    sx,  sy  = transform.get("scaleX", 1.0) or 1.0, transform.get("scaleY", 1.0) or 1.0
    shx, shy = transform.get("shearX", 0)   or 0,   transform.get("shearY", 0)   or 0
    return math.sqrt(sx*sx + shy*shy), math.sqrt(sy*sy + shx*shx)


def compose_transforms(pt: dict, ct: dict) -> dict:
    psx,psy   = pt.get("scaleX",1.0) or 1.0, pt.get("scaleY",1.0) or 1.0
    pshx,pshy = pt.get("shearX",0)   or 0,   pt.get("shearY",0)   or 0
    ptx, pty  = pt.get("translateX",0) or 0,  pt.get("translateY",0) or 0
    csx,csy   = ct.get("scaleX",1.0) or 1.0, ct.get("scaleY",1.0) or 1.0
    cshx,cshy = ct.get("shearX",0)   or 0,   ct.get("shearY",0)   or 0
    ctx, cty  = ct.get("translateX",0) or 0,  ct.get("translateY",0) or 0
    return {
        "scaleX": psx*csx + pshx*cshy,   "shearX": psx*cshx + pshx*csy,
        "shearY": pshy*csx + psy*cshy,   "scaleY": pshy*cshx + psy*csy,
        "translateX": psx*ctx + pshx*cty + ptx,
        "translateY": pshy*ctx + psy*cty + pty, "unit": "EMU",
    }


def _bounds(el: dict, slide_w: float, slide_h: float) -> tuple[float, float, float, float]:
    t        = el.get("transform", {})
    s        = el.get("size", {})
    tx, ty   = t.get("translateX", 0) or 0, t.get("translateY", 0) or 0
    esx, esy = eff_scale(t)
    return (
        round(tx / slide_w * 100, 2),
        round(ty / slide_h * 100, 2),
        round(s.get("width",  {}).get("magnitude", 0) * esx / slide_w * 100, 2),
        round(s.get("height", {}).get("magnitude", 0) * esy / slide_h * 100, 2),
    )


def _download(url: str, dest_base: pathlib.Path) -> pathlib.Path | None:
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            ct  = r.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()
            ext = {"image/jpeg":"jpg","image/png":"png","image/gif":"gif","image/webp":"webp"}.get(ct,"jpg")
            dest = dest_base.with_suffix(f".{ext}")
            dest.write_bytes(r.read())
            return dest
    except Exception:
        return None
