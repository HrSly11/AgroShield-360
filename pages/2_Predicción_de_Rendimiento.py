import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Predicción de Rendimiento", page_icon="🌱", layout="wide")

st.title("🌱 Predicción de Rendimiento del Cultivo")
st.markdown("---")

# Verificar si existen datos del productor
if 'datos_productor' not in st.session_state or not st.session_state.datos_productor:
    st.warning("⚠️ Primero debe ingresar los datos del productor en la página anterior")
    st.stop()

datos = st.session_state.datos_productor

# Mostrar información del cultivo
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Cultivo", datos.get('tipo_cultivo', 'N/A'))
with col2:
    st.metric("Área", f"{datos.get('area_disponible', 0):.1f} ha")
with col3:
    st.metric("Ubicación", datos.get('ubicacion', 'N/A'))
with col4:
    st.metric("Duración", f"{datos.get('duracion_dias', 0)} días")

st.markdown("---")

# Parámetros del modelo predictivo
st.subheader("⚙️ Parámetros del Modelo Predictivo")

col5, col6 = st.columns(2)

with col5:
    fertilidad_suelo = st.slider(
        "Fertilidad del Suelo (escala 1-10)",
        min_value=1,
        max_value=10,
        value=7,
        help="Calidad estimada del suelo: 1=Pobre, 10=Excelente"
    )
    
    disponibilidad_agua = st.slider(
        "Disponibilidad de Agua (escala 1-10)",
        min_value=1,
        max_value=10,
        value=8,
        help="Acceso y disponibilidad de agua para riego"
    )

with col6:
    tecnologia = st.slider(
        "Nivel Tecnológico (escala 1-10)",
        min_value=1,
        max_value=10,
        value=6,
        help="Nivel de tecnología aplicada: 1=Tradicional, 10=Avanzado"
    )
    
    experiencia = st.slider(
        "Experiencia del Productor (años)",
        min_value=0,
        max_value=50,
        value=10,
        help="Años de experiencia en agricultura"
    )

# Base de rendimientos por cultivo (kg/ha)
rendimientos_base = {
    'Maíz': {'min': 4000, 'medio': 8000, 'max': 12000},
    'Papa': {'min': 15000, 'medio': 25000, 'max': 35000},
    'Arroz': {'min': 6000, 'medio': 9000, 'max': 12000},
    'Trigo': {'min': 2500, 'medio': 4000, 'max': 6000},
    'Quinua': {'min': 1200, 'medio': 2000, 'max': 3000},
    'Espárrago': {'min': 8000, 'medio': 12000, 'max': 18000},
    'Palta': {'min': 8000, 'medio': 15000, 'max': 22000},
    'Café': {'min': 800, 'medio': 1500, 'max': 2500},
    'Cacao': {'min': 600, 'medio': 1200, 'max': 2000},
    'Algodón': {'min': 2500, 'medio': 4000, 'max': 6000}
}

# Factores climáticos simulados por región
factores_region = {
    'Lima': 0.95, 'Arequipa': 0.90, 'La Libertad': 0.92,
    'Lambayeque': 0.88, 'Piura': 0.85, 'Ica': 0.93,
    'Junín': 0.87, 'Cajamarca': 0.86, 'Cusco': 0.84,
    'Ancash': 0.89, 'Ayacucho': 0.85, 'Huánuco': 0.86,
    'San Martín': 0.91
}

# Calcular rendimiento predictivo
cultivo = datos.get('tipo_cultivo', 'Maíz')
ubicacion = datos.get('ubicacion', 'Lima')

if cultivo in rendimientos_base:
    base = rendimientos_base[cultivo]
    factor_region = factores_region.get(ubicacion, 0.9)
    
    # Factor de ajuste basado en parámetros
    factor_ajuste = (
        (fertilidad_suelo / 10) * 0.3 +
        (disponibilidad_agua / 10) * 0.3 +
        (tecnologia / 10) * 0.25 +
        min(experiencia / 20, 1.0) * 0.15
    )
    
    # Calcular rendimientos ajustados
    rendimiento_minimo = base['min'] * factor_region * max(factor_ajuste - 0.2, 0.5)
    rendimiento_probable = base['medio'] * factor_region * factor_ajuste
    rendimiento_maximo = base['max'] * factor_region * min(factor_ajuste + 0.2, 1.2)
    
    # Calcular producción total
    area = datos.get('area_disponible', 1)
    produccion_minima = rendimiento_minimo * area
    produccion_probable = rendimiento_probable * area
    produccion_maxima = rendimiento_maximo * area
    
    st.markdown("---")
    st.subheader("📊 Resultados de la Predicción")
    
    # Mostrar métricas
    col7, col8, col9 = st.columns(3)
    
    with col7:
        st.metric(
            "Escenario Mínimo",
            f"{rendimiento_minimo:,.0f} kg/ha",
            f"{produccion_minima:,.0f} kg total"
        )
    
    with col8:
        st.metric(
            "Escenario Probable",
            f"{rendimiento_probable:,.0f} kg/ha",
            f"{produccion_probable:,.0f} kg total",
            delta_color="off"
        )
    
    with col9:
        st.metric(
            "Escenario Máximo",
            f"{rendimiento_maximo:,.0f} kg/ha",
            f"{produccion_maxima:,.0f} kg total"
        )
    
    # Gráfico de barras comparativo
    fig_barras = go.Figure()
    
    fig_barras.add_trace(go.Bar(
        name='Rendimiento kg/ha',
        x=['Mínimo', 'Probable', 'Máximo'],
        y=[rendimiento_minimo, rendimiento_probable, rendimiento_maximo],
        marker_color=['#FF6B6B', '#4ECDC4', '#95E1D3'],
        text=[f"{rendimiento_minimo:,.0f}", f"{rendimiento_probable:,.0f}", 
              f"{rendimiento_maximo:,.0f}"],
        textposition='auto'
    ))
    
    fig_barras.update_layout(
        title=f"Rendimiento Estimado - {cultivo}",
        xaxis_title="Escenario",
        yaxis_title="Rendimiento (kg/ha)",
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_barras, use_container_width=True)
    
    # Gráfico de distribución probabilística
    fig_dist = go.Figure()
    
    x_vals = np.linspace(rendimiento_minimo, rendimiento_maximo, 100)
    y_vals = np.exp(-((x_vals - rendimiento_probable) ** 2) / 
                    (2 * ((rendimiento_maximo - rendimiento_minimo) / 6) ** 2))
    
    fig_dist.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        fill='tozeroy',
        name='Probabilidad',
        line=dict(color='#4ECDC4', width=2)
    ))
    
    fig_dist.add_vline(x=rendimiento_probable, line_dash="dash", 
                       line_color="red", annotation_text="Probable")
    
    fig_dist.update_layout(
        title="Distribución de Probabilidad del Rendimiento",
        xaxis_title="Rendimiento (kg/ha)",
        yaxis_title="Probabilidad Relativa",
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_dist, use_container_width=True)
    
    # Análisis de factores
    st.markdown("---")
    st.subheader("🔍 Análisis de Factores")
    
    factores_df = pd.DataFrame({
        'Factor': ['Fertilidad del Suelo', 'Disponibilidad de Agua', 
                   'Tecnología', 'Experiencia'],
        'Valor': [fertilidad_suelo, disponibilidad_agua, tecnologia, 
                  min(experiencia/5, 10)],
        'Peso': ['30%', '30%', '25%', '15%']
    })
    
    fig_factores = px.bar(
        factores_df,
        x='Factor',
        y='Valor',
        text='Peso',
        color='Valor',
        color_continuous_scale='Viridis',
        title="Contribución de Factores al Rendimiento"
    )
    
    fig_factores.update_traces(textposition='outside')
    fig_factores.update_layout(height=400)
    
    st.plotly_chart(fig_factores, use_container_width=True)
    
    # Guardar predicción en session_state
    st.session_state.prediccion_rendimiento = {
        'rendimiento_minimo': rendimiento_minimo,
        'rendimiento_probable': rendimiento_probable,
        'rendimiento_maximo': rendimiento_maximo,
        'produccion_minima': produccion_minima,
        'produccion_probable': produccion_probable,
        'produccion_maxima': produccion_maxima,
        'factor_ajuste': factor_ajuste,
        'factor_region': factor_region,
        'parametros': {
            'fertilidad_suelo': fertilidad_suelo,
            'disponibilidad_agua': disponibilidad_agua,
            'tecnologia': tecnologia,
            'experiencia': experiencia
        }
    }
    
    st.success("✅ Predicción de rendimiento calculada correctamente")
    
else:
    st.error("❌ Cultivo no válido para predicción")