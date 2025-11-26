# codex/urls.py
from django.urls import path
from . import views

app_name = 'codex'

urlpatterns = [
    path('', views.codex_index, name='index'),

    # Historias (Lore)
    path('historias/', views.lore_index, name='lore_index'),
    path('historias/<slug:slug>/', views.lore_detail, name='lore_detail'),

    # Personajes
    path('personajes/', views.characters_index, name='characters_index'),
    path('personajes/<slug:slug>/', views.character_detail, name='character_detail'),

    # Enemigos
    path('enemigos/', views.enemies_index, name='enemies_index'),
    path('enemigos/<slug:slug>/', views.enemy_detail, name='enemy_detail'),

    # Dominios
    path('dominios/', views.domains_index, name='domains_index'),
    path('dominios/<slug:slug>/', views.domain_detail, name='domain_detail'),

    # Artefactos
    path('artefactos/', views.artifacts_index, name='artifacts_index'),
    path('artefactos/<slug:slug>/', views.artifact_detail, name='artifact_detail'),

    # Guías
    path('guias/', views.guides_index, name='guides_index'),
    path('guias/<slug:slug>/', views.guide_detail, name='guide_detail'),
]
