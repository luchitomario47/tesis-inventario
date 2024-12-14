from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('guardarDatos/', views.guardarDatos, name='guardarDatos'),
    path('reportes/', views.reportes, name='reportes'),
    path('detalle-inventario/<int:idInventario>/', views.reporte_detalles, name='reporte_detalles'),
    ]