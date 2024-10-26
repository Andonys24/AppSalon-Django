from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_custom_email(subject, message, recipient_list, html_message=None):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
        html_message=html_message,
    )

def send_confirmation_email(user, token):
    subject = "Confirma tu cuenta"
    message = render_to_string(
        "confirm_email.html", {"token": token, "username": user.username, 'app_url': settings.APP_URL}
    )
    recipient_list = [user.email]
    send_custom_email(subject, message, recipient_list, html_message=message)

def send_recovery_email(user, token):
    subject = "Recupera tu contraseña"
    message = render_to_string(
        "recover_email.html", {"token": token, "username": user.username, 'app_url': settings.APP_URL}
    )
    recipient_list = [user.email]
    send_custom_email(subject, message, recipient_list, html_message=message)