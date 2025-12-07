import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from numpy_financial import npv, irr

st.set_page_config(page_title="Evaluación Económica", page_icon="💰", layout="wide")

st.title("💰 Evaluación Económica del Proyecto")
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

# Parámetros económicos
st.sidebar.subheader("⚙️ Parámetros Económicos")
tasa_descuento = st.sidebar.slider(
    "Tasa de Descuento Anual (%)",
    min_value=5.0,
    max_value=30.0,
    value=12.0,
    step=0.5,
    help="Tasa de descuento para calcular el VAN"
) / 100

# Mostrar información general
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Cultivo", datos['tipo_cultivo'])
with col2:
    st.metric("Inversión Total", f"S/. {datos['costo_total']:,.0f}")
with col3:
    st.metric("Duración", f"{datos['duracion_dias']} días")
with col4:
    st.metric("Tasa Descuento", f"{tasa_descuento*100:.1f}%")

st.markdown("---")

# Calcular ingresos y costos
produccion_esperada = prediccion['produccion_probable']
precio_venta = datos['precio_venta_esperado']
ingreso_total = produccion_esperada * precio_venta
costo_total = datos['costo_total']

# Calcular utilidad
utilidad_bruta = ingreso_total - costo_total
margen_utilidad = (utilidad_bruta / ingreso_total * 100) if ingreso_total > 0 else 0

# Calcular punto de equilibrio
if precio_venta > 0:
    punto_equilibrio_kg = costo_total / precio_venta
    punto_equilibrio_ha = punto_equilibrio_kg / datos['area_disponible']
else:
    punto_equilibrio_kg = 0
    punto_equilibrio_ha = 0

st.subheader("📊 Resumen Financiero")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Ingresos Totales",
        f"S/. {ingreso_total:,.0f}",
        delta=None
    )

with col6:
    st.metric(
        "Costos Totales",
        f"S/. {costo_total:,.0f}",
        delta=None
    )

with col7:
    st.metric(
        "Utilidad Bruta",
        f"S/. {utilidad_bruta:,.0f}",
        delta=f"{margen_utilidad:.1f}%"
    )

with col8:
    st.metric(
        "ROI",
        f"{(utilidad_bruta/costo_total*100):.1f}%",
        delta=None
    )

# Gráfico de ingresos vs costos
st.markdown("---")

fig_financiero = go.Figure()

fig_financiero.add_trace(go.Bar(
    name='Ingresos',
    x=['Financiero'],
    y=[ingreso_total],
    marker_color='#95E1D3',
    text=[f"S/. {ingreso_total:,.0f}"],
    textposition='auto'
))

fig_financiero.add_trace(go.Bar(
    name='Costos',
    x=['Financiero'],
    y=[costo_total],
    marker_color='#FF6B6B',
    text=[f"S/. {costo_total:,.0f}"],
    textposition='auto'
))

fig_financiero.add_trace(go.Bar(
    name='Utilidad',
    x=['Financiero'],
    y=[utilidad_bruta],
    marker_color='#4ECDC4',
    text=[f"S/. {utilidad_bruta:,.0f}"],
    textposition='auto'
))

fig_financiero.update_layout(
    title="Comparación Financiera",
    xaxis_title="",
    yaxis_title="Monto (S/.)",
    barmode='group',
    height=400
)

st.plotly_chart(fig_financiero, use_container_width=True)

# Desglose de costos
st.markdown("---")
st.subheader("💸 Desglose de Costos")

costos_detalle = {
    'Mano de Obra': datos['costo_mano_obra'],
    'Semillas/Plantones': datos['costo_semillas'],
    'Fertilizantes': datos['costo_fertilizantes'],
    'Agua/Riego': datos['costo_agua'],
    'Maquinaria': datos['costo_maquinaria'],
    'Otros': datos['otros_costos']
}

df_costos = pd.DataFrame({
    'Categoría': list(costos_detalle.keys()),
    'Monto': list(costos_detalle.values()),
    'Porcentaje': [v/costo_total*100 for v in costos_detalle.values()]
})

col9, col10 = st.columns(2)

with col9:
    fig_pie = go.Figure(data=[go.Pie(
        labels=df_costos['Categoría'],
        values=df_costos['Monto'],
        hole=0.4,
        textinfo='label+percent',
        marker=dict(colors=['#FF6B6B', '#4ECDC4', '#95E1D3', 
                           '#FFD93D', '#6C5CE7', '#A29BFE'])
    )])
    
    fig_pie.update_layout(
        title="Distribución de Costos",
        height=400
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

with col10:
    st.dataframe(
        df_costos.style.format({
            'Monto': 'S/. {:,.0f}',
            'Porcentaje': '{:.1f}%'
        }),
        height=400,
        use_container_width=True
    )

# Flujo de caja
st.markdown("---")
st.subheader("💵 Flujo de Caja Proyectado")

# Simular flujo mensual
duracion_meses = max(int(datos['duracion_dias'] / 30), 1)
meses = list(range(duracion_meses + 1))

# Distribuir costos a lo largo del tiempo
costos_mensuales = []
costos_mensuales.append(-costo_total * 0.3)  # Inversión inicial

for i in range(1, duracion_meses):
    costos_mensuales.append(-costo_total * 0.7 / (duracion_meses - 1))

costos_mensuales.append(ingreso_total - costo_total * 0.7 / (duracion_meses - 1))

flujo_acumulado = np.cumsum(costos_mensuales)

df_flujo = pd.DataFrame({
    'Mes': meses,
    'Flujo': costos_mensuales,
    'Acumulado': flujo_acumulado
})

fig_flujo = go.Figure()

fig_flujo.add_trace(go.Bar(
    x=df_flujo['Mes'],
    y=df_flujo['Flujo'],
    name='Flujo Mensual',
    marker_color=['red' if x < 0 else 'green' for x in df_flujo['Flujo']]
))

fig_flujo.add_trace(go.Scatter(
    x=df_flujo['Mes'],
    y=df_flujo['Acumulado'],
    name='Flujo Acumulado',
    mode='lines+markers',
    line=dict(color='#4ECDC4', width=3),
    yaxis='y2'
))

fig_flujo.update_layout(
    title="Flujo de Caja del Proyecto",
    xaxis_title="Mes",
    yaxis=dict(title="Flujo Mensual (S/.)"),
    yaxis2=dict(title="Flujo Acumulado (S/.)", overlaying='y', side='right'),
    height=400,
    hovermode='x unified'
)

st.plotly_chart(fig_flujo, use_container_width=True)

# Cálculo de VAN y TIR
st.markdown("---")
st.subheader("📈 Indicadores de Rentabilidad")

# Convertir tasa anual a tasa por período
tasa_periodo = tasa_descuento / 12

# Calcular VAN
van = npv(tasa_periodo, costos_mensuales)

# Calcular TIR
try:
    tir_periodo = irr(costos_mensuales)
    tir_anual = (1 + tir_periodo) ** 12 - 1
except:
    tir_anual = None

# Período de recuperación
periodos_recuperacion = None
for i, acum in enumerate(flujo_acumulado):
    if acum >= 0:
        periodos_recuperacion = i
        break

col11, col12, col13, col14 = st.columns(4)

with col11:
    color_van = "normal" if van > 0 else "inverse"
    st.metric(
        "VAN (VPN)",
        f"S/. {van:,.0f}",
        delta="Positivo" if van > 0 else "Negativo",
        delta_color=color_van
    )

with col12:
    if tir_anual is not None:
        st.metric(
            "TIR Anual",
            f"{tir_anual*100:.2f}%",
            delta=f"{(tir_anual - tasa_descuento)*100:.2f}% vs tasa desc."
        )
    else:
        st.metric("TIR Anual", "N/A")

with col13:
    st.metric(
        "Punto de Equilibrio",
        f"{punto_equilibrio_kg:,.0f} kg",
        delta=f"{punto_equilibrio_ha:,.0f} kg/ha"
    )

with col14:
    if periodos_recuperacion:
        st.metric(
            "Período de Recuperación",
            f"{periodos_recuperacion} meses",
            delta=None
        )
    else:
        st.metric("Período de Recuperación", "No se recupera")

# Análisis de rentabilidad
st.markdown("---")
st.subheader("🎯 Análisis de Viabilidad")

viabilidad_economica = "VIABLE" if van > 0 and utilidad_bruta > 0 else "NO VIABLE"
color_viabilidad = "#95E1D3" if viabilidad_economica == "VIABLE" else "#FF6B6B"

col15, col16 = st.columns([2, 1])

with col15:
    st.markdown(f"""
    <div style="background-color: {color_viabilidad}; padding: 20px; border-radius: 10px;">
        <h2 style="color: #2C3E50; margin: 0;">Proyecto {viabilidad_economica}</h2>
        <p style="color: #34495E; margin: 10px 0;">
            {'✅ El proyecto presenta indicadores económicos positivos' if viabilidad_economica == 'VIABLE' 
             else '❌ El proyecto presenta indicadores económicos negativos'}
        </p>
    </div>
    """, unsafe_allow_html=True)

with col16:
    if van > 0:
        st.success("VAN Positivo ✅")
    else:
        st.error("VAN Negativo ❌")
    
    if utilidad_bruta > 0:
        st.success("Utilidad Positiva ✅")
    else:
        st.error("Pérdida ❌")

# Guardar evaluación económica
st.session_state.evaluacion_economica = {
    'ingreso_total': ingreso_total,
    'costo_total': costo_total,
    'utilidad_bruta': utilidad_bruta,
    'margen_utilidad': margen_utilidad,
    'van': van,
    'tir': tir_anual if tir_anual else 0,
    'punto_equilibrio_kg': punto_equilibrio_kg,
    'punto_equilibrio_ha': punto_equilibrio_ha,
    'periodo_recuperacion': periodos_recuperacion,
    'viabilidad': viabilidad_economica,
    'tasa_descuento': tasa_descuento,
    'flujo_caja': costos_mensuales
}

st.success("✅ Evaluación económica completada")