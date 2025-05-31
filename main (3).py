import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def cargar_datos():
    df = pd.read_excel('Entrenamiento_R3.xlsx')
    df['Fecha de Capa'] = pd.to_datetime(df['Fecha de Capa'], errors='coerce')
    df['Fecha de Inicio'] = pd.to_datetime(df['Fecha de Inicio'], errors='coerce')
    return df

df = cargar_datos()

st.title("Dashboard Completo de Capacitación - Entrenamiento R³")

# --- FILTROS ---
ejecutivos = df['Asesor Evaluado'].dropna().unique()
evaluadores = df['Evaluador'].dropna().unique()

# Selección de filtros
ejecutivo_seleccionado = st.selectbox("Selecciona el Ejecutivo (Asesor Evaluado):", sorted(ejecutivos))
evaluador_seleccionado = st.selectbox("Selecciona el Capacitador (Evaluador):", ["Todos"] + sorted(evaluadores))

fecha_min = df['Fecha de Capa'].min()
fecha_max = df['Fecha de Capa'].max()

fecha_inicio, fecha_fin = st.date_input("Selecciona rango de fechas (Fecha de Capa):",
                                        [fecha_min, fecha_max])

# --- FILTRAR DATOS ---
df_filtrado = df[df['Asesor Evaluado'] == ejecutivo_seleccionado]

if evaluador_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Evaluador'] == evaluador_seleccionado]

df_filtrado = df_filtrado[(df_filtrado['Fecha de Capa'] >= pd.to_datetime(fecha_inicio)) &
                          (df_filtrado['Fecha de Capa'] <= pd.to_datetime(fecha_fin))]

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
else:
    st.subheader(f"Información general para: {ejecutivo_seleccionado}")

    # Tabla resumen con columnas relevantes
    columnas_mostrar = ['ID', 'Evaluador', 'Fecha de Capa', 'Duración de Capa',
                        'Nivel de Expertise en Presentación',
                        'Nivel de Expertise en Sondeo',
                        'Nivel de Expertise en Argumentación',
                        'Nivel de Expertise en Rebate',
                        'Nivel de Expertise en Cierre',
                        'Detalles o Comentarios Adicionales']
    st.dataframe(df_filtrado[columnas_mostrar].reset_index(drop=True))

    # Calcular puntaje promedio por fila
    expertise_cols = [
        'Nivel de Expertise en Presentación',
        'Nivel de Expertise en Sondeo',
        'Nivel de Expertise en Argumentación',
        'Nivel de Expertise en Rebate',
        'Nivel de Expertise en Cierre'
    ]
    df_filtrado['Puntaje Promedio'] = df_filtrado[expertise_cols].mean(axis=1)

    # GRÁFICO 1: Duración de capacitación en el tiempo
    fig_duracion = px.line(df_filtrado.sort_values('Fecha de Capa'),
                           x='Fecha de Capa',
                           y='Duración de Capa',
                           title='Duración de Capacitación en el Tiempo',
                           markers=True)
    st.plotly_chart(fig_duracion, use_container_width=True)

    # GRÁFICO 2: Puntaje promedio por sesión en el tiempo
    fig_puntaje = px.bar(df_filtrado.sort_values('Fecha de Capa'),
                         x='Fecha de Capa',
                         y='Puntaje Promedio',
                         title='Puntaje Promedio por Sesión',
                         labels={'Puntaje Promedio': 'Puntaje Promedio', 'Fecha de Capa': 'Fecha'})
    st.plotly_chart(fig_puntaje, use_container_width=True)

    # Estadísticas generales
    st.subheader("Estadísticas generales")
    duracion_media = df_filtrado['Duración de Capa'].mean()
    puntaje_medio = df_filtrado['Puntaje Promedio'].mean()

    st.write(f"- Duración media de capacitación: {duracion_media:.2f} minutos")
    st.write(f"- Puntaje promedio general: {puntaje_medio:.2f}")

    # Mostrar resumen/comentarios de todas las sesiones filtradas
    st.subheader("Resumen / Comentarios de sesiones")
    for idx, row in df_filtrado.iterrows():
        comentario = row['Detalles o Comentarios Adicionales']
        if pd.isna(comentario):
            comentario = "No hay comentarios."
        st.markdown(f"**Sesión ID {row['ID']} ({row['Fecha de Capa'].date()}):** {comentario}")