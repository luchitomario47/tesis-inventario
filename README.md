# Sistema de Gestión de Inventarios - Tesis

**Sistema de Gestión de Inventarios** es un proyecto de tesis diseñado para optimizar la toma y análisis de inventarios mediante la integración de herramientas avanzadas de análisis de datos y la predicción de la demanda de productos. El sistema está orientado a gestionar los inventarios de diferentes tiendas y proporcionar análisis detallados mediante gráficos interactivos.

## Descripción

Este sistema permite:

- **Visualizar inventarios de tiendas**: Agrupados por fecha e identificador de inventario, con filtros por tienda.
- **Analizar inventarios por modelo**: Excluir modelos irrelevantes y calcular el stock total por SKU.
- **Generar gráficos interactivos**: Utilizando herramientas como Pandas y Matplotlib para proporcionar visualizaciones claras y detalladas.

## Características

- **Dashboard de Tiendas**: Visualización de inventarios agrupados por tienda y fecha.
- **Análisis de Inventarios por Modelo**: Análisis dinámico de stock por SKU con visualización gráfica.
- **Optimización de Carga de Datos**: Los datos se cargan solo cuando el usuario selecciona una tienda, mejorando la eficiencia.
- **Exclusión de SKUs irrelevantes**: Excluye los SKUs que comienzan con la letra "M" para centrarse en productos relevantes.
- **Gráficos Interactivos**: Creación de gráficos de barras y otros tipos de gráficos dinámicos.

## Instalación

Para instalar y ejecutar este proyecto en tu máquina local, sigue estos pasos:

### Requisitos

- Python 3.10 o superior
- Django 4.2
- MySQL
- Pandas
- Matplotlib

### Pasos de instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/luchitomario47/tesis-inventario.git
   cd tesis-inventario

2. Crea un entorno virtual
    python3 -m venv venv
    source venv/bin/activate  # En Linux/Mac
    venv\Scripts\activate     # En Windows

3. Instala dependendencias
    pip install -r requirements.txt

4. Configura la base de datos:

    Asegúrate de tener una base de datos MySQL configurada y agrega las credenciales en settings.py.

5. Realiza migraciones:
    python manage.py migrate

6. Carga los datos de inventario (Si es necesario)
    python manage.py loaddata inventarios.json

7. Ejecuta el servidor de desarrollo:
    python manage.py runserver

8. Accede a la aplicación en tu navegador en http://127.0.0.1:8000.

###Uso
**Dashboard de Tiendas**: Ve a la sección "Dashboard" para ver un resumen de los inventarios de las tiendas.
**Análisis de Inventarios**: Dirígete a la sección "Análisis de Inventarios" para ver los detalles del stock por modelo y SKU.
**Generación de Gráficos**: Los gráficos se generan automáticamente según los datos disponibles y las selecciones del usuario.

###Contribuciones

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

Haz un fork de este repositorio.
Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
Realiza tus cambios y haz un commit (git commit -am 'Agregada nueva funcionalidad').
Haz push a la rama (git push origin feature/nueva-funcionalidad).
Abre un Pull Request para que tus cambios sean revisados.

###Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.

###Agradecimientos

Este proyecto no habría sido posible sin el apoyo y la inspiración de mis seres queridos: mi madre, padre, hermanas, abuelos, tías, primas y mi gatita Tini. A todos ellos, mi más sincero agradecimiento por su constante apoyo durante este proceso.

*Este proyecto fue realizado como parte de mi tesis de Universidad Andres Bello.*


### Explicación de las secciones:

1. **Descripción**: Un resumen sobre lo que hace el proyecto. Es importante para que el usuario entienda rápidamente de qué trata el sistema.
2. **Características**: Sección con las principales funcionalidades del sistema.
3. **Instalación**: Guía detallada para instalar y configurar el proyecto en tu máquina local, incluyendo los requisitos, pasos y comandos necesarios.
4. **Uso**: Explicación de cómo utilizar el sistema una vez instalado.
5. **Contribuciones**: Instrucciones sobre cómo contribuir al proyecto, con detalles sobre cómo hacer un *fork* y crear un *pull request*.
6. **Licencia**: Información sobre la licencia que estás utilizando para tu proyecto. Si usas la Licencia MIT, este es el texto que debes incluir.
7. **Agradecimientos**: Un agradecimiento a las personas que te apoyaron en el proyecto.
8. **Notas adicionales**: Sección final en donde puedes incluir detalles sobre tu universidad o cualquier otra información adicional.

Este archivo `README.md` está completamente listo para que lo pongas en tu repositorio de GitHub. Solo cópialo y pégalo en el archivo `README.md` en tu repositorio. ¡Espero que te sea útil!
