import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_excel("CE_procesado.xlsx")

# Título general
st.title("Probabilidad por tipo de roca")

# Función para graficar
def graficar_probabilidad(tipo_funcion, columna_probabilidad, color):
    df_filtrado = df[df['FUNCIÓN'].str.lower() == tipo_funcion.lower()]
    if df_filtrado.empty:
        st.warning(f"No se encontraron datos para '{tipo_funcion}'.")
        return
    resumen = df_filtrado.groupby("Litología única")[columna_probabilidad].mean().sort_values(ascending=False)

    # Mostrar gráfico
    st.subheader(f"{tipo_funcion.capitalize()}: Probabilidad promedio por litología")
    fig, ax = plt.subplots()
    resumen.plot(kind='bar', color=color, ax=ax)
    ax.set_ylabel(f"% Probabilidad de ser {tipo_funcion.lower()}")
    ax.set_xlabel("Litología")
    st.pyplot(fig)

# Mostrar cada gráfico
graficar_probabilidad("Sello", "% Sello", "#4B4B4B")
graficar_probabilidad("Generadora", "% Gener", "#A0522D")
graficar_probabilidad("Reservorio", "% Reserv", "#1f77b4")
