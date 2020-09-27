from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path("login/", views.user_login, name="user-login"),
    path("register/", views.user_register, name="user-register"),
    path("logout/", views.user_logout, name="user-logout"),
    path("", views.user_home, name="user-home"),
]
