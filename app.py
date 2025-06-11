import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_excel("CE_procesado.xlsx")

# Título general
st.title("Probabilidad por tipo de roca")

# Función para graficar
def graficar_probabilidad(tipo_funcion, columna_probabilidad, color):
    df_filtrado = df[df['FUNCION'].str.lower() == tipo_funcion.lower()]
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
graficar_probabilidad("Generadora", "% Roca Madre", "#A0522D")
graficar_probabilidad("Reservorio", "% Reservorio", "#1f77b4")
# Mostrar resumen de espesores por tipo de roca
st.header("Resumen de espesores acumulados por tipo de roca")

# Agrupar y sumar espesores
espesores = df.groupby("FUNCION")["ESPESOR"].sum()

# Filtrar los tipos clave
espesor_sello = espesores.get("Sello", 0)
espesor_generadora = espesores.get("Generadora", 0)
espesor_reservorio = espesores.get("Reservorio", 0)

# Mostrar resultados
st.markdown(f"- **Roca Sello:** {espesor_sello} m")
st.markdown(f"- **Roca Generadora:** {espesor_generadora} m")
st.markdown(f"- **Roca Reservorio:** {espesor_reservorio} m")
