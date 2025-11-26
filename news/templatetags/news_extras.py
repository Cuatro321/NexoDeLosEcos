from django import template
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_embed(url: str) -> str:
    """
    Convierte URLs de YouTube a formato embebido.
    Acepta:
      - https://www.youtube.com/watch?v=ID
      - https://youtu.be/ID
      - https://www.youtube.com/shorts/ID
      - https://www.youtube.com/embed/ID
    Devuelve https://www.youtube-nocookie.com/embed/ID?rel=0[&start=SEG]
    """
    if not url:
        return ""
    try:
        u = urlparse(url)
        host = u.netloc.lower()
        path = u.path
        qs = parse_qs(u.query)
        vid = ""

        if "youtu.be" in host:
            # /VIDEO_ID
            vid = path.lstrip("/")
        elif "youtube.com" in host:
            if path.startswith("/watch"):
                vid = qs.get("v", [""])[0]
            elif path.startswith("/shorts/"):
                # /shorts/VIDEO_ID
                vid = path.split("/shorts/")[1].split("/")[0]
            elif path.startswith("/embed/"):
                vid = path.split("/embed/")[1].split("/")[0]

        if not vid:
            return ""

        # Soporte básico para ?t=segundos
        start_param = ""
        t = qs.get("t", [""])[0]
        if t.isdigit():
            start_param = f"&start={t}"

        return f"https://www.youtube-nocookie.com/embed/{vid}?rel=0{start_param}"
    except Exception:
        return ""

@register.filter
def is_http_video(url: str) -> bool:
    """Detecta enlaces directos a video (mp4/webm/ogg)."""
    if not url:
        return False
    low = url.lower()
    return low.endswith(".mp4") or low.endswith(".webm") or low.endswith(".ogg")
