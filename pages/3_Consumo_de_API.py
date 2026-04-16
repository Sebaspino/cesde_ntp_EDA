import streamlit as st
import pandas as pd
import requests

# Configuración de la página
st.set_page_config(
    page_title="SerenityLab - Bienestar Psicológico CESDE",
    page_icon="🧘",
    layout="wide"
)

st.title("🧘 SerenityLab — Gestión de Bienestar Psicológico")
st.markdown("""
### Objetivo
Esta plataforma centraliza los recursos de bienestar psicológico del **CESDE**, permitiendo consultar
el equipo de psicólogos disponibles y las citas agendadas por los estudiantes.
Los datos son consumidos desde **MockAPI**, que simula el backend de SerenityLab con dos entidades: `psicologos` y `citas`.
""")

# --- Configuración de la API (MockAPI) ---
# REEMPLAZA ESTE ID CON TU PROPIO ID DE MOCKAPI
MOCK_API_ID = "69e0417e29c070e6597b4ae0"
MOCK_API_BASE_URL = f"https://{MOCK_API_ID}.mockapi.io"

# --- Botón para Limpiar Caché ---
if st.button("🔄 Refrescar Datos (Limpiar Caché)"):
    st.cache_data.clear()
    st.rerun()

# --- Función para obtener datos de MockAPI ---
@st.cache_data
def get_mockapi_data(entity):
    paths_to_try = [
        f"{MOCK_API_BASE_URL}/{entity}",
        f"{MOCK_API_BASE_URL}/api/v1/{entity}"
    ]
    last_error = ""
    for url in paths_to_try:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return pd.DataFrame(data)
                else:
                    return pd.DataFrame([data])
            else:
                last_error = f"Status {response.status_code} en {url}"
        except Exception as e:
            last_error = f"Error: {e} en {url}"

    st.error(f"No se pudo conectar con '{entity}'. Último intento: {last_error}")
    return pd.DataFrame()

# --- Carga de Datos ---
with st.spinner("Conectando con MockAPI..."):
    df_psicologos = get_mockapi_data("psicologos")
    df_citas = get_mockapi_data("citas")

# ---------------------------------------------------------------
# Sección 1: Equipo de Psicólogos
# ---------------------------------------------------------------
st.header("👩‍⚕️ Equipo de Psicólogos")
st.markdown("Directorio del equipo profesional de bienestar psicológico del CESDE.")

if not df_psicologos.empty:
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        # Filtro por especialidad (si la columna existe)
        if 'especialidad' in df_psicologos.columns:
            especialidades = ["Todas"] + sorted(df_psicologos['especialidad'].dropna().unique().tolist())
            sel_esp = st.selectbox("Filtrar por Especialidad:", especialidades, key="sel_especialidad")
        else:
            sel_esp = "Todas"

    with col_p2:
        # Búsqueda por nombre
        search_nombre = st.text_input("Buscar psicólogo por nombre:", "", key="search_psicologo")

    # Aplicar filtros
    f_psicologos = df_psicologos.copy()
    if sel_esp != "Todas" and 'especialidad' in df_psicologos.columns:
        f_psicologos = f_psicologos[f_psicologos['especialidad'] == sel_esp]
    if search_nombre and 'nombre' in df_psicologos.columns:
        f_psicologos = f_psicologos[
            f_psicologos['nombre'].str.contains(search_nombre, case=False, na=False)
        ]

    # Métricas
    mp1, mp2, mp3 = st.columns(3)
    with mp1:
        st.metric("Total Psicólogos", len(f_psicologos))
    with mp2:
        if 'especialidad' in df_psicologos.columns:
            st.metric("Especialidades", df_psicologos['especialidad'].nunique())
    with mp3:
        if 'licencia' in df_psicologos.columns:
            st.metric("Con Licencia Registrada", df_psicologos['licencia'].notna().sum())

    st.dataframe(f_psicologos, use_container_width=True)
else:
    st.info("💡 Esperando datos de 'psicologos'... Asegúrate de que la entidad exista en tu MockAPI.")

st.divider()

# ---------------------------------------------------------------
# Sección 2: Gestión de Citas
# ---------------------------------------------------------------
st.header("📅 Citas Agendadas")
st.markdown("Visualiza y filtra las citas de atención psicológica registradas por los estudiantes del CESDE.")

if not df_citas.empty:
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        # Filtro por estado de la cita
        if 'estado_cita' in df_citas.columns:
            estados = ["Todos"] + sorted(df_citas['estado_cita'].dropna().unique().tolist())
            sel_estado = st.selectbox("Filtrar por Estado:", estados, key="sel_estado_cita")
        else:
            sel_estado = "Todos"

    with col_c2:
        # Filtro por psicólogo asignado
        if 'psicologo_id' in df_citas.columns:
            psic_ids = ["Todos"] + sorted(df_citas['psicologo_id'].dropna().astype(str).unique().tolist())
            sel_psic = st.selectbox("Filtrar por ID Psicólogo:", psic_ids, key="sel_psicologo_cita")
        else:
            sel_psic = "Todos"

    # Aplicar filtros
    f_citas = df_citas.copy()
    if sel_estado != "Todos" and 'estado_cita' in df_citas.columns:
        f_citas = f_citas[f_citas['estado_cita'] == sel_estado]
    if sel_psic != "Todos" and 'psicologo_id' in df_citas.columns:
        f_citas = f_citas[f_citas['psicologo_id'].astype(str) == sel_psic]

    # Métricas
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.metric("Total Citas", len(f_citas))
    with mc2:
        if 'estado_cita' in df_citas.columns:
            pendientes = (df_citas['estado_cita'] == 'Pendiente').sum()
            st.metric("⏳ Pendientes", pendientes)
    with mc3:
        if 'estado_cita' in df_citas.columns:
            confirmadas = (df_citas['estado_cita'] == 'Confirmada').sum()
            st.metric("✅ Confirmadas", confirmadas)
    with mc4:
        if 'estado_cita' in df_citas.columns:
            canceladas = (df_citas['estado_cita'] == 'Cancelada').sum()
            st.metric("❌ Canceladas", canceladas)

    st.dataframe(f_citas, use_container_width=True)
else:
    st.info("💡 Esperando datos de 'citas'... Asegúrate de que la entidad exista en tu MockAPI.")

# --- Información Técnica ---
st.divider()
st.info(f"""
**Detalles Técnicos — MockAPI:**
- **Base URL:** `{MOCK_API_BASE_URL}`
- **Entidades:** `/psicologos` y `/citas`
- **Campos sugeridos para `psicologos`:** `id`, `nombre`, `apellido`, `especialidad`, `licencia`, `email`, `telefono`
- **Campos sugeridos para `citas`:** `id`, `estudiante_id`, `psicologo_id`, `fecha_cita`, `hora_cita`, `estado_cita`
- **Nota:** Los nombres de los recursos en MockAPI deben coincidir exactamente (sin espacios ni mayúsculas).
""")