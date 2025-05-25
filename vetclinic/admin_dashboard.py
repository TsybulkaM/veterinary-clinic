from django.contrib import admin
from django.apps import apps
from django.urls import path
from django.template.response import TemplateResponse

class CustomAdminSite(admin.AdminSite):
    site_header = "VetClinic Management"
    site_title = "VetClinic Admin"
    index_title = "Welcome to VetClinic Administration"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.custom_index), name='index'),
        ]
        return custom_urls + urls[1:]

    def custom_index(self, request):
        # Models statistics collection
        stats = []
        for model in apps.get_models():
            try:
                stats.append({
                    "name": model._meta.verbose_name_plural.title(),
                    "count": model.objects.count()
                })
            except Exception:
                pass
        context = dict(
            self.each_context(request),
            stats=stats[-8:],
        )
        return TemplateResponse(request, "admin/custom_index.html", context)

custom_admin_site = CustomAdminSite(name='custom_admin')