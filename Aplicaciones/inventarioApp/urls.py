from django.urls import path
from . import views

urlpatterns = [
    path('', views.tomaInventario, name='tomaInventario'),
    path('tomaInventario/', views.tomaInventario, name='tomaInventario'),
    path('contarInventario/', views.contarInventario, name='contarInventario'),
    path('guardarDatos/', views.guardarDatos, name='guardarDatos'),
    path('reportes/', views.reportes, name='reportes'),
    path('detalle-inventario/<int:idInventario>/', views.reporte_detalles, name='reporte_detalles'),
    path('prediccionDemanda/', views.predecirDemanda, name='prediccionDemanda'),
    path('descargar_predicciones/', views.descargar_predicciones, name='descargar_predicciones'),
    ]