from django.shortcuts import get_object_or_404, render, get_list_or_404
import json
from .models import InvCab, InvDet, Datos  # Asegúrate de importar tu modelo Datos
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Sum
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta

def tomaInventario(request):
    # Obtener todas las cabeceras de inventarios y las tiendas activas
    cabeceras = InvCab.objects.all()  # Si necesitas los datos de InvCab
    tiendas = Datos.objects.filter(activo=1)  # Filtra las tiendas activas
    return render(request, 'gestionInventarios.html', {
        "Inventarios": cabeceras,
        "Tiendas": tiendas  # Agregar tiendas activas al contexto
    })

def contarInventario(request):
    # Obtener todas las cabeceras de inventarios y las tiendas activas
    cabeceras = InvCab.objects.all()  # Si necesitas los datos de InvCab
    tiendas = Datos.objects.filter(activo=1)  # Filtra las tiendas activas
    return render(request, 'contarInv.html', {
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

def predecirDemanda(request):
    # Obtener datos históricos de InvDet
    ventas = InvDet.objects.values('idInventario_id', 'sku', 'cantidad', 'fecha_creacion')

    # Convertir a DataFrame
    df = pd.DataFrame(ventas)

    # Extraer el store de los últimos 3 dígitos del idInventario
    df['store'] = df['idInventario_id'].astype(str).str[-3:]

    # Convertir a datetime
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])

    # Agrupar por store, sku y mes
    df_grouped = df.groupby([
        pd.Grouper(key='fecha_creacion', freq='M'),  # Agrupar por mes
        'store',
        'sku'
    ]).agg({'cantidad': 'sum'}).reset_index()

    # Lista de tiendas para el combobox
    tiendas = df_grouped['store'].unique()

    # Obtener la tienda seleccionada desde el request
    tienda_seleccionada = request.GET.get('store', None)
    predicciones = []

    if tienda_seleccionada:
        # Filtrar datos por la tienda seleccionada
        df_store = df_grouped[df_grouped['store'] == tienda_seleccionada]

        skus = df_store['sku'].unique()  # Todos los SKUs para la tienda seleccionada

        # Fecha actual y próxima fecha
        fecha_actual = datetime.now()
        proxima_fecha = (fecha_actual + timedelta(days=30)).replace(day=1)  # Primer día del siguiente mes
        proxima_fecha_timestamp = int(proxima_fecha.timestamp() * 10**9)  # Convertir a nanosegundos

        for sku in skus:
            # Filtrar datos por SKU específico dentro de la tienda
            df_sku = df_store[df_store['sku'] == sku]

            # Convertir fechas a números para la regresión (timestamps en nanosegundos)
            X = df_sku['fecha_creacion'].astype('int64').values.reshape(-1, 1)  # Timestamps
            y = df_sku['cantidad'].values

            # Verificar que haya suficientes datos para entrenar
            if len(X) > 1:
                # Entrenar modelo
                model = LinearRegression()
                model.fit(X, y)

                # Predicción para el próximo mes
                prediccion = model.predict([[proxima_fecha_timestamp]])[0]

                # Excluir predicciones <= 0 y valores irrelevantes
                if prediccion > 0:
                    mes_despacho = proxima_fecha.strftime('%Y-%m')  # Año y mes del próximo despacho
                    predicciones.append({
                        'store': tienda_seleccionada,
                        'sku': sku,
                        'prediccion': int(round(prediccion)),  # Redondear predicción
                        'mes_despacho': mes_despacho
                    })

    # Pasar predicciones y tiendas a la plantilla
    return render(request, 'analisis/prediccion_tienda.html', {
        'predicciones': predicciones,
        'tiendas': tiendas,
        'tienda_seleccionada': tienda_seleccionada
    })

def descargar_predicciones(request):
    # Obtener datos históricos de InvDet
    ventas = InvDet.objects.values('idInventario_id', 'sku', 'cantidad', 'fecha_creacion')

    # Convertir a DataFrame
    df = pd.DataFrame(ventas)

    # Extraer el store de los últimos 3 dígitos del idInventario
    df['store'] = df['idInventario_id'].astype(str).str[-3:]

    # Convertir a datetime
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])

    # Agrupar por store, sku y mes
    df_grouped = df.groupby([
        pd.Grouper(key='fecha_creacion', freq='M'),  # Agrupar por mes
        'store',
        'sku'
    ]).agg({'cantidad': 'sum'}).reset_index()

    # Obtener tienda seleccionada
    tienda_seleccionada = request.GET.get('store', None)

    # Filtrar por la tienda seleccionada si existe
    if tienda_seleccionada:
        df_grouped = df_grouped[df_grouped['store'] == tienda_seleccionada]

    # Fecha actual y próxima fecha
    fecha_actual = datetime.now()
    proxima_fecha = (fecha_actual + timedelta(days=30)).replace(day=1)  # Primer día del siguiente mes
    proxima_fecha_timestamp = int(proxima_fecha.timestamp() * 10**9)  # Convertir a nanosegundos

    predicciones = []
    for sku in df_grouped['sku'].unique():
        df_sku = df_grouped[df_grouped['sku'] == sku]
        X = df_sku['fecha_creacion'].astype('int64').values.reshape(-1, 1)
        y = df_sku['cantidad'].values

        if len(X) > 1:
            model = LinearRegression()
            model.fit(X, y)
            prediccion = model.predict([[proxima_fecha_timestamp]])[0]

            if prediccion > 0:
                predicciones.append({
                    'store': tienda_seleccionada or 'Todas',
                    'sku': sku,
                    'prediccion': int(round(prediccion)),
                    'mes_despacho': proxima_fecha.strftime('%Y-%m')
                })

    # Convertir predicciones a DataFrame
    df_predicciones = pd.DataFrame(predicciones)

    # Generar CSV o XLSX (en este ejemplo, CSV)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="predicciones.csv"'

    # Convertir DataFrame a CSV
    df_predicciones.to_csv(response, index=False)

    return response