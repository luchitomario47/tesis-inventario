from django.shortcuts import render
from .models import InvCab, InvConteo, InvDet, Datos  # Asegúrate de importar tu modelo Datos

def home(request):
    cabeceras = InvCab.objects.all()  # Mantén esto si necesitas los datos de InvCab
    tiendas = Datos.objects.filter(activo=1)  # Filtra las tiendas activas, ajusta según necesites
    return render(request, 'gestionInventarios.html', {
        "Inventarios": cabeceras,
        "Tiendas": tiendas  # Agrega las tiendas al contexto
    })
