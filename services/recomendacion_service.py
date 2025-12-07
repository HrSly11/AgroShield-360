"""
Servicio de Recomendación
==========================
Sistema inteligente de recomendaciones para proyectos agrícolas.
"""

from typing import Dict, List, Tuple


class RecomendacionService:
    """Servicio para generar recomendaciones inteligentes"""
    
    def __init__(self):
        # Umbrales de decisión
        self.umbrales = {
            'puntuacion_excelente': 80,
            'puntuacion_buena': 60,
            'puntuacion_regular': 40,
            'van_minimo': 0,
            'roi_minimo': 15,
            'ira_maximo_bajo': 0.33,
            'ira_maximo_medio': 0.67
        }
    
    def calcular_puntuacion_proyecto(self,
                                    evaluacion_economica: Dict,
                                    analisis_riesgos: Dict,
                                    resultados_escenarios: Dict) -> Dict:
        """
        Calcula puntuación integral del proyecto.
        
        Args:
            evaluacion_economica: Resultados de evaluación económica
            analisis_riesgos: Resultados de análisis de riesgos
            resultados_escenarios: Resultados de simulación de escenarios
            
        Returns:
            Dict con puntuación detallada
        """
        # 1. Criterio: Rentabilidad (40 puntos)
        puntos_rentabilidad = self._evaluar_rentabilidad(evaluacion_economica)
        
        # 2. Criterio: Riesgo (30 puntos)
        puntos_riesgo = self._evaluar_riesgo(analisis_riesgos)
        
        # 3. Criterio: Estabilidad de Escenarios (20 puntos)
        puntos_escenarios = self._evaluar_escenarios(resultados_escenarios)
        
        # 4. Criterio: Condiciones de Mercado (10 puntos)
        puntos_mercado = self._evaluar_mercado(evaluacion_economica, analisis_riesgos)
        
        # Puntuación total
        puntuacion_total = (puntos_rentabilidad + puntos_riesgo + 
                          puntos_escenarios + puntos_mercado)
        
        return {
            'puntuacion_total': puntuacion_total,
            'puntos_rentabilidad': puntos_rentabilidad,
            'puntos_riesgo': puntos_riesgo,
            'puntos_escenarios': puntos_escenarios,
            'puntos_mercado': puntos_mercado,
            'porcentaje': round(puntuacion_total, 2),
            'detalles': {
                'rentabilidad': self._detalle_rentabilidad(evaluacion_economica),
                'riesgo': self._detalle_riesgo(analisis_riesgos),
                'escenarios': self._detalle_escenarios(resultados_escenarios),
                'mercado': self._detalle_mercado(evaluacion_economica, analisis_riesgos)
            }
        }
    
    def _evaluar_rentabilidad(self, evaluacion: Dict) -> float:
        """Evalúa criterio de rentabilidad (máximo 40 puntos)"""
        puntos = 0
        
        # VAN positivo (15 puntos)
        if evaluacion.get('van', 0) > 0:
            puntos += 15
        
        # ROI (15 puntos)
        roi = evaluacion.get('roi', 0)
        if roi > 50:
            puntos += 15
        elif roi > 30:
            puntos += 12
        elif roi > 20:
            puntos += 10
        elif roi > 10:
            puntos += 7
        elif roi > 0:
            puntos += 5
        
        # Margen de utilidad (10 puntos)
        margen = evaluacion.get('margen_utilidad', 0)
        if margen > 30:
            puntos += 10
        elif margen > 20:
            puntos += 8
        elif margen > 15:
            puntos += 7
        elif margen > 10:
            puntos += 5
        elif margen > 0:
            puntos += 3
        
        return min(puntos, 40)
    
    def _evaluar_riesgo(self, analisis: Dict) -> float:
        """Evalúa criterio de riesgo (máximo 30 puntos)"""
        ira = analisis.get('ira', 1.0)
        
        # Puntuación inversa al riesgo
        if ira < 0.33:
            return 30
        elif ira < 0.40:
            return 25
        elif ira < 0.50:
            return 22
        elif ira < 0.67:
            return 15
        elif ira < 0.80:
            return 8
        else:
            return 0
    
    def _evaluar_escenarios(self, escenarios: Dict) -> float:
        """Evalúa criterio de escenarios (máximo 20 puntos)"""
        puntos = 0
        
        # VAN positivo en escenario pesimista (10 puntos)
        van_pesimista = escenarios.get('Pesimista', {}).get('van', -999999)
        if van_pesimista > 0:
            puntos += 10
        elif van_pesimista > -1000:
            puntos += 5
        
        # Estabilidad entre escenarios (10 puntos)
        van_base = escenarios.get('Base', {}).get('van', 0)
        van_optimista = escenarios.get('Optimista', {}).get('van', 0)
        
        if van_base != 0:
            variabilidad = abs(van_optimista - van_pesimista) / abs(van_base)
            
            if variabilidad < 1.0:
                puntos += 10
            elif variabilidad < 1.5:
                puntos += 8
            elif variabilidad < 2.0:
                puntos += 6
            else:
                puntos += 2
        
        return min(puntos, 20)
    
    def _evaluar_mercado(self, evaluacion: Dict, riesgos: Dict) -> float:
        """Evalúa criterio de mercado (máximo 10 puntos)"""
        puntos = 0
        
        # Punto de equilibrio alcanzable (5 puntos)
        pe_kg = evaluacion.get('punto_equilibrio_kg', 999999)
        ingresos = evaluacion.get('ingreso_total', 0)
        
        if pe_kg < ingresos * 0.5:
            puntos += 5
        elif pe_kg < ingresos * 0.7:
            puntos += 3
        elif pe_kg < ingresos * 0.9:
            puntos += 1
        
        # Volatilidad de precios (5 puntos)
        riesgo_mercado = riesgos.get('componentes', {}).get('mercado', {}).get('volatilidad', 0.5)
        
        if riesgo_mercado < 0.20:
            puntos += 5
        elif riesgo_mercado < 0.30:
            puntos += 4
        elif riesgo_mercado < 0.40:
            puntos += 2
        else:
            puntos += 1
        
        return min(puntos, 10)
    
    def _detalle_rentabilidad(self, evaluacion: Dict) -> str:
        """Genera detalle de evaluación de rentabilidad"""
        van = evaluacion.get('van', 0)
        roi = evaluacion.get('roi', 0)
        margen = evaluacion.get('margen_utilidad', 0)
        
        if van > 0 and roi > 30 and margen > 20:
            return "Excelente rentabilidad en todos los indicadores"
        elif van > 0 and roi > 15:
            return "Rentabilidad satisfactoria"
        elif van > 0:
            return "Rentabilidad positiva pero ajustada"
        else:
            return "Rentabilidad insuficiente"
    
    def _detalle_riesgo(self, analisis: Dict) -> str:
        """Genera detalle de evaluación de riesgo"""
        categoria = analisis.get('categoria', 'ALTO')
        
        if categoria == 'BAJO':
            return "Nivel de riesgo bajo y manejable"
        elif categoria == 'MEDIO':
            return "Nivel de riesgo moderado, requiere monitoreo"
        else:
            return "Nivel de riesgo alto, se requieren medidas de mitigación"
    
    def _detalle_escenarios(self, escenarios: Dict) -> str:
        """Genera detalle de evaluación de escenarios"""
        van_pes = escenarios.get('Pesimista', {}).get('van', 0)
        
        if van_pes > 0:
            return "Proyecto viable incluso en escenario pesimista"
        elif van_pes > -5000:
            return "Vulnerabilidad moderada en escenario pesimista"
        else:
            return "Alta vulnerabilidad en condiciones adversas"
    
    def _detalle_mercado(self, evaluacion: Dict, riesgos: Dict) -> str:
        """Genera detalle de evaluación de mercado"""
        volatilidad = riesgos.get('componentes', {}).get('mercado', {}).get('volatilidad', 0.5)
        
        if volatilidad < 0.25:
            return "Mercado estable con baja volatilidad"
        elif volatilidad < 0.40:
            return "Volatilidad de precios moderada"
        else:
            return "Alta volatilidad de precios, considerar estrategias de cobertura"
    
    def generar_recomendacion_final(self, puntuacion: Dict) -> Dict:
        """
        Genera la recomendación final del sistema.
        
        Args:
            puntuacion: Dict con puntuación calculada
            
        Returns:
            Dict con recomendación final
        """
        puntaje = puntuacion['puntuacion_total']
        
        if puntaje >= self.umbrales['puntuacion_excelente']:
            recomendacion = "CONVIENE SEMBRAR ESTE CULTIVO"
            emoji = "✅"
            color = "#95E1D3"
            detalle = """
            **PROYECTO ALTAMENTE RECOMENDADO**
            
            El análisis integral indica que este proyecto agrícola presenta:
            - Excelentes indicadores de rentabilidad
            - Riesgos controlados y manejables
            - Estabilidad favorable en diferentes escenarios
            - Condiciones de mercado positivas
            
            **Recomendación**: Proceda con la implementación del proyecto siguiendo 
            las mejores prácticas agronómicas identificadas.
            """
        
        elif puntaje >= self.umbrales['puntuacion_buena']:
            recomendacion = "CONVIENE SEMBRAR CON PRECAUCIONES"
            emoji = "⚠️"
            color = "#FFD93D"
            detalle = """
            **PROYECTO VIABLE CON CONSIDERACIONES**
            
            El proyecto es viable pero requiere atención a:
            - Implementar medidas de mitigación de riesgos identificados
            - Monitorear de cerca las condiciones de mercado
            - Considerar seguros agrícolas
            - Optimizar costos de producción
            
            **Recomendación**: Puede proceder pero implemente las medidas de gestión 
            de riesgo sugeridas en el informe.
            """
        
        elif puntaje >= self.umbrales['puntuacion_regular']:
            recomendacion = "SE RECOMIENDA ROTAR O AJUSTAR CULTIVO"
            emoji = "🔄"
            color = "#FFA500"
            detalle = """
            **PROYECTO CON RIESGOS SIGNIFICATIVOS**
            
            El análisis sugiere considerar:
            - Evaluar cultivos alternativos más rentables para la región
            - Reducir costos de producción mediante optimización
            - Mejorar tecnología y prácticas agronómicas
            - Buscar mercados con mejores condiciones de precio
            
            **Recomendación**: Considere ajustar el plan antes de proceder o evalúe 
            alternativas de cultivo más adecuadas.
            """
        
        else:
            recomendacion = "NO SE RECOMIENDA SEMBRAR EN ESTA CAMPAÑA"
            emoji = "❌"
            color = "#FF6B6B"
            detalle = """
            **PROYECTO NO RECOMENDADO**
            
            El análisis indica riesgos y condiciones desfavorables:
            - Rentabilidad insuficiente o negativa
            - Riesgos elevados no mitigables en el corto plazo
            - Condiciones de mercado adversas
            - Vulnerabilidad alta ante cambios
            
            **Recomendación**: NO proceda con este proyecto. Evalúe alternativas 
            completamente diferentes o espere condiciones más favorables en futuras campañas.
            """
        
        return {
            'recomendacion': recomendacion,
            'emoji': emoji,
            'color': color,
            'detalle': detalle,
            'nivel_confianza': self._calcular_nivel_confianza(puntuacion),
            'acciones_inmediatas': self._generar_acciones_inmediatas(
                puntaje, puntuacion
            )
        }
    
    def _calcular_nivel_confianza(self, puntuacion: Dict) -> str:
        """Calcula el nivel de confianza de la recomendación"""
        # Basado en la distribución de puntos
        puntos = [
            puntuacion['puntos_rentabilidad'],
            puntuacion['puntos_riesgo'],
            puntuacion['puntos_escenarios'],
            puntuacion['puntos_mercado']
        ]
        
        maximos = [40, 30, 20, 10]
        porcentajes = [p/m*100 for p, m in zip(puntos, maximos)]
        
        # Si todos los criterios están balanceados, mayor confianza
        desviacion = max(porcentajes) - min(porcentajes)
        
        if desviacion < 20:
            return "Muy Alta"
        elif desviacion < 40:
            return "Alta"
        elif desviacion < 60:
            return "Media"
        else:
            return "Baja (criterios desbalanceados)"
    
    def _generar_acciones_inmediatas(self, puntaje: float, 
                                     puntuacion: Dict) -> List[str]:
        """Genera lista de acciones inmediatas"""
        acciones = []
        
        if puntaje >= 80:
            acciones.extend([
                "Iniciar preparación de terreno según cronograma",
                "Asegurar disponibilidad de insumos de calidad",
                "Establecer calendario de monitoreo fitosanitario"
            ])
        elif puntaje >= 60:
            acciones.extend([
                "Contratar seguro agrícola antes de iniciar",
                "Implementar sistema de riego eficiente",
                "Establecer plan de contingencia para riesgos identificados"
            ])
        elif puntaje >= 40:
            acciones.extend([
                "Reevaluar alternativas de cultivo para la región",
                "Buscar asesoría técnica especializada",
                "Realizar análisis de mercado más profundo"
            ])
        else:
            acciones.extend([
                "Suspender el proyecto temporalmente",
                "Evaluar cultivos alternativos completamente diferentes",
                "Considerar asociarse con productores experimentados"
            ])
        
        return acciones


def generar_recomendacion_rapida(van: float, roi: float, ira: float) -> str:
    """
    Función auxiliar para recomendación rápida.
    
    Args:
        van: VAN del proyecto
        roi: ROI del proyecto
        ira: Índice de riesgo
        
    Returns:
        String con recomendación
    """
    if van > 0 and roi > 20 and ira < 0.5:
        return "RECOMENDADO"
    elif van > 0 and roi > 10:
        return "VIABLE CON PRECAUCIONES"
    else:
        return "NO RECOMENDADO"