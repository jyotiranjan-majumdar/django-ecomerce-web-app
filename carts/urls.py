from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from . import views


urlpatterns = [
    path("cart/", views.view, name="cart"),
    path("add_to_cart/<slug:slug>/)", views.add_to_cart, name="add_to_cart"),
    path("cart/<id>/)", views.remove_from_cart, name="remove_from_cart"),
    #path(r'^cart/(?p<id>\d)/$', views.remove_from_cart, name="remove_from_cart"),
    
    ]

