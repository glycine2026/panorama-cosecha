import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Panorama de cosecha", page_icon="🌾", layout="wide")

logo_col, titulo_col = st.columns([1,6])

with logo_col:
    st.image("logo.png", width=120)

with titulo_col:
    st.title("Panorama de cosecha")

# =============================
# CARGAR MAESTROS DESDE EXCEL
# =============================

campos_loc = pd.read_excel("maestros.xlsx", sheet_name="campos_localidades")
socios_df = pd.read_excel("maestros.xlsx", sheet_name="socios")
especies_df = pd.read_excel("maestros.xlsx", sheet_name="especies")
estado_df = pd.read_excel("maestros.xlsx", sheet_name="estado_cupo")

campos = sorted(campos_loc["Campo"].dropna().unique())
socios = sorted(socios_df["Socio"].dropna().unique())
especies = sorted(especies_df["Especie"].dropna().unique())
estados = sorted(estado_df["Estado"].dropna().unique())

# =============================
# TABLA EN MEMORIA
# =============================

if "tabla" not in st.session_state:
    st.session_state.tabla = pd.DataFrame(
        columns=[
            "Fecha",
            "Campo",
            "Localidad",
            "Especie",
            "Destino",
            "Cupos",
            "Socio",
            "Estado"
        ]
    )

# =============================
# FORMULARIO DE CARGA
# =============================

st.subheader("Carga de datos")

col1, col2, col3 = st.columns(3)

with col1:
    fecha = st.date_input("Fecha", value=date.today())
    campo = st.selectbox("Campo", campos)
    especie = st.selectbox("Especie", especies)

with col2:
    # Localidades dependientes del campo
    localidades_filtradas = campos_loc[campos_loc["Campo"] == campo]["Localidad"].unique()
    localidad = st.selectbox("Localidad", sorted(localidades_filtradas))
    socio = st.selectbox("Socio", socios)

with col3:
    destino = st.text_input("Destino")
    cupos = st.number_input("Cupos", min_value=0)
    estado = st.selectbox("Estado del cupo", estados)

# =============================
# BOTON AGREGAR FILA
# =============================

if st.button("Agregar fila"):

    nueva_fila = pd.DataFrame(
        [[fecha, campo, localidad, especie, destino, cupos, socio, estado]],
        columns=[
            "Fecha",
            "Campo",
            "Localidad",
            "Especie",
            "Destino",
            "Cupos",
            "Socio",
            "Estado"
        ]
    )

    st.session_state.tabla = pd.concat(
        [st.session_state.tabla, nueva_fila],
        ignore_index=True
    )

# =============================
# MOSTRAR TABLA
# =============================

st.subheader("Panorama cargado")

st.dataframe(
    st.session_state.tabla,
    use_container_width=True
)

# =============================
# DESCARGAR CSV
# =============================

csv = st.session_state.tabla.to_csv(index=False).encode("utf-8")

st.download_button(
    "Descargar CSV",
    csv,
    "panorama_cosecha.csv",
    "text/csv"
)
