from django.urls import path
from . import views

urlpatterns = [
    path("", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path("olvide/", views.forget, name="forget"),
    path("recuperar/<str:token>/", views.recover, name="recover"),
    path("registrar/", views.register, name="register"),
    path("confirmar/<str:token>/", views.confirmation, name="confirmation"),
]
