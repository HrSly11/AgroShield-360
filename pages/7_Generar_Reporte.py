import streamlit as st
from datetime import datetime
import json

st.set_page_config(page_title="Generar Reporte", page_icon="📄", layout="wide")

st.title("📄 Generación de Reporte Ejecutivo")
st.markdown("---")

# Verificar que existan todos los datos
modulos_requeridos = {
    'datos_productor': 'Datos del Productor',
    'prediccion_rendimiento': 'Predicción de Rendimiento',
    'analisis_riesgos': 'Análisis de Riesgos',
    'evaluacion_economica': 'Evaluación Económica',
    'escenarios': 'Simulador de Escenarios',
    'recomendacion_final': 'Recomendación Final'
}

faltantes = []
for modulo, nombre in modulos_requeridos.items():
    if modulo not in st.session_state:
        faltantes.append(nombre)

if faltantes:
    st.error(f"⚠️ Debe completar todos los módulos antes de generar el reporte. Faltan: {', '.join(faltantes)}")
    st.stop()

# Recuperar todos los datos
datos = st.session_state.datos_productor
prediccion = st.session_state.prediccion_rendimiento
riesgos = st.session_state.analisis_riesgos
evaluacion = st.session_state.evaluacion_economica
escenarios = st.session_state.escenarios
recomendacion = st.session_state.recomendacion_final

# Opciones de reporte
st.subheader("⚙️ Configuración del Reporte")

col1, col2 = st.columns(2)

with col1:
    incluir_graficos = st.checkbox("Incluir descripción de gráficos", value=True)
    incluir_detalles = st.checkbox("Incluir detalles técnicos", value=True)

with col2:
    formato_reporte = st.selectbox(
        "Formato de descarga",
        ["HTML", "Texto plano (TXT)", "JSON"]
    )

st.markdown("---")

# Vista previa del reporte
st.subheader("👁️ Vista Previa del Reporte")

# Generar contenido del reporte
fecha_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

reporte_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte AgroShield 360</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .section {{
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        .metric {{
            display: inline-block;
            background: #f8f9fa;
            padding: 15px;
            margin: 10px;
            border-radius: 5px;
            min-width: 200px;
        }}
        .metric-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }}
        .metric-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }}
        .recomendacion {{
            background: {recomendacion['color']};
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }}
        .recomendacion h3 {{
            font-size: 2em;
            margin: 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #667eea;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌾 REPORTE AGROSHIELD 360</h1>
        <p>Análisis Integral de Proyecto Agrícola</p>
        <p>Generado el: {fecha_reporte}</p>
    </div>

    <div class="section">
        <h2>📋 1. INFORMACIÓN GENERAL DEL PROYECTO</h2>
        <div class="metric">
            <div class="metric-label">Productor</div>
            <div class="metric-value">{datos.get('nombre_productor', 'N/A')}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Cultivo</div>
            <div class="metric-value">{datos['tipo_cultivo']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Ubicación</div>
            <div class="metric-value">{datos['ubicacion']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Área</div>
            <div class="metric-value">{datos['area_disponible']:.1f} ha</div>
        </div>
        <div class="metric">
            <div class="metric-label">Duración Campaña</div>
            <div class="metric-value">{datos['duracion_dias']} días</div>
        </div>
        <div class="metric">
            <div class="metric-label">Inversión Total</div>
            <div class="metric-value">S/. {datos['costo_total']:,.0f}</div>
        </div>
    </div>

    <div class="section">
        <h2>🌱 2. PREDICCIÓN DE RENDIMIENTO</h2>
        <table>
            <tr>
                <th>Escenario</th>
                <th>Rendimiento (kg/ha)</th>
                <th>Producción Total (kg)</th>
            </tr>
            <tr>
                <td>Mínimo</td>
                <td>{prediccion['rendimiento_minimo']:,.0f}</td>
                <td>{prediccion['produccion_minima']:,.0f}</td>
            </tr>
            <tr>
                <td>Probable</td>
                <td>{prediccion['rendimiento_probable']:,.0f}</td>
                <td>{prediccion['produccion_probable']:,.0f}</td>
            </tr>
            <tr>
                <td>Máximo</td>
                <td>{prediccion['rendimiento_maximo']:,.0f}</td>
                <td>{prediccion['produccion_maxima']:,.0f}</td>
            </tr>
        </table>
        <p><strong>Factores considerados:</strong></p>
        <ul>
            <li>Fertilidad del suelo: {prediccion['parametros']['fertilidad_suelo']}/10</li>
            <li>Disponibilidad de agua: {prediccion['parametros']['disponibilidad_agua']}/10</li>
            <li>Nivel tecnológico: {prediccion['parametros']['tecnologia']}/10</li>
            <li>Experiencia: {prediccion['parametros']['experiencia']} años</li>
        </ul>
    </div>

    <div class="section">
        <h2>⚠️ 3. ANÁLISIS DE RIESGOS</h2>
        <div class="metric">
            <div class="metric-label">Índice de Riesgo Agro-Económico (IRA)</div>
            <div class="metric-value">{riesgos['ira']:.2%} - {riesgos['categoria']}</div>
        </div>
        <h3>Componentes del Riesgo:</h3>
        <table>
            <tr>
                <th>Tipo de Riesgo</th>
                <th>Nivel</th>
            </tr>
            <tr>
                <td>Riesgo Climático</td>
                <td>{riesgos['riesgo_climatico']:.2%}</td>
            </tr>
            <tr>
                <td>Riesgo de Mercado</td>
                <td>{riesgos['riesgo_mercado']:.2%}</td>
            </tr>
            <tr>
                <td>Riesgo de Producción</td>
                <td>{riesgos['riesgo_produccion']:.2%}</td>
            </tr>
        </table>
        <h3>Recomendaciones de Mitigación:</h3>
        <ul>
"""

for rec in riesgos.get('recomendaciones', []):
    reporte_html += f"            <li>{rec.replace('**', '').replace('🚰', '').replace('❄️', '').replace('💰', '').replace('📊', '').replace('⚠️', '')}</li>\n"

reporte_html += """
        </ul>
    </div>

    <div class="section">
        <h2>💰 4. EVALUACIÓN ECONÓMICA</h2>
        <div class="metric">
            <div class="metric-label">Ingresos Totales</div>
            <div class="metric-value">S/. """ + f"{evaluacion['ingreso_total']:,.0f}" + """</div>
        </div>
        <div class="metric">
            <div class="metric-label">Costos Totales</div>
            <div class="metric-value">S/. """ + f"{evaluacion['costo_total']:,.0f}" + """</div>
        </div>
        <div class="metric">
            <div class="metric-label">Utilidad Bruta</div>
            <div class="metric-value">S/. """ + f"{evaluacion['utilidad_bruta']:,.0f}" + """</div>
        </div>
        <div class="metric">
            <div class="metric-label">Margen de Utilidad</div>
            <div class="metric-value">""" + f"{evaluacion['margen_utilidad']:.1f}%" + """</div>
        </div>
        <div class="metric">
            <div class="metric-label">VAN (VPN)</div>
            <div class="metric-value">S/. """ + f"{evaluacion['van']:,.0f}" + """</div>
        </div>
        <div class="metric">
            <div class="metric-label">TIR</div>
            <div class="metric-value">""" + f"{evaluacion['tir']*100:.2f}%" + """</div>
        </div>
        <div class="metric">
            <div class="metric-label">Punto de Equilibrio</div>
            <div class="metric-value">""" + f"{evaluacion['punto_equilibrio_kg']:,.0f} kg" + """</div>
        </div>
    </div>

    <div class="section">
        <h2>🎲 5. ANÁLISIS DE ESCENARIOS</h2>
        <table>
            <tr>
                <th>Escenario</th>
                <th>Rendimiento</th>
                <th>Precio</th>
                <th>Ingresos</th>
                <th>Utilidad</th>
                <th>VAN</th>
            </tr>
"""

for nombre, esc in escenarios.items():
    reporte_html += f"""
            <tr>
                <td>{nombre}</td>
                <td>{esc['rendimiento']:,.0f} kg/ha</td>
                <td>S/. {esc['precio']:.2f}/kg</td>
                <td>S/. {esc['ingreso']:,.0f}</td>
                <td>S/. {esc['utilidad']:,.0f}</td>
                <td>S/. {esc['van']:,.0f}</td>
            </tr>
"""

reporte_html += f"""
        </table>
    </div>

    <div class="recomendacion">
        <h3>{recomendacion['emoji']} RECOMENDACIÓN FINAL</h3>
        <h2>{recomendacion['recomendacion']}</h2>
        <p><strong>Puntuación del Proyecto: {recomendacion['puntuacion_total']}/100 ({recomendacion['porcentaje']:.1f}%)</strong></p>
    </div>

    <div class="section">
        <h2>📊 6. DETALLE DE PUNTUACIÓN</h2>
        <table>
            <tr>
                <th>Criterio</th>
                <th>Puntos Obtenidos</th>
                <th>Máximo</th>
            </tr>
            <tr>
                <td>Rentabilidad</td>
                <td>{recomendacion['puntos_rentabilidad']}</td>
                <td>40</td>
            </tr>
            <tr>
                <td>Gestión de Riesgos</td>
                <td>{recomendacion['puntos_riesgo']}</td>
                <td>30</td>
            </tr>
            <tr>
                <td>Estabilidad de Escenarios</td>
                <td>{recomendacion['puntos_escenarios']}</td>
                <td>20</td>
            </tr>
            <tr>
                <td>Condiciones de Mercado</td>
                <td>{recomendacion['puntos_mercado']}</td>
                <td>10</td>
            </tr>
            <tr style="font-weight: bold; background-color: #f0f0f0;">
                <td>TOTAL</td>
                <td>{recomendacion['puntuacion_total']}</td>
                <td>100</td>
            </tr>
        </table>
    </div>

    <div class="footer">
        <p><strong>AgroShield 360</strong> - Sistema de Análisis Agrícola Integral</p>
        <p>Este reporte ha sido generado automáticamente basado en los datos ingresados y modelos predictivos.</p>
        <p>© AgroShield 360. Todos los derechos reservados.</p>
    </div>
</body>
</html>
"""

# Mostrar vista previa
with st.expander("📄 Ver Vista Previa Completa", expanded=True):
    st.components.v1.html(reporte_html, height=800, scrolling=True)

st.markdown("---")

# Botones de descarga
st.subheader("⬇️ Descargar Reporte")

col3, col4, col5 = st.columns(3)

with col3:
    if formato_reporte == "HTML":
        st.download_button(
            label="📥 Descargar HTML",
            data=reporte_html,
            file_name=f"reporte_agroshield_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            type="primary",
            use_container_width=True
        )

with col4:
    if formato_reporte == "Texto plano (TXT)":
        # Generar versión texto
        reporte_txt = f"""
REPORTE AGROSHIELD 360
======================
Generado el: {fecha_reporte}

1. INFORMACIÓN GENERAL
----------------------
Productor: {datos.get('nombre_productor', 'N/A')}
Cultivo: {datos['tipo_cultivo']}
Ubicación: {datos['ubicacion']}
Área: {datos['area_disponible']:.1f} ha
Duración: {datos['duracion_dias']} días
Inversión: S/. {datos['costo_total']:,.0f}

2. PREDICCIÓN DE RENDIMIENTO
-----------------------------
Rendimiento Mínimo: {prediccion['rendimiento_minimo']:,.0f} kg/ha
Rendimiento Probable: {prediccion['rendimiento_probable']:,.0f} kg/ha
Rendimiento Máximo: {prediccion['rendimiento_maximo']:,.0f} kg/ha

3. ANÁLISIS DE RIESGOS
-----------------------
IRA: {riesgos['ira']:.2%} - {riesgos['categoria']}
Riesgo Climático: {riesgos['riesgo_climatico']:.2%}
Riesgo de Mercado: {riesgos['riesgo_mercado']:.2%}
Riesgo de Producción: {riesgos['riesgo_produccion']:.2%}

4. EVALUACIÓN ECONÓMICA
------------------------
Ingresos: S/. {evaluacion['ingreso_total']:,.0f}
Costos: S/. {evaluacion['costo_total']:,.0f}
Utilidad: S/. {evaluacion['utilidad_bruta']:,.0f}
VAN: S/. {evaluacion['van']:,.0f}
TIR: {evaluacion['tir']*100:.2f}%

5. RECOMENDACIÓN FINAL
-----------------------
{recomendacion['recomendacion']}
Puntuación: {recomendacion['puntuacion_total']}/100

---
AgroShield 360 © 2024
        """
        
        st.download_button(
            label="📥 Descargar TXT",
            data=reporte_txt,
            file_name=f"reporte_agroshield_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            type="primary",
            use_container_width=True
        )

with col5:
    if formato_reporte == "JSON":
        # Generar versión JSON
        reporte_json = {
            'fecha_generacion': fecha_reporte,
            'datos_productor': datos,
            'prediccion_rendimiento': prediccion,
            'analisis_riesgos': riesgos,
            'evaluacion_economica': evaluacion,
            'escenarios': {k: v for k, v in escenarios.items()},
            'recomendacion_final': recomendacion
        }
        
        st.download_button(
            label="📥 Descargar JSON",
            data=json.dumps(reporte_json, indent=2, ensure_ascii=False, default=str),
            file_name=f"reporte_agroshield_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            type="primary",
            use_container_width=True
        )

st.success("✅ Reporte generado exitosamente. Use los botones de arriba para descargar en el formato deseado.")

# Opción para reiniciar
st.markdown("---")
if st.button("🔄 Iniciar Nuevo Análisis", type="secondary"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()