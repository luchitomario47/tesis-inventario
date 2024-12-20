from django.shortcuts import get_object_or_404, render, get_list_or_404
import json
from .models import InvCab, InvDet, Datos, repositorioVentas, repositorioVentasTienda  # Asegúrate de importar tu modelo Datos
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Sum
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64


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

def analisisVentasAgno(request):

    # Definir rango de fechas para el último año
    hoy = datetime.now()
    hace_un_anio = hoy - timedelta(days=365)

    # Consultar datos de ventas del último año
    ventas_data = repositorioVentasTienda.objects.filter(
        create_date__range=[hace_un_anio, hoy]
    ).values('store_code', 'total_amount')

    ventas_df = pd.DataFrame(list(ventas_data))

    if not ventas_df.empty:
        # Convertir a formato numérico
        ventas_df['total_amount'] = pd.to_numeric(ventas_df['total_amount'], errors='coerce')
        # Agrupar por tienda
        ventas_resumen = ventas_df.groupby('store_code')['total_amount'].sum().sort_values(ascending=False)
    else:
        ventas_resumen = pd.Series([])

    # Crear gráficos
    def create_chart(data, title, xlabel, ylabel, color):
        if data.empty:
            return None  # Retornar None si no hay datos
        fig, ax = plt.subplots(figsize=(10, 6))
        data.plot(kind='bar', ax=ax, color=color)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        return chart

    # Generar gráficos de ventas
    ventas_chart = create_chart(
        ventas_resumen, 'Ventas por Tienda (Último Año)', 'Tiendas', 'Ventas Totales', 'green'
    )

    # Obtener las tiendas que más y menos han vendido
    top_tiendas = ventas_resumen.head(5).to_dict() if not ventas_resumen.empty else {}
    low_tiendas = ventas_resumen.tail(5).to_dict() if not ventas_resumen.empty else {}

    # Pasar los datos al template
    context = {
        'ventas_chart': ventas_chart,
        'top_tiendas': top_tiendas,
        'low_tiendas': low_tiendas,
    }

    return render(request, 'analisis_ventas_ultimo_ano.html', context)


def analizar_datos_mensual(request):
    from datetime import datetime
    hoy = datetime.now()
    mes_seleccionado = hoy.month
    anio_seleccionado = hoy.year

    if request.method == 'GET' and 'mes' in request.GET and 'anio' in request.GET:
        mes_seleccionado = int(request.GET['mes'])
        anio_seleccionado = int(request.GET['anio'])

    # Filtrar las ventas del mes y año seleccionados
    ventas_data = repositorioVentasTienda.objects.filter(
        create_date__year=anio_seleccionado,
        create_date__month=mes_seleccionado
    ).values('store_code', 'total_amount')

    ventas_df = pd.DataFrame(list(ventas_data))

    if not ventas_df.empty:
        ventas_df['total_amount'] = pd.to_numeric(ventas_df['total_amount'], errors='coerce')
        ventas_resumen = ventas_df.groupby('store_code')['total_amount'].sum().sort_values(ascending=False)
    else:
        ventas_resumen = pd.Series([])

    def create_chart(data, title, xlabel, ylabel, color):
        if data.empty:
            return None
        fig, ax = plt.subplots(figsize=(10, 6))
        data.plot(kind='bar', ax=ax, color=color)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        return chart

    ventas_chart = create_chart(
        ventas_resumen,
        f'Ventas por Tienda - {mes_seleccionado}/{anio_seleccionado}',
        'Tiendas',
        'Ventas Totales',
        'blue'
    )

    context = {
        'ventas_chart': ventas_chart,
        'ventas_resumen': ventas_resumen.to_dict() if not ventas_resumen.empty else {},
        'mes_seleccionado': mes_seleccionado,
        'anio_seleccionado': anio_seleccionado,
        'meses': range(1, 13),  # Agrega el rango de meses
        'anios': range(2020, 2030),  # Agrega el rango de años
    }

    return render(request, 'analisis_ventas_mensual.html', context)

from django.shortcuts import render
import pandas as pd
from .models import InvDet

def analisisInventarios(request):
    # Consultar los datos de inventario
    inventarios_data = InvDet.objects.values('idInventario', 'sku', 'modelo', 'cantidad')

    # Convertir los datos a un DataFrame
    inventarios_df = pd.DataFrame(list(inventarios_data))

    if not inventarios_df.empty:
        # Extraer la tienda (últimos tres dígitos de idInventario)
        inventarios_df['store_code'] = inventarios_df['idInventario'].apply(lambda x: str(x)[-3:])
        
        # Calcular la cantidad total de prendas en cada tienda
        inventarios_resumen = inventarios_df.groupby('store_code')['cantidad'].sum().sort_values(ascending=False)
        
        # Calcular las prendas con más existencias
        top_prendas = inventarios_df.groupby('sku')['cantidad'].sum().sort_values(ascending=False).head(5)
    else:
        inventarios_resumen = pd.Series([])
        top_prendas = pd.Series([])

    # Crear gráficos para mostrar los datos
    def create_chart(data, title, xlabel, ylabel, color):
        if data.empty:
            return None  # Retornar None si no hay datos
        fig, ax = plt.subplots(figsize=(10, 6))
        data.plot(kind='bar', ax=ax, color=color)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=45)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        return chart

    # Crear gráficos para el análisis de inventarios
    inventarios_chart = create_chart(
        inventarios_resumen, 'Total de Prendas por Tienda', 'Tiendas', 'Cantidad de Prendas', 'blue'
    )
    
    top_prendas_chart = create_chart(
        top_prendas, 'Prendas con Más Existencias', 'Prendas', 'Cantidad de Existencias', 'orange'
    )

    # Pasar los datos al template
    context = {
        'inventarios_chart': inventarios_chart,
        'top_prendas_chart': top_prendas_chart,
        'inventarios_resumen': inventarios_resumen.to_dict() if not inventarios_resumen.empty else {},
        'top_prendas': top_prendas.to_dict() if not top_prendas.empty else {},
    }

    return render(request, 'analisis_inventarios.html', context)
