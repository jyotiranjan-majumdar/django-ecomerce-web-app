from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
     path("logout_view/", views.logout_view, name="logout_view"),
     path("login_view/", views.login_view, name="login_view"),
     path("registration_view/", views.registration_view, name="registration_view"),
     path("activation_view/<activation_key>/", views.activation_view, name="activation_view"),
     path("add_user_address/", views.add_user_address, name="add_user_address"),

    ]
