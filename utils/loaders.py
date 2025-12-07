"""
Cargadores de Datos
===================
Funciones para cargar y validar datos del sistema.
"""

import pandas as pd
import json
from typing import Dict, List, Optional
import os


class DataLoader:
    """Clase para cargar y gestionar datos del sistema"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self._cache = {}
    
    def cargar_clima_simulado(self) -> pd.DataFrame:
        """
        Carga datos climáticos simulados.
        
        Returns:
            DataFrame con datos climáticos
        """
        if 'clima' in self._cache:
            return self._cache['clima'].copy()
        
        try:
            ruta = os.path.join(self.data_dir, 'clima_simulado.csv')
            df = pd.read_csv(ruta)
            self._cache['clima'] = df
            return df.copy()
        except FileNotFoundError:
            return pd.DataFrame()
    
    def cargar_precios_historicos(self) -> pd.DataFrame:
        """
        Carga datos de precios históricos.
        
        Returns:
            DataFrame con precios históricos
        """
        if 'precios' in self._cache:
            return self._cache['precios'].copy()
        
        try:
            ruta = os.path.join(self.data_dir, 'precios_historicos.csv')
            df = pd.read_csv(ruta)
            self._cache['precios'] = df
            return df.copy()
        except FileNotFoundError:
            return pd.DataFrame()
    
    def cargar_cultivos(self) -> Dict:
        """
        Carga información de cultivos.
        
        Returns:
            Dict con información de cultivos
        """
        if 'cultivos' in self._cache:
            return self._cache['cultivos'].copy()
        
        try:
            ruta = os.path.join(self.data_dir, 'cultivos.json')
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cache['cultivos'] = data
                return data.copy()
        except FileNotFoundError:
            return {'cultivos': []}
    
    def cargar_ubicaciones(self) -> Dict:
        """
        Carga información de ubicaciones/regiones.
        
        Returns:
            Dict con información de regiones
        """
        if 'ubicaciones' in self._cache:
            return self._cache['ubicaciones'].copy()
        
        try:
            ruta = os.path.join(self.data_dir, 'ubicaciones.json')
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cache['ubicaciones'] = data
                return data.copy()
        except FileNotFoundError:
            return {'regiones': []}
    
    def obtener_cultivo_por_nombre(self, nombre: str) -> Optional[Dict]:
        """
        Obtiene información de un cultivo específico.
        
        Args:
            nombre: Nombre del cultivo
            
        Returns:
            Dict con información del cultivo o None
        """
        data = self.cargar_cultivos()
        cultivos = data.get('cultivos', [])
        
        for cultivo in cultivos:
            if cultivo['nombre'].lower() == nombre.lower():
                return cultivo
        
        return None
    
    def obtener_region_por_nombre(self, nombre: str) -> Optional[Dict]:
        """
        Obtiene información de una región específica.
        
        Args:
            nombre: Nombre de la región
            
        Returns:
            Dict con información de la región o None
        """
        data = self.cargar_ubicaciones()
        regiones = data.get('regiones', [])
        
        for region in regiones:
            if region['nombre'].lower() == nombre.lower():
                return region
        
        return None
    
    def obtener_clima_region_mes(self, region: str, mes: int) -> Optional[Dict]:
        """
        Obtiene datos climáticos de una región para un mes específico.
        
        Args:
            region: Nombre de la región
            mes: Número del mes (1-12)
            
        Returns:
            Dict con datos climáticos o None
        """
        df = self.cargar_clima_simulado()
        
        if df.empty:
            return None
        
        meses = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        
        nombre_mes = meses.get(mes, '')
        
        filtro = (df['region'] == region) & (df['mes'] == nombre_mes)
        resultado = df[filtro]
        
        if not resultado.empty:
            return resultado.iloc[0].to_dict()
        
        return None
    
    def obtener_precio_cultivo_mes(self, cultivo: str, 
                                   mes: int, año: int = 2023) -> Optional[float]:
        """
        Obtiene precio de un cultivo para un mes específico.
        
        Args:
            cultivo: Nombre del cultivo
            mes: Número del mes
            año: Año de consulta
            
        Returns:
            Precio promedio o None
        """
        df = self.cargar_precios_historicos()
        
        if df.empty:
            return None
        
        meses = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        
        nombre_mes = meses.get(mes, '')
        
        filtro = (df['cultivo'] == cultivo) & (df['año'] == año) & (df['mes'] == nombre_mes)
        resultado = df[filtro]
        
        if not resultado.empty:
            return resultado.iloc[0]['precio_promedio_soles_kg']
        
        return None
    
    def listar_cultivos_disponibles(self) -> List[str]:
        """
        Lista todos los cultivos disponibles.
        
        Returns:
            Lista de nombres de cultivos
        """
        data = self.cargar_cultivos()
        cultivos = data.get('cultivos', [])
        return [c['nombre'] for c in cultivos]
    
    def listar_regiones_disponibles(self) -> List[str]:
        """
        Lista todas las regiones disponibles.
        
        Returns:
            Lista de nombres de regiones
        """
        data = self.cargar_ubicaciones()
        regiones = data.get('regiones', [])
        return [r['nombre'] for r in regiones]
    
    def obtener_cultivos_por_region(self, region: str) -> List[str]:
        """
        Obtiene cultivos aptos para una región.
        
        Args:
            region: Nombre de la región
            
        Returns:
            Lista de cultivos aptos
        """
        region_info = self.obtener_region_por_nombre(region)
        
        if region_info and 'principales_cultivos' in region_info:
            return region_info['principales_cultivos']
        
        return []
    
    def validar_datos_completos(self) -> Dict[str, bool]:
        """
        Valida que todos los archivos de datos estén disponibles.
        
        Returns:
            Dict con estado de cada archivo
        """
        return {
            'clima': not self.cargar_clima_simulado().empty,
            'precios': not self.cargar_precios_historicos().empty,
            'cultivos': len(self.cargar_cultivos().get('cultivos', [])) > 0,
            'ubicaciones': len(self.cargar_ubicaciones().get('regiones', [])) > 0
        }
    
    def limpiar_cache(self):
        """Limpia el caché de datos"""
        self._cache = {}
    
    def obtener_estadisticas_precio(self, cultivo: str) -> Dict:
        """
        Calcula estadísticas de precio de un cultivo.
        
        Args:
            cultivo: Nombre del cultivo
            
        Returns:
            Dict con estadísticas
        """
        df = self.cargar_precios_historicos()
        
        if df.empty:
            return {}
        
        cultivo_data = df[df['cultivo'] == cultivo]
        
        if cultivo_data.empty:
            return {}
        
        precios = cultivo_data['precio_promedio_soles_kg']
        
        return {
            'precio_medio': round(precios.mean(), 2),
            'precio_minimo': round(precios.min(), 2),
            'precio_maximo': round(precios.max(), 2),
            'desviacion_estandar': round(precios.std(), 2),
            'volatilidad': round(precios.std() / precios.mean(), 4)
        }
    
    def obtener_estadisticas_clima(self, region: str) -> Dict:
        """
        Calcula estadísticas climáticas de una región.
        
        Args:
            region: Nombre de la región
            
        Returns:
            Dict con estadísticas
        """
        df = self.cargar_clima_simulado()
        
        if df.empty:
            return {}
        
        region_data = df[df['region'] == region]
        
        if region_data.empty:
            return {}
        
        return {
            'temperatura_promedio': round(region_data['temperatura_promedio'].mean(), 2),
            'precipitacion_anual': round(region_data['precipitacion_mm'].sum(), 2),
            'humedad_promedio': round(region_data['humedad_relativa'].mean(), 2),
            'riesgo_sequia_promedio': round(region_data['riesgo_sequia'].mean(), 4),
            'riesgo_heladas_promedio': round(region_data['riesgo_heladas'].mean(), 4),
            'riesgo_inundacion_promedio': round(region_data['riesgo_inundacion'].mean(), 4)
        }


# Instancia global del cargador
_loader = None

def get_loader() -> DataLoader:
    """
    Obtiene la instancia global del cargador de datos.
    
    Returns:
        Instancia de DataLoader
    """
    global _loader
    if _loader is None:
        _loader = DataLoader()
    return _loader


# Funciones de conveniencia
def cargar_datos_completos() -> Dict:
    """
    Carga todos los datos del sistema.
    
    Returns:
        Dict con todos los datos
    """
    loader = get_loader()
    return {
        'clima': loader.cargar_clima_simulado(),
        'precios': loader.cargar_precios_historicos(),
        'cultivos': loader.cargar_cultivos(),
        'ubicaciones': loader.cargar_ubicaciones()
    }


def verificar_integridad_datos() -> bool:
    """
    Verifica que todos los datos necesarios estén disponibles.
    
    Returns:
        True si todos los datos están disponibles
    """
    loader = get_loader()
    estado = loader.validar_datos_completos()
    return all(estado.values())