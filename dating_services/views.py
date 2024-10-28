from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Services, ServicesQuotes, Quotes
from authentication.models import CustomUser
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

# Create your views here.


# Vistas de Citas
@login_required(login_url="login")
def cita(request):
    # Establece la fecha mínima permitida para la cita como un día después de la fecha y hora actuales
    minimun_date = timezone.now() + timedelta(days=1)
    return render(
        request,
        "cita.html",
        {
            "title": "Cita",
            "name_page": "Crea Nueva Cita",
            "description_page": "Elige tus servicios a continuacion",
            "minimun_date": minimun_date,
        },
    )


@csrf_exempt
@login_required(login_url="login")
def api_quotes_keep(request):
    if request.method == "POST":
        try:
            # Obtener datos del POST
            user_id = request.POST.get("usuario_id")
            date = request.POST.get("fecha")
            hour = request.POST.get("hora")
            # Obtener lista de servicios como cadena
            servicios = request.POST.get("servicios")
            
            # Separar la cadena de servicios en una lista
            service_list = servicios.split(",")

            # Crear la cita y guardar en la base de datos
            user = CustomUser.objects.get(id=user_id)
            cita = Quotes.objects.create(user=user, date=date, hour=hour)

            # Guardar los servicios asociados con el ID de la cita
            for servicio_id in service_list:
                servicio = Services.objects.get(id=servicio_id.strip())
                ServicesQuotes.objects.create(quote=cita, service=servicio)

            # Devolver una respuesta JSON con el resultado
            resultado = {"id": cita.id}
            return JsonResponse({"resultado": resultado})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


# Vistas de Servicios
@login_required(login_url="login")
def api_services(request):
    # Obtener todos los servicios disponibles con sus campos id, name y price
    services = Services.objects.all().values("id", "name", "price")
    
    # Convertir el QuerySet a una lista de diccionarios
    services_list = list(services)
    
    # Devolver la lista de servicios como una respuesta JSON
    return JsonResponse(services_list, safe=False)
