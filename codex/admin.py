# codex/admin.py
from django.contrib import admin
from .models import (
    Domain, LoreEntry, Artifact, Character, CharacterAnimation,
    Enemy, EnemyAnimation, Trap, Guide, Asset
)

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "color", "icon")
    list_editable = ("order",)
    search_fields = ("name", "slug", "short_description")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(LoreEntry)
class LoreEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "domain", "created")
    list_filter = ("domain",)
    search_fields = ("title", "slug", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "domain", "rarity", "bearer", "epoch")
    list_filter = ("domain", "rarity")
    search_fields = ("name", "slug", "description", "bearer", "epoch")
    prepopulated_fields = {"slug": ("name",)}

class CharacterAnimationInline(admin.TabularInline):
    model = CharacterAnimation
    extra = 0

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "domain", "role", "playable")
    list_filter = ("domain", "playable")
    search_fields = ("name", "slug", "role", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CharacterAnimationInline]

class EnemyAnimationInline(admin.TabularInline):
    model = EnemyAnimation
    extra = 0

@admin.register(Enemy)
class EnemyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "domain")
    list_filter = ("domain",)
    search_fields = ("name", "slug", "description", "behavior")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [EnemyAnimationInline]

@admin.register(Trap)
class TrapAdmin(admin.ModelAdmin):
    list_display = ("title", "domain")
    list_filter = ("domain",)
    search_fields = ("title", "description")

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "domain", "read_time", "created")
    list_filter = ("domain",)
    search_fields = ("title", "slug", "summary", "body", "tags")
    filter_horizontal = ("related_artifacts", "related_characters", "related_enemies")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("file", "kind", "caption")
    list_filter = ("kind",)
    search_fields = ("caption", "file")
