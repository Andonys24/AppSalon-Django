from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.utils import timezone
from dating_services.models import Quotes, Services
from .decorators import superuser_required
from dating_services.forms import FormService


@login_required(login_url="login")
@superuser_required
def index(request):
    # Obtener la fecha de la solicitud GET o usar la fecha actual
    date_str = request.GET.get("fecha", timezone.now().date().isoformat())
    date = parse_date(date_str)

    # Validar la fecha
    if not date:
        return redirect("administration")

    # Consultar la base de datos
    citas = (
        Quotes.objects.filter(date=date)
        .select_related("user")
        .prefetch_related("servicesquotes_set__service")
    )

    # Preparar los datos para la plantilla
    citas_data = []
    for cita in citas:
        servicios = []
        total = 0
        for service_quote in cita.servicesquotes_set.all():
            servicios.append(
                {
                    "nombre": service_quote.service.name,
                    "precio": service_quote.service.price,
                }
            )
            total += service_quote.service.price
        citas_data.append(
            {
                "id": cita.id,
                "hora": cita.hour,
                "cliente": f"{cita.user.first_name} {cita.user.last_name}",
                "email": cita.user.email,
                "telefono": cita.user.phone,
                "servicios": servicios,
                "total": total,
            }
        )

    return render(
        request,
        "administration/index.html",
        {
            "title": "Administracion",
            "name_page": "Panel de administracion",
            "description_page": "Panel de administración para gestionar y administrar citas programadas.",
            "citas": citas_data,
            "fecha": date_str,
        },
    )


@login_required(login_url="login")
@superuser_required
def delete_appointment(request):
    if request.method == "POST":
        id = request.POST.get("id")
        Quotes.objects.get(id=id).delete()
        messages.success(request, "Cita eliminada correctamente", extra_tags="exito")

    # Redireccionar a la misma página
    return redirect(request.META.get("HTTP_REFERER", "administracion"))


@login_required(login_url="login")
@superuser_required
def services(request):
    services = Services.objects.all().values("id", "name", "price")
    return render(
        request,
        "servicios/index.html",
        {
            "title": "Servicios",
            "name_page": "Servicios",
            "description_page": "Administracion de servicios.",
            "services": services,
        },
    )


@login_required(login_url="login")
@superuser_required
def services_create(request):
    alerts = []
    if request.method == "POST":
        form = FormService(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Servicio agregado correctamente", extra_tags="exito"
            )
            return redirect("services")
        else:
            alerts = [error for errors in form.errors.values() for error in errors]
    else:
        form = FormService()
    return render(
        request,
        "servicios/create.html",
        {
            "form": form,
            "alerts": alerts,
            "title": "Agregar servicio",
            "name_page": "Nuevo Servicio",
            "description_page": "Llena los campos para agregar un nuevo servicio.",
        },
    )


@login_required(login_url="login")
@superuser_required
def services_update(request, id):
    alerts = []
    if request.method == "POST":
        form = FormService(request.POST, instance=Services.objects.get(id=id))
        if form.is_valid():
            form.save()
            messages.success(
                request, "Servicio actualizado correctamente", extra_tags="exito"
            )
            return redirect("services")
        else:
            alerts = [error for errors in form.errors.values() for error in errors]
    else:
        form = FormService(instance=Services.objects.get(id=id))
    return render(
        request,
        "servicios/update.html",
        {
            "form": form,
            "alerts": alerts,
            "title": "Actualizar servicio",
            "name_page": "Actualizar Servicio",
            "description_page": "Llena los campos para actualizar el servicio.",
        },
    )


@login_required(login_url="login")
@superuser_required
def services_delete(request):
    if request.method == "POST":
        id = request.POST.get("id")
        services = Services.objects.get(id=id)
        if services:
            services.delete()
            messages.success(
                request, "Servicio eliminado correctamente", extra_tags="exito"
            )
        return redirect("services")
