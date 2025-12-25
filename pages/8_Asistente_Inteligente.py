import streamlit as st
import json
from pathlib import Path

from services.asistente_llm_service import generar_respuesta_ia

# ===============================
# Configuración de página
# ===============================
st.set_page_config(
    page_title="Asistente Inteligente",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Asistente Inteligente AgroShield-360")
st.markdown("Interpretación inteligente basada en tu último análisis agrícola.")

st.markdown("---")

# ===============================
# 1️⃣ Cargar reporte JSON
# ===============================
ruta_reporte = Path("reports/reporte_final.json")

if not ruta_reporte.exists():
    st.warning(
        "⚠️ No se encontró el reporte final.\n\n"
        "👉 Genera el reporte en **formato JSON** desde el módulo *Generar Reporte*."
    )
    st.stop()

try:
    with open(ruta_reporte, "r", encoding="utf-8") as f:
        reporte = json.load(f)
except json.JSONDecodeError:
    st.error("❌ El reporte está vacío o dañado. Genéralo nuevamente.")
    st.stop()

# ===============================
# 2️⃣ Mostrar DATOS REALES del reporte
# ===============================
st.subheader("📊 Resumen del Último Reporte")

datos = reporte["datos_productor"]
eco = reporte["evaluacion_economica"]
rec = reporte["recomendacion_final"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌱 Cultivo", datos["tipo_cultivo"])
    st.metric("📍 Ubicación", datos["ubicacion"])
    st.metric("📐 Área (ha)", datos["area_disponible"])

with col2:
    st.metric("💰 Inversión Total", f"S/. {eco['costo_total']:,.0f}")
    st.metric("📈 Ingresos", f"S/. {eco['ingreso_total']:,.0f}")
    st.metric("💵 Utilidad", f"S/. {eco['utilidad_bruta']:,.0f}")

with col3:
    st.metric("📊 VAN", f"S/. {eco['van']:,.0f}")
    st.metric("📉 TIR", f"{eco['tir']*100:.2f}%")
    st.metric("✅ Recomendación", rec["recomendacion"])

st.markdown("---")

# ===============================
# 3️⃣ Interpretación IA (controlada)
# ===============================
if "interpretacion_ia" not in st.session_state:
    prompt_interpretacion = (
        "Eres un asesor agrícola.\n"
        "Usa ÚNICAMENTE los datos proporcionados.\n"
        "No inventes cultivos ni regiones.\n"
        "Responde en español.\n\n"
        "Explica en máximo 5 líneas:\n"
        "1. Si conviene o no sembrar\n"
        "2. Por qué\n"
        "3. Un consejo práctico para el agricultor"
    )

    with st.spinner("🤖 Generando interpretación del proyecto..."):
        st.session_state.interpretacion_ia = generar_respuesta_ia(
            reporte,
            prompt_interpretacion
        )

st.subheader("🧠 Interpretación del Proyecto")
st.info(st.session_state.interpretacion_ia)

st.markdown("---")

# ===============================
# 4️⃣ Chat conversacional
# ===============================
st.subheader("💬 Conversa con el asistente")

if "chat" not in st.session_state:
    st.session_state.chat = []

pregunta = st.chat_input("Ej: ¿Qué riesgo es el más peligroso?")

if pregunta:
    with st.spinner("🤖 Analizando..."):
        respuesta = generar_respuesta_ia(reporte, pregunta)

    st.session_state.chat.append(("usuario", pregunta))
    st.session_state.chat.append(("ia", respuesta))

for rol, mensaje in st.session_state.chat:
    if rol == "usuario":
        st.chat_message("user").write(mensaje)
    else:
        st.chat_message("assistant").write(mensaje)

# ===============================
# 5️⃣ Ayudas
# ===============================
with st.expander("💡 Preguntas sugeridas"):
    st.markdown("""
- ¿Conviene sembrar este cultivo?
- ¿Qué riesgo debo vigilar más?
- ¿Qué escenario es más rentable?
- ¿Cómo puedo mejorar la utilidad?
- Explícamelo como agricultor.
""")

# ===============================
# 6️⃣ Limpiar chat
# ===============================
st.markdown("---")
if st.button("🧹 Limpiar conversación"):
    st.session_state.chat = []
    st.rerun()
