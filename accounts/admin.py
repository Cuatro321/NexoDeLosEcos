# accounts/admin.py
from django.contrib import admin
from .models import Profile, Notification

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "display_name",
        "gamer_tag",      # <- nombre correcto del campo
        "country",
        "city",
        "favorite_domain",
        "has_avatar",
    )
    list_filter = ("favorite_domain",)
    search_fields = ("user__username", "display_name", "gamer_tag", "country", "city")
    fieldsets = (
        ("Usuario", {"fields": ("user",)}),
        ("Perfil", {
            "fields": (
                "display_name",
                "gamer_tag",
                "bio",
                "country",
                "city",
                "favorite_domain",
                "avatar",
            )
        }),
    )

    def has_avatar(self, obj):
        return bool(obj.avatar)
    has_avatar.boolean = True
    has_avatar.short_description = "Avatar"

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message_short", "is_read", "created")
    list_filter = ("is_read", "created")
    search_fields = ("user__username", "message")

    def message_short(self, obj):
        return (obj.message[:60] + "…") if len(obj.message) > 60 else obj.message
    message_short.short_description = "Mensaje"
