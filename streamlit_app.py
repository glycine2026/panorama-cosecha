import streamlit as st
import pandas as pd
from datetime import date, datetime

st.set_page_config(page_title="Panorama de cosecha", page_icon="🌾", layout="wide")

fecha_creacion = datetime.now().strftime("%d/%m/%Y")

# =============================
# ESTILOS
# =============================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

.card {
    background-color: white;
    padding: 1.2rem;
    border-radius: 10px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}

.section-title {
    color: #006651;
    font-weight: 700;
    margin-bottom: 0.6rem;
}

.report-title {
    color: #006651;
    font-size: 2.2rem;
    font-weight: 800;
}

.report-subtitle {
    color: #6b7280;
}

</style>
""", unsafe_allow_html=True)

# =============================
# CARGAR MAESTROS
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
    st.session_state.tabla = pd.DataFrame(columns=[
        "Fecha","Campo","Localidad","Especie",
        "Transporte","Destino","Cupos","Socio",
        "Estado","Observaciones"
    ])

# =============================
# HEADER
# =============================

logo_col, titulo_col = st.columns([1.5,6])

with logo_col:
    st.image("logo.png", width=200)

with titulo_col:
    st.markdown(f"""
    <div style="padding-top:20px">
        <div class="report-title">Panorama de cosecha</div>
        <div class="report-subtitle">Distribución de camiones</div>
    </div>
    """, unsafe_allow_html=True)

# =============================
# METRICAS
# =============================

df_actual = st.session_state.tabla

total_cupos = int(df_actual["Cupos"].sum()) if not df_actual.empty else 0
total_registros = len(df_actual)
total_campos = df_actual["Campo"].nunique() if not df_actual.empty else 0

m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Total de cupos", total_cupos)

with m2:
    st.metric("Registros cargados", total_registros)

with m3:
    st.metric("Campos activos", total_campos)

st.write("")

# =============================
# FORMULARIO
# =============================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Carga de datos</div>', unsafe_allow_html=True)

c1,c2,c3 = st.columns(3)

with c1:
    fecha = st.date_input("Fecha", value=date.today())
    campo = st.selectbox("Campo", campos)
    especie = st.selectbox("Especie", especies)

with c2:
    localidades = campos_loc[campos_loc["Campo"]==campo]["Localidad"].dropna().unique()
    localidad = st.selectbox("Localidad", sorted(localidades))
    socio = st.selectbox("Socio", socios)

with c3:
    transporte = st.selectbox("Tipo transporte", ["Camión","Bolsón"])
    destino = st.text_input("Destino")
    cupos = st.number_input("Cupos", min_value=0, step=1)

estado = st.selectbox("Estado del cupo", estados)
observaciones = st.text_input("Observaciones")

# =============================
# BOTONES
# =============================

b1,b2,b3 = st.columns(3)

with b1:
    if st.button("Agregar fila"):

        nueva = pd.DataFrame(
            [[fecha,campo,localidad,especie,transporte,destino,cupos,socio,estado,observaciones]],
            columns=[
                "Fecha","Campo","Localidad","Especie","Transporte",
                "Destino","Cupos","Socio","Estado","Observaciones"
            ]
        )

        st.session_state.tabla = pd.concat([st.session_state.tabla,nueva], ignore_index=True)
        st.rerun()

with b2:
    if st.button("Eliminar última fila"):
        if not st.session_state.tabla.empty:
            st.session_state.tabla = st.session_state.tabla.iloc[:-1]
            st.rerun()

with b3:
    if st.button("Resetear tabla"):
        st.session_state.tabla = st.session_state.tabla.iloc[0:0]
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# =============================
# COLOR ESTADO
# =============================

def color_estado(val):

    if val == "Confirmado con Cupo":
        return "background-color:#d1fae5;font-weight:bold"

    if val == "Confirmado sin Cupo":
        return "background-color:#fef3c7;font-weight:bold"

    if val == "Solicitado":
        return "background-color:#fef3c7;font-weight:bold"

    if val == "Cancelado":
        return "background-color:#fee2e2;font-weight:bold"

    return ""

# =============================
# TABLA PRINCIPAL
# =============================

st.markdown('<div class="card">', unsafe_allow_html=True)

titulo,logo = st.columns([6,1])

with titulo:
    st.markdown(f"""
    <div style="font-weight:700;font-size:18px;color:#006651">
    Distribución de camiones
    </div>
    <div style="color:#374151;font-size:14px;font-weight:700">
    Creado el: {fecha_creacion}
    </div>
    """, unsafe_allow_html=True)

with logo:
    st.image("logo.png", width=90)

df = st.session_state.tabla.copy()

if not df.empty:
    df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime("%d/%m/%Y")

tabla_estilo = (
    df.style
    .hide(axis="index")
    .set_properties(**{
        "text-align":"center",
        "color":"black",
        "background-color":"white",
        "font-size":"13px"
    })
    .set_table_styles([
        {"selector":"th","props":[
            ("background","#f3f4f6"),
            ("color","black"),
            ("font-weight","bold"),
            ("text-align","center"),
            ("padding","4px"),
            ("border","1px solid #d1d5db")
        ]},
        {"selector":"td","props":[
            ("padding","4px"),
            ("border","1px solid #e5e7eb")
        ]}
    ])
    .applymap(color_estado, subset=["Estado"])
)

st.markdown(tabla_estilo.to_html(), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =============================
# RESUMEN
# =============================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Resumen por socio y especie</div>', unsafe_allow_html=True)

if not st.session_state.tabla.empty:

    resumen = (
        st.session_state.tabla
        .groupby(["Fecha","Socio","Especie"])["Cupos"]
        .sum()
        .reset_index()
    )

    resumen["Fecha"] = pd.to_datetime(resumen["Fecha"]).dt.strftime("%d/%m/%Y")

    st.table(resumen)

st.markdown('</div>', unsafe_allow_html=True)

# =============================
# DESCARGA CSV
# =============================

fecha_archivo = datetime.now().strftime("%Y-%m-%d")

csv = st.session_state.tabla.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    "Descargar Excel",
    csv,
    f"panorama_cosecha_{fecha_archivo}.csv",
    "text/csv"
)
