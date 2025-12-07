# 🌾 AgroShield 360

## Sistema Integral de Análisis Agrícola

**AgroShield 360** es una plataforma web avanzada diseñada para pequeños y medianos productores agrícolas del Perú. Permite evaluar la rentabilidad de cultivos, predecir rendimientos, gestionar riesgos climáticos y de mercado, y realizar análisis económico completo antes de invertir.

---

## 🎯 Características Principales

### 📊 Predicción de Rendimiento
- Modelo predictivo basado en múltiples factores agronómicos
- Consideración de fertilidad del suelo, disponibilidad de agua, tecnología y experiencia
- Predicción de rendimientos mínimo, probable y máximo
- Ajustes por región y condiciones climáticas

### ⚠️ Análisis de Riesgos
- **Índice de Riesgo Agro-Económico (IRA)** multi-dimensional
- Evaluación de riesgo climático (sequía, heladas, lluvias, plagas)
- Análisis de volatilidad de precios de mercado
- Evaluación de riesgo de producción
- Recomendaciones automáticas de mitigación

### 💰 Evaluación Económica
- Cálculo de **VAN (VPN)** y **TIR**
- Análisis de flujo de caja proyectado
- Determinación de punto de equilibrio
- Cálculo de ROI y márgenes de utilidad
- Período de recuperación de inversión

### 🎲 Simulación de Escenarios
- Tres escenarios obligatorios: Pesimista, Base y Optimista
- Análisis de sensibilidad bivariado (rendimiento vs precio)
- Simulación Monte Carlo para gestión de incertidumbre
- Comparación visual de resultados

### 🎯 Sistema de Recomendación Inteligente
- Puntuación integral sobre 100 puntos
- Criterios ponderados: Rentabilidad (40%), Riesgo (30%), Escenarios (20%), Mercado (10%)
- Recomendación final clara: Conviene/No Conviene Sembrar
- Acciones prioritarias sugeridas

### 📄 Generación de Reportes
- Reportes ejecutivos en formato HTML, TXT y JSON
- Vista previa interactiva
- Incluye todos los análisis y gráficos
- Listo para compartir e imprimir

---

## 🚀 Instalación

### Prerrequisitos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**
```bash
git clone https://github.com/tu-usuario/agroshield360.git
cd agroshield360
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Crear carpetas necesarias**
```bash
mkdir -p data reports assets
```

5. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## 📁 Estructura del Proyecto

```
AgroShield360/
│
├── app.py                        # Aplicación principal de Streamlit
│
├── pages/                        # Páginas del sistema
│   ├── 1_Datos_del_Productor.py
│   ├── 2_Predicción_de_Rendimiento.py
│   ├── 3_Análisis_de_Riesgos.py
│   ├── 4_Evaluación_Económica.py
│   ├── 5_Simulador_de_Escenarios.py
│   ├── 6_Recomendación_Final.py
│   └── 7_Generar_Reporte.py
│
├── data/                         # Datos del sistema
│   ├── clima_simulado.csv        # Datos climáticos por región
│   ├── precios_historicos.csv    # Precios históricos de cultivos
│   ├── cultivos.json             # Información de cultivos
│   └── ubicaciones.json          # Información de regiones
│
├── models/                       # Modelos predictivos
│   ├── rendimiento_model.py      # Modelo de predicción de rendimiento
│   └── riesgo_model.py           # Modelo de análisis de riesgo
│
├── services/                     # Lógica de negocio
│   ├── rendimiento_service.py
│   ├── riesgo_service.py
│   ├── economia_service.py
│   ├── escenarios_service.py
│   └── recomendacion_service.py
│
├── utils/                        # Utilidades
│   ├── helpers.py                # Funciones auxiliares
│   ├── loaders.py                # Cargadores de datos
│   └── charts.py                 # Utilidades para gráficos
│
├── reports/                      # Reportes generados
├── assets/                       # Recursos (imágenes, logos)
│
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Este archivo
```

---

## 🎮 Uso del Sistema

### Flujo de Trabajo Típico

1. **Inicio de Sesión**
   - Abre la aplicación en tu navegador
   - Familiarízate con la interfaz principal

2. **Ingreso de Datos (Módulo 1)**
   - Nombre del productor
   - Cultivo a sembrar
   - Ubicación/Región
   - Área disponible en hectáreas
   - Fechas de siembra y cosecha
   - Costos de producción detallados
   - Precio de venta esperado

3. **Predicción de Rendimiento (Módulo 2)**
   - Configura parámetros agronómicos:
     - Fertilidad del suelo (1-10)
     - Disponibilidad de agua (1-10)
     - Nivel tecnológico (1-10)
     - Experiencia del productor (años)
   - Obtén predicciones de rendimiento

4. **Análisis de Riesgos (Módulo 3)**
   - Revisa el IRA (Índice de Riesgo Agro-Económico)
   - Identifica riesgos principales
   - Lee recomendaciones de mitigación

5. **Evaluación Económica (Módulo 4)**
   - Analiza el VAN y TIR del proyecto
   - Revisa el flujo de caja
   - Verifica el punto de equilibrio
   - Ajusta la tasa de descuento si es necesario

6. **Simulación de Escenarios (Módulo 5)**
   - Explora escenarios Pesimista, Base y Optimista
   - Analiza sensibilidad a cambios de precio y rendimiento
   - Comprende el rango de resultados posibles

7. **Recomendación Final (Módulo 6)**
   - Obtén puntuación integral (0-100)
   - Lee la recomendación del sistema
   - Revisa acciones prioritarias sugeridas

8. **Generación de Reporte (Módulo 7)**
   - Genera reporte ejecutivo completo
   - Descarga en formato HTML, TXT o JSON
   - Comparte con socios o asesores

---

## 📊 Base de Datos

### Cultivos Soportados
- 🌽 Maíz
- 🥔 Papa
- 🍚 Arroz
- 🌾 Trigo
- 🌾 Quinua
- 🥬 Espárrago
- 🥑 Palta
- ☕ Café
- 🍫 Cacao
- 🌸 Algodón

### Regiones Cubiertas
- Lima
- Arequipa
- La Libertad
- Lambayeque
- Piura
- Ica
- Junín
- Cajamarca
- Cusco
- Ancash
- Ayacucho
- Huánuco
- San Martín

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje de programación
- **Streamlit**: Framework web interactivo
- **Pandas**: Manipulación de datos
- **NumPy**: Cálculos numéricos
- **Plotly**: Visualizaciones interactivas
- **NumPy-Financial**: Cálculos financieros (VAN, TIR)
- **Scikit-learn**: Modelos predictivos

---

## 📈 Modelos Implementados

### Modelo de Rendimiento
- Predicción basada en factores ponderados
- Ajuste regional automático
- Consideración de estacionalidad
- Rangos de confianza (mínimo, probable, máximo)

### Modelo de Riesgo (IRA)
- Componente climático (40%)
  - Riesgo de sequía, heladas, inundaciones, plagas
- Componente de mercado (35%)
  - Volatilidad de precios históricos
- Componente de producción (25%)
  - Variabilidad de rendimientos

### Modelo Económico
- Flujo de caja con distribución temporal de costos
- VAN con tasa de descuento ajustable
- TIR calculada a partir de flujos
- Análisis de sensibilidad multi-variable

---

## 🔧 Configuración Avanzada

### Personalización de Parámetros

Puedes modificar parámetros del sistema editando los archivos de servicios:

**Tasa de descuento por defecto:**
```python
# En services/economia_service.py
self.tasa_descuento_default = 0.12  # 12% anual
```

**Pesos del IRA:**
```python
# En models/riesgo_model.py
self.pesos_ira = {
    'climatico': 0.40,
    'mercado': 0.35,
    'produccion': 0.25
}
```

**Factores de escenarios:**
```python
# En services/escenarios_service.py
'Pesimista': {
    'factor_rendimiento': 0.80,  # -20%
    'factor_precio': 0.85         # -15%
}
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📝 Notas Importantes

### Datos Simulados
- Los datos climáticos y de precios incluidos son simulaciones basadas en promedios históricos
- Para uso en producción, se recomienda integrar datos reales de:
  - SENAMHI (Servicio Nacional de Meteorología e Hidrología del Perú)
  - MINAGRI (Ministerio de Agricultura y Riego)
  - Mercados locales y bolsas de productos

### Limitaciones
- El sistema no reemplaza el criterio de un agrónomo experto
- Las predicciones son estimaciones basadas en modelos matemáticos
- Se recomienda validar resultados con asesores técnicos locales

### Seguridad
- No se almacenan datos sensibles del usuario
- Todos los datos se guardan temporalmente en `session_state`
- Los reportes generados son locales y no se envían a servidores externos

---

## 📞 Soporte y Contacto

Para reportar bugs, sugerir mejoras o solicitar ayuda:

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/agroshield360/issues)
- **Email**: soporte@agroshield360.com
- **Documentación**: [Wiki del Proyecto](https://github.com/tu-usuario/agroshield360/wiki)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 🙏 Agradecimientos

- Datos climáticos basados en información pública de SENAMHI
- Precios de referencia del MINAGRI
- Inspirado en las necesidades de pequeños productores agrícolas del Perú

---

## 🚀 Roadmap Futuro

- [ ] Integración con APIs de datos en tiempo real
- [ ] Módulo de gestión de múltiples parcelas
- [ ] Sistema de alertas climáticas
- [ ] Comparación con otros productores (benchmarking)
- [ ] Aplicación móvil
- [ ] Integración con sistemas de contabilidad
- [ ] Soporte para más cultivos y regiones
- [ ] Machine Learning avanzado para predicciones

---

<div align="center">
  <p><strong>AgroShield 360</strong></p>
  <p>Desarrollado con ❤️ para los agricultores del Perú</p>
  <p>© 2025 - Versión 1.0</p>
</div>
