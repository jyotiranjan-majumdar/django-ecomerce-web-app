from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("s/", views.search, name="search"),
    path("product", views.product, name="product"),
    path("products/<slug:slug>/", views.singel_product, name="singel_product"),
    ]
