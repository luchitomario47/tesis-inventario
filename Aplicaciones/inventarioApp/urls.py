from django.urls import path
from . import views

urlpatterns = [
    path('', views.tomaInventario, name='tomaInventario'),
    path('tomaInventario/', views.tomaInventario, name='tomaInventario'),
    path('contarInventario/', views.contarInventario, name='contarInventario'),
    path('guardarDatos/', views.guardarDatos, name='guardarDatos'),
    path('reportes/', views.reportes, name='reportes'),
    path('detalle-inventario/<int:idInventario>/', views.reporte_detalles, name='reporte_detalles'),
    path('analisisVentasAgno/', views.analisisVentasAgno, name='analisisVentasAgno'),
    path('analisisVentasMes/', views.analizar_datos_mensual, name='analisisVentasMes'),
    path('analisisInventarios/', views.analisisInventarios, name='analisisInventarios'),
    path('prediccion_demanda/', views.prediccion_demanda, name='prediccion_demanda'),
    path('dashboardTiendas/', views.dashboard_tiendas, name='dashboardTiendas'),
    path('analisisModelo/', views.analisisModelo, name='analisisModelo'),
    path('detectarAnomalias/', views.detectar_anomalias, name='detectar_anomalias'),
    ]