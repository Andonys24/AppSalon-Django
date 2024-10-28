import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Services


class FormService(forms.ModelForm):
    class Meta:
        model = Services
        fields = ["name", "price"]
        labels = {
            "name": "Nombre",
            "price": "Precio",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "id": "name",
                    "placeholder": "Ingresa el Nombre del Servicio",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "id": "price",
                    "placeholder": "Ingresa el Precio del Servicio",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise ValidationError("El nombre del servicio es requerido.")
        if len(name) < 3:
            raise ValidationError(
                "El nombre del servicio debe tener al menos 3 caracteres."
            )
        if len(name) > 100:
            raise ValidationError(
                "El nombre del servicio no puede tener más de 100 caracteres."
            )
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", name):
            raise ValidationError("El nombre del servicio solo puede contener letras.")
        return name.strip()

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if not price:
            raise ValidationError("El precio del servicio es requerido.")
        if price <= 0:
            raise ValidationError("El precio del servicio debe ser mayor a 0.")
        return price
