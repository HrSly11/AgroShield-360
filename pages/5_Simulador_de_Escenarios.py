import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from numpy_financial import npv

st.set_page_config(page_title="Simulador de Escenarios", page_icon="🎲", layout="wide")

st.title("🎲 Simulador de Escenarios")
st.markdown("---")

# Verificar datos previos
if 'datos_productor' not in st.session_state or not st.session_state.datos_productor:
    st.warning("⚠️ Primero debe completar todos los módulos anteriores")
    st.stop()

if 'prediccion_rendimiento' not in st.session_state:
    st.warning("⚠️ Debe generar la predicción de rendimiento primero")
    st.stop()

if 'evaluacion_economica' not in st.session_state:
    st.warning("⚠️ Debe completar la evaluación económica primero")
    st.stop()

datos = st.session_state.datos_productor
prediccion = st.session_state.prediccion_rendimiento
evaluacion = st.session_state.evaluacion_economica

st.subheader("📊 Comparación de Escenarios")

# Definir escenarios
escenarios = {
    'Pesimista': {
        'factor_rendimiento': 0.80,  # -20%
        'factor_precio': 0.85,        # -15%
        'color': '#FF6B6B',
        'emoji': '😟'
    },
    'Base': {
        'factor_rendimiento': 1.00,
        'factor_precio': 1.00,
        'color': '#FFD93D',
        'emoji': '😐'
    },
    'Optimista': {
        'factor_rendimiento': 1.20,  # +20%
        'factor_precio': 1.15,        # +15%
        'color': '#95E1D3',
        'emoji': '😊'
    }
}

# Calcular resultados para cada escenario
resultados = {}

for nombre, config in escenarios.items():
    # Ajustar rendimiento y precio
    rendimiento_ajustado = prediccion['rendimiento_probable'] * config['factor_rendimiento']
    produccion_ajustada = rendimiento_ajustado * datos['area_disponible']
    precio_ajustado = datos['precio_venta_esperado'] * config['factor_precio']
    
    # Calcular financieros
    ingreso = produccion_ajustada * precio_ajustado
    costo = datos['costo_total']
    utilidad = ingreso - costo
    margen = (utilidad / ingreso * 100) if ingreso > 0 else 0
    roi = (utilidad / costo * 100) if costo > 0 else 0
    
    # Calcular VAN simplificado
    tasa_periodo = evaluacion['tasa_descuento'] / 12
    duracion_meses = max(int(datos['duracion_dias'] / 30), 1)
    
    flujo = [-costo * 0.3]
    for i in range(1, duracion_meses):
        flujo.append(-costo * 0.7 / (duracion_meses - 1))
    flujo.append(ingreso - costo * 0.7 / (duracion_meses - 1))
    
    van_escenario = npv(tasa_periodo, flujo)
    
    resultados[nombre] = {
        'rendimiento': rendimiento_ajustado,
        'produccion': produccion_ajustada,
        'precio': precio_ajustado,
        'ingreso': ingreso,
        'costo': costo,
        'utilidad': utilidad,
        'margen': margen,
        'roi': roi,
        'van': van_escenario,
        'color': config['color'],
        'emoji': config['emoji']
    }

# Mostrar métricas por escenario
col1, col2, col3 = st.columns(3)

for idx, (nombre, resultado) in enumerate(resultados.items()):
    col = [col1, col2, col3][idx]
    
    with col:
        st.markdown(f"""
        <div style="background-color: {resultado['color']}; padding: 20px; border-radius: 10px; text-align: center;">
            <h2 style="color: #2C3E50; margin: 0;">{resultado['emoji']} {nombre}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Rendimiento", f"{resultado['rendimiento']:,.0f} kg/ha")
        st.metric("Producción Total", f"{resultado['produccion']:,.0f} kg")
        st.metric("Precio Venta", f"S/. {resultado['precio']:.2f}/kg")
        st.metric("Ingreso Total", f"S/. {resultado['ingreso']:,.0f}")
        st.metric("Utilidad", f"S/. {resultado['utilidad']:,.0f}")
        st.metric("Margen", f"{resultado['margen']:.1f}%")
        st.metric("ROI", f"{resultado['roi']:.1f}%")
        st.metric("VAN", f"S/. {resultado['van']:,.0f}")

st.markdown("---")

# Gráficos comparativos
st.subheader("📈 Análisis Comparativo")

# Crear DataFrame para gráficos
df_comparacion = pd.DataFrame({
    'Escenario': list(resultados.keys()),
    'Ingresos': [r['ingreso'] for r in resultados.values()],
    'Utilidad': [r['utilidad'] for r in resultados.values()],
    'VAN': [r['van'] for r in resultados.values()],
    'ROI': [r['roi'] for r in resultados.values()]
})

# Gráfico de barras agrupadas
fig_barras = go.Figure()

fig_barras.add_trace(go.Bar(
    name='Ingresos',
    x=df_comparacion['Escenario'],
    y=df_comparacion['Ingresos'],
    marker_color='#4ECDC4',
    text=[f"S/. {v:,.0f}" for v in df_comparacion['Ingresos']],
    textposition='outside'
))

fig_barras.add_trace(go.Bar(
    name='Utilidad',
    x=df_comparacion['Escenario'],
    y=df_comparacion['Utilidad'],
    marker_color='#95E1D3',
    text=[f"S/. {v:,.0f}" for v in df_comparacion['Utilidad']],
    textposition='outside'
))

fig_barras.update_layout(
    title="Comparación de Ingresos y Utilidad por Escenario",
    xaxis_title="Escenario",
    yaxis_title="Monto (S/.)",
    barmode='group',
    height=450
)

st.plotly_chart(fig_barras, use_container_width=True)

# Gráfico de VAN
fig_van = go.Figure()

colors = [resultados[esc]['color'] for esc in df_comparacion['Escenario']]

fig_van.add_trace(go.Bar(
    x=df_comparacion['Escenario'],
    y=df_comparacion['VAN'],
    marker_color=colors,
    text=[f"S/. {v:,.0f}" for v in df_comparacion['VAN']],
    textposition='outside'
))

fig_van.add_hline(y=0, line_dash="dash", line_color="red", 
                  annotation_text="Punto de Equilibrio")

fig_van.update_layout(
    title="Valor Actual Neto (VAN) por Escenario",
    xaxis_title="Escenario",
    yaxis_title="VAN (S/.)",
    height=400
)

st.plotly_chart(fig_van, use_container_width=True)

# Gráfico de ROI
fig_roi = go.Figure()

fig_roi.add_trace(go.Scatter(
    x=df_comparacion['Escenario'],
    y=df_comparacion['ROI'],
    mode='lines+markers',
    marker=dict(size=15, color=colors),
    line=dict(width=3, color='#4ECDC4'),
    text=[f"{v:.1f}%" for v in df_comparacion['ROI']],
    textposition='top center'
))

fig_roi.update_layout(
    title="Retorno sobre Inversión (ROI) por Escenario",
    xaxis_title="Escenario",
    yaxis_title="ROI (%)",
    height=400
)

st.plotly_chart(fig_roi, use_container_width=True)

# Análisis de sensibilidad
st.markdown("---")
st.subheader("🔍 Análisis de Sensibilidad")

col4, col5 = st.columns(2)

with col4:
    st.markdown("### 📊 Sensibilidad al Rendimiento")
    
    # Variar rendimiento de -40% a +40%
    variaciones_rend = np.linspace(-0.4, 0.4, 9)
    vans_rend = []
    
    for var in variaciones_rend:
        factor = 1 + var
        rend_temp = prediccion['rendimiento_probable'] * factor
        prod_temp = rend_temp * datos['area_disponible']
        ing_temp = prod_temp * datos['precio_venta_esperado']
        util_temp = ing_temp - datos['costo_total']
        
        tasa_periodo = evaluacion['tasa_descuento'] / 12
        duracion_meses = max(int(datos['duracion_dias'] / 30), 1)
        flujo_temp = [-datos['costo_total'] * 0.3]
        for i in range(1, duracion_meses):
            flujo_temp.append(-datos['costo_total'] * 0.7 / (duracion_meses - 1))
        flujo_temp.append(ing_temp - datos['costo_total'] * 0.7 / (duracion_meses - 1))
        
        van_temp = npv(tasa_periodo, flujo_temp)
        vans_rend.append(van_temp)
    
    fig_sens_rend = go.Figure()
    fig_sens_rend.add_trace(go.Scatter(
        x=variaciones_rend * 100,
        y=vans_rend,
        mode='lines+markers',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=8)
    ))
    fig_sens_rend.add_hline(y=0, line_dash="dash", line_color="red")
    fig_sens_rend.add_vline(x=0, line_dash="dash", line_color="gray")
    
    fig_sens_rend.update_layout(
        title="Impacto de Variación en Rendimiento",
        xaxis_title="Variación en Rendimiento (%)",
        yaxis_title="VAN (S/.)",
        height=400
    )
    
    st.plotly_chart(fig_sens_rend, use_container_width=True)

with col5:
    st.markdown("### 💰 Sensibilidad al Precio")
    
    # Variar precio de -40% a +40%
    variaciones_precio = np.linspace(-0.4, 0.4, 9)
    vans_precio = []
    
    for var in variaciones_precio:
        factor = 1 + var
        precio_temp = datos['precio_venta_esperado'] * factor
        ing_temp = prediccion['produccion_probable'] * precio_temp
        util_temp = ing_temp - datos['costo_total']
        
        tasa_periodo = evaluacion['tasa_descuento'] / 12
        duracion_meses = max(int(datos['duracion_dias'] / 30), 1)
        flujo_temp = [-datos['costo_total'] * 0.3]
        for i in range(1, duracion_meses):
            flujo_temp.append(-datos['costo_total'] * 0.7 / (duracion_meses - 1))
        flujo_temp.append(ing_temp - datos['costo_total'] * 0.7 / (duracion_meses - 1))
        
        van_temp = npv(tasa_periodo, flujo_temp)
        vans_precio.append(van_temp)
    
    fig_sens_precio = go.Figure()
    fig_sens_precio.add_trace(go.Scatter(
        x=variaciones_precio * 100,
        y=vans_precio,
        mode='lines+markers',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8)
    ))
    fig_sens_precio.add_hline(y=0, line_dash="dash", line_color="red")
    fig_sens_precio.add_vline(x=0, line_dash="dash", line_color="gray")
    
    fig_sens_precio.update_layout(
        title="Impacto de Variación en Precio",
        xaxis_title="Variación en Precio (%)",
        yaxis_title="VAN (S/.)",
        height=400
    )
    
    st.plotly_chart(fig_sens_precio, use_container_width=True)

# Tabla resumen
st.markdown("---")
st.subheader("📋 Tabla Resumen de Escenarios")

df_tabla = pd.DataFrame({
    'Escenario': list(resultados.keys()),
    'Rendimiento (kg/ha)': [f"{r['rendimiento']:,.0f}" for r in resultados.values()],
    'Precio (S/./kg)': [f"{r['precio']:.2f}" for r in resultados.values()],
    'Ingresos (S/.)': [f"{r['ingreso']:,.0f}" for r in resultados.values()],
    'Utilidad (S/.)': [f"{r['utilidad']:,.0f}" for r in resultados.values()],
    'Margen (%)': [f"{r['margen']:.1f}" for r in resultados.values()],
    'ROI (%)': [f"{r['roi']:.1f}" for r in resultados.values()],
    'VAN (S/.)': [f"{r['van']:,.0f}" for r in resultados.values()]
})

st.dataframe(df_tabla, use_container_width=True, hide_index=True)

# Guardar escenarios
st.session_state.escenarios = resultados

st.success("✅ Simulación de escenarios completada")