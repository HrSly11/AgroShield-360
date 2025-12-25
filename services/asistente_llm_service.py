import subprocess
import json


def generar_respuesta_ia(reporte: dict, pregunta: str) -> str:
    """
    Genera una respuesta usando TinyLlama vía Ollama.
    Compatible con Windows (UTF-8, sin emojis).
    """

    # ===============================
    # 1️⃣ Validaciones básicas
    # ===============================
    if not reporte:
        return "No hay información del proyecto para analizar."

    if not pregunta.strip():
        return "Hazme una pregunta sobre tu proyecto agrícola."

    # ===============================
    # 2️⃣ Preparar contexto (SIN EMOJIS)
    # ===============================
    contexto = f"""
Eres un asesor agrícola experto.
Responde de forma clara, sencilla y práctica,
como si hablaras con un agricultor.

DATOS DEL PROYECTO:

Cultivo: {reporte['datos_productor'].get('tipo_cultivo', 'No especificado')}
Ubicación: {reporte['datos_productor'].get('ubicacion', 'No especificado')}
Área: {reporte['datos_productor'].get('area_disponible', 0)} hectáreas
Duración campaña: {reporte['datos_productor'].get('duracion_dias', 0)} días
Inversión total: {reporte['datos_productor'].get('costo_total', 0)} soles

RENDIMIENTO ESPERADO:
- Mínimo: {reporte['prediccion_rendimiento'].get('rendimiento_minimo', 0)} kg/ha
- Probable: {reporte['prediccion_rendimiento'].get('rendimiento_probable', 0)} kg/ha
- Máximo: {reporte['prediccion_rendimiento'].get('rendimiento_maximo', 0)} kg/ha

RIESGOS:
- Índice de riesgo (IRA): {reporte['analisis_riesgos'].get('ira', 0)}
- Categoría: {reporte['analisis_riesgos'].get('categoria', '')}

ECONOMÍA:
- Ingresos: {reporte['evaluacion_economica'].get('ingreso_total', 0)} soles
- Costos: {reporte['evaluacion_economica'].get('costo_total', 0)} soles
- Utilidad: {reporte['evaluacion_economica'].get('utilidad_bruta', 0)} soles
- VAN: {reporte['evaluacion_economica'].get('van', 0)}
- TIR: {reporte['evaluacion_economica'].get('tir', 0)}

RECOMENDACIÓN GENERAL:
{reporte['recomendacion_final'].get('recomendacion', '')}

Ahora responde a la siguiente pregunta del agricultor
usando este contexto y dando consejos prácticos.
"""

    # ===============================
    # 3️⃣ Prompt final
    # ===============================
    prompt = f"""
{contexto}

PREGUNTA:
{pregunta}

RESPUESTA:
"""

    # Limpieza defensiva UTF-8 (clave para Windows)
    prompt = prompt.encode("utf-8", "ignore").decode("utf-8")

    # ===============================
    # 4️⃣ Llamar a Ollama (TinyLlama)
    # ===============================
    try:
        proceso = subprocess.run(
            ["ollama", "run", "tinyllama"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=120
        )
    except FileNotFoundError:
        return (
            "Ollama no está disponible en el sistema.\n\n"
            "Asegúrate de:\n"
            "- Tener Ollama instalado\n"
            "- Ejecutar: ollama run tinyllama\n"
            "- Que Ollama esté activo"
        )

    # ===============================
    # 5️⃣ Manejo de errores
    # ===============================
    if proceso.returncode != 0:
        return (
            "Error al comunicarse con la IA.\n\n"
            f"Detalle: {proceso.stderr.strip()}"
        )

    respuesta = proceso.stdout.strip()

    if not respuesta:
        return "La IA no generó una respuesta. Intenta nuevamente."

    return respuesta
