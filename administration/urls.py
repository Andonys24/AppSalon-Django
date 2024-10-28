from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="administration"),
    path("eliminar/", views.delete_appointment, name="delete_appointment"),
    path("servicios/", views.services, name="services"),
    path("servicios/crear/", views.services_create, name="services_create"),
    path("servicios/editar/<int:id>", views.services_update, name="services_update"),
    path("servicios/eliminar/", views.services_delete, name="services_delete"),
]
