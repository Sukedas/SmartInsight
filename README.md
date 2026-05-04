# SmartInsight - Gestor Financiero

SmartInsight es una aplicación diseñada para gestionar y analizar tus finanzas personales, registrando ingresos y gastos, y comparándolos con tu presupuesto de manera intuitiva y visual. Cumple con todos los requerimientos funcionales y no funcionales especificados.

## Requisitos Previos

Antes de ejecutar la aplicación, asegúrate de tener instalados:

1. **Python 3.8+**: [Descargar Python](https://www.python.org/downloads/)
2. **PostgreSQL**: [Descargar PostgreSQL](https://www.postgresql.org/download/)

## Configuración de la Base de Datos (PostgreSQL)

1. Abre tu herramienta de PostgreSQL (pgAdmin o psql) y crea una nueva base de datos llamada `smartinsight`.
   ```sql
   CREATE DATABASE smartinsight;
   ```
2. Renombra el archivo `.env.example` a `.env` en la raíz del proyecto.
3. Edita el archivo `.env` y configura tus credenciales de PostgreSQL:
   ```env
   DB_HOST=localhost
   DB_NAME=smartinsight
   DB_USER=postgres
   DB_PASSWORD=tu_contraseña_aqui
   DB_PORT=5432
   ```

*Nota: La aplicación creará las tablas necesarias (`transactions` y `budgets`) automáticamente la primera vez que se ejecute.*

## Instalación

1. Clona el repositorio o navega a la carpeta del proyecto en tu terminal:
   ```bash
   cd ruta/al/proyecto/SmartInsight
   ```

2. (Opcional pero recomendado) Crea y activa un entorno virtual:
   ```bash
   # En Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

## Cómo usar y abrir la aplicación

La aplicación utiliza **Streamlit** para proporcionar una interfaz moderna, interactiva y accesible desde cualquier navegador web.

Para iniciar la aplicación, ejecuta el siguiente comando en tu terminal:

```bash
streamlit run app.py
```

Esto abrirá automáticamente una pestaña en tu navegador predeterminado apuntando a `http://localhost:8501`. 

### Navegación en la aplicación
- **Dashboard**: Vista principal con resumen de tu estado financiero, comparación de presupuesto vs gasto (RF4), distribución por categorías (RF3) y el día de mayor gasto (RF7).
- **Registrar Transacción**: Formulario para ingresar nuevos ingresos y gastos, clasificarlos y marcar su naturaleza (RF1, RF2).
- **Gestión de Presupuestos**: Define presupuestos por categoría y periodo (RF6).
- **Historial de Movimientos**: Consulta todos tus movimientos en diferentes escalas de tiempo: diario, semanal, mensual y anual (RF5).

## Estructura del Proyecto

- `app.py`: Archivo principal que contiene la interfaz web de Streamlit y la lógica de la aplicación.
- `db.py`: Módulo para la conexión y configuración de la base de datos PostgreSQL (RF8).
- `requirements.txt`: Dependencias del proyecto.
- `.env`: (A crear por el usuario) Variables de entorno para seguridad (RNF3).
- `Requerimientos App.txt`: Documento de requisitos del proyecto.

> **Nota para el desarrollador/profesor:** La versión anterior del prototipo utilizaba PyQt6. Se ha migrado a Streamlit y PostgreSQL para cumplir de forma óptima con los requisitos de usabilidad (RNF2), visualización de datos de alta calidad (RNF5) y accesibilidad (RNF1). La antigua carpeta `src/` puede ser ignorada o eliminada.
