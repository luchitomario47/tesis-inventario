# Release Notes - **Sistema de Gestión de Inventarios** (Tesis)

## **Versión 1.0 - 22 de diciembre de 2024**

### **Descripción general**
Este es el lanzamiento inicial del **Sistema de Gestión de Inventarios**, un proyecto de tesis que busca optimizar la toma y análisis de inventarios mediante la integración de tecnologías avanzadas y herramientas de análisis de datos. El sistema está diseñado para predecir la demanda de productos, analizar los inventarios de distintas tiendas, y proporcionar visualizaciones detalladas que ayuden a la toma de decisiones en tiempo real.

### **Novedades y Funcionalidades**

#### **1. Dashboard de Tiendas**
- Se ha desarrollado un dashboard interactivo que permite visualizar el inventario de cada tienda, agrupado por fecha e identificador de inventario. El sistema permite:
  - **Filtrar inventarios por tienda**.
  - **Visualizar gráficos dinámicos** que muestran la distribución del stock por tienda.
  - **Acceder a un resumen detallado de cada inventario**, con la fecha de registro y el total de prendas disponibles.

#### **2. Análisis de Inventarios por Modelo**
- Se ha implementado una funcionalidad de análisis de inventarios por modelo, con los siguientes detalles:
  - **Exclusión de modelos** que comienzan con la letra "M" para centrarse solo en los modelos relevantes.
  - **Cálculo y visualización del stock total por SKU** en un gráfico de barras, mostrando los 40 SKUs con mayor stock.
  - Gráficos **dinámicos y personalizables** para facilitar el análisis visual de los datos.

#### **3. Integración con herramientas de análisis de datos**
- El sistema utiliza **Pandas** para el análisis de datos y **Matplotlib** para la creación de gráficos dinámicos, garantizando una experiencia interactiva en el análisis de inventarios.

### **Mejoras y Optimización**
- **Optimización de consultas SQL**: Se han mejorado las consultas a la base de datos para obtener los inventarios de manera más eficiente, lo que reduce los tiempos de carga.
- **Rediseño de la visualización de datos**: Los gráficos y las tablas se muestran de manera más clara y comprensible para el usuario, con títulos y etiquetas más informativas.
- **Carga dinámica de datos**: Los datos de inventarios y predicciones se cargan solo cuando el usuario selecciona la tienda deseada, mejorando la eficiencia en la carga de la información.

### **Correcciones de Errores**
- **Manejo de datos vacíos**: Se resolvió un problema que generaba errores al intentar renderizar gráficos con datos vacíos o nulos.
- **Exclusión de SKUs "M"**: Se corrigió un bug que impedía la correcta exclusión de los SKUs que comienzan con "M" en el análisis de inventarios.
- **Sincronización de fechas e inventarios**: Se corrigió el formato y la sincronización de las fechas de inventarios, garantizando que los datos se muestren correctamente para cada tienda.

### **Tecnologías Utilizadas**
- **Backend**: Django 4.2, Python 3.10
- **Frontend**: HTML5, CSS3, JavaScript (AJAX)
- **Gráficos**: Matplotlib, Pandas
- **Base de Datos**: MySQL, integración con Retail Pro y SAP

### **Próximos Pasos**
- **Integración de la inteligencia artificial**: Implementación de modelos predictivos para la predicción de la demanda de productos, basado en el análisis histórico de ventas y tendencias.
- **Mejoras en la visualización de datos**: Incorporación de nuevas visualizaciones interactivas (como gráficos de líneas, mapas de calor, etc.) para enriquecer la experiencia de usuario.
- **Automatización de la integración de datos**: Desarrollar un sistema de actualización automática de los datos de inventarios desde Retail Pro y SAP para mejorar la sincronización en tiempo real.

### **Agradecimientos**
Este proyecto no habría sido posible sin el apoyo y la inspiración de mis seres queridos: mi madre, padre, hermanas, abuelos, tías, primas y mi gatita Tini. A todos ellos, mi más sincero agradecimiento por su constante apoyo durante este proceso.
