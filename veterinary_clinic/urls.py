from django.contrib import admin
from django.urls import path, include
from vetclinic.admin_dashboard import custom_admin_site
from vetclinic import views

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', include('vetclinic.urls')),
    path('captcha/', include('captcha.urls')),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
]
