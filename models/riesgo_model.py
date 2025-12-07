"""
Modelo de Análisis de Riesgos Agro-Económicos
==============================================
Modelo para evaluar y cuantificar riesgos en proyectos agrícolas.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import json


class RiesgoModel:
    """
    Modelo de análisis de riesgos que evalúa múltiples factores
    para calcular el Índice de Riesgo Agro-Económico (IRA).
    """
    
    def __init__(self):
        """Inicializa el modelo con datos de riesgos"""
        self.riesgos_climaticos = self._load_riesgos_climaticos()
        self.volatilidad_precios = self._load_volatilidad_precios()
        
        # Pesos de componentes del IRA
        self.pesos_ira = {
            'climatico': 0.40,
            'mercado': 0.35,
            'produccion': 0.25
        }
        
        # Umbrales de categorización
        self.umbrales = {
            'bajo': 0.33,
            'medio': 0.67,
            'alto': 1.00
        }
    
    def _load_riesgos_climaticos(self) -> Dict:
        """Carga datos de riesgos climáticos por región"""
        try:
            df = pd.read_csv('data/clima_simulado.csv')
            riesgos_por_region = {}
            
            for region in df['region'].unique():
                region_data = df[df['region'] == region]
                riesgos_por_region[region] = {
                    'sequia': region_data['riesgo_sequia'].mean(),
                    'heladas': region_data['riesgo_heladas'].mean(),
                    'inundacion': region_data['riesgo_inundacion'].mean(),
                    'temperatura_promedio': region_data['temperatura_promedio'].mean(),
                    'precipitacion_promedio': region_data['precipitacion_mm'].mean()
                }
            
            return riesgos_por_region
        except FileNotFoundError:
            # Datos por defecto
            return {
                'Lima': {'sequia': 0.3, 'heladas': 0.1, 'inundacion': 0.2},
                'Arequipa': {'sequia': 0.4, 'heladas': 0.3, 'inundacion': 0.15},
                'La Libertad': {'sequia': 0.25, 'heladas': 0.15, 'inundacion': 0.3}
            }
    
    def _load_volatilidad_precios(self) -> Dict:
        """Carga volatilidad histórica de precios por cultivo"""
        try:
            df = pd.read_csv('data/precios_historicos.csv')
            volatilidad = {}
            
            for cultivo in df['cultivo'].unique():
                cultivo_data = df[df['cultivo'] == cultivo]
                precios = cultivo_data['precio_promedio_soles_kg'].values
                
                # Calcular volatilidad (desviación estándar / media)
                if len(precios) > 0:
                    vol = np.std(precios) / np.mean(precios)
                    volatilidad[cultivo] = round(vol, 3)
            
            return volatilidad
        except FileNotFoundError:
            # Volatilidades por defecto
            return {
                'Maíz': 0.25, 'Papa': 0.35, 'Arroz': 0.20,
                'Trigo': 0.22, 'Quinua': 0.30, 'Espárrago': 0.28,
                'Palta': 0.32, 'Café': 0.40, 'Cacao': 0.38, 'Algodón': 0.35
            }
    
    def calcular_riesgo_climatico(self, region: str, 
                                  mes_siembra: int = None) -> Dict:
        """
        Calcula el riesgo climático para una región específica.
        
        Args:
            region: Nombre de la región
            mes_siembra: Mes de siembra (1-12), opcional
            
        Returns:
            Diccionario con componentes y riesgo total
        """
        if region not in self.riesgos_climaticos:
            region = 'Lima'  # Default
        
        riesgos = self.riesgos_climaticos[region]
        
        # Agregar factor de plagas (estimado)
        riesgo_plagas = 0.25 + (riesgos.get('temperatura_promedio', 20) - 15) * 0.01
        riesgo_plagas = max(0.15, min(riesgo_plagas, 0.45))
        
        componentes = {
            'sequia': riesgos.get('sequia', 0.3),
            'heladas': riesgos.get('heladas', 0.2),
            'lluvias': riesgos.get('inundacion', 0.25),
            'plagas': riesgo_plagas
        }
        
        # Calcular riesgo climático agregado con pesos
        riesgo_total = (
            componentes['sequia'] * 0.35 +
            componentes['heladas'] * 0.25 +
            componentes['lluvias'] * 0.25 +
            componentes['plagas'] * 0.15
        )
        
        # Ajuste estacional si se proporciona mes
        if mes_siembra:
            factor_estacional = self._calcular_factor_estacional(region, mes_siembra)
            riesgo_total *= factor_estacional
        
        return {
            'componentes': componentes,
            'riesgo_total': round(riesgo_total, 4),
            'categoria': self._categorizar_riesgo(riesgo_total)
        }
    
    def _calcular_factor_estacional(self, region: str, mes: int) -> float:
        """Calcula factor de ajuste estacional del riesgo"""
        # Meses de mayor riesgo climático por región (simplificado)
        meses_riesgo_alto = {
            'Lima': [6, 7, 8, 9],  # Invierno
            'Arequipa': [6, 7, 8],
            'Junín': [1, 2, 3, 12],  # Temporada de lluvias
            'Cusco': [1, 2, 3, 12],
            'Piura': [1, 2, 3, 4]  # Lluvias/Niño
        }
        
        if mes in meses_riesgo_alto.get(region, []):
            return 1.15  # Incremento del 15% en meses críticos
        return 1.0
    
    def calcular_riesgo_mercado(self, cultivo: str,
                               precio_esperado: float = None) -> Dict:
        """
        Calcula el riesgo de mercado basado en volatilidad de precios.
        
        Args:
            cultivo: Nombre del cultivo
            precio_esperado: Precio esperado de venta (opcional)
            
        Returns:
            Diccionario con volatilidad y nivel de riesgo
        """
        volatilidad = self.volatilidad_precios.get(cultivo, 0.30)
        
        # Calcular precio promedio histórico si está disponible
        precio_historico = None
        try:
            df = pd.read_csv('data/precios_historicos.csv')
            cultivo_data = df[df['cultivo'] == cultivo]
            if not cultivo_data.empty:
                precio_historico = cultivo_data['precio_promedio_soles_kg'].mean()
        except:
            pass
        
        # Evaluar si el precio esperado es realista
        desviacion_precio = 0
        if precio_esperado and precio_historico:
            desviacion_precio = abs(precio_esperado - precio_historico) / precio_historico
        
        # Ajustar riesgo si la expectativa de precio es muy alta/baja
        riesgo_ajustado = volatilidad
        if desviacion_precio > 0.3:
            riesgo_ajustado *= 1.2  # Incrementar riesgo por expectativa poco realista
        
        return {
            'volatilidad': round(volatilidad, 4),
            'riesgo_ajustado': round(riesgo_ajustado, 4),
            'precio_historico': round(precio_historico, 2) if precio_historico else None,
            'desviacion_precio': round(desviacion_precio, 4) if precio_esperado else 0,
            'categoria': self._categorizar_riesgo(riesgo_ajustado)
        }
    
    def calcular_riesgo_produccion(self, 
                                   rendimiento_minimo: float,
                                   rendimiento_probable: float,
                                   rendimiento_maximo: float) -> Dict:
        """
        Calcula el riesgo de producción basado en variabilidad de rendimientos.
        
        Args:
            rendimiento_minimo: Rendimiento mínimo esperado (kg/ha)
            rendimiento_probable: Rendimiento probable (kg/ha)
            rendimiento_maximo: Rendimiento máximo esperado (kg/ha)
            
        Returns:
            Diccionario con métricas de riesgo de producción
        """
        # Calcular coeficiente de variación
        rango = rendimiento_maximo - rendimiento_minimo
        cv = rango / rendimiento_probable if rendimiento_probable > 0 else 0
        
        # Normalizar el CV a un riesgo entre 0 y 1
        riesgo_produccion = min(cv / 2, 0.8)
        
        # Calcular margen de seguridad
        margen_seguridad = (rendimiento_probable - rendimiento_minimo) / rendimiento_probable
        
        return {
            'coeficiente_variacion': round(cv, 4),
            'riesgo': round(riesgo_produccion, 4),
            'margen_seguridad': round(margen_seguridad, 4),
            'estabilidad': 'Alta' if cv < 0.3 else 'Media' if cv < 0.6 else 'Baja',
            'categoria': self._categorizar_riesgo(riesgo_produccion)
        }
    
    def calcular_ira(self,
                    region: str,
                    cultivo: str,
                    rendimiento_minimo: float,
                    rendimiento_probable: float,
                    rendimiento_maximo: float,
                    precio_esperado: float = None,
                    mes_siembra: int = None) -> Dict:
        """
        Calcula el Índice de Riesgo Agro-Económico (IRA) completo.
        
        Args:
            region: Nombre de la región
            cultivo: Nombre del cultivo
            rendimiento_minimo: Rendimiento mínimo esperado
            rendimiento_probable: Rendimiento probable
            rendimiento_maximo: Rendimiento máximo esperado
            precio_esperado: Precio de venta esperado
            mes_siembra: Mes de siembra
            
        Returns:
            Diccionario con IRA y componentes detallados
        """
        # Calcular componentes individuales
        riesgo_clim = self.calcular_riesgo_climatico(region, mes_siembra)
        riesgo_merc = self.calcular_riesgo_mercado(cultivo, precio_esperado)
        riesgo_prod = self.calcular_riesgo_produccion(
            rendimiento_minimo, rendimiento_probable, rendimiento_maximo
        )
        
        # Calcular IRA ponderado
        ira = (
            riesgo_clim['riesgo_total'] * self.pesos_ira['climatico'] +
            riesgo_merc['riesgo_ajustado'] * self.pesos_ira['mercado'] +
            riesgo_prod['riesgo'] * self.pesos_ira['produccion']
        )
        
        # Categorizar IRA
        if ira < self.umbrales['bajo']:
            categoria = 'BAJO'
            color = '#95E1D3'
        elif ira < self.umbrales['medio']:
            categoria = 'MEDIO'
            color = '#FFD93D'
        else:
            categoria = 'ALTO'
            color = '#FF6B6B'
        
        # Generar recomendaciones
        recomendaciones = self.generar_recomendaciones(
            riesgo_clim, riesgo_merc, riesgo_prod, categoria
        )
        
        return {
            'ira': round(ira, 4),
            'categoria': categoria,
            'color': color,
            'componentes': {
                'climatico': riesgo_clim,
                'mercado': riesgo_merc,
                'produccion': riesgo_prod
            },
            'pesos': self.pesos_ira,
            'recomendaciones': recomendaciones
        }
    
    def generar_recomendaciones(self,
                               riesgo_climatico: Dict,
                               riesgo_mercado: Dict,
                               riesgo_produccion: Dict,
                               categoria_ira: str) -> List[str]:
        """
        Genera recomendaciones basadas en el análisis de riesgos.
        
        Args:
            riesgo_climatico: Resultados del análisis climático
            riesgo_mercado: Resultados del análisis de mercado
            riesgo_produccion: Resultados del análisis de producción
            categoria_ira: Categoría del IRA (BAJO, MEDIO, ALTO)
            
        Returns:
            Lista de recomendaciones
        """
        recomendaciones = []
        
        # Recomendaciones climáticas
        componentes_clim = riesgo_climatico['componentes']
        if componentes_clim['sequia'] > 0.4:
            recomendaciones.append(
                "🚰 Alta probabilidad de sequía: Implementar sistema de riego "
                "eficiente y considerar cultivos resistentes a sequía"
            )
        
        if componentes_clim['heladas'] > 0.3:
            recomendaciones.append(
                "❄️ Riesgo de heladas significativo: Considerar sistemas de "
                "protección antiheladas o ajustar fechas de siembra"
            )
        
        if componentes_clim['lluvias'] > 0.4:
            recomendaciones.append(
                "🌧️ Alto riesgo de lluvias intensas: Implementar sistemas de "
                "drenaje adecuados y considerar seguros contra inundación"
            )
        
        if componentes_clim['plagas'] > 0.4:
            recomendaciones.append(
                "🐛 Alta presión de plagas esperada: Implementar manejo "
                "integrado de plagas y monitoreo constante"
            )
        
        # Recomendaciones de mercado
        if riesgo_mercado['volatilidad'] > 0.35:
            recomendaciones.append(
                "💰 Alta volatilidad de precios: Considerar contratos a "
                "futuro o diversificación de mercados"
            )
        
        if riesgo_mercado.get('desviacion_precio', 0) > 0.3:
            recomendaciones.append(
                "📊 Expectativa de precio poco realista: Revisar estudios de "
                "mercado y ajustar proyecciones"
            )
        
        # Recomendaciones de producción
        if riesgo_produccion['riesgo'] > 0.5:
            recomendaciones.append(
                "📈 Alta variabilidad en rendimiento: Mejorar manejo agronómico "
                "y considerar seguros agrícolas"
            )
        
        if riesgo_produccion['margen_seguridad'] < 0.3:
            recomendaciones.append(
                "⚠️ Margen de seguridad bajo: El rendimiento mínimo está muy "
                "cerca del esperado. Mejorar prácticas de cultivo"
            )
        
        # Recomendación general según IRA
        if categoria_ira == 'ALTO':
            recomendaciones.append(
                "🔴 Riesgo general elevado: Evaluar medidas de mitigación "
                "integrales antes de proceder con el proyecto"
            )
        elif categoria_ira == 'MEDIO':
            recomendaciones.append(
                "⚠️ Riesgo moderado: Implementar plan de contingencia y "
                "monitoreo constante"
            )
        else:
            recomendaciones.append(
                "✅ Riesgo bajo: Mantener buenas prácticas agrícolas y "
                "monitoreo preventivo"
            )
        
        return recomendaciones
    
    def _categorizar_riesgo(self, valor_riesgo: float) -> str:
        """Categoriza un valor de riesgo"""
        if valor_riesgo < self.umbrales['bajo']:
            return 'Bajo'
        elif valor_riesgo < self.umbrales['medio']:
            return 'Medio'
        else:
            return 'Alto'
    
    def simular_monte_carlo(self,
                           rendimiento_probable: float,
                           volatilidad: float,
                           n_simulaciones: int = 1000) -> Dict:
        """
        Simula escenarios usando Monte Carlo.
        
        Args:
            rendimiento_probable: Rendimiento esperado
            volatilidad: Volatilidad del rendimiento
            n_simulaciones: Número de simulaciones
            
        Returns:
            Diccionario con estadísticas de la simulación
        """
        # Generar simulaciones con distribución normal
        simulaciones = np.random.normal(
            rendimiento_probable,
            rendimiento_probable * volatilidad,
            n_simulaciones
        )
        
        # Asegurar valores positivos
        simulaciones = np.maximum(simulaciones, rendimiento_probable * 0.3)
        
        return {
            'media': round(np.mean(simulaciones), 2),
            'mediana': round(np.median(simulaciones), 2),
            'desviacion_estandar': round(np.std(simulaciones), 2),
            'percentil_5': round(np.percentile(simulaciones, 5), 2),
            'percentil_95': round(np.percentile(simulaciones, 95), 2),
            'probabilidad_perdida': round(
                np.sum(simulaciones < rendimiento_probable * 0.8) / n_simulaciones, 4
            )
        }


# Función auxiliar para cálculo rápido de IRA
def calcular_ira_rapido(region: str, cultivo: str, 
                        prediccion_rendimiento: Dict) -> Dict:
    """
    Calcula rápidamente el IRA dado una predicción de rendimiento.
    
    Args:
        region: Nombre de la región
        cultivo: Nombre del cultivo
        prediccion_rendimiento: Diccionario con rendimientos min, prob, max
        
    Returns:
        Diccionario con IRA y componentes
    """
    modelo = RiesgoModel()
    
    return modelo.calcular_ira(
        region=region,
        cultivo=cultivo,
        rendimiento_minimo=prediccion_rendimiento['rendimiento_minimo'],
        rendimiento_probable=prediccion_rendimiento['rendimiento_probable'],
        rendimiento_maximo=prediccion_rendimiento['rendimiento_maximo']
    )