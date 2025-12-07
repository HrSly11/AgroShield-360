"""
Modelo de Predicción de Rendimiento Agrícola
=============================================
Modelo basado en regresión y factores agronómicos para predecir
el rendimiento de cultivos.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple
import json


class RendimientoModel:
    """
    Modelo predictivo de rendimiento agrícola basado en múltiples factores.
    Utiliza un enfoque de ajuste factorial sobre rendimientos base.
    """
    
    def __init__(self):
        """Inicializa el modelo con parámetros base"""
        self.cultivos_data = self._load_cultivos_data()
        self.regiones_data = self._load_regiones_data()
        
        # Pesos de factores para el modelo
        self.pesos_factores = {
            'fertilidad_suelo': 0.30,
            'disponibilidad_agua': 0.30,
            'tecnologia': 0.25,
            'experiencia': 0.15
        }
        
        # Factores de ajuste por región
        self.factores_region = {
            'Lima': 0.95, 'Arequipa': 0.90, 'La Libertad': 0.92,
            'Lambayeque': 0.88, 'Piura': 0.85, 'Ica': 0.93,
            'Junín': 0.87, 'Cajamarca': 0.86, 'Cusco': 0.84,
            'Ancash': 0.89, 'Ayacucho': 0.85, 'Huánuco': 0.86,
            'San Martín': 0.91
        }
    
    def _load_cultivos_data(self) -> Dict:
        """Carga datos de cultivos desde JSON"""
        try:
            with open('data/cultivos.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {c['nombre']: c for c in data['cultivos']}
        except FileNotFoundError:
            # Datos por defecto si no existe el archivo
            return {
                'Maíz': {'rendimiento_promedio_kg_ha': 8000, 
                        'rendimiento_minimo_kg_ha': 4000,
                        'rendimiento_maximo_kg_ha': 12000},
                'Papa': {'rendimiento_promedio_kg_ha': 25000,
                        'rendimiento_minimo_kg_ha': 15000,
                        'rendimiento_maximo_kg_ha': 35000},
                'Arroz': {'rendimiento_promedio_kg_ha': 9000,
                         'rendimiento_minimo_kg_ha': 6000,
                         'rendimiento_maximo_kg_ha': 12000}
            }
    
    def _load_regiones_data(self) -> Dict:
        """Carga datos de regiones desde JSON"""
        try:
            with open('data/ubicaciones.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {r['nombre']: r for r in data['regiones']}
        except FileNotFoundError:
            return {}
    
    def calcular_factor_ajuste(self, 
                              fertilidad_suelo: float,
                              disponibilidad_agua: float, 
                              tecnologia: float,
                              experiencia: float) -> float:
        """
        Calcula el factor de ajuste basado en los parámetros ingresados.
        
        Args:
            fertilidad_suelo: Escala 1-10
            disponibilidad_agua: Escala 1-10
            tecnologia: Escala 1-10
            experiencia: Años de experiencia
            
        Returns:
            Factor de ajuste entre 0 y 1.2
        """
        # Normalizar experiencia (máximo 20 años)
        exp_normalizada = min(experiencia / 20, 1.0)
        
        # Calcular factor ponderado
        factor = (
            (fertilidad_suelo / 10) * self.pesos_factores['fertilidad_suelo'] +
            (disponibilidad_agua / 10) * self.pesos_factores['disponibilidad_agua'] +
            (tecnologia / 10) * self.pesos_factores['tecnologia'] +
            exp_normalizada * self.pesos_factores['experiencia']
        )
        
        return factor
    
    def predecir_rendimiento(self,
                            cultivo: str,
                            region: str,
                            fertilidad_suelo: float,
                            disponibilidad_agua: float,
                            tecnologia: float,
                            experiencia: float) -> Tuple[float, float, float]:
        """
        Predice el rendimiento del cultivo en kg/ha.
        
        Args:
            cultivo: Nombre del cultivo
            region: Nombre de la región
            fertilidad_suelo: Escala 1-10
            disponibilidad_agua: Escala 1-10
            tecnologia: Escala 1-10
            experiencia: Años de experiencia
            
        Returns:
            Tupla (rendimiento_minimo, rendimiento_probable, rendimiento_maximo)
        """
        # Obtener datos base del cultivo
        if cultivo not in self.cultivos_data:
            raise ValueError(f"Cultivo {cultivo} no encontrado en la base de datos")
        
        cultivo_info = self.cultivos_data[cultivo]
        base_min = cultivo_info['rendimiento_minimo_kg_ha']
        base_medio = cultivo_info['rendimiento_promedio_kg_ha']
        base_max = cultivo_info['rendimiento_maximo_kg_ha']
        
        # Obtener factor regional
        factor_region = self.factores_region.get(region, 0.9)
        
        # Calcular factor de ajuste
        factor_ajuste = self.calcular_factor_ajuste(
            fertilidad_suelo, disponibilidad_agua, tecnologia, experiencia
        )
        
        # Calcular rendimientos ajustados
        rendimiento_minimo = base_min * factor_region * max(factor_ajuste - 0.2, 0.5)
        rendimiento_probable = base_medio * factor_region * factor_ajuste
        rendimiento_maximo = base_max * factor_region * min(factor_ajuste + 0.2, 1.2)
        
        return rendimiento_minimo, rendimiento_probable, rendimiento_maximo
    
    def predecir_con_clima(self,
                          cultivo: str,
                          region: str,
                          mes_siembra: int,
                          fertilidad_suelo: float,
                          disponibilidad_agua: float,
                          tecnologia: float,
                          experiencia: float) -> Dict:
        """
        Predicción avanzada considerando factores climáticos históricos.
        
        Args:
            cultivo: Nombre del cultivo
            region: Nombre de la región
            mes_siembra: Mes de siembra (1-12)
            fertilidad_suelo: Escala 1-10
            disponibilidad_agua: Escala 1-10
            tecnologia: Escala 1-10
            experiencia: Años de experiencia
            
        Returns:
            Diccionario con predicciones detalladas
        """
        # Predicción base
        rend_min, rend_prob, rend_max = self.predecir_rendimiento(
            cultivo, region, fertilidad_suelo, 
            disponibilidad_agua, tecnologia, experiencia
        )
        
        # Ajuste por estacionalidad (ejemplo simplificado)
        meses_optimos = {
            'Maíz': [9, 10, 11],  # Septiembre-Noviembre
            'Papa': [8, 9, 10],    # Agosto-Octubre
            'Arroz': [11, 12, 1],  # Noviembre-Enero
            'Trigo': [4, 5, 6],    # Abril-Junio
            'Quinua': [8, 9, 10],  # Agosto-Octubre
            'Espárrago': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # Todo el año
            'Palta': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # Perenne
            'Café': [4, 5, 6],     # Abril-Junio
            'Cacao': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # Todo el año
            'Algodón': [8, 9, 10]  # Agosto-Octubre
        }
        
        es_mes_optimo = mes_siembra in meses_optimos.get(cultivo, [])
        factor_estacional = 1.0 if es_mes_optimo else 0.92
        
        # Aplicar ajuste estacional
        rend_prob_ajustado = rend_prob * factor_estacional
        rend_max_ajustado = rend_max * factor_estacional
        
        return {
            'rendimiento_minimo': round(rend_min, 2),
            'rendimiento_probable': round(rend_prob_ajustado, 2),
            'rendimiento_maximo': round(rend_max_ajustado, 2),
            'factor_region': self.factores_region.get(region, 0.9),
            'factor_ajuste': round(self.calcular_factor_ajuste(
                fertilidad_suelo, disponibilidad_agua, tecnologia, experiencia
            ), 3),
            'mes_optimo': es_mes_optimo,
            'factor_estacional': factor_estacional,
            'confianza': self._calcular_confianza(
                fertilidad_suelo, disponibilidad_agua, tecnologia
            )
        }
    
    def _calcular_confianza(self, fertilidad: float, agua: float, 
                           tecnologia: float) -> str:
        """Calcula el nivel de confianza de la predicción"""
        promedio = (fertilidad + agua + tecnologia) / 3
        
        if promedio >= 8:
            return "Alta"
        elif promedio >= 6:
            return "Media"
        else:
            return "Baja"
    
    def obtener_recomendaciones(self, 
                               cultivo: str,
                               region: str,
                               rendimiento_probable: float) -> list:
        """
        Genera recomendaciones para mejorar el rendimiento.
        
        Args:
            cultivo: Nombre del cultivo
            region: Nombre de la región
            rendimiento_probable: Rendimiento probable calculado
            
        Returns:
            Lista de recomendaciones
        """
        recomendaciones = []
        
        if cultivo not in self.cultivos_data:
            return recomendaciones
        
        cultivo_info = self.cultivos_data[cultivo]
        rendimiento_base = cultivo_info['rendimiento_promedio_kg_ha']
        
        # Si el rendimiento está por debajo del promedio
        if rendimiento_probable < rendimiento_base * 0.8:
            recomendaciones.append(
                "El rendimiento estimado está por debajo del promedio. "
                "Considere mejorar la fertilidad del suelo y el sistema de riego."
            )
        
        # Recomendaciones específicas por cultivo
        if cultivo == "Papa":
            recomendaciones.append(
                "Para papa, es crucial el control de plagas (especialmente rancha). "
                "Implemente un programa preventivo."
            )
        elif cultivo == "Café":
            recomendaciones.append(
                "El café requiere sombra parcial y control de broca. "
                "Considere plantas de sombrío y manejo integrado de plagas."
            )
        elif cultivo == "Arroz":
            recomendaciones.append(
                "El arroz requiere manejo cuidadoso del agua. "
                "Asegure riego por inundación constante durante la fase vegetativa."
            )
        
        # Recomendación regional
        if region in self.regiones_data:
            region_info = self.regiones_data[region]
            if region_info.get('disponibilidad_agua', '').lower() in ['baja', 'media']:
                recomendaciones.append(
                    f"En {region}, considere sistemas de riego eficiente "
                    "(goteo o aspersión) debido a la limitada disponibilidad de agua."
                )
        
        return recomendaciones


# Función auxiliar para uso rápido
def predecir_rendimiento_rapido(cultivo: str, region: str, 
                                parametros: Dict) -> Dict:
    """
    Función auxiliar para predicción rápida de rendimiento.
    
    Args:
        cultivo: Nombre del cultivo
        region: Nombre de la región
        parametros: Diccionario con parámetros del modelo
        
    Returns:
        Diccionario con resultados de la predicción
    """
    modelo = RendimientoModel()
    
    rend_min, rend_prob, rend_max = modelo.predecir_rendimiento(
        cultivo=cultivo,
        region=region,
        fertilidad_suelo=parametros.get('fertilidad_suelo', 7),
        disponibilidad_agua=parametros.get('disponibilidad_agua', 7),
        tecnologia=parametros.get('tecnologia', 6),
        experiencia=parametros.get('experiencia', 10)
    )
    
    return {
        'rendimiento_minimo': round(rend_min, 2),
        'rendimiento_probable': round(rend_prob, 2),
        'rendimiento_maximo': round(rend_max, 2)
    }