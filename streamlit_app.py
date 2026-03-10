import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Panorama de cosecha", page_icon="🌾", layout="wide")

# =============================
# ESTILOS
# =============================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.card {
    background-color: white;
    padding: 1.4rem;
    border-radius: 16px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
    margin-bottom: 1.2rem;
}

.section-title {
    color: #006651;
    font-weight: 700;
    margin-bottom: 0.8rem;
}

.kpi-card {
    background-color: white;
    padding: 1rem 1.2rem;
    border-radius: 14px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    border-left: 6px solid #006651;
}

.kpi-label {
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 0.2rem;
}

.kpi-value {
    color: #1F2933;
    font-size: 1.6rem;
    font-weight: 700;
}

.report-title {
    color: #006651;
    font-weight: 800;
    font-size: 2.4rem;
    margin-top: 0.4rem;
}

.report-subtitle {
    color: #6b7280;
    font-size: 1rem;
    margin-top: -0.2rem;
}

div.stButton > button {
    background-color: #006651;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
}

div.stDownloadButton > button {
    background-color: #006651;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: 600;
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
# HEADER
# =============================
logo_col, titulo_col = st.columns([1, 7])

with logo_col:
    st.image("logo.png", width=110)

with titulo_col:
    st.markdown('<div class="report-title">Panorama de cosecha</div>', unsafe_allow_html=True)
    st.markdown('<div class="report-subtitle">Reporte operativo institucional</div>', unsafe_allow_html=True)

st.write("")

# =============================
# METRICAS
# =============================
df_actual = st.session_state.tabla.copy()

total_cupos = int(df_actual["Cupos"].sum()) if not df_actual.empty else 0
total_registros = len(df_actual)
total_campos = df_actual["Campo"].nunique() if not df_actual.empty else 0

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total de cupos</div>
        <div class="kpi-value">{total_cupos}</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Registros cargados</div>
        <div class="kpi-value">{total_registros}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Campos activos</div>
        <div class="kpi-value">{total_campos}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =============================
# CARGA DE DATOS
# =============================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Carga de datos</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    fecha = st.date_input("Fecha", value=date.today())
    campo = st.selectbox("Campo", campos)
    especie = st.selectbox("Especie", especies)

with col2:
    localidades_filtradas = campos_loc[campos_loc["Campo"] == campo]["Localidad"].dropna().unique()
    localidad = st.selectbox("Localidad", sorted(localidades_filtradas))
    socio = st.selectbox("Socio", socios)

with col3:
    destino = st.text_input("Destino")
    cupos = st.number_input("Cupos", min_value=0, step=1)
    estado = st.selectbox("Estado del cupo", estados)

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
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# =============================
# TABLA REPORTE
# =============================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Panorama cargado</div>', unsafe_allow_html=True)

df_mostrar = st.session_state.tabla.copy()

if not df_mostrar.empty:
    df_mostrar["Fecha"] = pd.to_datetime(df_mostrar["Fecha"]).dt.strftime("%d/%m/%Y")

st.dataframe(
    df_mostrar,
    use_container_width=True,
    hide_index=True
)

csv = st.session_state.tabla.to_csv(index=False).encode("utf-8-sig")

st.write("")
st.download_button(
    "Descargar CSV",
    csv,
    "panorama_cosecha.csv",
    "text/csv"
)

st.markdown('</div>', unsafe_allow_html=True)
