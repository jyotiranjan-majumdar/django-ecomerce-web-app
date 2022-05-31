from django.urls import path
from . import views



urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("userorders/", views.userorders, name="userorders"),
    ]
