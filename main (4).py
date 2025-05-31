import streamlit as st
import pandas as pd
import plotly.express as px

# Función para cargar y preparar datos
@st.cache_data
def cargar_datos():
    df = pd.read_excel('Entrenamiento_R3.xlsx')
    df['Fecha de Capa'] = pd.to_datetime(df['Fecha de Capa'], errors='coerce')
    # Crear columna de puntaje promedio de expertise
    expertise_cols = [
        'Nivel de Expertise en Presentación',
        'Nivel de Expertise en Sondeo',
        'Nivel de Expertise en Argumentación',
        'Nivel de Expertise en Rebate',
        'Nivel de Expertise en Cierre'
    ]
    df['Puntaje Promedio'] = df[expertise_cols].mean(axis=1)
    return df

df = cargar_datos()

st.set_page_config(page_title="Dashboard Capacitación", layout="wide")
st.title("📊 Dashboard de Capacitación por Asesor Evaluado")

# Selección del asesor evaluado
asesores = df['Asesor Evaluado'].dropna().unique()
asesor_seleccionado = st.selectbox("🔎 Selecciona el Asesor Evaluado:", sorted(asesores))

df_asesor = df[df['Asesor Evaluado'] == asesor_seleccionado].sort_values('Fecha de Capa')

if df_asesor.empty:
    st.warning("⚠️ No se encontraron datos para el asesor seleccionado.")
else:
    # Estadísticas clave
    total_sesiones = len(df_asesor)
    duracion_total = df_asesor['Duración de Capa'].sum()
    duracion_media = df_asesor['Duración de Capa'].mean()
    puntaje_medio = df_asesor['Puntaje Promedio'].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sesiones Totales", total_sesiones)
    col2.metric("Duración Total (min)", f"{duracion_total:.2f}")
    col3.metric("Duración Media (min)", f"{duracion_media:.2f}")
    col4.metric("Puntaje Promedio", f"{puntaje_medio:.2f}")

    st.markdown("---")

    # Gráfico Duración de sesiones en el tiempo
    fig_duracion = px.bar(
        df_asesor,
        x='Fecha de Capa',
        y='Duración de Capa',
        title="Duración de Capacitación por Fecha",
        labels={'Duración de Capa': 'Duración (minutos)', 'Fecha de Capa': 'Fecha'},
        text='Duración de Capa'
    )
    fig_duracion.update_traces(textposition='outside')
    fig_duracion.update_layout(yaxis_range=[0, max(df_asesor['Duración de Capa']) * 1.2])
    st.plotly_chart(fig_duracion, use_container_width=True)

    # Gráfico Puntaje promedio por sesión
    fig_puntaje = px.line(
        df_asesor,
        x='Fecha de Capa',
        y='Puntaje Promedio',
        markers=True,
        title="Puntaje Promedio por Sesión",
        labels={'Puntaje Promedio': 'Puntaje Promedio', 'Fecha de Capa': 'Fecha'}
    )
    fig_puntaje.update_layout(yaxis_range=[0, 5])  # Asumiendo escala 1-5
    st.plotly_chart(fig_puntaje, use_container_width=True)

    # Tabla con información detallada
    columnas_mostrar = [
        'ID',
        'Evaluador',
        'Fecha de Capa',
        'Duración de Capa',
        'Puntaje Promedio',
        'Detalles o Comentarios Adicionales'
    ]
    st.subheader("📋 Detalles de Sesiones")
    st.dataframe(df_asesor[columnas_mostrar].reset_index(drop=True))

    # Comentarios ampliados por sesión
    st.subheader("📝 Comentarios por Sesión")
    for _, row in df_asesor.iterrows():
        comentario = row['Detalles o Comentarios Adicionales']
        if pd.isna(comentario):
            comentario = "_No hay comentarios._"
        st.markdown(f"**Sesión ID {row['ID']} ({row['Fecha de Capa'].date()}):** {comentario}")