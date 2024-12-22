from django.test import TestCase
from django.urls import reverse
from .models import InvDet  # Asegúrate de importar tu modelo correctamente
import pandas as pd

class AnalisisModeloTestCase(TestCase):
    def setUp(self):
        # Crear datos de prueba para los inventarios
        InvDet.objects.create(idInventario='202312010001', sku='A123', modelo='Modelo1', cantidad=100)
        InvDet.objects.create(idInventario='202312020002', sku='B234', modelo='Modelo2', cantidad=50)
        InvDet.objects.create(idInventario='202312030003', sku='M345', modelo='Modelo3', cantidad=200)
        InvDet.objects.create(idInventario='202312040004', sku='A123', modelo='Modelo1', cantidad=150)

    def test_analisis_modelo_view(self):
        # Acceder a la vista analisisModelo
        response = self.client.get(reverse('analisis_modelo'))  # Asumiendo que tienes la URL configurada

        # Verificar que la respuesta es 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verificar que el gráfico está presente en el contexto (si el gráfico está en base64)
        self.assertIn('top_skus_chart', response.context)

        # Verificar que el contexto contiene los datos correctos para los SKUs
        self.assertIn('top_skus', response.context)
        self.assertIsInstance(response.context['top_skus'], dict)

        # Validar que los datos en el gráfico son los esperados
        # Excluimos el SKU que comienza con 'M' (debe quedar fuera)
        top_skus = response.context['top_skus']
        self.assertIn('A123', top_skus)  # Verificar que el SKU 'A123' está en el resultado
        self.assertNotIn('M345', top_skus)  # Verificar que el SKU 'M345' NO está en el resultado

    def test_empty_inventory_data(self):
        # Eliminar todos los datos de inventario
        InvDet.objects.all().delete()

        # Acceder a la vista cuando no hay datos
        response = self.client.get(reverse('analisis_modelo'))

        # Verificar que la respuesta es 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verificar que no hay gráfico
        self.assertIsNone(response.context.get('top_skus_chart'))

        # Verificar que no hay datos en 'top_skus'
        self.assertEqual(response.context.get('top_skus'), {})
