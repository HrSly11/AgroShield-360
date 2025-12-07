"""
Servicio de Predicción de Rendimiento
======================================
Capa de servicio que integra el modelo de rendimiento con la lógica de negocio.
"""

import sys
sys.path.append('.')

from models.rendimiento_model import RendimientoModel, predecir_rendimiento_rapido
from typing import Dict, Tuple
import pandas as pd
import numpy as np


class RendimientoService:
    """Servicio para gestionar predicciones de rendimiento"""
    
    def __init__(self):
        self.modelo = RendimientoModel()
    
    def predecir_rendimiento_completo(self,
                                     cultivo: str,
                                     region: str,
                                     area_disponible: float,
                                     parametros: Dict) -> Dict:
        """
        Realiza una predicción completa de rendimiento incluyendo producción total.
        
        Args:
            cultivo: Nombre del cultivo
            region: Región del cultivo
            area_disponible: Hectáreas disponibles
            parametros: Dict con fertilidad_suelo, disponibilidad_agua, tecnologia, experiencia
            
        Returns:
            Dict con todos los resultados de predicción
        """
        # Predicción de rendimiento por hectárea
        rend_min, rend_prob, rend_max = self.modelo.predecir_rendimiento(
            cultivo=cultivo,
            region=region,
            fertilidad_suelo=parametros.get('fertilidad_suelo', 7),
            disponibilidad_agua=parametros.get('disponibilidad_agua', 7),
            tecnologia=parametros.get('tecnologia', 6),
            experiencia=parametros.get('experiencia', 10)
        )
        
        # Calcular producción total
        prod_min = rend_min * area_disponible
        prod_prob = rend_prob * area_disponible
        prod_max = rend_max * area_disponible
        
        # Obtener recomendaciones
        recomendaciones = self.modelo.obtener_recomendaciones(
            cultivo, region, rend_prob
        )
        
        # Factor de ajuste calculado
        factor_ajuste = self.modelo.calcular_factor_ajuste(
            parametros.get('fertilidad_suelo', 7),
            parametros.get('disponibilidad_agua', 7),
            parametros.get('tecnologia', 6),
            parametros.get('experiencia', 10)
        )
        
        return {
            'rendimiento_minimo': round(rend_min, 2),
            'rendimiento_probable': round(rend_prob, 2),
            'rendimiento_maximo': round(rend_max, 2),
            'produccion_minima': round(prod_min, 2),
            'produccion_probable': round(prod_prob, 2),
            'produccion_maxima': round(prod_max, 2),
            'factor_ajuste': round(factor_ajuste, 3),
            'factor_region': self.modelo.factores_region.get(region, 0.9),
            'parametros': parametros,
            'recomendaciones': recomendaciones,
            'area_disponible': area_disponible
        }
    
    def comparar_cultivos(self,
                         cultivos: list,
                         region: str,
                         area_disponible: float,
                         parametros: Dict) -> pd.DataFrame:
        """
        Compara múltiples cultivos para la misma región y condiciones.
        
        Args:
            cultivos: Lista de nombres de cultivos
            region: Región del cultivo
            area_disponible: Hectáreas disponibles
            parametros: Parámetros del modelo
            
        Returns:
            DataFrame con comparación de cultivos
        """
        resultados = []
        
        for cultivo in cultivos:
            try:
                prediccion = self.predecir_rendimiento_completo(
                    cultivo, region, area_disponible, parametros
                )
                
                resultados.append({
                    'Cultivo': cultivo,
                    'Rendimiento (kg/ha)': prediccion['rendimiento_probable'],
                    'Producción Total (kg)': prediccion['produccion_probable'],
                    'Rend. Mínimo (kg/ha)': prediccion['rendimiento_minimo'],
                    'Rend. Máximo (kg/ha)': prediccion['rendimiento_maximo']
                })
            except:
                continue
        
        return pd.DataFrame(resultados)
    
    def calcular_brecha_productiva(self,
                                   cultivo: str,
                                   rendimiento_actual: float,
                                   rendimiento_objetivo: float = None) -> Dict:
        """
        Calcula la brecha entre rendimiento actual y potencial.
        
        Args:
            cultivo: Nombre del cultivo
            rendimiento_actual: Rendimiento actual del productor
            rendimiento_objetivo: Rendimiento objetivo (opcional)
            
        Returns:
            Dict con análisis de brecha productiva
        """
        cultivo_info = self.modelo.cultivos_data.get(cultivo)
        if not cultivo_info:
            return {'error': 'Cultivo no encontrado'}
        
        if rendimiento_objetivo is None:
            rendimiento_objetivo = cultivo_info['rendimiento_promedio_kg_ha']
        
        brecha_absoluta = rendimiento_objetivo - rendimiento_actual
        brecha_relativa = (brecha_absoluta / rendimiento_objetivo) * 100 if rendimiento_objetivo > 0 else 0
        
        # Categorizar el rendimiento actual
        if rendimiento_actual >= cultivo_info['rendimiento_maximo_kg_ha']:
            categoria = "Excelente"
        elif rendimiento_actual >= cultivo_info['rendimiento_promedio_kg_ha']:
            categoria = "Bueno"
        elif rendimiento_actual >= cultivo_info['rendimiento_minimo_kg_ha']:
            categoria = "Regular"
        else:
            categoria = "Bajo"
        
        return {
            'rendimiento_actual': rendimiento_actual,
            'rendimiento_objetivo': rendimiento_objetivo,
            'brecha_absoluta': round(brecha_absoluta, 2),
            'brecha_relativa': round(brecha_relativa, 2),
            'categoria': categoria,
            'potencial_mejora': round(brecha_absoluta, 2) if brecha_absoluta > 0 else 0
        }


def obtener_prediccion_simple(cultivo: str, region: str, area: float) -> Dict:
    """
    Función auxiliar para obtener predicción rápida con parámetros por defecto.
    
    Args:
        cultivo: Nombre del cultivo
        region: Región
        area: Área en hectáreas
        
    Returns:
        Dict con predicción
    """
    servicio = RendimientoService()
    parametros = {
        'fertilidad_suelo': 7,
        'disponibilidad_agua': 7,
        'tecnologia': 6,
        'experiencia': 10
    }
    return servicio.predecir_rendimiento_completo(cultivo, region, area, parametros)