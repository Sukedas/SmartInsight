# SmartInsight - Gestión de Finanzas Personales

SmartInsight es una aplicación diseñada para registrar, clasificar y analizar transacciones financieras, permitiendo un control detallado de presupuestos y hábitos de gasto.

## Requerimientos Implementados
- **RF1-RF2:** Registro y clasificación de transacciones (ingresos, gastos, recurrentes, esporádicos).
- **RF3:** Visualización de distribución de gastos por categoría (mensual).
- **RF4:** Comparación visual entre presupuesto definido y gasto real.
- **RF5-RF6:** Consulta de movimientos por diferentes periodos y gestión de presupuestos por categoría.
- **RF7:** Identificación del día de mayor gasto en el mes.
- **RF8:** Integración con base de datos de transacciones.
- **RF9, RNF1-RNF5:** Interfaz gráfica clara, multiplataforma, segura y de alto rendimiento.

## Arquitectura (MVC)
El proyecto está estructurado de manera modular usando el patrón Modelo-Vista-Controlador:
- `src/Model/`: Contiene la lógica de negocio, cálculos y manejo de base de datos (`database.py`, `transaction_model.py`, `budget_model.py`).
- `src/View/`: Contiene la interfaz gráfica de usuario y componentes visuales (`main_window.py`, `dashboard_view.py`, `transaction_view.py`).
- `src/Controller/`: Actúa como intermediario conectando la Vista con el Modelo y gestionando eventos (`main_controller.py`, `transaction_controller.py`).

## Instalación
1. Clonar el repositorio.
2. Crear un entorno virtual: `python -m venv venv`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar la aplicación: `python src/main.py`
