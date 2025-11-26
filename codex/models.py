# codex/models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify  # (puedes quitar si no lo usas)
import time

# ---------- Helpers de rutas (nombres estables) ----------
def _ts() -> int:
    return int(time.time())

# Compat (por migraciones antiguas): no lo uses nuevo, pero déjalo para que no falle.
def upload_codex(instance, filename):
    return f'codex/legacy/{_ts()}_{filename}'

def upload_domain_cover(instance, filename):
    return f'codex/domains/{instance.slug}/cover_{_ts()}_{filename}'

def upload_domain_banner(instance, filename):
    return f'codex/domains/{instance.slug}/banner_{_ts()}_{filename}'

def upload_asset_file(instance, filename):
    kind = getattr(instance, "kind", "misc")
    return f'codex/assets/{kind}/{_ts()}_{filename}'

def upload_artifact_media(instance, filename):
    slug = getattr(instance, "slug", "artifact")
    return f'codex/artifacts/{slug}/{_ts()}_{filename}'

def upload_character_image(instance, filename):
    slug = getattr(instance, "slug", "character")
    return f'codex/characters/{slug}/{_ts()}_{filename}'

def upload_enemy_image(instance, filename):
    slug = getattr(instance, "slug", "enemy")
    return f'codex/enemies/{slug}/{_ts()}_{filename}'

def upload_character_media(instance, filename):
    # Para CharacterAnimation
    try:
        slug = instance.character.slug
    except Exception:
        slug = "character"
    return f'codex/characters/{slug}/{_ts()}_{filename}'

def upload_enemy_media(instance, filename):
    # Para EnemyAnimation
    try:
        slug = instance.enemy.slug
    except Exception:
        slug = "enemy"
    return f'codex/enemies/{slug}/{_ts()}_{filename}'

def upload_trap_image(instance, filename):
    # Trampas por dominio
    try:
        dslug = instance.domain.slug
    except Exception:
        dslug = "domain"
    return f'codex/traps/{dslug}/{_ts()}_{filename}'


# ---------- Dominio ----------
class Domain(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    short_description = models.TextField(blank=True, default="")
    cover_image = models.ImageField(upload_to="codex/domains/", blank=True, null=True)
    banner_image = models.ImageField(upload_to="codex/domains/", blank=True, null=True)
    color = models.CharField(max_length=32, blank=True, default="")      # #hex o var(--*)
    icon = models.CharField(max_length=120, blank=True, default="")       # ej. fa-solid fa-hourglass-half
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("codex:domain_detail", args=[self.slug])


# ---------- Asset genérico (galerías) ----------
class Asset(models.Model):
    KIND_CHOICES = (
        ('image', 'Imagen'),
        ('gif', 'GIF'),
        ('video', 'Video'),
    )
    file = models.FileField(upload_to=upload_asset_file)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default='image')
    caption = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return f'{self.get_kind_display()} - {self.caption or self.file.name}'


# ---------- Historias / Lore ----------
class LoreEntry(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    summary = models.TextField(blank=True)
    body = models.TextField()
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True, blank=True, related_name='lore')
    cover_image = models.ImageField(upload_to=upload_asset_file, blank=True, null=True)
    video_url = models.URLField(blank=True)
    gallery = models.ManyToManyField(Asset, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Historia"
        verbose_name_plural = "Historias"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('codex:lore_detail', args=[self.slug])


# ---------- Artefactos (mostrados como Emblemas en el admin) ----------
class Artifact(models.Model):
    RARITY = (
        ('comun', 'Común'),
        ('raro', 'Raro'),
        ('epico', 'Épico'),
        ('mitico', 'Mítico'),
    )

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=160, unique=True)
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True, blank=True, related_name='artifacts')
    quote = models.CharField(max_length=200, blank=True, help_text='Eco / frase')
    rarity = models.CharField(max_length=10, choices=RARITY, default='raro')
    bearer = models.CharField(max_length=120, blank=True, help_text='Portador')
    epoch = models.CharField(max_length=120, blank=True, help_text='Época')
    description = models.TextField(blank=True)
    usage = models.TextField(blank=True, help_text='Sugerencias de uso / ventajas')
    image = models.ImageField(upload_to=upload_artifact_media, blank=True, null=True)
    gif = models.FileField(upload_to=upload_artifact_media, blank=True, null=True)
    video_url = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Emblema"
        verbose_name_plural = "Emblemas"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('codex:artifact_detail', args=[self.slug])


# ---------- Personajes ----------
class Character(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=160, unique=True)
    role = models.CharField(max_length=120, blank=True, help_text='Clase / rol')
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True, blank=True, related_name='characters')
    description = models.TextField(blank=True)
    playable = models.BooleanField(default=False)

    sprite_still = models.ImageField(upload_to=upload_character_image, blank=True, null=True, help_text='Sprite estático')
    sprite_gif = models.FileField(upload_to=upload_character_image, blank=True, null=True, help_text='Animación principal (GIF)')
    sprite_sheet = models.ImageField(upload_to=upload_character_image, blank=True, null=True, help_text='Sprite sheet (opcional)')
    sprite_meta = models.JSONField(blank=True, null=True, help_text='{"frame_w":32,"frame_h":32,"fps":12} (opcional)')

    video_url = models.URLField(blank=True)
    image_full = models.ImageField(upload_to=upload_character_image, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Personaje"
        verbose_name_plural = "Personajes"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('codex:character_detail', args=[self.slug])


class CharacterAnimation(models.Model):
    character = models.ForeignKey(Character, related_name='animations', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    gif = models.FileField(upload_to=upload_character_media, blank=True, null=True)
    mp4 = models.FileField(upload_to=upload_character_media, blank=True, null=True)
    webm = models.FileField(upload_to=upload_character_media, blank=True, null=True)
    sprite_sheet = models.ImageField(upload_to=upload_character_media, blank=True, null=True)
    sprite_meta = models.JSONField(blank=True, null=True, help_text='{"frame_w":32,"frame_h":32,"fps":12}')
    loop = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Animación de personaje"
        verbose_name_plural = "Animaciones de personaje"

    def __str__(self):
        return f'{self.character.name} · {self.name}'


# ---------- Enemigos ----------
class Enemy(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=160, unique=True)
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True, blank=True, related_name='enemies')
    description = models.TextField(blank=True)
    behavior = models.TextField(blank=True, help_text='Comportamiento / ataques')

    sprite_still = models.ImageField(upload_to=upload_enemy_image, blank=True, null=True)
    sprite_gif = models.FileField(upload_to=upload_enemy_image, blank=True, null=True)
    image_full = models.ImageField(upload_to=upload_enemy_image, blank=True, null=True)

    video_url = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Enemigo"
        verbose_name_plural = "Enemigos"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('codex:enemy_detail', args=[self.slug])


class EnemyAnimation(models.Model):
    enemy = models.ForeignKey(Enemy, related_name='animations', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    gif = models.FileField(upload_to=upload_enemy_media, blank=True, null=True)
    mp4 = models.FileField(upload_to=upload_enemy_media, blank=True, null=True)
    webm = models.FileField(upload_to=upload_enemy_media, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    loop = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Animación de enemigo"
        verbose_name_plural = "Animaciones de enemigo"

    def __str__(self):
        return f'{self.enemy.name} · {self.name}'


# ---------- Trampas por dominio ----------
class Trap(models.Model):
    domain = models.ForeignKey(Domain, related_name='traps', on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=upload_trap_image, blank=True, null=True)
    gif = models.FileField(upload_to=upload_trap_image, blank=True, null=True)

    class Meta:
        ordering = ['domain__name', 'title']
        verbose_name = "Trampa"
        verbose_name_plural = "Trampas"

    def __str__(self):
        return f'{self.domain.name} · {self.title}'


# ---------- Guías ----------
class Guide(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)  # <-- corregido: max_length
    summary = models.TextField(blank=True)
    body = models.TextField()

    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True, blank=True, related_name='guides')
    related_artifacts = models.ManyToManyField(Artifact, blank=True)
    related_characters = models.ManyToManyField(Character, blank=True)
    related_enemies = models.ManyToManyField(Enemy, blank=True)

    tags = models.CharField(max_length=200, blank=True, help_text='comas: movilidad,combate,secretos')
    cover_image = models.ImageField(upload_to=upload_asset_file, blank=True, null=True)
    read_time = models.PositiveIntegerField(default=4, help_text='Minutos estimados')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)  # <-- NUEVO

    class Meta:
        ordering = ['-updated', '-created', 'title']
        verbose_name = "Guía"
        verbose_name_plural = "Guías"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('codex:guide_detail', args=[self.slug])
