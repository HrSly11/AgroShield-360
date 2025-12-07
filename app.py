"""
AgroShield 360 - Sistema de Análisis Agrícola Integral
=======================================================
Plataforma web para evaluación de rentabilidad, predicción de rendimientos,
gestión de riesgos y análisis económico de proyectos agrícolas.

Autor: AgroShield Team
Versión: 1.0
Fecha: 2024
"""

import streamlit as st
import sys
from pathlib import Path

# Agregar directorio raíz al path
root_dir = Path(__file__).parent
sys.path.append(str(root_dir))

# Configuración de la página principal
st.set_page_config(
    page_title="AgroShield 360",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    /* Estilo general */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Título principal */
    h1 {
        color: #2C3E50;
        font-size: 2.5em;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5em;
    }
    
    /* Subtítulos */
    h2 {
        color: #34495E;
        font-size: 1.8em;
        margin-top: 1em;
    }
    
    h3 {
        color: #4ECDC4;
        font-size: 1.3em;
    }
    
    /* Cards de información */
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    
    /* Botones */
    .stButton>button {
        background-color: #4ECDC4;
        color: white;
        border-radius: 5px;
        padding: 0.5em 2em;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #45B7AA;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 1.8em;
        font-weight: 700;
    }
    
    /* Alertas */
    .stAlert {
        border-radius: 8px;
        padding: 1em;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    
    # Header con logo y título
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1>🌾 AgroShield 360</h1>
            <p style="font-size: 1.2em; color: #666;">
                Sistema Integral de Análisis Agrícola
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Información de bienvenida
    st.markdown("""
    ### 👋 Bienvenido a AgroShield 360
    
    **AgroShield 360** es una plataforma avanzada diseñada para pequeños y medianos productores 
    agrícolas que desean evaluar la viabilidad y rentabilidad de sus proyectos antes de invertir.
    """)
    
    # Características principales
    st.markdown("### ✨ Características Principales")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>📊 Predicción de Rendimiento</h3>
            <p>Modelos predictivos basados en factores agronómicos, climáticos y tecnológicos 
            para estimar rendimientos esperados.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>⚠️ Análisis de Riesgos</h3>
            <p>Evaluación integral de riesgos climáticos, de mercado y de producción con el 
            Índice de Riesgo Agro-Económico (IRA).</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>💰 Evaluación Económica</h3>
            <p>Análisis financiero completo con VAN, TIR, flujo de caja y punto de equilibrio 
            para tomar decisiones informadas.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="info-card">
            <h3>🎲 Simulación de Escenarios</h3>
            <p>Evaluación de escenarios optimistas, base y pesimistas para comprender el rango 
            de resultados posibles.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="info-card">
            <h3>🎯 Recomendaciones Inteligentes</h3>
            <p>Sistema de puntuación y recomendaciones automáticas basadas en criterios múltiples 
            de evaluación.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div class="info-card">
            <h3>📄 Reportes Ejecutivos</h3>
            <p>Generación de reportes completos en múltiples formatos (HTML, PDF, JSON) para 
            compartir y archivar.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Instrucciones de uso
    st.markdown("### 📋 Cómo Usar AgroShield 360")
    
    st.info("""
    **Sigue estos pasos para realizar un análisis completo:**
    
    1. **Datos del Productor** 📝: Ingresa información básica sobre tu proyecto (cultivo, área, ubicación, costos)
    2. **Predicción de Rendimiento** 🌱: Configura parámetros agronómicos y obtén predicciones de rendimiento
    3. **Análisis de Riesgos** ⚠️: Revisa los riesgos identificados y sus componentes
    4. **Evaluación Económica** 💰: Analiza la viabilidad financiera con indicadores clave
    5. **Simulador de Escenarios** 🎲: Explora diferentes escenarios y su impacto
    6. **Recomendación Final** 🎯: Obtén una recomendación basada en el análisis integral
    7. **Generar Reporte** 📄: Descarga un reporte completo de tu análisis
    
    **Navega usando el menú de la izquierda ⬅️**
    """)
    
    # Estadísticas del sistema
    st.markdown("### 📊 Base de Datos del Sistema")
    
    col7, col8, col9, col10 = st.columns(4)
    
    with col7:
        st.metric("Cultivos Soportados", "10", delta="Principales del Perú")
    
    with col8:
        st.metric("Regiones Cubiertas", "13", delta="Todo el Perú")
    
    with col9:
        st.metric("Datos Climáticos", "156", delta="Registros mensuales")
    
    with col10:
        st.metric("Precios Históricos", "120", delta="Datos de 2023")
    
    st.markdown("---")
    
    # Cultivos y regiones soportados
    with st.expander("🌾 Ver Cultivos y Regiones Soportados"):
        col_cultivos, col_regiones = st.columns(2)
        
        with col_cultivos:
            st.markdown("**Cultivos Disponibles:**")
            cultivos = [
                "🌽 Maíz", "🥔 Papa", "🍚 Arroz", "🌾 Trigo",
                "🌾 Quinua", "🥬 Espárrago", "🥑 Palta", "☕ Café",
                "🍫 Cacao", "🌸 Algodón"
            ]
            for cultivo in cultivos:
                st.write(f"  • {cultivo}")
        
        with col_regiones:
            st.markdown("**Regiones Disponibles:**")
            regiones = [
                "Lima", "Arequipa", "La Libertad", "Lambayeque",
                "Piura", "Ica", "Junín", "Cajamarca", "Cusco",
                "Ancash", "Ayacucho", "Huánuco", "San Martín"
            ]
            for region in regiones:
                st.write(f"  • {region}")
    
    # Información técnica
    with st.expander("ℹ️ Información Técnica"):
        st.markdown("""
        **Tecnologías Utilizadas:**
        - **Python 3.10+**: Lenguaje de programación principal
        - **Streamlit**: Framework para la interfaz web
        - **Plotly**: Visualizaciones interactivas
        - **NumPy/Pandas**: Procesamiento de datos
        - **Scikit-learn**: Modelos predictivos
        
        **Modelos Implementados:**
        - Modelo de predicción de rendimiento basado en factores múltiples
        - Modelo de análisis de riesgo multi-dimensional (IRA)
        - Simulación Monte Carlo para análisis de incertidumbre
        - Evaluación económica con VAN, TIR y análisis de sensibilidad
        
        **Base de Datos:**
        - Datos climáticos históricos por región
        - Precios históricos de cultivos
        - Información técnica de cultivos
        - Características regionales del Perú
        """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 20px; color: #666;">
        <p><strong>AgroShield 360</strong> - Sistema de Análisis Agrícola Integral</p>
        <p>Versión 1.0 | © 2024 | Desarrollado para pequeños productores agrícolas del Perú</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Limpiar estado si el usuario lo solicita
    if st.sidebar.button("🔄 Reiniciar Análisis"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Información de estado en sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Estado del Análisis")
    
    modulos_completados = 0
    total_modulos = 6
    
    modulos = [
        ('datos_productor', '📝 Datos del Productor'),
        ('prediccion_rendimiento', '🌱 Predicción'),
        ('analisis_riesgos', '⚠️ Riesgos'),
        ('evaluacion_economica', '💰 Economía'),
        ('escenarios', '🎲 Escenarios'),
        ('recomendacion_final', '🎯 Recomendación')
    ]
    
    for modulo, nombre in modulos:
        if modulo in st.session_state:
            st.sidebar.success(f"✅ {nombre}")
            modulos_completados += 1
        else:
            st.sidebar.warning(f"⏳ {nombre}")
    
    progreso = modulos_completados / total_modulos
    st.sidebar.progress(progreso)
    st.sidebar.metric("Progreso", f"{modulos_completados}/{total_modulos} módulos")
    
    if modulos_completados == total_modulos:
        st.sidebar.balloons()
        st.sidebar.success("🎉 ¡Análisis completo!")


if __name__ == "__main__":
    main()