from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    # Feed principal
    path("", views.feed, name="feed"),

    # -------- Posts --------
    path("post/nuevo/", views.post_create, name="post_create"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/<slug:slug>/editar/", views.post_edit, name="post_edit"),
    path("post/<slug:slug>/eliminar/", views.post_delete, name="post_delete"),

    # Reacciones a posts
    path(
        "post/<slug:slug>/reaccion/<str:reaction>/",
        views.post_react,
        name="post_react",
    ),

    # -------- Comentarios --------
    path(
        "post/<slug:slug>/comentar/",
        views.comment_create,
        name="comment_create",
    ),
    path(
        "comentario/<int:pk>/responder/",
        views.comment_reply,
        name="comment_reply",
    ),
    path(
        "comentario/<int:pk>/eliminar/",
        views.comment_delete,
        name="comment_delete",
    ),

    # Reacciones a comentarios
    path(
        "comentario/<int:pk>/reaccion/<str:reaction>/",
        views.comment_react,
        name="comment_react",
    ),

    # -------- Foros --------
    path("foro/", views.forum_index, name="forum_index"),
    path("foro/<slug:slug>/", views.forum_detail, name="forum_detail"),
    path("hilo/nuevo/", views.thread_create, name="thread_create"),
    path(
        "foro/<slug:forum_slug>/hilo/<slug:slug>/",
        views.thread_detail,
        name="thread_detail",
    ),
    path(
        "hilo/<slug:slug>/responder/",
        views.thread_reply,
        name="thread_reply",
    ),
    path(
        "respuesta/<int:pk>/eliminar/",
        views.reply_delete,
        name="reply_delete",
    ),
    path(
        "hilo/<slug:slug>/eliminar/",
        views.thread_delete,
        name="thread_delete",
    ),
]
