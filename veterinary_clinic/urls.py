from django.contrib import admin
from django.urls import path, include
from vetclinic.admin_dashboard import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', include('vetclinic.urls')),
]