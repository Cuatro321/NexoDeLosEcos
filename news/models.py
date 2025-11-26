# news/models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from codex.models import Asset  # reutilizamos las galerías del códex
import time

User = get_user_model()

def _ts() -> int:
    return int(time.time())

def upload_news_media(instance, filename):
    slug = getattr(instance, "slug", None)
    if not slug and hasattr(instance, "article") and instance.article:
        slug = instance.article.slug
    slug = slug or "news"
    return f'news/{slug}/{_ts()}_{filename}'


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    color = models.CharField(max_length=32, blank=True, default="", help_text="CSS var o #hex")
    icon = models.CharField(max_length=120, blank=True, default="", help_text="fa-solid fa-bolt")

    class Meta:
        ordering = ["name"]
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("news:index") + f"?categoria={self.slug}"


class Tag(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("news:index") + f"?tag={self.slug}"


class NewsArticle(models.Model):
    STATUS = (
        ("draft", "Borrador"),
        ("scheduled", "Programado"),
        ("published", "Publicado"),
    )

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    summary = models.TextField(blank=True, default="")
    body = models.TextField(help_text="Contenido (puedes usar HTML simple)")

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="news")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles")
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")

    hero_image = models.ImageField(upload_to=upload_news_media, blank=True, null=True)
    banner_image = models.ImageField(upload_to=upload_news_media, blank=True, null=True)
    video_url = models.URLField(blank=True, default="", help_text="YouTube, Vimeo o .mp4/.webm directo")
    gallery = models.ManyToManyField(Asset, blank=True, related_name="news_articles")

    status = models.CharField(max_length=10, choices=STATUS, default="draft")
    publish_at = models.DateTimeField(blank=True, null=True, help_text="Si se programa, se publicará a esta hora")
    pin_home = models.BooleanField(default=False, help_text="Destacar en portada de noticias")
    is_patch_notes = models.BooleanField(default=False, help_text="Marcar como 'Notas del parche'")
    version = models.CharField(max_length=40, blank=True, default="", help_text="v1.2.0 (opcional)")
    reading_time = models.PositiveIntegerField(default=4, help_text="Minutos estimados")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publish_at", "-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.title or "nota"
            self.slug = slugify(base)[:175]
        super().save(*args, **kwargs)
