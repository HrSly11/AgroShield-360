"""
Utilidades y Funciones Auxiliares
==================================
Funciones de ayuda comunes para todo el sistema.
"""

import streamlit as st
from datetime import datetime, date
import json
import os
from typing import Any, Dict


def formatear_moneda(valor: float, moneda: str = "S/.") -> str:
    """
    Formatea un valor numérico como moneda.
    
    Args:
        valor: Valor numérico
        moneda: Símbolo de moneda
        
    Returns:
        String formateado
    """
    return f"{moneda} {valor:,.2f}"


def formatear_porcentaje(valor: float, decimales: int = 2) -> str:
    """
    Formatea un valor como porcentaje.
    
    Args:
        valor: Valor decimal (0.25 = 25%)
        decimales: Número de decimales
        
    Returns:
        String formateado
    """
    return f"{valor * 100:.{decimales}f}%"


def formatear_numero(valor: float, decimales: int = 2, 
                    separador_miles: bool = True) -> str:
    """
    Formatea un número con opciones personalizadas.
    
    Args:
        valor: Valor numérico
        decimales: Número de decimales
        separador_miles: Si usar separador de miles
        
    Returns:
        String formateado
    """
    if separador_miles:
        return f"{valor:,.{decimales}f}"
    else:
        return f"{valor:.{decimales}f}"


def calcular_diferencia_dias(fecha1: date, fecha2: date) -> int:
    """
    Calcula la diferencia en días entre dos fechas.
    
    Args:
        fecha1: Primera fecha
        fecha2: Segunda fecha
        
    Returns:
        Número de días de diferencia
    """
    return abs((fecha2 - fecha1).days)


def validar_rango(valor: float, minimo: float, maximo: float) -> bool:
    """
    Valida que un valor esté dentro de un rango.
    
    Args:
        valor: Valor a validar
        minimo: Valor mínimo permitido
        maximo: Valor máximo permitido
        
    Returns:
        True si está en rango, False si no
    """
    return minimo <= valor <= maximo


def calcular_promedio_ponderado(valores: list, pesos: list) -> float:
    """
    Calcula el promedio ponderado de una lista de valores.
    
    Args:
        valores: Lista de valores
        pesos: Lista de pesos
        
    Returns:
        Promedio ponderado
    """
    if len(valores) != len(pesos):
        raise ValueError("Valores y pesos deben tener la misma longitud")
    
    if sum(pesos) == 0:
        return 0
    
    return sum(v * p for v, p in zip(valores, pesos)) / sum(pesos)


def crear_directorio_si_no_existe(ruta: str):
    """
    Crea un directorio si no existe.
    
    Args:
        ruta: Ruta del directorio
    """
    if not os.path.exists(ruta):
        os.makedirs(ruta)


def guardar_json(datos: Dict, ruta: str):
    """
    Guarda datos en formato JSON.
    
    Args:
        datos: Diccionario con datos
        ruta: Ruta del archivo
    """
    crear_directorio_si_no_existe(os.path.dirname(ruta))
    
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4, default=str)


def cargar_json(ruta: str) -> Dict:
    """
    Carga datos desde un archivo JSON.
    
    Args:
        ruta: Ruta del archivo
        
    Returns:
        Diccionario con datos
    """
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def limpiar_session_state(excluir: list = None):
    """
    Limpia el session_state de Streamlit.
    
    Args:
        excluir: Lista de claves a no eliminar
    """
    if excluir is None:
        excluir = []
    
    keys_to_delete = [k for k in st.session_state.keys() if k not in excluir]
    for key in keys_to_delete:
        del st.session_state[key]


def obtener_color_por_valor(valor: float, umbral_bajo: float, 
                           umbral_alto: float, invertir: bool = False) -> str:
    """
    Retorna un color basado en el valor y umbrales.
    
    Args:
        valor: Valor a evaluar
        umbral_bajo: Umbral bajo
        umbral_alto: Umbral alto
        invertir: Si invertir la lógica (menor es mejor)
        
    Returns:
        String con código de color
    """
    if invertir:
        if valor <= umbral_bajo:
            return "#95E1D3"  # Verde
        elif valor <= umbral_alto:
            return "#FFD93D"  # Amarillo
        else:
            return "#FF6B6B"  # Rojo
    else:
        if valor >= umbral_alto:
            return "#95E1D3"  # Verde
        elif valor >= umbral_bajo:
            return "#FFD93D"  # Amarillo
        else:
            return "#FF6B6B"  # Rojo


def obtener_emoji_por_categoria(categoria: str) -> str:
    """
    Retorna un emoji según la categoría.
    
    Args:
        categoria: Categoría (BAJO, MEDIO, ALTO, etc.)
        
    Returns:
        String con emoji
    """
    emojis = {
        'BAJO': '✅',
        'MEDIO': '⚠️',
        'ALTO': '🔴',
        'EXCELENTE': '🌟',
        'BUENO': '👍',
        'REGULAR': '😐',
        'MALO': '👎',
        'VIABLE': '✅',
        'NO VIABLE': '❌'
    }
    
    return emojis.get(categoria.upper(), '❓')


def truncar_texto(texto: str, longitud_maxima: int = 50) -> str:
    """
    Trunca un texto si excede la longitud máxima.
    
    Args:
        texto: Texto a truncar
        longitud_maxima: Longitud máxima permitida
        
    Returns:
        Texto truncado
    """
    if len(texto) <= longitud_maxima:
        return texto
    return texto[:longitud_maxima - 3] + "..."


def convertir_meses_a_texto(meses: int) -> str:
    """
    Convierte número de meses a texto legible.
    
    Args:
        meses: Número de meses
        
    Returns:
        Texto descriptivo
    """
    if meses < 12:
        return f"{meses} meses"
    
    años = meses // 12
    meses_restantes = meses % 12
    
    if meses_restantes == 0:
        return f"{años} año{'s' if años > 1 else ''}"
    else:
        return f"{años} año{'s' if años > 1 else ''} y {meses_restantes} mes{'es' if meses_restantes > 1 else ''}"


def calcular_tasa_crecimiento(valor_inicial: float, valor_final: float) -> float:
    """
    Calcula la tasa de crecimiento porcentual.
    
    Args:
        valor_inicial: Valor inicial
        valor_final: Valor final
        
    Returns:
        Tasa de crecimiento decimal
    """
    if valor_inicial == 0:
        return 0
    
    return (valor_final - valor_inicial) / valor_inicial


def obtener_nombre_mes(numero_mes: int) -> str:
    """
    Retorna el nombre del mes dado su número.
    
    Args:
        numero_mes: Número del mes (1-12)
        
    Returns:
        Nombre del mes
    """
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    
    if 1 <= numero_mes <= 12:
        return meses[numero_mes - 1]
    return "Mes inválido"


def mostrar_alerta_exitosa(mensaje: str):
    """Muestra una alerta de éxito en Streamlit"""
    st.success(f"✅ {mensaje}")


def mostrar_alerta_error(mensaje: str):
    """Muestra una alerta de error en Streamlit"""
    st.error(f"❌ {mensaje}")


def mostrar_alerta_advertencia(mensaje: str):
    """Muestra una alerta de advertencia en Streamlit"""
    st.warning(f"⚠️ {mensaje}")


def mostrar_alerta_info(mensaje: str):
    """Muestra una alerta informativa en Streamlit"""
    st.info(f"ℹ️ {mensaje}")


def crear_card_metrica(titulo: str, valor: Any, delta: Any = None,
                      color: str = "#4ECDC4"):
    """
    Crea una tarjeta de métrica HTML personalizada.
    
    Args:
        titulo: Título de la métrica
        valor: Valor principal
        delta: Valor delta (opcional)
        color: Color de fondo
    """
    delta_html = ""
    if delta is not None:
        delta_html = f'<p style="color: #666; margin: 5px 0 0 0;">{delta}</p>'
    
    card_html = f"""
    <div style="background: linear-gradient(135deg, {color} 0%, {color}CC 100%); 
                padding: 20px; border-radius: 10px; text-align: center; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h4 style="color: white; margin: 0 0 10px 0;">{titulo}</h4>
        <h2 style="color: white; margin: 0;">{valor}</h2>
        {delta_html}
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def validar_datos_completos(datos: Dict, campos_requeridos: list) -> Tuple[bool, list]:
    """
    Valida que un diccionario contenga todos los campos requeridos.
    
    Args:
        datos: Diccionario con datos
        campos_requeridos: Lista de campos requeridos
        
    Returns:
        Tupla (es_valido, campos_faltantes)
    """
    campos_faltantes = [campo for campo in campos_requeridos if campo not in datos]
    return len(campos_faltantes) == 0, campos_faltantes


def generar_id_unico() -> str:
    """
    Genera un ID único basado en timestamp.
    
    Returns:
        String con ID único
    """
    return datetime.now().strftime("%Y%m%d%H%M%S")


def redondear_a_multiplo(valor: float, multiplo: int) -> int:
    """
    Redondea un valor al múltiplo más cercano.
    
    Args:
        valor: Valor a redondear
        multiplo: Múltiplo deseado
        
    Returns:
        Valor redondeado
    """
    return round(valor / multiplo) * multiplo