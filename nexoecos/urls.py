# urls.py (raíz del proyecto)

from django.contrib import admin as dj_admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import ManifestView, ServiceWorkerView, OfflineView
from core.admin_site import nexo_admin_site  # AdminSite sólo superusuarios

# Clonar registros del admin “normal”
dj_admin.autodiscover()
nexo_admin_site._registry = dj_admin.site._registry

urlpatterns = [
    # Admin SOLO superusuarios
    path("admin/", nexo_admin_site.urls),

    # Apps del sitio
    path("", include(("core.urls", "core"), namespace="core")),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("codex/", include(("codex.urls", "codex"), namespace="codex")),
    path("comunidad/", include(("community.urls", "community"), namespace="community")),
    path("noticias/", include(("news.urls", "news"), namespace="news")),

    # PWA
    path("manifest.webmanifest", ManifestView.as_view(), name="pwa-manifest"),
    path("service-worker.js", ServiceWorkerView.as_view(), name="pwa-sw"),
    path("offline/", OfflineView.as_view(), name="offline"),
]

# Media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
