from django.shortcuts import get_object_or_404, render, get_list_or_404
import json
from .models import InvCab, InvDet, Datos  # Asegúrate de importar tu modelo Datos
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Sum

def home(request):
    # Obtener todas las cabeceras de inventarios y las tiendas activas
    cabeceras = InvCab.objects.all()  # Si necesitas los datos de InvCab
    tiendas = Datos.objects.filter(activo=1)  # Filtra las tiendas activas
    return render(request, 'gestionInventarios.html', {
        "Inventarios": cabeceras,
        "Tiendas": tiendas  # Agregar tiendas activas al contexto
    })

@csrf_exempt
def guardarDatos(request):
    if request.method == 'POST':
        try:
            # Cargar los datos recibidos desde el cuerpo de la solicitud
            data = json.loads(request.body)
            print("Datos recibidos:", data)

            # Verificar que las claves mínimas existan en 'data'
            if 'invCab' not in data or 'inventario' not in data:
                return JsonResponse({'status': 'error', 'message': 'Datos incompletos'}, status=400)

            # Extraer datos de invCab
            inv_cab_data = data['invCab']
            inventario_data = data['inventario']  # Esto debería ser una lista

            # Verificar que 'inventario_data' sea una lista y que tenga los campos necesarios
            if not isinstance(inventario_data, list) or not all(
                all(k in item for k in ['idInventario', 'sku', 'modelo', 'zona', 'cantidad', 'username', 'store'])
                for item in inventario_data
            ):
                return JsonResponse({'status': 'error', 'message': 'Estructura de inventario inválida'}, status=400)

            # Crear o recuperar el registro de InvCab
            inv_cab, created = InvCab.objects.get_or_create(
                idInventario=inv_cab_data['idInv'],
                defaults={
                    'store': inv_cab_data['tienda'],
                    #'id_user': 'lperez',
                    'estado': 1
                }
            )

            # Verificar si el registro fue creado
            if created:
                print(f"Nuevo InvCab creado: {inv_cab}")
            else:
                print(f"InvCab existente utilizado: {inv_cab}")

            # Crear y guardar los registros en InvDet
            for item in inventario_data:
                InvDet.objects.create(
                    idInventario=inv_cab,
                    zona=item['zona'],
                    sku=item['sku'],
                    modelo=item['modelo'],
                    cantidad=item['cantidad'],
                    username=item['username']
                )
                print(f"Nuevo registro de InvDet creado para SKU: {item['sku']}")

            # Responder con un mensaje de éxito
            return JsonResponse({'status': 'success', 'message': 'Datos guardados exitosamente'}, status=200)

        except Exception as e:
            # Capturar cualquier excepción y devolver un mensaje de error
            print("Error al guardar los datos:", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # Responder si el método HTTP no es POST
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def reportes(request):
    # Obtener todos los registros de InvCab y ordenarlos por fecha descendente
    inventarios = InvCab.objects.all().order_by('-date_created')
    paginator = Paginator(inventarios, 20)  # 20 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'reportes.html', {
        'inventarios': inventarios,
        'page_obj': page_obj,
    })



def reporte_detalles(request, idInventario):
    # Obtener el inventario
    inventario = get_object_or_404(InvCab, idInventario=idInventario)
    
    # Obtener el término de búsqueda para SKU y zona (si existen)
    sku_buscar = request.GET.get('sku', '').strip()
    zona_buscar = request.GET.get('zona', '').strip()

    # Obtener los detalles agrupados por SKU, ordenados por zona
    detalles_list = (
        InvDet.objects.filter(idInventario=inventario)
        .values('sku', 'zona')  # Agrupación por SKU y zona
    )
    
    # Filtrar por SKU si se proporciona un término de búsqueda
    if sku_buscar:
        detalles_list = detalles_list.filter(sku__icontains=sku_buscar)
    
    # Filtrar por zona (exacta) si se proporciona un término de búsqueda
    if zona_buscar:
        detalles_list = detalles_list.filter(zona__exact=zona_buscar)
    
    # Sumar cantidades y ordenar por zona
    detalles_list = (
        detalles_list
        .annotate(cantidad_total=Sum('cantidad'))  # Sumar cantidades
        .order_by('zona')  # Ordenar por zona
    )
    
    # Configurar el paginador
    paginator = Paginator(detalles_list, 50)  # 50 detalles por página
    page_number = request.GET.get('page')
    detalles = paginator.get_page(page_number)
    
    # Renderizar el template
    return render(request, 'reportes_detalles.html', {
        'inventario': inventario,
        'detalles': detalles,
        'sku_buscar': sku_buscar,  # Pasar el término de búsqueda de SKU al template
        'zona_buscar': zona_buscar,  # Pasar el término de búsqueda de zona al template
    })
