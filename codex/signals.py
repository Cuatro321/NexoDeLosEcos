# codex/signals.py
from __future__ import annotations

from typing import Any, Dict, List

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import (
    Asset,
    Domain,
    Artifact,     # Emblemas
    Character,
    Enemy,
    Guide,
    LoreEntry,    # Historias
    Trap,
)

import firebase_admin
from firebase_admin import credentials, firestore

# ─────────────────────────────────────────────────────────────
# Inicializar Firebase Admin UNA sola vez
# ─────────────────────────────────────────────────────────────
if not firebase_admin._apps:
    cred_path = settings.FIREBASE_SERVICE_ACCOUNT
    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(cred, {
        "projectId": settings.FIREBASE_PROJECT_ID,
    })

db = firestore.client()


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def abs_media_url(file_field) -> str:
    """
    Devuelve URL absoluta para un FileField/ImageField.
    Si ya es http(s), la deja igual.
    """
    if not file_field:
        return ""
    url = file_field.url  # normalmente /media/...
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return settings.SITE_URL + url


# ─────────────────────────────────────────────────────────────
# Assets
# ─────────────────────────────────────────────────────────────
def asset_to_dict(instance: Asset) -> Dict[str, Any]:
    return {
        "id": instance.pk,
        "kind": instance.kind,
        "caption": instance.caption,
        "fileUrl": abs_media_url(getattr(instance, "file", None)),
    }


@receiver(post_save, sender=Asset)
def sync_asset_to_firestore(sender, instance: Asset, **kwargs):
    data = asset_to_dict(instance)
    db.collection("assets").document(str(instance.pk)).set(data)


@receiver(post_delete, sender=Asset)
def delete_asset_from_firestore(sender, instance: Asset, **kwargs):
    db.collection("assets").document(str(instance.pk)).delete()


# ─────────────────────────────────────────────────────────────
# Domains
# ─────────────────────────────────────────────────────────────
def domain_to_dict(instance: Domain) -> Dict[str, Any]:
    return {
        "name": instance.name,
        "slug": instance.slug,
        "shortDescription": getattr(instance, "short_description", ""),
        "coverImageUrl": abs_media_url(getattr(instance, "cover_image", None)),
        "bannerImageUrl": abs_media_url(getattr(instance, "banner_image", None)),
        "color": getattr(instance, "color", ""),
        "icon": getattr(instance, "icon", ""),
        "videoUrl": getattr(instance, "video_url", ""),
        "order": getattr(instance, "order", 0),
    }


@receiver(post_save, sender=Domain)
def sync_domain_to_firestore(sender, instance: Domain, **kwargs):
    data = domain_to_dict(instance)
    db.collection("domains").document(instance.slug).set(data)


@receiver(post_delete, sender=Domain)
def delete_domain_from_firestore(sender, instance: Domain, **kwargs):
    db.collection("domains").document(instance.slug).delete()


# ─────────────────────────────────────────────────────────────
# Emblemas (Artifact)
# ─────────────────────────────────────────────────────────────
def emblem_to_dict(instance: Artifact) -> Dict[str, Any]:
    return {
        "name": instance.name,
        "slug": instance.slug,
        "domainId": instance.domain.slug if getattr(instance, "domain", None) else None,
        "quote": getattr(instance, "quote", ""),
        "rarity": getattr(instance, "rarity", ""),
        "usage": getattr(instance, "usage", ""),
        "epoch": getattr(instance, "epoch", ""),
        "description": getattr(instance, "description", ""),
        "imageUrl": abs_media_url(getattr(instance, "image", None)),
        "gifUrl": abs_media_url(getattr(instance, "gif", None)),
        "videoUrl": getattr(instance, "video_url", ""),
    }


@receiver(post_save, sender=Artifact)
def sync_emblem_to_firestore(sender, instance: Artifact, **kwargs):
    data = emblem_to_dict(instance)
    db.collection("emblems").document(instance.slug).set(data)


@receiver(post_delete, sender=Artifact)
def delete_emblem_from_firestore(sender, instance: Artifact, **kwargs):
    db.collection("emblems").document(instance.slug).delete()


# ─────────────────────────────────────────────────────────────
# Personajes (Character)
# ─────────────────────────────────────────────────────────────
def character_to_dict(instance: Character) -> Dict[str, Any]:
    return {
        "name": instance.name,
        "slug": instance.slug,
        "role": getattr(instance, "role", ""),
        "domainId": instance.domain.slug if getattr(instance, "domain", None) else None,
        "description": getattr(instance, "description", ""),
        "playable": getattr(instance, "playable", False),
        "imageUrl": abs_media_url(getattr(instance, "sprite_still", None)),
        "gifUrl": abs_media_url(getattr(instance, "sprite_gif", None)),
    }


@receiver(post_save, sender=Character)
def sync_character_to_firestore(sender, instance: Character, **kwargs):
    data = character_to_dict(instance)
    db.collection("characters").document(instance.slug).set(data)


@receiver(post_delete, sender=Character)
def delete_character_from_firestore(sender, instance: Character, **kwargs):
    db.collection("characters").document(instance.slug).delete()


# ─────────────────────────────────────────────────────────────
# Enemigos (Enemy)
# ─────────────────────────────────────────────────────────────
def enemy_to_dict(instance: Enemy) -> Dict[str, Any]:
    return {
        "name": instance.name,
        "slug": instance.slug,
        "domainId": instance.domain.slug if getattr(instance, "domain", None) else None,
        "description": getattr(instance, "description", ""),
        "behavior": getattr(instance, "behavior", ""),
        "spriteStillUrl": abs_media_url(getattr(instance, "sprite_still", None)),
        "spriteGifUrl": abs_media_url(getattr(instance, "sprite_gif", None)),
        "imageFullUrl": abs_media_url(getattr(instance, "image_full", None)),
        "videoUrl": getattr(instance, "video_url", ""),
    }


@receiver(post_save, sender=Enemy)
def sync_enemy_to_firestore(sender, instance: Enemy, **kwargs):
    data = enemy_to_dict(instance)
    db.collection("enemies").document(instance.slug).set(data)


@receiver(post_delete, sender=Enemy)
def delete_enemy_from_firestore(sender, instance: Enemy, **kwargs):
    db.collection("enemies").document(instance.slug).delete()


# ─────────────────────────────────────────────────────────────
# Guías (Guide)
# ─────────────────────────────────────────────────────────────
def guide_to_dict(instance: Guide) -> Dict[str, Any]:
    def slugs(qs) -> List[str]:
        return [obj.slug for obj in qs.all()]

    return {
        "title": instance.title,
        "slug": instance.slug,
        "summary": getattr(instance, "summary", ""),
        "body": getattr(instance, "body", ""),
        "domainId": instance.domain.slug if getattr(instance, "domain", None) else None,
        "relatedArtifacts": slugs(getattr(instance, "related_artifacts", [])),
        "relatedCharacters": slugs(getattr(instance, "related_characters", [])),
        "relatedEnemies": slugs(getattr(instance, "related_enemies", [])),
        "tags": getattr(instance, "tags", ""),
        "coverImageUrl": abs_media_url(getattr(instance, "cover_image", None)),
        "readTime": getattr(instance, "read_time", 0),
    }


@receiver(post_save, sender=Guide)
def sync_guide_to_firestore(sender, instance: Guide, **kwargs):
    data = guide_to_dict(instance)
    db.collection("guides").document(instance.slug).set(data)


@receiver(post_delete, sender=Guide)
def delete_guide_from_firestore(sender, instance: Guide, **kwargs):
    db.collection("guides").document(instance.slug).delete()


# ─────────────────────────────────────────────────────────────
# Historias (LoreEntry)
# ─────────────────────────────────────────────────────────────
def loreentry_to_dict(instance: LoreEntry) -> Dict[str, Any]:
    gallery_ids = (
        [str(a.pk) for a in instance.gallery.all()]
        if hasattr(instance, "gallery")
        else []
    )

    return {
        "title": instance.title,
        "slug": instance.slug,
        "summary": getattr(instance, "summary", ""),
        "body": getattr(instance, "body", ""),
        "domainId": instance.domain.slug if getattr(instance, "domain", None) else None,
        "coverImageUrl": abs_media_url(getattr(instance, "cover_image", None)),
        "videoUrl": getattr(instance, "video_url", ""),
        "galleryAssetIds": gallery_ids,
    }


@receiver(post_save, sender=LoreEntry)
def sync_loreentry_to_firestore(sender, instance: LoreEntry, **kwargs):
    data = loreentry_to_dict(instance)
    db.collection("stories").document(instance.slug).set(data)


@receiver(post_delete, sender=LoreEntry)
def delete_loreentry_from_firestore(sender, instance: LoreEntry, **kwargs):
    db.collection("stories").document(instance.slug).delete()


# ─────────────────────────────────────────────────────────────
# Trampas (Trap) – SIN slug obligatorio
# ─────────────────────────────────────────────────────────────
def trap_to_dict(instance: Trap) -> Dict[str, Any]:
  # Trap en tu modelo solo tiene: domain, title, description, image, gif
    slug_value = getattr(instance, "slug", "")  # por si algún día le agregas slug

    return {
        "title": instance.title,
        "slug": slug_value,
        "domainId": instance.domain.slug if getattr(instance, "domain", None) else None,
        "description": getattr(instance, "description", ""),
        "imageUrl": abs_media_url(getattr(instance, "image", None)),
        "gifUrl": abs_media_url(getattr(instance, "gif", None)),
    }


@receiver(post_save, sender=Trap)
def sync_trap_to_firestore(sender, instance: Trap, **kwargs):
    data = trap_to_dict(instance)
    # Si NO hay slug en el modelo, usamos el ID de la trampa como documentId
    doc_id = data.get("slug") or str(instance.pk)
    db.collection("traps").document(doc_id).set(data)


@receiver(post_delete, sender=Trap)
def delete_trap_from_firestore(sender, instance: Trap, **kwargs):
    doc_id = getattr(instance, "slug", None) or str(instance.pk)
    db.collection("traps").document(doc_id).delete()
    