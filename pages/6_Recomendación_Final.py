import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Recomendación Final", page_icon="🎯", layout="wide")

st.title("🎯 Recomendación Final del Sistema")
st.markdown("---")

# Verificar datos previos
modulos_requeridos = {
    'datos_productor': 'Datos del Productor',
    'prediccion_rendimiento': 'Predicción de Rendimiento',
    'analisis_riesgos': 'Análisis de Riesgos',
    'evaluacion_economica': 'Evaluación Económica',
    'escenarios': 'Simulador de Escenarios'
}

faltantes = []
for modulo, nombre in modulos_requeridos.items():
    if modulo not in st.session_state:
        faltantes.append(nombre)

if faltantes:
    st.error(f"⚠️ Debe completar los siguientes módulos primero: {', '.join(faltantes)}")
    st.stop()

# Recuperar datos
datos = st.session_state.datos_productor
prediccion = st.session_state.prediccion_rendimiento
riesgos = st.session_state.analisis_riesgos
evaluacion = st.session_state.evaluacion_economica
escenarios = st.session_state.escenarios

# Mostrar resumen ejecutivo
st.subheader("📊 Resumen Ejecutivo del Proyecto")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Cultivo", datos['tipo_cultivo'])
    st.metric("Área", f"{datos['area_disponible']:.1f} ha")

with col2:
    st.metric("Inversión", f"S/. {evaluacion['costo_total']:,.0f}")
    st.metric("Ingreso Esperado", f"S/. {evaluacion['ingreso_total']:,.0f}")

with col3:
    st.metric("Utilidad Esperada", f"S/. {evaluacion['utilidad_bruta']:,.0f}")
    st.metric("ROI", f"{evaluacion['utilidad_bruta']/evaluacion['costo_total']*100:.1f}%")

with col4:
    st.metric("VAN", f"S/. {evaluacion['van']:,.0f}")
    st.metric("Índice de Riesgo", f"{riesgos['ira']:.2%}")

st.markdown("---")

# Sistema de puntuación para la recomendación
puntuacion_total = 0
max_puntuacion = 100

# Criterio 1: Rentabilidad (40 puntos)
st.subheader("📈 Análisis de Criterios de Decisión")

col5, col6 = st.columns([3, 1])

with col5:
    st.markdown("### 1. Rentabilidad (40 puntos)")
    
    puntos_rentabilidad = 0
    
    # VAN positivo (15 puntos)
    if evaluacion['van'] > 0:
        puntos_rentabilidad += 15
        st.success("✅ VAN positivo: +15 puntos")
    else:
        st.error("❌ VAN negativo: 0 puntos")
    
    # ROI > 20% (15 puntos)
    roi = evaluacion['utilidad_bruta'] / evaluacion['costo_total'] * 100
    if roi > 50:
        puntos_rentabilidad += 15
        st.success(f"✅ ROI excelente ({roi:.1f}%): +15 puntos")
    elif roi > 20:
        puntos_rentabilidad += 10
        st.success(f"✅ ROI bueno ({roi:.1f}%): +10 puntos")
    elif roi > 0:
        puntos_rentabilidad += 5
        st.warning(f"⚠️ ROI bajo ({roi:.1f}%): +5 puntos")
    else:
        st.error(f"❌ ROI negativo ({roi:.1f}%): 0 puntos")
    
    # Margen de utilidad (10 puntos)
    if evaluacion['margen_utilidad'] > 30:
        puntos_rentabilidad += 10
        st.success(f"✅ Margen excelente ({evaluacion['margen_utilidad']:.1f}%): +10 puntos")
    elif evaluacion['margen_utilidad'] > 15:
        puntos_rentabilidad += 7
        st.success(f"✅ Margen bueno ({evaluacion['margen_utilidad']:.1f}%): +7 puntos")
    elif evaluacion['margen_utilidad'] > 0:
        puntos_rentabilidad += 3
        st.warning(f"⚠️ Margen bajo ({evaluacion['margen_utilidad']:.1f}%): +3 puntos")
    else:
        st.error(f"❌ Margen negativo ({evaluacion['margen_utilidad']:.1f}%): 0 puntos")

with col6:
    st.metric("Puntos Rentabilidad", f"{puntos_rentabilidad}/40")
    progreso_rent = puntos_rentabilidad / 40
    st.progress(progreso_rent)

puntuacion_total += puntos_rentabilidad

st.markdown("---")

# Criterio 2: Riesgo (30 puntos)
col7, col8 = st.columns([3, 1])

with col7:
    st.markdown("### 2. Gestión de Riesgos (30 puntos)")
    
    puntos_riesgo = 0
    ira = riesgos['ira']
    
    # Puntuación inversa al riesgo
    if ira < 0.33:
        puntos_riesgo = 30
        st.success(f"✅ Riesgo BAJO ({ira:.2%}): +30 puntos")
    elif ira < 0.50:
        puntos_riesgo = 22
        st.success(f"✅ Riesgo MEDIO-BAJO ({ira:.2%}): +22 puntos")
    elif ira < 0.67:
        puntos_riesgo = 15
        st.warning(f"⚠️ Riesgo MEDIO ({ira:.2%}): +15 puntos")
    elif ira < 0.80:
        puntos_riesgo = 8
        st.warning(f"⚠️ Riesgo MEDIO-ALTO ({ira:.2%}): +8 puntos")
    else:
        puntos_riesgo = 0
        st.error(f"❌ Riesgo ALTO ({ira:.2%}): 0 puntos")

with col8:
    st.metric("Puntos Riesgo", f"{puntos_riesgo}/30")
    progreso_riesgo = puntos_riesgo / 30
    st.progress(progreso_riesgo)

puntuacion_total += puntos_riesgo

st.markdown("---")

# Criterio 3: Escenarios (20 puntos)
col9, col10 = st.columns([3, 1])

with col9:
    st.markdown("### 3. Estabilidad de Escenarios (20 puntos)")
    
    puntos_escenarios = 0
    
    # Verificar VAN positivo en escenario pesimista
    van_pesimista = escenarios['Pesimista']['van']
    van_base = escenarios['Base']['van']
    van_optimista = escenarios['Optimista']['van']
    
    if van_pesimista > 0:
        puntos_escenarios += 10
        st.success("✅ VAN positivo en escenario pesimista: +10 puntos")
    else:
        st.warning("⚠️ VAN negativo en escenario pesimista: 0 puntos")
    
    # Verificar estabilidad entre escenarios
    variabilidad = (van_optimista - van_pesimista) / van_base if van_base != 0 else 999
    
    if variabilidad < 1.0:
        puntos_escenarios += 10
        st.success(f"✅ Baja variabilidad entre escenarios: +10 puntos")
    elif variabilidad < 2.0:
        puntos_escenarios += 6
        st.success(f"✅ Variabilidad moderada entre escenarios: +6 puntos")
    else:
        puntos_escenarios += 2
        st.warning(f"⚠️ Alta variabilidad entre escenarios: +2 puntos")

with col10:
    st.metric("Puntos Escenarios", f"{puntos_escenarios}/20")
    progreso_esc = puntos_escenarios / 20
    st.progress(progreso_esc)

puntuacion_total += puntos_escenarios

st.markdown("---")

# Criterio 4: Mercado (10 puntos)
col11, col12 = st.columns([3, 1])

with col11:
    st.markdown("### 4. Condiciones de Mercado (10 puntos)")
    
    puntos_mercado = 0
    
    # Precio competitivo
    precio = datos['precio_venta_esperado']
    if precio > 1.5:
        puntos_mercado += 5
        st.success(f"✅ Precio de venta competitivo (S/. {precio:.2f}/kg): +5 puntos")
    else:
        puntos_mercado += 2
        st.warning(f"⚠️ Precio de venta bajo (S/. {precio:.2f}/kg): +2 puntos")
    
    # Rendimiento por encima de mínimo
    rend_probable = prediccion['rendimiento_probable']
    rend_minimo = prediccion['rendimiento_minimo']
    margen_rend = (rend_probable - rend_minimo) / rend_minimo
    
    if margen_rend > 0.5:
        puntos_mercado += 5
        st.success(f"✅ Rendimiento probable supera significativamente al mínimo: +5 puntos")
    elif margen_rend > 0.2:
        puntos_mercado += 3
        st.success(f"✅ Rendimiento probable supera al mínimo: +3 puntos")
    else:
        puntos_mercado += 1
        st.warning(f"⚠️ Margen estrecho entre rendimiento probable y mínimo: +1 punto")

with col12:
    st.metric("Puntos Mercado", f"{puntos_mercado}/10")
    progreso_merc = puntos_mercado / 10
    st.progress(progreso_merc)

puntuacion_total += puntos_mercado

st.markdown("---")

# Mostrar puntuación total
st.subheader("🏆 Puntuación Total del Proyecto")

porcentaje_total = (puntuacion_total / max_puntuacion) * 100

col13, col14, col15 = st.columns([1, 2, 1])

with col14:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=puntuacion_total,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Puntuación Final", 'font': {'size': 24}},
        delta={'reference': 70, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#FF6B6B'},
                {'range': [50, 70], 'color': '#FFD93D'},
                {'range': [70, 100], 'color': '#95E1D3'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig_gauge.update_layout(height=400)
    st.plotly_chart(fig_gauge, use_container_width=True)

# Determinar recomendación
st.markdown("---")
st.subheader("🎯 Recomendación del Sistema AgroShield 360")

if puntuacion_total >= 80:
    recomendacion = "CONVIENE SEMBRAR ESTE CULTIVO"
    color_rec = "#95E1D3"
    emoji_rec = "✅"
    detalle = """
    **PROYECTO ALTAMENTE RECOMENDADO**
    
    El análisis integral indica que este proyecto agrícola presenta:
    - Excelentes indicadores de rentabilidad
    - Riesgos controlados y manejables
    - Estabilidad favorable en diferentes escenarios
    - Condiciones de mercado positivas
    
    **Recomendación**: Proceda con la implementación del proyecto siguiendo las mejores prácticas agronómicas.
    """
elif puntuacion_total >= 60:
    recomendacion = "CONVIENE SEMBRAR CON PRECAUCIONES"
    color_rec = "#FFD93D"
    emoji_rec = "⚠️"
    detalle = """
    **PROYECTO VIABLE CON CONSIDERACIONES**
    
    El proyecto es viable pero requiere atención a:
    - Implementar medidas de mitigación de riesgos identificados
    - Monitorear de cerca las condiciones de mercado
    - Considerar seguros agrícolas
    - Optimizar costos de producción
    
    **Recomendación**: Puede proceder pero implemente las medidas de gestión de riesgo sugeridas.
    """
elif puntuacion_total >= 40:
    recomendacion = "SE RECOMIENDA ROTAR O AJUSTAR CULTIVO"
    color_rec = "#FFA500"
    emoji_rec = "🔄"
    detalle = """
    **PROYECTO CON RIESGOS SIGNIFICATIVOS**
    
    El análisis sugiere considerar:
    - Evaluar cultivos alternativos más rentables
    - Reducir costos de producción
    - Mejorar tecnología y prácticas agronómicas
    - Buscar mercados con mejores precios
    
    **Recomendación**: Considere ajustar el plan antes de proceder o evalúe alternativas.
    """
else:
    recomendacion = "NO SE RECOMIENDA SEMBRAR EN ESTA CAMPAÑA"
    color_rec = "#FF6B6B"
    emoji_rec = "❌"
    detalle = """
    **PROYECTO NO RECOMENDADO**
    
    El análisis indica riesgos significativos:
    - Rentabilidad insuficiente o negativa
    - Riesgos elevados
    - Condiciones desfavorables
    
    **Recomendación**: NO proceda con este proyecto. Evalúe alternativas completamente diferentes o espere condiciones más favorables.
    """

st.markdown(f"""
<div style="background-color: {color_rec}; padding: 30px; border-radius: 15px; text-align: center;">
    <h1 style="color: #2C3E50; margin: 0;">{emoji_rec} {recomendacion}</h1>
    <h3 style="color: #34495E; margin: 10px 0;">Puntuación: {puntuacion_total}/100 ({porcentaje_total:.1f}%)</h3>
</div>
""", unsafe_allow_html=True)

st.markdown(detalle)

# Guardar recomendación
st.session_state.recomendacion_final = {
    'puntuacion_total': puntuacion_total,
    'porcentaje': porcentaje_total,
    'recomendacion': recomendacion,
    'puntos_rentabilidad': puntos_rentabilidad,
    'puntos_riesgo': puntos_riesgo,
    'puntos_escenarios': puntos_escenarios,
    'puntos_mercado': puntos_mercado,
    'detalle': detalle,
    'color': color_rec,
    'emoji': emoji_rec
}

st.success("✅ Recomendación generada exitosamente")