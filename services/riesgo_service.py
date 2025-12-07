"""
Servicio de Análisis de Riesgos
================================
Capa de servicio para gestión integral de riesgos agrícolas.
"""

import sys
sys.path.append('.')

from models.riesgo_model import RiesgoModel, calcular_ira_rapido
from typing import Dict, List
import pandas as pd


class RiesgoService:
    """Servicio para análisis integral de riesgos"""
    
    def __init__(self):
        self.modelo = RiesgoModel()
    
    def analizar_riesgos_completo(self,
                                 region: str,
                                 cultivo: str,
                                 prediccion_rendimiento: Dict,
                                 precio_esperado: float = None,
                                 mes_siembra: int = None) -> Dict:
        """
        Realiza análisis completo de riesgos del proyecto.
        
        Args:
            region: Región del proyecto
            cultivo: Cultivo a sembrar
            prediccion_rendimiento: Dict con rendimientos min, prob, max
            precio_esperado: Precio de venta esperado
            mes_siembra: Mes de inicio de siembra
            
        Returns:
            Dict con análisis completo de riesgos
        """
        resultado_ira = self.modelo.calcular_ira(
            region=region,
            cultivo=cultivo,
            rendimiento_minimo=prediccion_rendimiento['rendimiento_minimo'],
            rendimiento_probable=prediccion_rendimiento['rendimiento_probable'],
            rendimiento_maximo=prediccion_rendimiento['rendimiento_maximo'],
            precio_esperado=precio_esperado,
            mes_siembra=mes_siembra
        )
        
        # Agregar análisis adicional
        resultado_ira['nivel_atencion'] = self._determinar_nivel_atencion(
            resultado_ira['ira']
        )
        
        resultado_ira['acciones_prioritarias'] = self._generar_acciones_prioritarias(
            resultado_ira['componentes']
        )
        
        return resultado_ira
    
    def _determinar_nivel_atencion(self, ira: float) -> str:
        """Determina el nivel de atención requerido"""
        if ira < 0.33:
            return "Monitoreo rutinario"
        elif ira < 0.5:
            return "Atención moderada"
        elif ira < 0.67:
            return "Atención elevada"
        else:
            return "Atención crítica"
    
    def _generar_acciones_prioritarias(self, componentes: Dict) -> List[str]:
        """Genera acciones prioritarias según componentes de riesgo"""
        acciones = []
        
        # Riesgo climático
        if componentes['climatico']['riesgo_total'] > 0.5:
            acciones.append("Implementar sistema de monitoreo climático")
            acciones.append("Contratar seguro agrícola contra eventos climáticos")
        
        # Riesgo de mercado
        if componentes['mercado']['riesgo_ajustado'] > 0.4:
            acciones.append("Diversificar canales de comercialización")
            acciones.append("Evaluar contratos a futuro o pre-venta")
        
        # Riesgo de producción
        if componentes['produccion']['riesgo'] > 0.5:
            acciones.append("Implementar plan de manejo agronómico riguroso")
            acciones.append("Capacitar al personal en buenas prácticas")
        
        return acciones
    
    def evaluar_mitigacion_riesgos(self,
                                   ira_actual: float,
                                   medidas_propuestas: List[str]) -> Dict:
        """
        Evalúa el impacto de medidas de mitigación en el IRA.
        
        Args:
            ira_actual: IRA actual del proyecto
            medidas_propuestas: Lista de medidas a implementar
            
        Returns:
            Dict con estimación de reducción de riesgo
        """
        # Factores de reducción por tipo de medida
        factores_reduccion = {
            'seguro': 0.15,
            'riego': 0.12,
            'tecnologia': 0.10,
            'diversificacion': 0.08,
            'capacitacion': 0.06,
            'monitoreo': 0.05
        }
        
        reduccion_total = 0
        medidas_efectivas = []
        
        for medida in medidas_propuestas:
            medida_lower = medida.lower()
            for clave, factor in factores_reduccion.items():
                if clave in medida_lower:
                    reduccion_total += factor
                    medidas_efectivas.append({
                        'medida': medida,
                        'reduccion_estimada': factor
                    })
                    break
        
        # Limitar reducción máxima al 35%
        reduccion_total = min(reduccion_total, 0.35)
        ira_proyectado = max(ira_actual * (1 - reduccion_total), 0.1)
        
        return {
            'ira_actual': round(ira_actual, 4),
            'ira_proyectado': round(ira_proyectado, 4),
            'reduccion_absoluta': round(ira_actual - ira_proyectado, 4),
            'reduccion_relativa': round(reduccion_total * 100, 2),
            'medidas_efectivas': medidas_efectivas,
            'nueva_categoria': self._categorizar_ira(ira_proyectado)
        }
    
    def _categorizar_ira(self, ira: float) -> str:
        """Categoriza el IRA"""
        if ira < 0.33:
            return "BAJO"
        elif ira < 0.67:
            return "MEDIO"
        else:
            return "ALTO"
    
    def comparar_riesgos_regiones(self,
                                 cultivo: str,
                                 regiones: List[str],
                                 prediccion_rendimiento: Dict) -> pd.DataFrame:
        """
        Compara niveles de riesgo del mismo cultivo en diferentes regiones.
        
        Args:
            cultivo: Nombre del cultivo
            regiones: Lista de regiones a comparar
            prediccion_rendimiento: Predicción de rendimiento base
            
        Returns:
            DataFrame con comparación de riesgos
        """
        resultados = []
        
        for region in regiones:
            try:
                analisis = self.analizar_riesgos_completo(
                    region=region,
                    cultivo=cultivo,
                    prediccion_rendimiento=prediccion_rendimiento
                )
                
                resultados.append({
                    'Región': region,
                    'IRA': analisis['ira'],
                    'Categoría': analisis['categoria'],
                    'Riesgo Climático': analisis['componentes']['climatico']['riesgo_total'],
                    'Riesgo Mercado': analisis['componentes']['mercado']['riesgo_ajustado'],
                    'Riesgo Producción': analisis['componentes']['produccion']['riesgo']
                })
            except:
                continue
        
        df = pd.DataFrame(resultados)
        if not df.empty:
            df = df.sort_values('IRA')
        
        return df
    
    def generar_mapa_calor_riesgos(self,
                                   componentes: Dict) -> pd.DataFrame:
        """
        Genera matriz de calor de riesgos.
        
        Args:
            componentes: Componentes del análisis de riesgo
            
        Returns:
            DataFrame para visualización de mapa de calor
        """
        datos = []
        
        # Riesgo climático
        clim = componentes['climatico']['componentes']
        datos.extend([
            {'Categoría': 'Climático', 'Factor': 'Sequía', 'Nivel': clim['sequia']},
            {'Categoría': 'Climático', 'Factor': 'Heladas', 'Nivel': clim['heladas']},
            {'Categoría': 'Climático', 'Factor': 'Lluvias', 'Nivel': clim['lluvias']},
            {'Categoría': 'Climático', 'Factor': 'Plagas', 'Nivel': clim['plagas']}
        ])
        
        # Riesgo de mercado
        datos.append({
            'Categoría': 'Mercado',
            'Factor': 'Volatilidad',
            'Nivel': componentes['mercado']['riesgo_ajustado']
        })
        
        # Riesgo de producción
        datos.append({
            'Categoría': 'Producción',
            'Factor': 'Variabilidad',
            'Nivel': componentes['produccion']['riesgo']
        })
        
        return pd.DataFrame(datos)


def calcular_riesgo_simple(region: str, cultivo: str,
                          rendimiento_probable: float) -> Dict:
    """
    Función auxiliar para cálculo rápido de riesgo.
    
    Args:
        region: Región
        cultivo: Cultivo
        rendimiento_probable: Rendimiento esperado
        
    Returns:
        Dict con análisis de riesgo
    """
    servicio = RiesgoService()
    prediccion = {
        'rendimiento_minimo': rendimiento_probable * 0.7,
        'rendimiento_probable': rendimiento_probable,
        'rendimiento_maximo': rendimiento_probable * 1.3
    }
    return servicio.analizar_riesgos_completo(region, cultivo, prediccion)