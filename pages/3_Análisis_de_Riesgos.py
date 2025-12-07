import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Análisis de Riesgos", page_icon="⚠️", layout="wide")

st.title("⚠️ Análisis de Riesgos Agro-Económicos")
st.markdown("---")

# Verificar datos previos
if 'datos_productor' not in st.session_state or not st.session_state.datos_productor:
    st.warning("⚠️ Primero debe ingresar los datos del productor")
    st.stop()

if 'prediccion_rendimiento' not in st.session_state:
    st.warning("⚠️ Primero debe generar la predicción de rendimiento")
    st.stop()

datos = st.session_state.datos_productor
prediccion = st.session_state.prediccion_rendimiento

# Mostrar información general
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Cultivo", datos['tipo_cultivo'])
with col2:
    st.metric("Ubicación", datos['ubicacion'])
with col3:
    st.metric("Área", f"{datos['area_disponible']:.1f} ha")

st.markdown("---")

# Datos simulados de riesgos climáticos por región
riesgos_climaticos = {
    'Lima': {'sequia': 0.3, 'heladas': 0.1, 'lluvias': 0.2, 'plagas': 0.25},
    'Arequipa': {'sequia': 0.4, 'heladas': 0.3, 'lluvias': 0.15, 'plagas': 0.2},
    'La Libertad': {'sequia': 0.25, 'heladas': 0.15, 'lluvias': 0.3, 'plagas': 0.3},
    'Lambayeque': {'sequia': 0.35, 'heladas': 0.05, 'lluvias': 0.4, 'plagas': 0.35},
    'Piura': {'sequia': 0.45, 'heladas': 0.05, 'lluvias': 0.35, 'plagas': 0.3},
    'Ica': {'sequia': 0.5, 'heladas': 0.1, 'lluvias': 0.1, 'plagas': 0.25},
    'Junín': {'sequia': 0.2, 'heladas': 0.4, 'lluvias': 0.35, 'plagas': 0.3},
    'Cajamarca': {'sequia': 0.25, 'heladas': 0.35, 'lluvias': 0.4, 'plagas': 0.35},
    'Cusco': {'sequia': 0.2, 'heladas': 0.5, 'lluvias': 0.3, 'plagas': 0.25},
    'Ancash': {'sequia': 0.3, 'heladas': 0.4, 'lluvias': 0.35, 'plagas': 0.3},
    'Ayacucho': {'sequia': 0.35, 'heladas': 0.4, 'lluvias': 0.3, 'plagas': 0.35},
    'Huánuco': {'sequia': 0.2, 'heladas': 0.35, 'lluvias': 0.45, 'plagas': 0.4},
    'San Martín': {'sequia': 0.15, 'heladas': 0.1, 'lluvias': 0.5, 'plagas': 0.45}
}

# Volatilidad de precios por cultivo (desviación estándar simulada)
volatilidad_precios = {
    'Maíz': 0.25, 'Papa': 0.35, 'Arroz': 0.20, 'Trigo': 0.22,
    'Quinua': 0.30, 'Espárrago': 0.28, 'Palta': 0.32,
    'Café': 0.40, 'Cacao': 0.38, 'Algodón': 0.35
}

# Obtener riesgos específicos
ubicacion = datos['ubicacion']
cultivo = datos['tipo_cultivo']
riesgos = riesgos_climaticos.get(ubicacion, {'sequia': 0.3, 'heladas': 0.2, 
                                              'lluvias': 0.3, 'plagas': 0.3})
volatilidad = volatilidad_precios.get(cultivo, 0.30)

# Calcular componentes del IRA
st.subheader("📊 Componentes del Índice de Riesgo")

col4, col5 = st.columns(2)

with col4:
    st.markdown("### 🌦️ Riesgos Climáticos")
    
    # Calcular riesgo climático agregado
    riesgo_climatico = (riesgos['sequia'] * 0.35 + 
                       riesgos['heladas'] * 0.25 + 
                       riesgos['lluvias'] * 0.25 + 
                       riesgos['plagas'] * 0.15)
    
    df_clima = pd.DataFrame({
        'Tipo': ['Sequía', 'Heladas', 'Lluvias Extremas', 'Plagas/Enfermedades'],
        'Probabilidad': [riesgos['sequia'], riesgos['heladas'], 
                        riesgos['lluvias'], riesgos['plagas']],
        'Peso': ['35%', '25%', '25%', '15%']
    })
    
    fig_clima = px.bar(
        df_clima,
        x='Tipo',
        y='Probabilidad',
        text='Peso',
        color='Probabilidad',
        color_continuous_scale='Reds',
        title="Probabilidad de Eventos Climáticos Adversos"
    )
    fig_clima.update_traces(textposition='outside')
    fig_clima.update_layout(height=350)
    st.plotly_chart(fig_clima, use_container_width=True)
    
    st.metric("Riesgo Climático Agregado", f"{riesgo_climatico:.2%}")

with col5:
    st.markdown("### 💰 Riesgo de Mercado")
    
    # Simular variación histórica de precios
    precio_base = datos['precio_venta_esperado']
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
             'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    np.random.seed(42)
    precios_hist = precio_base * (1 + np.random.normal(0, volatilidad, 12))
    
    df_precios = pd.DataFrame({
        'Mes': meses,
        'Precio': precios_hist
    })
    
    fig_precios = go.Figure()
    fig_precios.add_trace(go.Scatter(
        x=df_precios['Mes'],
        y=df_precios['Precio'],
        mode='lines+markers',
        name='Precio Histórico',
        line=dict(color='#FF6B6B', width=2),
        fill='tozeroy'
    ))
    fig_precios.add_hline(y=precio_base, line_dash="dash", 
                          line_color="blue", annotation_text="Precio Esperado")
    
    fig_precios.update_layout(
        title="Variación Histórica de Precios (12 meses)",
        xaxis_title="Mes",
        yaxis_title="Precio (S/./kg)",
        height=350
    )
    st.plotly_chart(fig_precios, use_container_width=True)
    
    st.metric("Volatilidad de Precios", f"{volatilidad:.2%}")

# Calcular riesgo de producción basado en predicción
variacion_rendimiento = (prediccion['rendimiento_maximo'] - 
                         prediccion['rendimiento_minimo']) / prediccion['rendimiento_probable']
riesgo_produccion = min(variacion_rendimiento / 2, 0.8)

st.markdown("---")
st.subheader("🎯 Cálculo del Índice de Riesgo Agro-Económico (IRA)")

# Pesos para cada componente
peso_climatico = 0.40
peso_mercado = 0.35
peso_produccion = 0.25

# Calcular IRA
ira = (riesgo_climatico * peso_climatico + 
       volatilidad * peso_mercado + 
       riesgo_produccion * peso_produccion)

# Determinar categoría
if ira < 0.33:
    categoria = "BAJO"
    color_ira = "#95E1D3"
    emoji = "✅"
elif ira < 0.67:
    categoria = "MEDIO"
    color_ira = "#FFD93D"
    emoji = "⚠️"
else:
    categoria = "ALTO"
    color_ira = "#FF6B6B"
    emoji = "🔴"

# Mostrar IRA principal
col6, col7, col8 = st.columns([1, 2, 1])

with col7:
    st.markdown(f"""
    <div style="background-color: {color_ira}; padding: 30px; border-radius: 15px; text-align: center;">
        <h1 style="color: #2C3E50; margin: 0;">{emoji} IRA: {ira:.2%}</h1>
        <h2 style="color: #34495E; margin: 10px 0;">Riesgo {categoria}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Desglose de componentes
col9, col10, col11 = st.columns(3)

with col9:
    st.metric(
        "Riesgo Climático",
        f"{riesgo_climatico:.2%}",
        f"Peso: {peso_climatico:.0%}"
    )

with col10:
    st.metric(
        "Riesgo de Mercado",
        f"{volatilidad:.2%}",
        f"Peso: {peso_mercado:.0%}"
    )

with col11:
    st.metric(
        "Riesgo de Producción",
        f"{riesgo_produccion:.2%}",
        f"Peso: {peso_produccion:.0%}"
    )

# Gráfico de radar con componentes
fig_radar = go.Figure()

categorias = ['Climático', 'Mercado', 'Producción']
valores = [riesgo_climatico * 100, volatilidad * 100, riesgo_produccion * 100]

fig_radar.add_trace(go.Scatterpolar(
    r=valores,
    theta=categorias,
    fill='toself',
    name='Nivel de Riesgo',
    line_color='#FF6B6B'
))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    showlegend=False,
    title="Perfil de Riesgo del Proyecto",
    height=450
)

st.plotly_chart(fig_radar, use_container_width=True)

# Recomendaciones
st.markdown("---")
st.subheader("💡 Recomendaciones de Gestión de Riesgo")

recomendaciones = []

if riesgos['sequia'] > 0.4:
    recomendaciones.append("🚰 **Alta probabilidad de sequía**: Implementar sistema de riego eficiente y considerar cultivos resistentes a sequía")

if riesgos['heladas'] > 0.3:
    recomendaciones.append("❄️ **Riesgo de heladas significativo**: Considerar sistemas de protección antiheladas o ajustar fechas de siembra")

if volatilidad > 0.35:
    recomendaciones.append("💰 **Alta volatilidad de precios**: Considerar contratos a futuro o diversificación de mercados")

if riesgo_produccion > 0.5:
    recomendaciones.append("📊 **Alta variabilidad en rendimiento**: Mejorar manejo agronómico y considerar seguros agrícolas")

if ira > 0.5:
    recomendaciones.append("⚠️ **Riesgo general elevado**: Evaluar medidas de mitigación integrales antes de proceder")

for rec in recomendaciones:
    st.info(rec)

if not recomendaciones:
    st.success("✅ El nivel de riesgo es manejable con prácticas agrícolas estándar")

# Guardar análisis de riesgos
st.session_state.analisis_riesgos = {
    'ira': ira,
    'categoria': categoria,
    'riesgo_climatico': riesgo_climatico,
    'riesgo_mercado': volatilidad,
    'riesgo_produccion': riesgo_produccion,
    'componentes': riesgos,
    'recomendaciones': recomendaciones
}

st.success("✅ Análisis de riesgos completado")