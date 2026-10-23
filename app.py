import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de ClimateLab
st.set_page_config(
    page_title="ClimateLab",
    page_icon="🌎",
    layout="wide"
)

# Encabezado
st.title("🌎 ClimateLab")
st.subheader("Laboratorio científico del cambio climático")

st.write(
    "Explora datos, visualiza tendencias y aprende "
    "sobre los cambios del clima."
)

# Datos ilustrativos
datos = pd.DataFrame({
    "Año": [2015, 2017, 2019, 2021, 2023, 2025],
    "Temperatura": [0.90, 0.92, 1.00, 1.11, 1.18, 1.25]
})

# Tabla de datos
st.header("📊 Datos de temperatura")
st.caption("Valores ilustrativos para probar la aplicación.")
st.dataframe(datos, use_container_width=True)

# Gráfica
st.header("📈 Evolución de la temperatura")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    datos["Año"],
    datos["Temperatura"],
    marker="o"
)
ax.set_xlabel("Año")
ax.set_ylabel("Anomalía de temperatura (°C)")
ax.grid(True, alpha=0.3)

st.pyplot(fig)
plt.close(fig)

st.info(
    "Próximamente: datos científicos reales, "
    "análisis físico, químico y biológico."
)