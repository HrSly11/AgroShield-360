"""
Servicio de Simulación de Escenarios
=====================================
Servicios para simulación y análisis de escenarios agrícolas.
"""

import numpy as np
import pandas as pd
from typing import Dict, List
from numpy_financial import npv


class EscenariosService:
    """Servicio para simulación de escenarios"""
    
    def __init__(self):
        # Definir escenarios estándar
        self.escenarios_default = {
            'Pesimista': {
                'factor_rendimiento': 0.80,
                'factor_precio': 0.85,
                'descripcion': 'Condiciones desfavorables'
            },
            'Base': {
                'factor_rendimiento': 1.00,
                'factor_precio': 1.00,
                'descripcion': 'Condiciones esperadas'
            },
            'Optimista': {
                'factor_rendimiento': 1.20,
                'factor_precio': 1.15,
                'descripcion': 'Condiciones favorables'
            }
        }
    
    def simular_escenarios(self,
                          rendimiento_base: float,
                          precio_base: float,
                          area: float,
                          costos_totales: float,
                          tasa_descuento: float,
                          duracion_meses: int,
                          escenarios: Dict = None) -> Dict:
        """
        Simula múltiples escenarios del proyecto.
        
        Args:
            rendimiento_base: Rendimiento base en kg/ha
            precio_base: Precio base en soles/kg
            area: Área en hectáreas
            costos_totales: Costos totales del proyecto
            tasa_descuento: Tasa de descuento anual
            duracion_meses: Duración del proyecto
            escenarios: Dict de escenarios (opcional)
            
        Returns:
            Dict con resultados de cada escenario
        """
        if escenarios is None:
            escenarios = self.escenarios_default
        
        resultados = {}
        
        for nombre, config in escenarios.items():
            # Calcular rendimiento y precio ajustados
            rendimiento_ajustado = rendimiento_base * config['factor_rendimiento']
            precio_ajustado = precio_base * config['factor_precio']
            
            # Calcular producción e ingresos
            produccion = rendimiento_ajustado * area
            ingresos = produccion * precio_ajustado
            
            # Calcular utilidad
            utilidad = ingresos - costos_totales
            margen = (utilidad / ingresos * 100) if ingresos > 0 else 0
            roi = (utilidad / costos_totales * 100) if costos_totales > 0 else 0
            
            # Calcular VAN simplificado
            tasa_mensual = tasa_descuento / 12
            flujo = self._generar_flujo_simple(costos_totales, ingresos, duracion_meses)
            van = npv(tasa_mensual, flujo)
            
            resultados[nombre] = {
                'rendimiento': round(rendimiento_ajustado, 2),
                'precio': round(precio_ajustado, 2),
                'produccion': round(produccion, 2),
                'ingresos': round(ingresos, 2),
                'costos': costos_totales,
                'utilidad': round(utilidad, 2),
                'margen': round(margen, 2),
                'roi': round(roi, 2),
                'van': round(van, 2),
                'descripcion': config.get('descripcion', ''),
                'factores': {
                    'rendimiento': config['factor_rendimiento'],
                    'precio': config['factor_precio']
                }
            }
        
        return resultados
    
    def _generar_flujo_simple(self, costos: float, ingresos: float, 
                             meses: int) -> List[float]:
        """Genera flujo de caja simplificado"""
        flujo = [-costos * 0.3]
        
        if meses > 1:
            costo_mensual = (costos * 0.7) / (meses - 1)
            for _ in range(1, meses):
                flujo.append(-costo_mensual)
        
        ingreso_final = ingresos - (costos * 0.7 / meses if meses > 1 else 0)
        flujo.append(ingreso_final)
        
        return flujo
    
    def comparar_escenarios(self, resultados_escenarios: Dict) -> pd.DataFrame:
        """
        Genera tabla comparativa de escenarios.
        
        Args:
            resultados_escenarios: Dict con resultados de simular_escenarios
            
        Returns:
            DataFrame con comparación
        """
        datos = []
        
        for nombre, resultado in resultados_escenarios.items():
            datos.append({
                'Escenario': nombre,
                'Rendimiento (kg/ha)': resultado['rendimiento'],
                'Precio (S/./kg)': resultado['precio'],
                'Ingresos (S/.)': resultado['ingresos'],
                'Utilidad (S/.)': resultado['utilidad'],
                'Margen (%)': resultado['margen'],
                'ROI (%)': resultado['roi'],
                'VAN (S/.)': resultado['van']
            })
        
        return pd.DataFrame(datos)
    
    def analisis_sensibilidad_bivariado(self,
                                       rendimiento_base: float,
                                       precio_base: float,
                                       area: float,
                                       costos: float,
                                       variaciones_rend: List[float] = None,
                                       variaciones_precio: List[float] = None) -> pd.DataFrame:
        """
        Análisis de sensibilidad bivariado (rendimiento vs precio).
        
        Args:
            rendimiento_base: Rendimiento base
            precio_base: Precio base
            area: Área
            costos: Costos totales
            variaciones_rend: Lista de variaciones de rendimiento
            variaciones_precio: Lista de variaciones de precio
            
        Returns:
            DataFrame con matriz de sensibilidad
        """
        if variaciones_rend is None:
            variaciones_rend = [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3]
        
        if variaciones_precio is None:
            variaciones_precio = [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3]
        
        resultados = []
        
        for var_rend in variaciones_rend:
            for var_precio in variaciones_precio:
                rend = rendimiento_base * (1 + var_rend)
                precio = precio_base * (1 + var_precio)
                
                produccion = rend * area
                ingresos = produccion * precio
                utilidad = ingresos - costos
                
                resultados.append({
                    'Var_Rendimiento (%)': round(var_rend * 100, 0),
                    'Var_Precio (%)': round(var_precio * 100, 0),
                    'Utilidad (S/.)': round(utilidad, 2)
                })
        
        return pd.DataFrame(resultados)
    
    def simular_monte_carlo(self,
                           rendimiento_medio: float,
                           precio_medio: float,
                           area: float,
                           costos: float,
                           volatilidad_rend: float,
                           volatilidad_precio: float,
                           n_simulaciones: int = 1000) -> Dict:
        """
        Simulación Monte Carlo para análisis de riesgo.
        
        Args:
            rendimiento_medio: Rendimiento esperado
            precio_medio: Precio esperado
            area: Área
            costos: Costos totales
            volatilidad_rend: Volatilidad del rendimiento
            volatilidad_precio: Volatilidad del precio
            n_simulaciones: Número de simulaciones
            
        Returns:
            Dict con estadísticas de la simulación
        """
        np.random.seed(42)
        
        # Generar simulaciones
        rendimientos = np.random.normal(
            rendimiento_medio,
            rendimiento_medio * volatilidad_rend,
            n_simulaciones
        )
        
        precios = np.random.normal(
            precio_medio,
            precio_medio * volatilidad_precio,
            n_simulaciones
        )
        
        # Asegurar valores positivos
        rendimientos = np.maximum(rendimientos, rendimiento_medio * 0.3)
        precios = np.maximum(precios, precio_medio * 0.3)
        
        # Calcular utilidades
        producciones = rendimientos * area
        ingresos = producciones * precios
        utilidades = ingresos - costos
        
        # Estadísticas
        utilidad_media = np.mean(utilidades)
        utilidad_mediana = np.median(utilidades)
        desv_std = np.std(utilidades)
        
        # Percentiles
        percentil_5 = np.percentile(utilidades, 5)
        percentil_25 = np.percentile(utilidades, 25)
        percentil_75 = np.percentile(utilidades, 75)
        percentil_95 = np.percentile(utilidades, 95)
        
        # Probabilidades
        prob_perdida = np.sum(utilidades < 0) / n_simulaciones
        prob_utilidad_baja = np.sum(utilidades < utilidad_media * 0.5) / n_simulaciones
        prob_utilidad_alta = np.sum(utilidades > utilidad_media * 1.5) / n_simulaciones
        
        return {
            'utilidad_media': round(utilidad_media, 2),
            'utilidad_mediana': round(utilidad_mediana, 2),
            'desviacion_estandar': round(desv_std, 2),
            'percentil_5': round(percentil_5, 2),
            'percentil_25': round(percentil_25, 2),
            'percentil_75': round(percentil_75, 2),
            'percentil_95': round(percentil_95, 2),
            'probabilidad_perdida': round(prob_perdida, 4),
            'probabilidad_utilidad_baja': round(prob_utilidad_baja, 4),
            'probabilidad_utilidad_alta': round(prob_utilidad_alta, 4),
            'n_simulaciones': n_simulaciones,
            'utilidades_simuladas': utilidades.tolist()
        }
    
    def calcular_valor_esperado(self, 
                               escenarios_probabilidades: Dict) -> Dict:
        """
        Calcula el valor esperado considerando probabilidades.
        
        Args:
            escenarios_probabilidades: Dict con {escenario: {'resultado': float, 'probabilidad': float}}
            
        Returns:
            Dict con valor esperado y análisis
        """
        valor_esperado = 0
        suma_probabilidades = 0
        
        for escenario, datos in escenarios_probabilidades.items():
            resultado = datos['resultado']
            probabilidad = datos['probabilidad']
            
            valor_esperado += resultado * probabilidad
            suma_probabilidades += probabilidad
        
        # Validar que las probabilidades sumen 1
        if abs(suma_probabilidades - 1.0) > 0.01:
            return {
                'error': f'Las probabilidades deben sumar 1.0 (suman {suma_probabilidades})',
                'valor_esperado': None
            }
        
        return {
            'valor_esperado': round(valor_esperado, 2),
            'escenarios_analizados': len(escenarios_probabilidades),
            'suma_probabilidades': round(suma_probabilidades, 4)
        }


def simular_escenarios_rapido(rendimiento: float, precio: float,
                              area: float, costos: float) -> Dict:
    """
    Función auxiliar para simulación rápida de escenarios.
    
    Args:
        rendimiento: Rendimiento base kg/ha
        precio: Precio base soles/kg
        area: Área en hectáreas
        costos: Costos totales
        
    Returns:
        Dict con resultados de escenarios
    """
    servicio = EscenariosService()
    return servicio.simular_escenarios(
        rendimiento_base=rendimiento,
        precio_base=precio,
        area=area,
        costos_totales=costos,
        tasa_descuento=0.12,
        duracion_meses=4
    )