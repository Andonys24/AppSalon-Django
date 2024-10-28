from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Token
from .forms import CustomUserForm, PasswordRecoveryForm
from utils.task import send_confirmation_email, send_recovery_email


# Create your views here.
def custom_login(request):
    # Validar si el usuario está autenticado
    if request.user.is_authenticated:
        is_superuser = request.session.get("is_superuser")
        # validar si el usuario es superusuario
        if is_superuser:
            pass
            # return redirect("administracion")
        else:
            return redirect("cita")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
        else:
            if not user.is_active:
                messages.error(request, "Cuenta no confirmada")
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    request.session["is_superuser"] = user.is_superuser
                    if user.is_superuser:
                        pass
                        # return redirect("administracion")
                    else:
                        return redirect("cita")
                else:
                    messages.error(request, "Credenciales incorrectas")

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
    messages.success(request, "Sesión cerrada correctamente", extra_tags="exito")
    return redirect("login")


def forget(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
        else:
            if not user.is_active:
                messages.error(request, "Cuenta no confirmada")
            else:
                token = Token.objects.create(user=user)
                send_recovery_email(user, token.token)
                messages.success(
                    request, "Email de recuperación enviado", extra_tags="exito"
                )
    return render(
        request,
        "forget.html",
        {
            "title": "Olvidé",
            "name_page": "Olvidé mi contraseña",
            "description_page": "Restablece tu contraseña ingresando tu email a continuación",
        },
    )


def recover(request, token):
    alerts = []
    show = False

    if not token:
        return redirect("login")
    try:
        token = Token.objects.get(token=token)
    except Token.DoesNotExist:
        messages.error(request, "Token no válido")
    else:
        if token.used:
            messages.error(request, "Este token ya ha sido utilizado")
        elif token.is_expired():
            messages.error(request, "Token expirado")
        elif not token.user.is_active:
            messages.error(request, "Cuenta no confirmada")
        else:
            show = True
            if request.method == "POST":
                form = PasswordRecoveryForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data.get("password")
                    user = get_object_or_404(CustomUser, id=token.user.id)
                    user.set_password(password)
                    token.used = True
                    user.save()
                    token.save()
                    messages.success(
                        request,
                        "Contraseña actualizada correctamente",
                        extra_tags="exito",
                    )
                    return redirect("login")
                else:
                    alerts = [
                        error for errors in form.errors.values() for error in errors
                    ]

    return render(
        request,
        "recover.html",
        {
            "title": "Recuperar cuenta",
            "name_page": "Recuperar contraseña",
            "description_page": "Coloca tu nueva contraseña a continuación",
            "show": show,
            "alerts": alerts,
        },
    )


def register(request):
    alerts = []
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                token = Token.objects.get(user=user)
                if token:
                    send_confirmation_email(user, token.token)
                    messages.success(
                        request, "Cuenta creada correctamente", extra_tags="exito"
                    )
                    form = CustomUserForm()
                    return redirect("login")
                else:
                    alerts.append("Error al crear la cuenta")
            else:
                alerts.append("Error al crear la cuenta")
        else:
            alerts = [error for errors in form.errors.values() for error in errors]
    else:
        form = CustomUserForm()
    return render(
        request,
        "register.html",
        {
            "title": "Registrar",
            "name_page": "Crea tu cuenta",
            "description_page": "Llena el siguiente formulario para crear una cuenta",
            "form": form,
            "alerts": alerts,
        },
    )


def confirmation(request, token):
    if not token:
        return redirect("login")

    try:
        token = Token.objects.get(token=token)
    except Token.DoesNotExist:
        messages.error(request, "Token no válido")
    else:
        if token.used:
            messages.error(request, "Este token ya ha sido utilizado")
        elif token.is_expired():
            messages.error(request, "Token expirado")
        else:
            user = get_object_or_404(CustomUser, id=token.user.id)
            user.is_active = True
            token.used = True
            user.save()
            token.save()
            messages.success(
                request, "Cuenta confirmada correctamente", extra_tags="exito"
            )
            return redirect("login")

    return render(
        request,
        "confirmation.html",
        {
            "title": "Confirmación",
            "name_page": "Confirmación de cuenta",
        },
    )
