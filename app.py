import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from db import get_db_connection, init_db

# Configuración de página
st.set_page_config(page_title="SmartInsight - Finanzas", page_icon="💰", layout="wide")

# Inicializar Base de Datos
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

# Funciones de utilidad de la DB
def get_data(query, params=()):
    conn = get_db_connection()
    if conn is None:
        st.error("No se pudo conectar a la base de datos PostgreSQL. Verifica tus credenciales.")
        return pd.DataFrame()
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    finally:
        conn.close()

def execute_query(query, params=()):
    conn = get_db_connection()
    if conn is None:
        st.error("No se pudo conectar a la base de datos PostgreSQL. Verifica tus credenciales.")
        return False
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        st.error(f"Error en la operación: {e}")
        return False
    finally:
        conn.close()

# Título y Sidebar
st.sidebar.title("💰 SmartInsight")
st.sidebar.markdown("Tu gestor financiero inteligente")
menu = st.sidebar.radio("Navegación", ["Dashboard", "Registrar Transacción", "Gestión de Presupuestos", "Historial de Movimientos"])

# --- DASHBOARD ---
if menu == "Dashboard":
    st.title("📊 Dashboard Financiero")
    
    # Filtro de tiempo (RF5)
    st.sidebar.subheader("Filtro de Tiempo")
    period_filter = st.sidebar.selectbox("Periodo", ["Este Mes", "Mes Pasado", "Este Año", "Histórico Total"])
    
    today = date.today()
    if period_filter == "Este Mes":
        start_date = today.replace(day=1)
        end_date = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    elif period_filter == "Mes Pasado":
        end_date = today.replace(day=1) - timedelta(days=1)
        start_date = end_date.replace(day=1)
    elif period_filter == "Este Año":
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
    else:
        start_date = date(2000, 1, 1)
        end_date = date(2100, 12, 31)
    
    # Obtener datos
    df = get_data("SELECT * FROM transactions WHERE date >= %s AND date <= %s", (start_date, end_date))
    
    if df.empty:
        st.info("No hay transacciones registradas para este periodo.")
    else:
        # Métricas principales
        ingresos = df[df['type'] == 'Ingreso']['amount'].sum()
        gastos = df[df['type'] == 'Gasto']['amount'].sum()
        balance = ingresos - gastos
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Ingresos Totales", f"${ingresos:,.2f}", "+")
        col2.metric("Gastos Totales", f"${gastos:,.2f}", "-")
        col3.metric("Balance", f"${balance:,.2f}", f"{balance:,.2f}")
        
        st.markdown("---")
        
        col_charts1, col_charts2 = st.columns(2)
        
        with col_charts1:
            # RF3: Visualización de gastos por categoría
            st.subheader("Distribución de Gastos por Categoría")
            df_gastos = df[df['type'] == 'Gasto']
            if not df_gastos.empty:
                gastos_por_cat = df_gastos.groupby('category')['amount'].sum().reset_index()
                fig_pie = px.pie(gastos_por_cat, values='amount', names='category', hole=0.4, 
                                 color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No hay gastos registrados.")
                
        with col_charts2:
            # RF2: Clasificación de transacciones (Naturaleza)
            st.subheader("Gastos por Naturaleza")
            if not df_gastos.empty:
                gastos_nat = df_gastos.groupby('is_recurring')['amount'].sum().reset_index()
                gastos_nat['Naturaleza'] = gastos_nat['is_recurring'].map({True: 'Recurrente', False: 'Esporádico'})
                fig_bar = px.bar(gastos_nat, x='Naturaleza', y='amount', color='Naturaleza',
                                 color_discrete_map={'Recurrente': '#1f77b4', 'Esporádico': '#ff7f0e'})
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No hay gastos registrados.")

        st.markdown("---")
        
        # RF4: Comparación Presupuesto vs Gasto
        st.subheader("Presupuesto vs Gasto Real (Este Mes)")
        current_period = today.strftime("%Y-%m")
        df_budgets = get_data("SELECT * FROM budgets WHERE period = %s", (current_period,))
        
        if not df_budgets.empty and not df_gastos.empty:
            # Consolidar gastos
            gasto_actual = df_gastos.groupby('category')['amount'].sum().reset_index()
            gasto_actual.rename(columns={'amount': 'Gasto Real'}, inplace=True)
            
            # Cruzar con presupuestos
            presupuestos = df_budgets[['category', 'amount']].rename(columns={'amount': 'Presupuesto'})
            comparacion = pd.merge(presupuestos, gasto_actual, on='category', how='left').fillna(0)
            
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(x=comparacion['category'], y=comparacion['Presupuesto'], name='Presupuesto', marker_color='lightgray'))
            fig_comp.add_trace(go.Bar(x=comparacion['category'], y=comparacion['Gasto Real'], name='Gasto Real', marker_color='indianred'))
            fig_comp.update_layout(barmode='group', xaxis_title='Categoría', yaxis_title='Monto ($)')
            st.plotly_chart(fig_comp, use_container_width=True)
        else:
            st.info("No hay presupuestos definidos para este mes o no hay gastos para comparar.")

        st.markdown("---")

        # RF7: Día de mayor gasto
        if not df_gastos.empty:
            gasto_diario = df_gastos.groupby('date')['amount'].sum().reset_index()
            dia_max_gasto = gasto_diario.loc[gasto_diario['amount'].idxmax()]
            st.warning(f"🚨 **Día de mayor gasto:** {dia_max_gasto['date']} con un total de **${dia_max_gasto['amount']:,.2f}**")

# --- REGISTRAR TRANSACCIÓN ---
elif menu == "Registrar Transacción":
    st.title("➕ Registrar Transacción (RF1)")
    
    with st.form("transaccion_form"):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha", date.today())
            monto = st.number_input("Monto ($)", min_value=0.01, format="%.2f")
            tipo = st.selectbox("Tipo de Transacción", ["Gasto", "Ingreso"])
        
        with col2:
            categorias = ["Comida", "Transporte", "Vivienda", "Ocio", "Salud", "Educación", "Salario", "Otros"]
            categoria = st.selectbox("Categoría", categorias)
            recurrente = st.checkbox("¿Es un gasto recurrente? (RF2)")
            descripcion = st.text_area("Descripción (Opcional)")
            
        submit = st.form_submit_button("Guardar Transacción")
        
        if submit:
            query = """
                INSERT INTO transactions (date, amount, category, type, is_recurring, description)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            if execute_query(query, (fecha, monto, categoria, tipo, recurrente, descripcion)):
                st.success("✅ Transacción registrada exitosamente.")

# --- GESTIÓN DE PRESUPUESTOS ---
elif menu == "Gestión de Presupuestos":
    st.title("🎯 Gestión de Presupuestos (RF6)")
    
    with st.form("presupuesto_form"):
        col1, col2 = st.columns(2)
        with col1:
            categorias = ["Comida", "Transporte", "Vivienda", "Ocio", "Salud", "Educación", "General", "Otros"]
            categoria = st.selectbox("Categoría", categorias)
            monto = st.number_input("Monto del Presupuesto ($)", min_value=1.0, format="%.2f")
            
        with col2:
            mes = st.selectbox("Mes", range(1, 13), index=date.today().month - 1)
            anio = st.number_input("Año", min_value=2000, value=date.today().year)
            periodo = f"{anio}-{mes:02d}"
            
        submit = st.form_submit_button("Definir Presupuesto")
        
        if submit:
            query = """
                INSERT INTO budgets (category, amount, period)
                VALUES (%s, %s, %s)
                ON CONFLICT (category, period) 
                DO UPDATE SET amount = EXCLUDED.amount
            """
            if execute_query(query, (categoria, monto, periodo)):
                st.success(f"✅ Presupuesto para {categoria} en {periodo} guardado exitosamente.")
                
    st.markdown("### Presupuestos Actuales")
    df_b = get_data("SELECT * FROM budgets ORDER BY period DESC, category")
    if not df_b.empty:
        st.dataframe(df_b, use_container_width=True)
    else:
        st.info("No hay presupuestos registrados.")

# --- HISTORIAL DE MOVIMIENTOS ---
elif menu == "Historial de Movimientos":
    st.title("📋 Historial de Movimientos (RF5)")
    
    escala = st.radio("Ver por:", ["Diario", "Semanal", "Mensual", "Anual"], horizontal=True)
    
    df_all = get_data("SELECT * FROM transactions ORDER BY date DESC")
    
    if not df_all.empty:
        df_all['date'] = pd.to_datetime(df_all['date'])
        
        if escala == "Diario":
            resumen = df_all.groupby(['date', 'type'])['amount'].sum().unstack().fillna(0)
        elif escala == "Semanal":
            resumen = df_all.groupby([pd.Grouper(key='date', freq='W-MON'), 'type'])['amount'].sum().unstack().fillna(0)
        elif escala == "Mensual":
            resumen = df_all.groupby([pd.Grouper(key='date', freq='M'), 'type'])['amount'].sum().unstack().fillna(0)
        elif escala == "Anual":
            resumen = df_all.groupby([pd.Grouper(key='date', freq='Y'), 'type'])['amount'].sum().unstack().fillna(0)
            
        st.line_chart(resumen)
        
        st.markdown("### Detalle de Transacciones")
        st.dataframe(df_all.sort_values(by="date", ascending=False), use_container_width=True)
    else:
        st.info("No hay transacciones registradas.")
