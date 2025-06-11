import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Cargar datos
df = pd.read_excel("CE_procesado.xlsx")

# Título general
st.title("Análisis Petrológico de Litologías")

# ==== 1. Resumen de espesores ====
st.header("Resumen de espesores acumulados por tipo de roca")
espesores = df.groupby("FUNCION")["ESPESOR"].sum()
espesor_sello = espesores.get("Sello", 0)
espesor_generadora = espesores.get("Generadora", 0)
espesor_reservorio = espesores.get("Reservorio", 0)

st.markdown(f"- **Roca Sello:** {espesor_sello} m")
st.markdown(f"- **Roca Generadora:** {espesor_generadora} m")
st.markdown(f"- **Roca Reservorio:** {espesor_reservorio} m")

st.subheader("Comparación visual de espesores por tipo de roca")
fig1, ax1 = plt.subplots()
ax1.bar(["Sello", "Generadora", "Reservorio"],
        [espesor_sello, espesor_generadora, espesor_reservorio],
        color=["#4B4B4B", "#A0522D", "#1f77b4"])
ax1.set_ylabel("Espesor total (m)")
st.pyplot(fig1)

# ==== 2. Gráficos de probabilidad por tipo de roca ====
def graficar_probabilidad(tipo_funcion, columna_probabilidad, color):
    df_filtrado = df[df['FUNCION'].str.lower() == tipo_funcion.lower()]
    if df_filtrado.empty:
        st.warning(f"No se encontraron datos para '{tipo_funcion}'.")
        return
    resumen = df_filtrado.groupby("Litología única")[columna_probabilidad].mean().sort_values(ascending=False)

    st.subheader(f"{tipo_funcion.capitalize()}: Probabilidad promedio por litología")
    fig, ax = plt.subplots()
    resumen.plot(kind='bar', color=color, ax=ax)
    ax.set_ylabel(f"% Probabilidad de ser {tipo_funcion.lower()}")
    ax.set_xlabel("Litología")
    st.pyplot(fig)

graficar_probabilidad("Sello", "% Sello", "#4B4B4B")
graficar_probabilidad("Generadora", "% Roca Madre", "#A0522D")
graficar_probabilidad("Reservorio", "% Reservorio", "#1f77b4")

# ==== 3. Cálculo de función principal y gráfico de dispersión ====
st.header("Relación Tamaño de Grano vs. Permeabilidad (función dominante > 50%)")

# Calcular función dominante
def funcion_principal(row):
    funciones = {
        'Reservorio': row['% Reservorio'],
        'Sello': row['% Sello'],
        'Roca Madre': row['% Roca Madre']
    }
    top = max(funciones, key=funciones.get)
    return top if funciones[top] > 50 else 'No significativa'

df['Función principal'] = df.apply(funcion_principal, axis=1)
df_sig = df[df['Función principal'] != 'No significativa'].copy()

# Renombrar si es necesario
if 'Sentido de gradación' in df_sig.columns:
    df_sig.rename(columns={'Sentido de gradación': 'Gradación'}, inplace=True)

# Clasificar permeabilidad
def clasificar_perm(valor):
    if valor >= 70:
        return 'Alta permeabilidad'
    elif valor >= 30:
        return 'Media permeabilidad'
    else:
        return 'Baja permeabilidad'

df_sig['Clasificación permeabilidad'] = df_sig['Permeabilidad (1-100)'].apply(clasificar_perm)

# Gráfico de dispersión interactivo
fig_scatter = px.scatter(
    df_sig,
    x='Tamaño de grano (1-100)',
    y='Permeabilidad (1-100)',
    color='Función principal',
    size='ESPESOR',
    hover_name='Litología única',
    title="Relación entre Tamaño de Grano y Permeabilidad",
    labels={
        'Tamaño de grano (1-100)': 'Tamaño de grano',
        'Permeabilidad (1-100)': 'Permeabilidad',
        'ESPESOR': 'Espesor (m)'
    }
)
st.plotly_chart(fig_scatter, use_container_width=True)
