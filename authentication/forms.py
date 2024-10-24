import re
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "phone", "email", "password"]
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "username": "Username",
            "phone": "Teléfono",
            "email": "E-mail",
            "password": "Contraseña",
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "id": "first_name",
                    "placeholder": "Ingresa tu Nombre",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "id": "last_name",
                    "placeholder": "Ingresa tu Apellido",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "id": "username",
                    "placeholder": "Ingresa tu Nombre de Usuario",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "id": "phone",
                    "placeholder": "Ingresa tu Teléfono",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "id": "email",
                    "placeholder": "Ingresa tu Email",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "id": "password",
                    "placeholder": "Ingresa tu contraseña",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    def validate_string(self, value, limit_min, limit_max, field):
        value = self.cleaned_data.get(value)
        if not value:
            raise ValidationError(f"El campo {field} es requerido")
        if len(value) > limit_max:
            raise ValidationError(
                f"El campo {field} no puede tener más de {limit_max} caracteres"
            )
        if len(value) < limit_min:
            raise ValidationError(
                f"El campo {field} no puede tener menos de {limit_min} caracteres"
            )
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$", value):
            raise ValidationError(
                f"El campo {field} solo puede contener letras sin espacios"
            )
        return value.strip()

    def clean_first_name(self):
        return self.validate_string("first_name", 3, 60, "Nombre")

    def clean_last_name(self):
        return self.validate_string("last_name", 3, 60, "Apellido")

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone:
            raise ValidationError("El Teléfono es requerido")
        if len(phone) > 8:
            raise ValidationError("El Teléfono no puede tener más de 8 caracteres")
        if len(phone) < 8:
            raise ValidationError("El Teléfono no puede tener menos de 8 caracteres")
        if not re.match(r"^[0-9]+$", phone):
            raise ValidationError(
                "El Teléfono solo puede contener números sin espacios"
            )
        if CustomUser.objects.filter(phone=phone).exists():
            raise ValidationError("El Teléfono ya está en uso")
        return phone.strip()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("El Email es requerido")
        if len(email) > 255:
            raise ValidationError("El Email no puede tener más de 255 caracteres")
        if len(email) < 6:
            raise ValidationError("El Email no puede tener menos de 6 caracteres")
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise ValidationError("El Email no es válido")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("El Email ya está en uso")
        return email.strip()

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise ValidationError("La Contraseña es requerida")
        if len(password) < 8:
            raise ValidationError("La Contraseña no puede tener menos de 8 caracteres")
        if not re.search(r"[a-z]", password):
            raise ValidationError(
                "La Contraseña debe contener al menos una letra minúscula"
            )
        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                "La Contraseña debe contener al menos una letra mayúscula"
            )
        if not re.search(r"[0-9]", password):
            raise ValidationError("La Contraseña debe contener al menos un número")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                "La Contraseña debe contener al menos un carácter especial"
            )
        return password.strip()

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise ValidationError("El Username es requerido")
        if len(username) > 60:
            raise ValidationError("El Username no puede tener más de 60 caracteres")
        if len(username) < 4:
            raise ValidationError("El Username no puede tener menos de 4 caracteres")
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            raise ValidationError(
                "El Username solo puede contener letras, números y guiones bajos, sin espacios"
            )
        return username.strip()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
