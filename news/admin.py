# news/admin.py
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Category, Tag, NewsArticle

User = get_user_model()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color", "icon")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

def publish_and_notify(modeladmin, request, queryset):
    """
    Publica los artículos seleccionados y envía 1 notificación por usuario.
    OJO: si tienes muchísimos usuarios, esto puede tardar.
    """
    from accounts.models import Notification  # import local para evitar ciclos
    now = timezone.now()

    for article in queryset:
        article.status = "published"
        article.publish_at = article.publish_at or now
        article.save()

    users = User.objects.all().only("id", "username")
    notices = []
    for article in queryset:
        title = article.title
        if article.is_patch_notes and article.version:
            msg = f"Nuevas notas de parche {article.version}: {title}"
        else:
            msg = f"Nueva noticia: {title}"
        for u in users:
            notices.append(Notification(user=u, message=msg))
    # Crea en bloques para evitar consumo excesivo de memoria
    from django.db import transaction
    with transaction.atomic():
        Notification.objects.bulk_create(notices, batch_size=1000)

publish_and_notify.short_description = "Publicar y notificar a todos"

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "is_patch_notes", "version", "pin_home", "publish_at")
    list_filter = ("status", "category", "is_patch_notes", "pin_home", "tags")
    search_fields = ("title", "summary", "body", "version")
    date_hierarchy = "publish_at"
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags", "gallery")
    actions = [publish_and_notify]

    fieldsets = (
        ("Contenido", {
            "fields": ("title", "slug", "summary", "body")
        }),
        ("Metadatos", {
            "fields": ("author", "category", "tags", "reading_time")
        }),
        ("Medios", {
            "fields": ("hero_image", "banner_image", "video_url", "gallery")
        }),
        ("Publicación", {
            "fields": ("status", "publish_at", "pin_home", "is_patch_notes", "version")
        }),
    )
