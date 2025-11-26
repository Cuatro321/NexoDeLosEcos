# community/admin.py
from django.contrib import admin
from .models import Post, Comment, Forum, Thread, ThreadReply, ModerationLog

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "type", "created", "is_removed")
    list_filter  = ("type", "is_removed", "created")
    search_fields = ("title", "body", "author__username")
    raw_id_fields = ("author",)
    date_hierarchy = "created"
    prepopulated_fields = {}  # slug se genera en save()

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created", "is_removed")
    list_filter  = ("is_removed", "created")
    search_fields = ("body", "author__username", "post__title")
    raw_id_fields = ("post", "author")
    date_hierarchy = "created"

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("title", "forum", "author", "created", "is_locked", "is_removed")
    list_filter  = ("forum", "is_locked", "is_removed", "created")
    search_fields = ("title", "body", "author__username", "forum__title")
    raw_id_fields = ("forum", "author")
    date_hierarchy = "created"

@admin.register(ThreadReply)
class ThreadReplyAdmin(admin.ModelAdmin):
    list_display = ("thread", "author", "created", "is_removed")
    list_filter  = ("is_removed", "created")
    search_fields = ("body", "author__username", "thread__title")
    raw_id_fields = ("thread", "author")
    date_hierarchy = "created"

@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    list_display = ("content_type", "object_id", "removed_by", "owner", "created")
    list_filter  = ("content_type", "created")
    search_fields = ("reason", "removed_by__username", "owner__username")
    raw_id_fields = ("removed_by", "owner")
    date_hierarchy = "created"
