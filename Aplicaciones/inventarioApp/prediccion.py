# aplicaciones/inventarioApp/prediccion.py

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from tensorflow.keras.models import load_model
from django.db.models import Sum
from .models import InvDet

# Cargar el modelo ARIMA preentrenado
def cargar_modelo_arima(sku):
    # Recuperar los datos históricos del SKU
    inventarios = InvDet.objects.values('sku', 'fecha_creacion__date').annotate(total_vendido=Sum('cantidad')).order_by('fecha_creacion')
    df = pd.DataFrame(inventarios)
    df['fecha_creacion__date'] = pd.to_datetime(df['fecha_creacion__date'])
    df_sku = df[df['sku'] == sku]
    df_sku.set_index('fecha_creacion__date', inplace=True)
    
    # Ajustar el modelo ARIMA
    model = ARIMA(df_sku['total_vendido'], order=(5, 1, 0))  # (p, d, q)
    model_fit = model.fit()
    return model_fit

# Realizar la predicción con ARIMA
def predecir_demanda_arima(sku, dias_futuro=30):
    model_fit = cargar_modelo_arima(sku)
    forecast = model_fit.forecast(steps=dias_futuro)
    return forecast

# Si utilizas LSTM, puedes cargar el modelo de la siguiente manera
def cargar_modelo_lstm(sku):
    # Suponiendo que tienes un modelo guardado en un archivo '.h5'
    model = load_model('ruta/a/tu/modelo_lstm.h5')
    return model

def predecir_demanda_lstm(sku, dias_futuro=30):
    # Aquí cargarías los datos como se hizo antes, y luego usarías el modelo LSTM para predecir
    model = cargar_modelo_lstm(sku)
    # Preprocesar y predecir aquí (similares a lo mostrado antes en el código)
    predictions = model.predict(...)  # Preprocesar y hacer la predicción
    return predictions
