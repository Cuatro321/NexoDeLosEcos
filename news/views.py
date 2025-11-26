# news/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from urllib.parse import urlparse, parse_qs

from .models import NewsArticle, Category, Tag


def _youtube_embed(url: str) -> str | None:
    """
    Convierte un enlace de YouTube normal a un enlace embebible.
    Soporta:
      - https://www.youtube.com/watch?v=VIDEO_ID&...
      - https://youtu.be/VIDEO_ID?...
    Devuelve None si no es YouTube.
    """
    if not url:
        return None
    u = urlparse(url)
    host = (u.netloc or "").lower()
    if "youtu.be" in host:
        vid = u.path.strip("/").split("/")[0]
        return f"https://www.youtube.com/embed/{vid}" if vid else None
    if "youtube.com" in host:
        qs = parse_qs(u.query or "")
        vid = (qs.get("v") or [None])[0]
        return f"https://www.youtube.com/embed/{vid}" if vid else None
    return None


def news_index(request):
    qs = NewsArticle.objects.select_related("category", "author") \
                            .prefetch_related("tags") \
                            .filter(Q(status="published") |
                                    (Q(status="scheduled") & Q(publish_at__lte=timezone.now()))) \
                            .order_by("-pin_home", "-publish_at", "-created")

    cat_slug = request.GET.get("categoria")
    tag_slug = request.GET.get("tag")
    q = request.GET.get("q")

    if cat_slug:
        qs = qs.filter(category__slug=cat_slug)
    if tag_slug:
        qs = qs.filter(tags__slug=tag_slug)
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(body__icontains=q))

    p = Paginator(qs, 9).get_page(request.GET.get("page"))

    ctx = {
        "page_obj": p,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "current_category": cat_slug,
        "current_tag": tag_slug,
        "search_q": q or "",
        "pin": NewsArticle.objects.filter(pin_home=True, status="published").order_by("-publish_at", "-created")[:3],
        "patch": NewsArticle.objects.filter(is_patch_notes=True, status="published").order_by("-publish_at", "-created")[:5],
    }
    return render(request, "news/index.html", ctx)


def news_detail(request, slug):
    item = get_object_or_404(NewsArticle, slug=slug)
    related = NewsArticle.objects.filter(status="published").exclude(pk=item.pk) \
                                 .filter(Q(category=item.category) | Q(tags__in=item.tags.all())) \
                                 .distinct().order_by("-publish_at", "-created")[:6]

    embed_url = _youtube_embed(item.video_url)

    return render(request, "news/detail.html", {
        "item": item,
        "related": related,
        "embed_url": embed_url,   # <- lo usamos en la plantilla
    })


def patch_notes(request):
    qs = NewsArticle.objects.filter(is_patch_notes=True, status="published").order_by("-publish_at", "-created")
    p = Paginator(qs, 12).get_page(request.GET.get("page"))
    return render(request, "news/patch_notes.html", {"page_obj": p})
