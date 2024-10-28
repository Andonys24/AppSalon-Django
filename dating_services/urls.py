from django.urls import path
from . import views

urlpatterns = [
    path("cita/", views.cita, name="cita"),
    path("api/servicios/", views.api_services, name="api_services"),
    path("api/citas", views.api_quotes_keep, name="api_quotes_keep"),
]
