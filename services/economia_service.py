"""
Servicio de Evaluación Económica
=================================
Servicios para análisis financiero de proyectos agrícolas.
"""

import numpy as np
from numpy_financial import npv, irr
from typing import Dict, List, Tuple
import pandas as pd


class EconomiaService:
    """Servicio para evaluación económica y financiera"""
    
    def __init__(self):
        self.tasa_descuento_default = 0.12  # 12% anual
    
    def calcular_flujo_caja(self,
                           inversion_inicial: float,
                           ingresos_totales: float,
                           costos_operativos: float,
                           duracion_meses: int) -> List[float]:
        """
        Genera el flujo de caja del proyecto.
        
        Args:
            inversion_inicial: Inversión inicial total
            ingresos_totales: Ingresos totales esperados
            costos_operativos: Costos operativos totales
            duracion_meses: Duración del proyecto en meses
            
        Returns:
            Lista con flujo de caja por período
        """
        flujo = []
        
        # Mes 0: Inversión inicial (30% del total)
        flujo.append(-inversion_inicial * 0.3)
        
        # Meses intermedios: Costos operativos distribuidos
        if duracion_meses > 1:
            costo_mensual = (inversion_inicial * 0.7) / (duracion_meses - 1)
            for _ in range(1, duracion_meses):
                flujo.append(-costo_mensual)
        
        # Último mes: Ingresos - último costo
        ingreso_final = ingresos_totales - (inversion_inicial * 0.7 / duracion_meses if duracion_meses > 1 else 0)
        flujo.append(ingreso_final)
        
        return flujo
    
    def calcular_van_tir(self,
                        flujo_caja: List[float],
                        tasa_descuento_anual: float = None) -> Dict:
        """
        Calcula VAN (VPN) y TIR del proyecto.
        
        Args:
            flujo_caja: Lista con flujo de caja por período
            tasa_descuento_anual: Tasa de descuento anual (default: 12%)
            
        Returns:
            Dict con VAN, TIR y análisis
        """
        if tasa_descuento_anual is None:
            tasa_descuento_anual = self.tasa_descuento_default
        
        # Convertir tasa anual a mensual
        tasa_mensual = tasa_descuento_anual / 12
        
        # Calcular VAN
        van = npv(tasa_mensual, flujo_caja)
        
        # Calcular TIR
        try:
            tir_mensual = irr(flujo_caja)
            tir_anual = (1 + tir_mensual) ** 12 - 1
        except:
            tir_anual = None
        
        # Análisis de viabilidad
        viabilidad = "VIABLE" if van > 0 else "NO VIABLE"
        
        return {
            'van': round(van, 2),
            'tir_anual': round(tir_anual, 4) if tir_anual else None,
            'tir_porcentaje': round(tir_anual * 100, 2) if tir_anual else None,
            'viabilidad': viabilidad,
            'tasa_descuento': tasa_descuento_anual,
            'flujo_caja': flujo_caja
        }
    
    def calcular_punto_equilibrio(self,
                                  costos_fijos: float,
                                  costos_variables_unitarios: float,
                                  precio_venta_unitario: float) -> Dict:
        """
        Calcula el punto de equilibrio del proyecto.
        
        Args:
            costos_fijos: Costos fijos totales
            costos_variables_unitarios: Costo variable por unidad
            precio_venta_unitario: Precio de venta por unidad
            
        Returns:
            Dict con punto de equilibrio
        """
        if precio_venta_unitario <= costos_variables_unitarios:
            return {
                'error': 'El precio de venta debe ser mayor que los costos variables',
                'punto_equilibrio_unidades': 0,
                'punto_equilibrio_ingresos': 0
            }
        
        # Punto de equilibrio en unidades
        pe_unidades = costos_fijos / (precio_venta_unitario - costos_variables_unitarios)
        
        # Punto de equilibrio en ingresos
        pe_ingresos = pe_unidades * precio_venta_unitario
        
        return {
            'punto_equilibrio_unidades': round(pe_unidades, 2),
            'punto_equilibrio_ingresos': round(pe_ingresos, 2),
            'margen_contribucion': round(precio_venta_unitario - costos_variables_unitarios, 2),
            'margen_contribucion_porcentaje': round(
                (precio_venta_unitario - costos_variables_unitarios) / precio_venta_unitario * 100, 2
            )
        }
    
    def analisis_rentabilidad_completo(self,
                                      inversion_total: float,
                                      ingresos_totales: float,
                                      costos_totales: float,
                                      duracion_meses: int,
                                      tasa_descuento: float = None) -> Dict:
        """
        Realiza análisis de rentabilidad completo del proyecto.
        
        Args:
            inversion_total: Inversión total
            ingresos_totales: Ingresos esperados
            costos_totales: Costos totales
            duracion_meses: Duración en meses
            tasa_descuento: Tasa de descuento anual
            
        Returns:
            Dict con análisis completo
        """
        # Utilidad bruta
        utilidad_bruta = ingresos_totales - costos_totales
        
        # Margen de utilidad
        margen_utilidad = (utilidad_bruta / ingresos_totales * 100) if ingresos_totales > 0 else 0
        
        # ROI
        roi = (utilidad_bruta / costos_totales * 100) if costos_totales > 0 else 0
        
        # Flujo de caja
        flujo = self.calcular_flujo_caja(
            inversion_total, ingresos_totales, costos_totales, duracion_meses
        )
        
        # VAN y TIR
        van_tir = self.calcular_van_tir(flujo, tasa_descuento)
        
        # Período de recuperación
        flujo_acumulado = np.cumsum(flujo)
        periodo_recuperacion = None
        for i, acum in enumerate(flujo_acumulado):
            if acum >= 0:
                periodo_recuperacion = i
                break
        
        # Índice de rentabilidad
        inversion_inicial = abs(flujo[0])
        van_flujos_positivos = sum([f / ((1 + (tasa_descuento or self.tasa_descuento_default)/12) ** i) 
                                   for i, f in enumerate(flujo) if f > 0])
        indice_rentabilidad = van_flujos_positivos / inversion_inicial if inversion_inicial > 0 else 0
        
        return {
            'utilidad_bruta': round(utilidad_bruta, 2),
            'margen_utilidad': round(margen_utilidad, 2),
            'roi': round(roi, 2),
            'van': van_tir['van'],
            'tir_anual': van_tir['tir_anual'],
            'tir_porcentaje': van_tir['tir_porcentaje'],
            'viabilidad': van_tir['viabilidad'],
            'periodo_recuperacion_meses': periodo_recuperacion,
            'indice_rentabilidad': round(indice_rentabilidad, 2),
            'flujo_caja': flujo,
            'flujo_acumulado': flujo_acumulado.tolist()
        }
    
    def analisis_sensibilidad(self,
                             ingresos_base: float,
                             costos_base: float,
                             variacion_porcentaje: List[float] = None) -> pd.DataFrame:
        """
        Realiza análisis de sensibilidad de la utilidad.
        
        Args:
            ingresos_base: Ingresos base del proyecto
            costos_base: Costos base del proyecto
            variacion_porcentaje: Lista de variaciones a analizar
            
        Returns:
            DataFrame con análisis de sensibilidad
        """
        if variacion_porcentaje is None:
            variacion_porcentaje = [-30, -20, -10, 0, 10, 20, 30]
        
        resultados = []
        
        for var in variacion_porcentaje:
            factor = 1 + (var / 100)
            
            # Escenarios
            ing_var = ingresos_base * factor
            utilidad_ing = ing_var - costos_base
            
            cost_var = costos_base * factor
            utilidad_cost = ingresos_base - cost_var
            
            ambos_var_opt = (ingresos_base * factor) - (costos_base / factor)
            ambos_var_pes = (ingresos_base / factor) - (costos_base * factor)
            
            resultados.append({
                'Variación (%)': var,
                'Utilidad (Var. Ingresos)': round(utilidad_ing, 2),
                'Utilidad (Var. Costos)': round(utilidad_cost, 2),
                'Utilidad (Escenario Optimista)': round(ambos_var_opt, 2),
                'Utilidad (Escenario Pesimista)': round(ambos_var_pes, 2)
            })
        
        return pd.DataFrame(resultados)
    
    def calcular_ratios_financieros(self,
                                   activos_totales: float,
                                   pasivos_totales: float,
                                   ingresos: float,
                                   utilidad_neta: float) -> Dict:
        """
        Calcula ratios financieros del proyecto.
        
        Args:
            activos_totales: Total de activos
            pasivos_totales: Total de pasivos
            ingresos: Ingresos totales
            utilidad_neta: Utilidad neta
            
        Returns:
            Dict con ratios financieros
        """
        patrimonio = activos_totales - pasivos_totales
        
        # Ratio de endeudamiento
        ratio_endeudamiento = (pasivos_totales / activos_totales * 100) if activos_totales > 0 else 0
        
        # Ratio de autonomía
        ratio_autonomia = (patrimonio / activos_totales * 100) if activos_totales > 0 else 0
        
        # ROA (Return on Assets)
        roa = (utilidad_neta / activos_totales * 100) if activos_totales > 0 else 0
        
        # ROE (Return on Equity)
        roe = (utilidad_neta / patrimonio * 100) if patrimonio > 0 else 0
        
        # Margen neto
        margen_neto = (utilidad_neta / ingresos * 100) if ingresos > 0 else 0
        
        return {
            'ratio_endeudamiento': round(ratio_endeudamiento, 2),
            'ratio_autonomia': round(ratio_autonomia, 2),
            'roa': round(roa, 2),
            'roe': round(roe, 2),
            'margen_neto': round(margen_neto, 2),
            'patrimonio': round(patrimonio, 2)
        }


def calcular_viabilidad_rapida(inversion: float, ingresos: float, 
                               costos: float) -> Dict:
    """
    Función auxiliar para evaluación rápida de viabilidad.
    
    Args:
        inversion: Inversión total
        ingresos: Ingresos esperados
        costos: Costos totales
        
    Returns:
        Dict con evaluación básica
    """
    servicio = EconomiaService()
    utilidad = ingresos - costos
    roi = (utilidad / costos * 100) if costos > 0 else 0
    
    return {
        'utilidad': round(utilidad, 2),
        'roi': round(roi, 2),
        'viable': utilidad > 0
    }