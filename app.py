import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Tablero Analítico - Subtes CABA",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. CARGA Y PROCESAMIENTO DE DATOS (CON CACHÉ)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # Carga de la base transaccional de estaciones
    df = pd.read_csv('subte_procesado.csv')
    df['LINEA'] = df['LINEA'].str.strip()
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    df['DIA_SEMANA'] = df['FECHA'].dt.dayofweek # 0=Lunes, 6=Domingo
    df['ES_HABIL'] = df['DIA_SEMANA'] < 5
    
    # Clasificación de franjas horarias operativas
    def clasificar_franja(hora):
        if hora in [7, 8, 9]:
            return 'Pico Mañana'
        elif hora in [16, 17, 18]:
            return 'Pico Tarde'
        else:
            return 'Valle'
            
    df['FRANJA'] = df['HORA'].apply(clasificar_franja)
    
    # Carga de datos complementarios de tarifas y viajes anuales
    df_tarifas = pd.read_csv('registro-historico-del-precio-del-boleto.csv')
    df_viajes = pd.read_csv('viajes_anual.csv')
    
    return df, df_tarifas, df_viajes

df, df_tarifas, df_viajes = load_data()

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL: CONTROL DE FILTROS DINÁMICOS
# -----------------------------------------------------------------------------
try:
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Subte_Buenos_Aires_%28logo%29.svg/300px-Subte_Buenos_Aires_%28logo%29.svg.png", width=120)
except Exception:
    st.sidebar.title("🚇 Subte BA")
st.sidebar.title("Filtros Operativos")

lineas = sorted(df['LINEA'].unique())
linea_sel = st.sidebar.selectbox("Seleccionar Línea:", ["Todas"] + lineas)

tipo_dia = st.sidebar.radio("Tipo de Día:", ["Todos", "Días Hábiles", "Fines de Semana"])

# Aplicación de filtros
df_view = df.copy()
if linea_sel != "Todas":
    df_view = df_view[df_view['LINEA'] == linea_sel]

if tipo_dia == "Días Hábiles":
    df_view = df_view[df_view['ES_HABIL']]
elif tipo_dia == "Fines de Semana":
    df_view = df_view[~df_view['ES_HABIL']]

# -----------------------------------------------------------------------------
# 4. ENCABEZADO Y TARJETAS DE INDICADORES (KPIs)
# -----------------------------------------------------------------------------
st.title("🚇 Tablero de Control y Analítica: Red de Subterráneos CABA")
st.markdown("**Proyecto Final Integrador - Metodología de la Investigación (UGR)**")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

total_validaciones = df_view['CANTIDAD'].sum()
promedio_diario = df_view.groupby('FECHA')['CANTIDAD'].sum().mean()
viajes_pico = df_view[df_view['FRANJA'].isin(['Pico Mañana', 'Pico Tarde'])]['CANTIDAD'].sum()
ratio_pico = (viajes_pico / total_validaciones * 100) if total_validaciones > 0 else 0

col1.metric("Total Validaciones", f"{total_validaciones:,.0f}".replace(",", "."))
col2.metric("Promedio Diario de Pasajeros", f"{promedio_diario:,.0f}".replace(",", "."))
col3.metric("Ratio en Horas Pico", f"{ratio_pico:.1f}%")
col4.metric("Estaciones Registradas", f"{df_view['ESTACION'].nunique()}")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. PESTAÑAS DE ANÁLISIS
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["🕒 Dinámica Temporal", "🗺️ Concentración Espacial", "📈 Sensibilidad Tarifaria (Ep)"])

# PESTAÑA 1: DINÁMICA TEMPORAL
with tab1:
    st.subheader("Curva de Demanda Intradiaria y Asimetría Horaria")
    col_t1, col_t2 = st.columns([2, 1])
    
    with col_t1:
        curva_horaria = df_view.groupby('HORA')['CANTIDAD'].sum().reset_index()
        fig_curva = px.line(
            curva_horaria, x='HORA', y='CANTIDAD', markers=True,
            title="Distribución Horaria del Flujo de Pasajeros",
            labels={'HORA': 'Hora de Operación (05:00 a 23:00)', 'CANTIDAD': 'Validaciones Acumuladas'},
            color_discrete_sequence=['#1f77b4']
        )
        fig_curva.update_layout(xaxis=dict(tickmode='linear', tick0=5, dtick=1))
        st.plotly_chart(fig_curva, use_container_width=True)
        
    with col_t2:
        df_hab_finde = df_view.groupby(['ES_HABIL'])['CANTIDAD'].sum().reset_index()
        df_hab_finde['Día'] = df_hab_finde['ES_HABIL'].map({True: 'Días Hábiles', False: 'Fines de Semana'})
        fig_pie = px.pie(
            df_hab_finde, values='CANTIDAD', names='Día',
            title="Proporción Hábil vs. Fin de Semana",
            color_discrete_sequence=['#2ca02c', '#d62728'],
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# PESTAÑA 2: CONCENTRACIÓN ESPACIAL
with tab2:
    st.subheader("Concentración de Pasajeros por Estación y Línea")
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        top_estaciones = df_view.groupby('ESTACION')['CANTIDAD'].sum().nlargest(10).reset_index()
        fig_top = px.bar(
            top_estaciones, x='CANTIDAD', y='ESTACION', orientation='h',
            title="Top 10 Estaciones con Mayor Afluencia",
            labels={'CANTIDAD': 'Validaciones Acumuladas', 'ESTACION': 'Estación'},
            color='CANTIDAD', color_continuous_scale='Blues'
        )
        fig_top.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_top, use_container_width=True)
        
    with col_s2:
        lineas_dist = df.groupby('LINEA')['CANTIDAD'].sum().reset_index()
        fig_lineas = px.bar(
            lineas_dist, x='LINEA', y='CANTIDAD',
            title="Distribución Total de Pasajeros por Línea de Subte",
            labels={'LINEA': 'Línea Comercial', 'CANTIDAD': 'Validaciones Acumuladas'},
            color='LINEA',
            color_discrete_map={'A': '#00AEEF', 'B': '#EC1C24', 'C': '#0055A5', 'D': '#00853F', 'E': '#6F2C91', 'H': '#FFD100'}
        )
        st.plotly_chart(fig_lineas, use_container_width=True)

# PESTAÑA 3: SENSIBILIDAD TARIFARIA
with tab3:
    st.subheader("Análisis de Demanda Histórica vs. Cuadro Tarifario")
    
    # Serie histórica anual
    viajes_anuales = df_viajes.groupby('year')['total'].sum().reset_index()
    tarifas_anuales = df_tarifas.groupby('año')['precio'].mean().reset_index()
    df_econometria = pd.merge(viajes_anuales, tarifas_anuales, left_on='year', right_on='año')
    
    fig_dual = go.Figure()
    fig_dual.add_trace(go.Bar(
        x=df_econometria['year'], y=df_econometria['total'],
        name="Viajes Anuales", marker_color='rgb(55, 83, 109)', yaxis='y1'
    ))
    fig_dual.add_trace(go.Scatter(
        x=df_econometria['year'], y=df_econometria['precio'],
        name="Tarifa Nominal Promedio ($)", marker_color='rgb(219, 64, 82)', yaxis='y2', mode='lines+markers'
    ))
    
    fig_dual.update_layout(
        title="Evolución de Viajes Anuales y Tarifa (2013-2019)",
        xaxis=dict(title="Año"),
        yaxis=dict(title="Total Viajes Transportados", side='left'),
        yaxis2=dict(title="Precio Promedio Boleto ($ ARS)", overlaying='y', side='right'),
        legend=dict(x=0.01, y=0.99)
    )
    st.plotly_chart(fig_dual, use_container_width=True)
    
    st.info("💡 **Conclusión del Módulo Econométrico:** Durante el período 2018-2019, la tarifa nominal experimentó un incremento medio del **+71,61%** (de $9,83 a $16,88), mientras que la afluencia de pasajeros apenas se contrajo un **-2,03%** (de 348,4M a 341,3M). La Elasticidad de Arco resultante es de **Ep = -0,0388**, confirmando de manera rigurosa el carácter altamente inelástico (|Ep| < 1) del servicio.")