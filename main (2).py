import streamlit as st
import pandas as pd

@st.cache_data
def cargar_datos():
    df = pd.read_excel('Entrenamiento_R3.xlsx')
    df['Fecha de Capa'] = pd.to_datetime(df['Fecha de Capa'], errors='coerce')
    df['Fecha de Inicio'] = pd.to_datetime(df['Fecha de Inicio'], errors='coerce')
    return df

df = cargar_datos()

st.title("Dashboard de Capacitación - Entrenamiento R³")

ejecutivos = df['Asesor Evaluado'].dropna().unique()
ejecutivo_seleccionado = st.selectbox("Selecciona el Ejecutivo (Asesor Evaluado):", sorted(ejecutivos))

df_filtrado = df[df['Asesor Evaluado'] == ejecutivo_seleccionado]

if df_filtrado.empty:
    st.warning("No hay datos para el ejecutivo seleccionado.")
else:
    st.subheader(f"Información de capacitación para: {ejecutivo_seleccionado}")
    for idx, row in df_filtrado.iterrows():
        st.markdown(f"### Sesión ID: {row['ID']}")
        st.write(f"**Capacitador (Evaluador):** {row['Evaluador']}")
        st.write(f"**Fecha de Capacitación:** {row['Fecha de Capa'].date() if pd.notnull(row['Fecha de Capa']) else 'No disponible'}")
        st.write(f"**Duración (minutos):** {round(row['Duración de Capa'], 2)}")

        expertise_cols = [
            'Nivel de Expertise en Presentación',
            'Nivel de Expertise en Sondeo',
            'Nivel de Expertise en Argumentación',
            'Nivel de Expertise en Rebate',
            'Nivel de Expertise en Cierre'
        ]
        niveles = row[expertise_cols].dropna()
        if not niveles.empty:
            puntaje_promedio = niveles.mean()
            st.write(f"**Puntaje Promedio de Expertise:** {puntaje_promedio:.2f}")
        else:
            st.write("**Puntaje Promedio de Expertise:** No disponible")

        comentarios = row['Detalles o Comentarios Adicionales']
        if pd.isna(comentarios):
            comentarios = "No hay comentarios."
        st.write(f"**Resumen / Comentarios:** {comentarios}")
        st.markdown("---")

    st.subheader("Tabla completa de sesiones para este ejecutivo")
    st.dataframe(df_filtrado)