from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def custom_login(request):
    return render(
        request,
        "login.html",
        {
            "title": "Iniciar sesión",
            "name_page": "Bienvenido a AppSalon",
            "description_page": "Inicia sesión con tus datos",
        },
    )


def custom_logout(request):
    logout(request)
    return redirect("login")


def forget(request):
    return render(
        request,
        "forget.html",
        {
            "title": "Olvidé",
            "name_page": "Olvidé mi contraseña",
            "description_page": "Restablece tu contraseña ingresando tu email a continuación",
        },
    )


def recover(request):
    return render(
        request,
        "recover.html",
        {
            "title": "Recuperar cuenta",
            "name_page": "Recuperar contraseña",
            "description_page": "Coloca tu nueva contraseña a continuación",
        },
    )


def register(request):
    return render(
        request,
        "register.html",
        {
            "title": "Registrar",
            "name_page": "Crea tu cuenta",
            "description_page": "Llena el siguiente formulario para crear una cuenta",
        },
    )
