# news/urls.py
from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.news_index, name="index"),
    path("parche/", views.patch_notes, name="patch_notes"),
    path("<slug:slug>/", views.news_detail, name="detail"),
]
