import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="ClimateLab",
    page_icon="🌎",
    layout="wide"
)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #07111f, #102b3f, #102d2a);
        color: #edf6ff;
    }

    [data-testid="stHeader"] {
        background: rgba(7, 17, 31, 0.65);
    }

    h1 {
        color: #63e6be !important;
        font-weight: 800 !important;
    }

    h2 {
        color: #74c0fc !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #d0bfff !important;
    }

    p, label, li {
        color: #e2edf7;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #142b42, #173b42);
        border: 1px solid #3b6979;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.18);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: #63e6be;
    }

    [data-testid="stMetricLabel"] {
        color: #a5c8e6 !important;
    }

    [data-testid="stMetricValue"] {
        color: #63e6be !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #3b6979;
        border-radius: 14px;
        overflow: hidden;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid #3b6979;
    }

    div[data-baseweb="select"] > div {
        background-color: #142b42;
        border-color: #3b6979;
        border-radius: 10px;
    }

    div[data-testid="stSlider"] [role="slider"] {
        background-color: #63e6be;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101d35, #142e39);
        border-right: 1px solid #294b5b;
    }

    #MainMenu, footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌎 ClimateLab")
st.sidebar.title("🌎 ClimateLab")
st.sidebar.caption("Laboratorio científico")

pagina = st.sidebar.radio(
    "Navegación",
    [
        "🏠 Inicio",
        "🌡️ Clima",
        
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Explora. Experimenta. Aprende.")
st.subheader("Laboratorio científico del cambio climático")
st.markdown("""
### 🧬 La vida frente al cambio climático

El cambio climático es una de las principales amenazas para los
ecosistemas del planeta. El aumento de la temperatura, las
alteraciones de las lluvias y los fenómenos meteorológicos extremos
pueden modificar las condiciones en las que viven los organismos.

*¿Cómo afecta a los seres vivos?*

- 🌱 *Plantas:* las sequías y las temperaturas extremas pueden
  dificultar la fotosíntesis, el crecimiento y la reproducción.
- 🐾 *Animales:* algunas especies deben cambiar sus zonas de
  distribución para encontrar alimento y condiciones adecuadas.
- 🌊 *Organismos acuáticos:* el calentamiento del agua puede
  reducir el oxígeno disuelto y alterar los hábitats.
- 🦋 *Biodiversidad:* los cambios ambientales pueden modificar
  las cadenas alimentarias y las relaciones entre especies.

### 🔬 La explicación científica

Los seres vivos dependen de condiciones ambientales específicas.
Cuando la temperatura o la disponibilidad de agua cambian demasiado,
algunas especies logran adaptarse, mientras que otras pueden sufrir
una disminución de sus poblaciones.

Por eso, estudiar el cambio climático también significa estudiar
la biología, la química de la atmósfera y el funcionamiento de los
ecosistemas.
""")

st.write(
    "Explora datos, visualiza tendencias y aprende "
    "sobre los cambios del clima."
)
if pagina == "🏠 Inicio":
    st.success("Bienvenido al centro de investigación ClimateLab.")
    st.write(
        "Explora el cambio climático mediante la física, "
        "la química, la biología y el análisis de datos."
    )

# Datos de temperatura de Berkeley Earth
url = (
    "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/"
    "Global/Land_and_Ocean_complete.txt"
)

try:
    datos = pd.read_csv(
        url,
        sep=r"\s+",
        comment="%",
        header=None,
        usecols=[0, 1, 2],
        names=["Año", "Mes", "Anomalía mensual (°C)"],
        na_values=["NaN"]
    )

    datos["Año"] = pd.to_numeric(datos["Año"], errors="coerce")
    datos["Mes"] = pd.to_numeric(datos["Mes"], errors="coerce")
    datos["Anomalía mensual (°C)"] = pd.to_numeric(
        datos["Anomalía mensual (°C)"],
        errors="coerce"
    )

    datos = datos.dropna(
        subset=["Año", "Mes", "Anomalía mensual (°C)"]
    )

    datos["Año"] = datos["Año"].astype(int)
    datos["Mes"] = datos["Mes"].astype(int)

    datos = datos[
        (datos["Año"] >= 2015)
        & (
            (datos["Año"] < 2026)
            | ((datos["Año"] == 2026) & (datos["Mes"] <= 6))
        )
        & datos["Mes"].between(1, 12)
    ].copy()

    datos["Fecha"] = pd.to_datetime(
        dict(
            year=datos["Año"],
            month=datos["Mes"],
            day=1
        )
    )

    datos = datos.sort_values("Fecha")

    st.success("Datos mensuales cargados para el periodo seleccionado.")

    st.header("📊 Temperatura desde enero de 2015")
    st.dataframe(
        datos[["Fecha", "Anomalía mensual (°C)"]],
        use_container_width=True
    )

    st.header("📈 Comparación anual de temperatura")

    # Promedio anual de las anomalías mensuales
    anual = (
        datos.groupby("Año")["Anomalía mensual (°C)"]
        .mean()
        .reset_index()
    )
    st.header("🌡️ Simulador de temperatura")

    st.write(
        "Modifica las variables y observa cómo responde "
        "este modelo educativo de temperatura."
    )

    aumento = st.slider(
        "Aumento hipotético de temperatura (°C)",
        min_value=0.0,
        max_value=5.0,
        value=5.0,
        step=0.5
    )

    st.metric(
        "Escenario seleccionado",
        f"+{aumento:.1f} °C"
    )

    st.caption(
        "Este control representa un escenario hipotético. "
        "No es una predicción real del clima."
    )

    st.header("🔬 Análisis científico")

    analisis = anual[
        anual["Año"].between(2020, 2024)
    ].sort_values("Año")

    if len(analisis) >= 2:
        primero = analisis.iloc[0]
        ultimo = analisis.iloc[-1]

        diferencia = (
            ultimo["Anomalía mensual (°C)"]
            - primero["Anomalía mensual (°C)"]
        )

        st.subheader("📊 ¿Qué nos dicen los datos?")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                f"Anomalía media en {int(primero['Año'])}",
                f"{primero['Anomalía mensual (°C)']:.2f} °C"
            )

        with col2:
            st.metric(
                f"Anomalía media en {int(ultimo['Año'])}",
                f"{ultimo['Anomalía mensual (°C)']:.2f} °C",
                delta=f"{diferencia:+.2f} °C"
            )

        st.markdown("### 🌡️ Interpretación")

        if diferencia > 0.05:
            st.write(
                f"Entre {int(primero['Año'])} y "
                f"{int(ultimo['Año'])}, la anomalía media anual "
                f"aumentó {diferencia:.2f} °C. Esto indica que "
                "el valor de 2024 fue superior al de 2020."
            )
        elif diferencia < -0.05:
            st.write(
                f"Entre {int(primero['Año'])} y "
                f"{int(ultimo['Año'])}, la anomalía media anual "
                f"disminuyó {abs(diferencia):.2f} °C. Esto indica "
                "que el valor de 2024 fue inferior al de 2020."
            )
        else:
            st.write(
                "Los valores de 2020 y 2024 fueron relativamente "
                "parecidos, aunque eso no significa que la "
                "temperatura se mantuviera estable todos los años."
            )

        st.info(
            "Una anomalía térmica es una diferencia respecto a "
            "un periodo de referencia. Esta comparación muestra "
            "el cambio entre dos años; por sí sola no demuestra "
            "la tendencia de todo el planeta. Las variaciones "
            "anuales también pueden verse influidas por fenómenos "
            "naturales como El Niño."
        )
    else:
        st.warning(
            "Se necesitan datos válidos de al menos dos años "
            "entre 2020 y 2024 para generar el análisis."
        )

    anual = anual[anual["Año"].between(2020, 2026)]

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.plot(
        anual["Año"],
        anual["Anomalía mensual (°C)"],
        marker="o",
        linewidth=2
    )

    ax.set_xlabel("Año")
    ax.set_ylabel("Anomalía media (°C)")
    ax.set_xticks(anual["Año"])
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)
    st.caption(
        "Fuente: Berkeley Earth. Se muestran los meses disponibles "
        "entre enero de 2015 y junio de 2026."
    )
    st.header("🌿 Impacto del cambio climático en los seres vivos")

    st.write(
        "El cambio climático modifica las condiciones ambientales "
        "y puede afectar la supervivencia de plantas, animales "
        "y otros organismos."
    )

    tema = st.selectbox(
        "Selecciona un área para explorar:",
        [
            "🌾 Cultivos y agricultura",
            "🐾 Animales y biodiversidad",
            "🌳 Bosques y ecosistemas",
            "🌊 Ecosistemas acuáticos"
        ]
    )

    if tema == "🌾 Cultivos y agricultura":
        st.subheader("🌾 Efectos en los cultivos")
        st.write(
            "Las temperaturas elevadas y las sequías pueden reducir "
            "el crecimiento de algunas plantas. Las lluvias intensas "
            "también pueden erosionar el suelo y afectar las cosechas."
        )
        st.info(
            "Relación científica: la disponibilidad de agua y la "
            "temperatura influyen en la fotosíntesis y el crecimiento."
        )

    elif tema == "🐾 Animales y biodiversidad":
        st.subheader("🐾 Efectos en los animales")
        st.write(
            "Algunas especies deben desplazarse para encontrar "
            "alimento o condiciones adecuadas. Los cambios de "
            "temperatura también pueden alterar la reproducción "
            "y las relaciones entre especies."
        )
        st.info(
            "Relación científica: la temperatura puede afectar "
            "la distribución de las especies y el equilibrio ecológico."
        )

    elif tema == "🌳 Bosques y ecosistemas":
        st.subheader("🌳 Efectos en los bosques")
        st.write(
            "Las sequías y las olas de calor pueden aumentar el "
            "estrés de los árboles y el riesgo de incendios. "
            "La pérdida de vegetación también afecta los hábitats."
        )
        st.info(
            "Relación científica: los bosques almacenan carbono "
            "y participan en el ciclo del agua."
        )

    else:
        st.subheader("🌊 Efectos en ecosistemas acuáticos")
        st.write(
            "El calentamiento del agua puede reducir el oxígeno "
            "disuelto y alterar los hábitats de peces y otros "
            "organismos. La respuesta depende de la especie "
            "y de las condiciones del ecosistema."
        )
        st.info(
            "Relación científica: la temperatura influye en el "
            "oxígeno disuelto, el metabolismo y la calidad del agua."
        )

    st.header("🧠 Datos curiosos del planeta")

    st.write(
        "Descubre fenómenos científicos que ayudan a comprender "
        "cómo funciona el sistema climático de la Tierra."
    )

    curiosidad = st.selectbox(
        "Elige un tema científico:",
        [
            "🌡️ El efecto invernadero",
            "🌊 Los océanos y el calor",
            "🌳 Los bosques y el carbono",
            "🧊 El hielo y la luz solar",
            "🐠 La vida acuática",
            "🌋 El clima y los volcanes"
        ]
    )

    if curiosidad == "🌡️ El efecto invernadero":
        st.subheader("¿Por qué la atmósfera conserva calor?")
        st.write("""
        La energía del Sol llega a la Tierra principalmente en forma
        de radiación de onda corta. Una parte se refleja hacia el
        espacio y otra es absorbida por la superficie, los océanos
        y la atmósfera. Después, la Tierra libera energía en forma
        de radiación infrarroja.

        Gases como el dióxido de carbono, el metano y el vapor de agua
        absorben y emiten parte de esa radiación infrarroja. Este
        proceso natural ayuda a mantener una temperatura compatible
        con la vida.

        El problema aparece cuando las actividades humanas aumentan
        la concentración de gases de efecto invernadero, especialmente
        al quemar carbón, petróleo y gas o al cambiar el uso del suelo.
        Esto altera el balance energético del planeta y favorece el
        calentamiento global.
        """)
        st.info(
            "Dato científico: el efecto invernadero natural no es "
            "contaminación en sí mismo; el desequilibrio adicional "
            "causado por el aumento de gases es el problema."
        )

    elif curiosidad == "🌊 Los océanos y el calor":
        st.subheader("El enorme regulador térmico de la Tierra")
        st.write("""
        Los océanos absorben gran parte del exceso de calor acumulado
        en el sistema climático. El agua puede almacenar mucha energía
        antes de experimentar un cambio considerable de temperatura.
        Esta propiedad se conoce como calor específico.

        Las corrientes marinas transportan energía entre regiones,
        por lo que influyen en las temperaturas costeras, los patrones
        de lluvia y los ecosistemas. Sin embargo, el calentamiento
        oceánico también puede contribuir a la expansión del agua,
        mientras que la pérdida de hielo terrestre añade agua al mar.

        El océano no elimina el problema del calentamiento global:
        absorbe parte del exceso de energía y también experimenta
        cambios físicos, químicos y biológicos.
        """)
        st.info(
            "Dato científico: el calentamiento del océano puede "
            "afectar a los arrecifes, la distribución de especies "
            "y la disponibilidad de oxígeno disuelto."
        )

    elif curiosidad == "🌳 Los bosques y el carbono":
        st.subheader("Árboles, fotosíntesis y dióxido de carbono")
        st.write("""
        Durante la fotosíntesis, las plantas utilizan energía luminosa
        para transformar agua y dióxido de carbono en compuestos
        orgánicos. En el proceso liberan oxígeno y almacenan carbono
        en sus tejidos.

        Parte de ese carbono permanece en troncos, raíces, hojas y
        suelos durante distintos periodos. Por eso, los bosques son
        importantes dentro del ciclo global del carbono. Sin embargo,
        la cantidad almacenada depende del tipo de bosque, su edad,
        el suelo y las condiciones ambientales.

        La deforestación, los incendios y la degradación forestal
        pueden liberar carbono y reducir la capacidad de los
        ecosistemas para absorber dióxido de carbono.
        """)
        st.info(
            "Dato científico: plantar árboles puede ayudar, pero "
            "proteger los bosques existentes y reducir las emisiones "
            "también es fundamental."
        )

    elif curiosidad == "🧊 El hielo y la luz solar":
        st.subheader("El papel del albedo")
        st.write("""
        El albedo es la proporción de radiación solar que una
        superficie refleja. La nieve y el hielo suelen reflejar
        mucha más luz solar que el océano abierto o los suelos oscuros.

        Cuando se reduce la superficie cubierta por nieve o hielo,
        quedan expuestas superficies que absorben más energía.
        Esto puede intensificar el calentamiento local y favorecer
        una pérdida adicional de hielo: es un ejemplo de
        retroalimentación climática.

        Este mecanismo no actúa de forma aislada; también intervienen
        las nubes, las corrientes oceánicas, la atmósfera y las
        condiciones de cada región.
        """)
        st.info(
            "Dato científico: el albedo conecta la física de la luz "
            "con los cambios observados en las regiones polares."
        )

    elif curiosidad == "🐠 La vida acuática":
        st.subheader("Temperatura, oxígeno y organismos acuáticos")
        st.write("""
        La temperatura influye en la cantidad de oxígeno que puede
        permanecer disuelto en el agua. En general, el agua más
        caliente puede contener menos oxígeno disuelto que el agua
        más fría, si las demás condiciones son comparables.

        Al mismo tiempo, muchos peces y otros organismos ectotermos
        modifican su metabolismo según la temperatura del ambiente.
        Si el agua se calienta demasiado, sus necesidades de oxígeno
        pueden aumentar mientras la disponibilidad de este gas
        disminuye.

        El resultado depende de la especie, la calidad del agua,
        la salinidad, la circulación y otros factores. Por eso,
        medir la temperatura y el oxígeno disuelto es importante
        en la acuicultura y en el manejo de ecosistemas acuáticos.
        """)
        st.info(
            "Dato científico: temperatura y oxígeno disuelto deben "
            "interpretarse juntos para comprender las condiciones "
            "de vida de los organismos acuáticos."
        )

    else:
        st.subheader("Los volcanes y el clima")
        st.write("""
        Las grandes erupciones volcánicas pueden inyectar dióxido
        de azufre en la estratosfera, donde se forman aerosoles
        que reflejan parte de la luz solar. Esto puede provocar
        un enfriamiento temporal de la superficie durante un periodo
        posterior a la erupción.

        El dióxido de carbono volcánico también contribuye al ciclo
        natural del carbono, pero las emisiones humanas actuales
        de dióxido de carbono son mucho mayores que las emisiones
        volcánicas globales.

        Por eso, aunque las erupciones pueden influir en el clima,
        no explican el calentamiento global observado en las últimas
        décadas, que se debe principalmente a las actividades humanas.
        """)
        st.info(
            "Dato científico: una erupción puede enfriar temporalmente "
            "el clima, mientras que el aumento sostenido de gases "
            "de efecto invernadero favorece el calentamiento."
        )

except Exception as e:
    st.error(f"No se pudieron cargar o representar los datos: {e}")
    st.stop()
    