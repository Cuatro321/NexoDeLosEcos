from django.contrib.admin import AdminSite

class NexoAdminSite(AdminSite):
    site_header = "Panel • El Nexo de los Ecos"
    site_title = "Admin Nexo"
    index_title = "Centro de control"

    # Solo superusuarios (no basta con is_staff)
    def has_permission(self, request):
        return bool(request.user and request.user.is_active and request.user.is_superuser)

nexo_admin_site = NexoAdminSite(name="nexo_admin")
