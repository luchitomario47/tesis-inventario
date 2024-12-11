from django.shortcuts import render
import json
from .models import InvCab, InvDet, Datos  # Asegúrate de importar tu modelo Datos
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
