# codex/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Domain, LoreEntry, Character, Enemy, Artifact, Guide


def codex_index(request):
    ctx = {
        "domains": Domain.objects.all(),
        "latest_lore": LoreEntry.objects.select_related("domain").order_by("-id")[:3],
        "latest_characters": Character.objects.select_related("domain").order_by("-id")[:4],
        "latest_enemies": Enemy.objects.select_related("domain").order_by("-id")[:4],
        "latest_guides": Guide.objects.select_related("domain").order_by("-id")[:3],
        "latest_artifacts": Artifact.objects.select_related("domain").order_by("-id")[:5],
    }
    return render(request, "codex/index.html", ctx)


# ----- Historias -----
def lore_index(request):
    qs = LoreEntry.objects.select_related("domain").order_by("title")
    page_obj = Paginator(qs, 12).get_page(request.GET.get("page"))
    return render(request, "codex/lore_index.html", {"page_obj": page_obj})


def lore_detail(request, slug):
    # Traemos también la galería para no hacer consultas extra
    item = get_object_or_404(
        LoreEntry.objects.select_related("domain").prefetch_related("gallery"),
        slug=slug,
    )

    # Galería completa (puede venir vacía)
    gallery = list(item.gallery.all())

    # Asset destacado: la primera imagen o gif (no video)
    hero_asset = None
    for a in gallery:
        kind = (getattr(a, "kind", "") or "").lower()
        # Ajusta estos valores a los que tengas en tus choices
        if kind in ("imagen", "image", "gif"):
            hero_asset = a
            break

    ctx = {
        "item": item,
        "gallery": gallery,
        "hero_asset": hero_asset,
    }
    return render(request, "codex/lore_detail.html", ctx)


# ----- Personajes -----
def characters_index(request):
    qs = Character.objects.select_related("domain").order_by("name")
    page_obj = Paginator(qs, 18).get_page(request.GET.get("page"))
    return render(request, "codex/characters_index.html", {"page_obj": page_obj})


def character_detail(request, slug):
    item = get_object_or_404(Character.objects.select_related("domain"), slug=slug)
    return render(request, "codex/character_detail.html", {"item": item})


# ----- Enemigos -----
def enemies_index(request):
    qs = Enemy.objects.select_related("domain").order_by("name")
    page_obj = Paginator(qs, 18).get_page(request.GET.get("page"))
    return render(request, "codex/enemies_index.html", {"page_obj": page_obj})


def enemy_detail(request, slug):
    item = get_object_or_404(Enemy.objects.select_related("domain"), slug=slug)
    return render(request, "codex/enemy_detail.html", {"item": item})


# ----- Dominios -----
def domains_index(request):
    items = Domain.objects.order_by("order", "name")
    return render(request, "codex/domains_index.html", {"items": items})


def domain_detail(request, slug):
    d = get_object_or_404(Domain, slug=slug)
    ctx = {
        "item": d,
        "lore": d.lore.all(),
        "characters": d.characters.all(),
        "enemies": d.enemies.all(),
        "artifacts": d.artifacts.all(),
        "traps": d.traps.all(),
        "guides": d.guides.all(),
    }
    return render(request, "codex/domain_detail.html", ctx)


# ----- Artefactos -----
def artifacts_index(request):
    qs = Artifact.objects.select_related("domain").order_by("name")
    page_obj = Paginator(qs, 18).get_page(request.GET.get("page"))
    return render(request, "codex/artifacts_index.html", {"page_obj": page_obj})


def artifact_detail(request, slug):
    item = get_object_or_404(Artifact.objects.select_related("domain"), slug=slug)
    return render(request, "codex/artifact_detail.html", {"item": item})


# ----- Guías -----
def guides_index(request):
    # Ahora existe 'updated' en Guide; se puede ordenar por última edición y creación.
    qs = Guide.objects.select_related("domain").order_by("-updated", "-created", "title")
    page_obj = Paginator(qs, 12).get_page(request.GET.get("page"))
    return render(request, "codex/guides_index.html", {"page_obj": page_obj})


def guide_detail(request, slug):
    item = get_object_or_404(Guide.objects.select_related("domain"), slug=slug)
    return render(request, "codex/guide_detail.html", {"item": item})
