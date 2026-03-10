import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Panorama de cosecha", page_icon="🌾", layout="wide")

st.title("Panorama de cosecha")

# listas iniciales (después las vamos a leer desde un Excel)
campos = ["Campo Norte", "Campo Sur", "Campo Este"]
localidades = ["Pergamino", "Rojas", "Junin"]
socios = ["Socio A", "Socio B", "Socio C"]

# crear tabla en memoria
if "tabla" not in st.session_state:
    st.session_state.tabla = pd.DataFrame(
        columns=["Fecha","Campo","Localidad","Destino","Cupos","Socio"]
    )

st.subheader("Carga de datos")

col1, col2, col3 = st.columns(3)

with col1:
    fecha = st.date_input("Fecha", value=date.today())
    campo = st.selectbox("Campo", campos)

with col2:
    localidad = st.selectbox("Localidad", localidades)
    socio = st.selectbox("Socio", socios)

with col3:
    destino = st.text_input("Destino")
    cupos = st.number_input("Cupos", min_value=0)

if st.button("Agregar fila"):

    nueva_fila = pd.DataFrame(
        [[fecha,campo,localidad,destino,cupos,socio]],
        columns=["Fecha","Campo","Localidad","Destino","Cupos","Socio"]
    )

    st.session_state.tabla = pd.concat(
        [st.session_state.tabla, nueva_fila],
        ignore_index=True
    )

st.subheader("Panorama cargado")

st.dataframe(st.session_state.tabla, use_container_width=True)

# descarga
csv = st.session_state.tabla.to_csv(index=False).encode("utf-8")

st.download_button(
    "Descargar CSV",
    csv,
    "panorama_cosecha.csv",
    "text/csv"
)
