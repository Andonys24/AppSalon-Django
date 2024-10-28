from django.shortcuts import render


# Create your views here.
def not_found(request, exception):
    return render(
        request,
        "not_found.html",
        {
            "title": "Página No Encontrada",
            "name_page": "Error 404",
            "description_page": "Lo sentimos, la página que estás buscando no existe. Verifica la URL o vuelve a la página principal.",
        },
        status=404,
    )
