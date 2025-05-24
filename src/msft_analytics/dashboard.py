import os
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# Configuración para la página
st.set_page_config(
    page_title="MSFT Insight 360 Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Personalizamos estilos
st.markdown("""
<style>
body { background-color: #f0f2f6; }
.section-header { font-size: 24px; font-weight: bold; margin-top: 20px; color: #0366d6; }
.metric-text { font-size: 20px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Ruta al CSV enriquecido
CSV_PATH = os.path.join(os.path.dirname(__file__), "static", "data", "historical_enriched.csv")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    if "Fecha" in df.columns:
        df.rename(columns={"Fecha": "fecha"}, inplace=True)
    df['fecha'] = pd.to_datetime(df['fecha'])
    df.set_index('fecha', inplace=True)
    df = df.sort_index()
    # Calculamos KPIs
    df['tasa_variacion'] = df['cerrar'].pct_change().fillna(0) * 100
    df['media_movil_7d'] = df['cerrar'].rolling(7).mean()
    df['volatilidad_7d'] = df['tasa_variacion'].rolling(7).std()
    primera = df['cerrar'].iloc[0]
    df['retorno_acumulado'] = (df['cerrar'] / primera - 1) * 100
    df['desviacion_estandar_acumulada'] = df['cerrar'].expanding().std()
    return df

# Título Principal
st.markdown("<div class='section-header'>MSFT Insight 360: Dashboard de KPIs y Series Temporales</div>", unsafe_allow_html=True)

# Cargamos Datos
df = load_data(CSV_PATH)

# Sidebar: Filtrado de fechas
st.sidebar.markdown("<div class='section-header'>Filtros</div>", unsafe_allow_html=True)
start_default = df.index.min().date()
end_default = df.index.max().date()
dates = st.sidebar.date_input(
    "Rango de Fechas",
    value=[start_default, end_default],
    min_value=start_default,
    max_value=end_default
)

if len(dates) != 2:
    st.sidebar.error("Selecciona dos fechas: inicio y fin.")
    st.stop()
start, end = dates
if start > end:
    st.sidebar.error("La fecha de inicio debe ser anterior a la de fin.")
    st.stop()

# Filtramos Dataframe
df_filtered = df.loc[start:end]

# KPIs Destacados
st.markdown("<div class='section-header'>KPIs Principales</div>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Tasa Variación (último)", f"{df_filtered['tasa_variacion'][-1]:.2f}%")
col2.metric("Media Móvil 7d (último)", f"{df_filtered['media_movil_7d'][-1]:.2f}")
col3.metric("Volatilidad 7d", f"{df_filtered['volatilidad_7d'][-1]:.2f}%")

# Mostramos Retorno Acumulado completo usando markdown
valor_ret = df_filtered['retorno_acumulado'][-1]
col4.markdown(
    f"**Retorno Acumulado**<br>"
    f"<span class='metric-text'>{valor_ret:,.2f}%</span>",
    unsafe_allow_html=True
)
col5.metric("Desv. Estándar Acum.", f"{df_filtered['desviacion_estandar_acumulada'][-1]:.2f}")

st.markdown("---")

# Gráficos interactivos con Plotly
st.markdown("<div class='section-header'>Visualización de Series</div>", unsafe_allow_html=True)

fig1 = px.line(
    df_filtered,
    x=df_filtered.index,
    y=['cerrar', 'media_movil_7d'],
    labels={'value':'Precio', 'fecha':'Fecha', 'variable':'Serie'},
    title='Precio de Cierre y Media Móvil 7d'
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(
    df_filtered,
    x=df_filtered.index,
    y=['volatilidad_7d', 'tasa_variacion'],
    labels={'value':'%', 'fecha':'Fecha', 'variable':'Serie'},
    title='Volatilidad 7d y Tasa de Variación'
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.line(
    df_filtered,
    x=df_filtered.index,
    y=['retorno_acumulado', 'desviacion_estandar_acumulada'],
    labels={'value':'%', 'fecha':'Fecha', 'variable':'Serie'},
    title='Retorno Acumulado y Desv. Estándar Acumulada'
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Distribuciones
st.markdown("<div class='section-header'>Distribución del Precio</div>", unsafe_allow_html=True)
colh1, colh2 = st.columns([2,1])
with colh1:
    fig4 = px.histogram(
        df_filtered,
        x='cerrar',
        nbins=50,
        title='Histograma de Precio de Cierre'
    )
    st.plotly_chart(fig4, use_container_width=True)
with colh2:
    fig5 = px.box(
        df_filtered,
        y='cerrar',
        title='Boxplot de Precio de Cierre'
    )
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# Pie de página
st.markdown(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", unsafe_allow_html=True)
