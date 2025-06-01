# vetclinic/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homePage'),
    path('appointment/', views.appointment, name='appointment'),
    path('location/', views.location, name='location'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('reviews/', views.reviews, name='reviews'),
    path('shop/', views.shop, name='shop'),
]