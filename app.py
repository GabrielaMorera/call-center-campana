"""
🗳️ SISTEMA DE SEGUIMIENTO DE LLAMADAS - CAMPAÑA DORA 2026
Call Center con Sistema de Semáforo
Con Google Sheets para persistencia
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timezone, timedelta
import gspread
from google.oauth2.service_account import Credentials

# ============== ZONA HORARIA COLOMBIA ==============
def obtener_hora_colombia():
    """Obtiene la hora actual en la zona horaria de Colombia (UTC-5)"""
    zona_colombia = timezone(timedelta(hours=-5))
    return datetime.now(zona_colombia)

# ============== CONFIGURACIÓN ==============
st.set_page_config(
    page_title="📞 Call Center Campaña",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ID de tu Google Sheet (sacado de la URL)
SPREADSHEET_ID = "1zMrAs6IHB6LUDpmbukRCOrBbgFPYjLv7VMDVRygEYjA"
META_DIARIA = 150

# ============== CONEXIÓN GOOGLE SHEETS ==============

@st.cache_resource
def get_google_connection():
    """Conecta a Google Sheets"""
    try:
        credentials_dict = {
            "type": st.secrets["gcp_service_account"]["type"],
            "project_id": st.secrets["gcp_service_account"]["project_id"],
            "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
            "private_key": st.secrets["gcp_service_account"]["private_key"],
            "client_email": st.secrets["gcp_service_account"]["client_email"],
            "client_id": st.secrets["gcp_service_account"]["client_id"],
            "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
            "token_uri": st.secrets["gcp_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"],
        }
        
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        credentials = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Error conectando a Google Sheets: {e}")
        return None

def get_sheet(name):
    """Obtiene una hoja específica"""
    client = get_google_connection()
    if client:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        return spreadsheet.worksheet(name)
    return None

# ============== SISTEMA DE USUARIOS ==============

def get_users():
    """Obtiene usuarios desde secrets"""
    try:
        if hasattr(st, 'secrets') and 'usuarios' in st.secrets:
            return dict(st.secrets['usuarios'])
    except:
        pass
    
    return {
        "admin": {"password": "gualiva2026", "nombre": "admin", "rol": "admin"},
        "adriana": {"password": "adriana123", "nombre": "Adriana Melo", "rol": "operadora"},
        "jesica": {"password": "jesica123", "nombre": "Jesica Tinoco", "rol": "operadora"}
    }

USUARIOS = get_users()

def verificar_credenciales(username, password):
    if username in USUARIOS:
        if USUARIOS[username]["password"] == password:
            return True
    return False

def obtener_operadoras():
    return [USUARIOS[u]["nombre"] for u in USUARIOS if USUARIOS[u]["rol"] == "operadora"]

# ============== ESTILOS CSS ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;900&family=Open+Sans:wght@400;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #FAFAFA 0%, #F0F0F0 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #E31837 0%, #B91430 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(227, 24, 55, 0.3);
        text-align: center;
    }
    
    .main-header h1 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 2rem;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .main-header p {
        font-family: 'Open Sans', sans-serif;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .contact-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border-left: 6px solid #E31837;
        margin: 1rem 0;
    }
    
    .contact-name {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .contact-phone {
        font-family: 'Open Sans', sans-serif;
        font-size: 1.4rem;
        color: #E31837;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    .stats-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }
    
    .stats-number {
        font-family: 'Montserrat', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        color: #E31837;
    }
    
    .stats-label {
        font-family: 'Open Sans', sans-serif;
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .progress-bar {
        background: #E0E0E0;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin-top: 0.5rem;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 10px;
    }
    
    .operadora-badge {
        display: inline-block;
        background: #E31837;
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .user-badge {
        background: linear-gradient(135deg, #E31837 0%, #B91430 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .metric-verde { border-top: 4px solid #28A745; }
    .metric-amarillo { border-top: 4px solid #FFC107; }
    .metric-rojo { border-top: 4px solid #DC3545; }
    .metric-gris { border-top: 4px solid #6C757D; }
</style>
""", unsafe_allow_html=True)

# ============== FUNCIONES DE DATOS ==============

@st.cache_data(ttl=30)
def cargar_contactos():
    """Carga contactos desde Google Sheets"""
    try:
        sheet = get_sheet("contactos")
        if sheet:
            data = sheet.get_all_records()
            return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error cargando contactos: {e}")
    return pd.DataFrame()

@st.cache_data(ttl=60)
def cargar_llamadas():
    """Carga llamadas desde Google Sheets"""
    try:
        sheet = get_sheet("llamadas")
        if sheet:
            data = sheet.get_all_records()
            return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error cargando llamadas: {e}")
    return pd.DataFrame()

def registrar_llamada(contacto_id, nombre_contacto, telefono, operadora, resultado, notas=""):
    """Registra una llamada en Google Sheets"""
    try:
        sheet = get_sheet("llamadas")
        if sheet:
            nueva_fila = [
                len(sheet.get_all_values()),  # id
                int(contacto_id),
                nombre_contacto,
                str(telefono),
                operadora,
                resultado,
                notas if notas else "",
                obtener_hora_colombia().date().isoformat(),
                obtener_hora_colombia().strftime("%H:%M:%S")
            ]
            sheet.append_row(nueva_fila)
            # Limpiar caché después de registrar
            cargar_llamadas.clear()
            return True
    except Exception as e:
        st.error(f"Error registrando llamada: {e}")
    return False

def obtener_contactos_pendientes(incluir_no_contesta=False):
    """Obtiene contactos no llamados hoy"""
    df_contactos = cargar_contactos()
    df_llamadas = cargar_llamadas()
    
    if df_contactos.empty:
        return pd.DataFrame()
    
    hoy = obtener_hora_colombia().date().isoformat()
    
    if not df_llamadas.empty and 'fecha' in df_llamadas.columns and 'contacto_id' in df_llamadas.columns:
        llamadas_hoy = df_llamadas[df_llamadas['fecha'] == hoy]
        
        if incluir_no_contesta:
            # Excluir solo los que SÍ contestaron (verde, amarillo, rojo)
            contactados = llamadas_hoy[llamadas_hoy['resultado'].isin(['verde', 'amarillo', 'rojo'])]
            llamados_hoy_ids = set(int(x) for x in contactados['contacto_id'].unique())
        else:
            # Excluir TODOS los llamados hoy (incluyendo no_contesta)
            llamados_hoy_ids = set(int(x) for x in llamadas_hoy['contacto_id'].unique())
        
        pendientes = df_contactos[~df_contactos.index.isin(llamados_hoy_ids)]
    else:
        pendientes = df_contactos
    
    return pendientes

def obtener_no_contestaron():
    """Obtiene los que no contestaron hoy para reintentar"""
    df_contactos = cargar_contactos()
    df_llamadas = cargar_llamadas()
    
    if df_contactos.empty or df_llamadas.empty:
        return pd.DataFrame()
    
    hoy = obtener_hora_colombia().date().isoformat()
    
    llamadas_hoy = df_llamadas[df_llamadas['fecha'] == hoy]
    no_contestaron = llamadas_hoy[llamadas_hoy['resultado'] == 'no_contesta']
    
    if no_contestaron.empty:
        return pd.DataFrame()
    
    ids_no_contestaron = set(int(x) for x in no_contestaron['contacto_id'].unique())
    return df_contactos[df_contactos.index.isin(ids_no_contestaron)]

def obtener_stats_operadora(operadora, fecha=None):
    """Estadísticas de una operadora"""
    df_llamadas = cargar_llamadas()
    
    if fecha is None:
        fecha = obtener_hora_colombia().date().isoformat()
    
    stats = {"total": 0, "verde": 0, "amarillo": 0, "rojo": 0, "no_contesta": 0, "progreso": 0}
    
    if df_llamadas.empty:
        return stats
    
    llamadas_dia = df_llamadas[(df_llamadas['operadora'] == operadora) & (df_llamadas['fecha'] == fecha)]
    
    stats["total"] = len(llamadas_dia)
    stats["verde"] = len(llamadas_dia[llamadas_dia['resultado'] == 'verde'])
    stats["amarillo"] = len(llamadas_dia[llamadas_dia['resultado'] == 'amarillo'])
    stats["rojo"] = len(llamadas_dia[llamadas_dia['resultado'] == 'rojo'])
    stats["no_contesta"] = len(llamadas_dia[llamadas_dia['resultado'] == 'no_contesta'])
    stats["progreso"] = min(100, (stats["total"] / META_DIARIA) * 100)
    
    return stats

# ============== PÁGINAS ==============

def pagina_login():
    st.markdown("""
    <div class="main-header">
        <h1>🗳️ Campaña Dora 2026</h1>
        <p>Sistema de Call Center - Gualivá</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("### 🔐 Iniciar Sesión")
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuario:", placeholder="Ingresa tu usuario")
            password = st.text_input("🔑 Contraseña:", type="password")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                if verificar_credenciales(username.lower().strip(), password):
                    st.session_state.logged_in = True
                    st.session_state.username = username.lower().strip()
                    st.session_state.user_data = USUARIOS[username.lower().strip()]
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")

def pagina_operadora():
    user = st.session_state.user_data
    operadora_nombre = user["nombre"]
    
    st.markdown(f"""
    <div class="main-header">
        <h1>📞 Call Center Campaña 2026</h1>
        <p>Bienvenida, {operadora_nombre}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón de refrescar arriba
    col_refresh = st.columns([3, 1])
    with col_refresh[1]:
        if st.button("🔄 Actualizar", use_container_width=True):
            cargar_llamadas.clear()
            cargar_contactos.clear()
            st.rerun()
    
    # Cargar datos UNA sola vez
    df_contactos = cargar_contactos()
    df_llamadas = cargar_llamadas()
    
    # Calcular stats desde los datos cargados
    hoy = obtener_hora_colombia().date().isoformat()
    mis_llamadas = df_llamadas[(df_llamadas['operadora'] == operadora_nombre) & (df_llamadas['fecha'] == hoy)] if not df_llamadas.empty else pd.DataFrame()
    
    stats = {
        "total": len(mis_llamadas),
        "verde": len(mis_llamadas[mis_llamadas['resultado'] == 'verde']) if not mis_llamadas.empty else 0,
        "amarillo": len(mis_llamadas[mis_llamadas['resultado'] == 'amarillo']) if not mis_llamadas.empty else 0,
        "rojo": len(mis_llamadas[mis_llamadas['resultado'] == 'rojo']) if not mis_llamadas.empty else 0,
        "no_contesta": len(mis_llamadas[mis_llamadas['resultado'] == 'no_contesta']) if not mis_llamadas.empty else 0,
    }
    stats["progreso"] = min(100, (stats["total"] / META_DIARIA) * 100)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['total']}/{META_DIARIA}</div>
            <div class="stats-label">Llamadas Hoy</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {stats['progreso']:.0f}%; background: {'#28A745' if stats['progreso'] >= 100 else '#FFC107' if stats['progreso'] >= 50 else '#DC3545'};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""<div class="stats-card metric-verde">
            <div class="stats-number" style="color: #28A745;">🟢 {stats['verde']}</div>
            <div class="stats-label">Sí Apoyan</div>
        </div>""", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""<div class="stats-card metric-amarillo">
            <div class="stats-number" style="color: #FFC107;">🟡 {stats['amarillo']}</div>
            <div class="stats-label">Tal vez</div>
        </div>""", unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""<div class="stats-card metric-rojo">
            <div class="stats-number" style="color: #DC3545;">🔴 {stats['rojo']}</div>
            <div class="stats-label">No Apoyan</div>
        </div>""", unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""<div class="stats-card metric-gris">
            <div class="stats-number" style="color: #6C757D;">⚫ {stats['no_contesta']}</div>
            <div class="stats-label">No Contesta</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Calcular pendientes y no_contestaron desde datos ya cargados
    if not df_llamadas.empty and 'fecha' in df_llamadas.columns:
        llamadas_hoy = df_llamadas[df_llamadas['fecha'] == hoy]
        todos_llamados = set(int(x) for x in llamadas_hoy['contacto_id'].unique()) if not llamadas_hoy.empty else set()
        no_contestaron_ids = set(int(x) for x in llamadas_hoy[llamadas_hoy['resultado'] == 'no_contesta']['contacto_id'].unique()) if not llamadas_hoy.empty else set()
    else:
        todos_llamados = set()
        no_contestaron_ids = set()
    
    pendientes_nuevos = df_contactos[~df_contactos.index.isin(todos_llamados)] if not df_contactos.empty else pd.DataFrame()
    pendientes_no_contesta = df_contactos[df_contactos.index.isin(no_contestaron_ids)] if not df_contactos.empty else pd.DataFrame()
    
    # Modo de trabajo
    if 'modo_reintentar' not in st.session_state:
        st.session_state.modo_reintentar = False
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"📞 Llamar Nuevos ({len(pendientes_nuevos)})", use_container_width=True, 
                     type="primary" if not st.session_state.modo_reintentar else "secondary"):
            st.session_state.modo_reintentar = False
            st.session_state.contacto_idx = 0
            st.rerun()
    with col2:
        if st.button(f"🔄 Reintentar No Contesta ({len(pendientes_no_contesta)})", use_container_width=True,
                     type="primary" if st.session_state.modo_reintentar else "secondary"):
            st.session_state.modo_reintentar = True
            st.session_state.contacto_idx = 0
            st.rerun()
    
    st.markdown("---")
    
    # Seleccionar lista según modo
    if st.session_state.modo_reintentar:
        pendientes = pendientes_no_contesta
        modo_texto = "🔄 REINTENTANDO"
    else:
        pendientes = pendientes_nuevos
        modo_texto = "📞 NUEVOS"
    
    if pendientes.empty:
        if st.session_state.modo_reintentar:
            st.info("✅ No hay contactos para reintentar.")
        else:
            st.success("🎉 **¡Felicitaciones!** Se completaron todos los contactos nuevos.")
        return
    
    # Índice actual
    if 'contacto_idx' not in st.session_state:
        st.session_state.contacto_idx = 0
    
    if st.session_state.contacto_idx >= len(pendientes):
        st.session_state.contacto_idx = 0
    
    contacto = pendientes.iloc[st.session_state.contacto_idx]
    contacto_id = pendientes.index[st.session_state.contacto_idx]
    
    nombre = contacto.get('nombre', 'Sin nombre')
    telefono = contacto.get('telefono', 'Sin teléfono')
    
    num_actual = st.session_state.contacto_idx + 1
    total_pendientes = len(pendientes)
    
    st.markdown(f"""
    <div class="contact-card">
        <div class="operadora-badge">{modo_texto} | Contacto {num_actual} de {total_pendientes}</div>
        <div class="contact-name">{nombre}</div>
        <div class="contact-phone">📱 {telefono}</div>
    </div>
    """, unsafe_allow_html=True)
    
    notas = st.text_area("📝 Notas (opcional):", placeholder="Ej: Muy interesada...", key="notas")
    
    st.markdown("### 🚦 ¿Cómo fue la llamada?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🟢 SÍ APOYA", use_container_width=True, type="primary"):
            if registrar_llamada(contacto_id, nombre, telefono, operadora_nombre, "verde", notas):
                st.balloons()
                st.session_state.contacto_idx = 0
                st.rerun()
    
    with col2:
        if st.button("🟡 TAL VEZ", use_container_width=True):
            if registrar_llamada(contacto_id, nombre, telefono, operadora_nombre, "amarillo", notas):
                st.session_state.contacto_idx = 0
                st.rerun()
    
    with col3:
        if st.button("🔴 NO APOYA", use_container_width=True):
            if registrar_llamada(contacto_id, nombre, telefono, operadora_nombre, "rojo", notas):
                st.session_state.contacto_idx = 0
                st.rerun()
    
    with col4:
        if st.button("⚫ NO CONTESTA", use_container_width=True):
            if registrar_llamada(contacto_id, nombre, telefono, operadora_nombre, "no_contesta", notas):
                st.session_state.contacto_idx = 0
                st.rerun()
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⏭️ Saltar este contacto", use_container_width=True):
            st.session_state.contacto_idx += 1
            st.rerun()

def pagina_admin():
    st.markdown("""
    <div class="main-header">
        <h1>📊 Panel de Administración</h1>
        <p>Dashboard de métricas y gestión</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Métricas", "👥 Operadoras", "🔄 Refrescar"])
    
    with tab1:
        mostrar_metricas()
    
    with tab2:
        ver_operadoras()
    
    with tab3:
        st.markdown("### 🔄 Refrescar Datos")
        if st.button("Limpiar caché y recargar", use_container_width=True):
            cargar_llamadas.clear()
            cargar_contactos.clear()
            st.success("✅ Datos actualizados")
            st.rerun()

def mostrar_metricas():
    import plotly.express as px
    
    df_llamadas = cargar_llamadas()
    
    if df_llamadas.empty:
        st.warning("📭 No hay llamadas registradas aún.")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Desde:", value=date.today())
    with col2:
        fecha_fin = st.date_input("Hasta:", value=date.today())
    
    df_filtrado = df_llamadas.copy()
    df_filtrado['fecha'] = pd.to_datetime(df_filtrado['fecha'])
    df_filtrado = df_filtrado[
        (df_filtrado['fecha'].dt.date >= fecha_inicio) &
        (df_filtrado['fecha'].dt.date <= fecha_fin)
    ]
    
    st.markdown("---")
    
    total = len(df_filtrado)
    verdes = len(df_filtrado[df_filtrado['resultado'] == 'verde'])
    amarillos = len(df_filtrado[df_filtrado['resultado'] == 'amarillo'])
    rojos = len(df_filtrado[df_filtrado['resultado'] == 'rojo'])
    no_contesta = len(df_filtrado[df_filtrado['resultado'] == 'no_contesta'])
    
    tasa_conv = (verdes / total * 100) if total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📞 Total", total)
    col2.metric("🟢 Conversión", f"{tasa_conv:.1f}%")
    col3.metric("🟢 Verdes", verdes)
    col4.metric("🟡 Amarillos", amarillos)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🥧 Distribución")
        fig = px.pie(
            values=[verdes, amarillos, rojos, no_contesta],
            names=['🟢 Sí', '🟡 Tal vez', '🔴 No', '⚫ No contesta'],
            color_discrete_sequence=['#28A745', '#FFC107', '#DC3545', '#6C757D'],
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Por Operadora")
        df_op = df_filtrado.groupby('operadora').size().reset_index(name='llamadas')
        fig2 = px.bar(df_op, x='operadora', y='llamadas', color_discrete_sequence=['#E31837'])
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📋 Registro")
    st.dataframe(df_filtrado.sort_values('fecha', ascending=False), use_container_width=True)
    
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar CSV", csv, f"llamadas_{date.today()}.csv", use_container_width=True)

def ver_operadoras():
    st.markdown("### 👥 Estado Hoy")
    
    for op in obtener_operadoras():
        stats = obtener_stats_operadora(op)
        with st.expander(f"📞 {op}", expanded=True):
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Total", stats['total'])
            col2.metric("🟢", stats['verde'])
            col3.metric("🟡", stats['amarillo'])
            col4.metric("🔴", stats['rojo'])
            col5.metric("⚫", stats['no_contesta'])
            st.progress(stats['progreso'] / 100)

def mostrar_sidebar():
    with st.sidebar:
        user = st.session_state.user_data
        st.markdown(f"""
        <div class="user-badge">
            👤 {user['nombre']}<br>
            <small>{user['rol'].upper()}</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Meses en español
        meses = {
            1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
            7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
        }
        
        hora_col = obtener_hora_colombia()
        fecha_formateada = f"{hora_col.day:02d} de {meses[hora_col.month]} de {hora_col.year}"
        st.markdown(f"📅 **{fecha_formateada}**")
        
        if user['rol'] == 'operadora':
            stats = obtener_stats_operadora(user['nombre'])
            st.metric("Mis llamadas", stats['total'])
            st.progress(stats['progreso'] / 100)
        
        st.markdown("---")
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        pagina_login()
        return
    
    mostrar_sidebar()
    
    user = st.session_state.user_data
    if user['rol'] == 'admin':
        pagina_admin()
    else:
        pagina_operadora()

if __name__ == "__main__":
    main()