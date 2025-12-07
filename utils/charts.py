"""
Utilidades para Gráficos
=========================
Funciones para crear visualizaciones con Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Optional


def crear_grafico_barras_simple(x: List, y: List, titulo: str = "",
                                xlabel: str = "", ylabel: str = "",
                                color: str = "#4ECDC4") -> go.Figure:
    """
    Crea un gráfico de barras simple.
    
    Args:
        x: Valores del eje X
        y: Valores del eje Y
        titulo: Título del gráfico
        xlabel: Etiqueta eje X
        ylabel: Etiqueta eje Y
        color: Color de las barras
        
    Returns:
        Figura de Plotly
    """
    fig = go.Figure(data=[
        go.Bar(x=x, y=y, marker_color=color,
               text=[f"{v:,.0f}" for v in y],
               textposition='auto')
    ])
    
    fig.update_layout(
        title=titulo,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        height=400,
        showlegend=False
    )
    
    return fig


def crear_grafico_lineas(x: List, y: List, titulo: str = "",
                        xlabel: str = "", ylabel: str = "",
                        nombre: str = "Serie") -> go.Figure:
    """
    Crea un gráfico de líneas.
    
    Args:
        x: Valores del eje X
        y: Valores del eje Y
        titulo: Título del gráfico
        xlabel: Etiqueta eje X
        ylabel: Etiqueta eje Y
        nombre: Nombre de la serie
        
    Returns:
        Figura de Plotly
    """
    fig = go.Figure(data=[
        go.Scatter(x=x, y=y, mode='lines+markers',
                  name=nombre, line=dict(width=3, color='#4ECDC4'),
                  marker=dict(size=8))
    ])
    
    fig.update_layout(
        title=titulo,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        height=400,
        hovermode='x unified'
    )
    
    return fig


def crear_grafico_pie(labels: List, values: List, 
                     titulo: str = "") -> go.Figure:
    """
    Crea un gráfico circular (pie).
    
    Args:
        labels: Etiquetas de las secciones
        values: Valores de las secciones
        titulo: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#FFD93D', 
              '#6C5CE7', '#A29BFE', '#FD79A8', '#FDCB6E']
    
    fig = go.Figure(data=[
        go.Pie(labels=labels, values=values, hole=0.4,
               marker=dict(colors=colors),
               textinfo='label+percent',
               textposition='auto')
    ])
    
    fig.update_layout(
        title=titulo,
        height=400
    )
    
    return fig


def crear_grafico_radar(categorias: List, valores: List,
                       titulo: str = "",
                       nombre: str = "Métrica") -> go.Figure:
    """
    Crea un gráfico de radar (araña).
    
    Args:
        categorias: Categorías del radar
        valores: Valores para cada categoría
        titulo: Título del gráfico
        nombre: Nombre de la serie
        
    Returns:
        Figura de Plotly
    """
    fig = go.Figure(data=[
        go.Scatterpolar(
            r=valores,
            theta=categorias,
            fill='toself',
            name=nombre,
            line_color='#FF6B6B'
        )
    ])
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(valores) * 1.2])
        ),
        showlegend=False,
        title=titulo,
        height=450
    )
    
    return fig


def crear_grafico_gauge(valor: float, titulo: str = "",
                       rango_min: float = 0,
                       rango_max: float = 100) -> go.Figure:
    """
    Crea un gráfico de velocímetro (gauge).
    
    Args:
        valor: Valor a mostrar
        titulo: Título del gráfico
        rango_min: Valor mínimo del rango
        rango_max: Valor máximo del rango
        
    Returns:
        Figura de Plotly
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=valor,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': titulo, 'font': {'size': 24}},
        delta={'reference': (rango_max - rango_min) * 0.7},
        gauge={
            'axis': {'range': [rango_min, rango_max], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [rango_min, rango_max * 0.5], 'color': '#FF6B6B'},
                {'range': [rango_max * 0.5, rango_max * 0.7], 'color': '#FFD93D'},
                {'range': [rango_max * 0.7, rango_max], 'color': '#95E1D3'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': rango_max * 0.7
            }
        }
    ))
    
    fig.update_layout(height=400)
    
    return fig


def crear_grafico_comparacion_escenarios(df_escenarios: pd.DataFrame,
                                        metrica: str = "van") -> go.Figure:
    """
    Crea gráfico comparativo de escenarios.
    
    Args:
        df_escenarios: DataFrame con resultados de escenarios
        metrica: Métrica a comparar (van, roi, utilidad, etc.)
        
    Returns:
        Figura de Plotly
    """
    colores = {'Pesimista': '#FF6B6B', 'Base': '#FFD93D', 'Optimista': '#95E1D3'}
    
    fig = go.Figure()
    
    for escenario in df_escenarios['Escenario']:
        valor = df_escenarios[df_escenarios['Escenario'] == escenario][metrica].iloc[0]
        color = colores.get(escenario, '#4ECDC4')
        
        fig.add_trace(go.Bar(
            x=[escenario],
            y=[valor],
            name=escenario,
            marker_color=color,
            text=[f"{valor:,.0f}"],
            textposition='auto'
        ))
    
    fig.update_layout(
        title=f"Comparación de {metrica.upper()} por Escenario",
        xaxis_title="Escenario",
        yaxis_title=metrica.upper(),
        showlegend=False,
        height=400
    )
    
    return fig


def crear_grafico_flujo_caja(flujo: List[float], 
                            titulo: str = "Flujo de Caja") -> go.Figure:
    """
    Crea gráfico de flujo de caja.
    
    Args:
        flujo: Lista con flujo de caja por período
        titulo: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    periodos = list(range(len(flujo)))
    flujo_acumulado = np.cumsum(flujo)
    
    colores = ['red' if x < 0 else 'green' for x in flujo]
    
    fig = go.Figure()
    
    # Flujo mensual
    fig.add_trace(go.Bar(
        x=periodos,
        y=flujo,
        name='Flujo Mensual',
        marker_color=colores
    ))
    
    # Flujo acumulado
    fig.add_trace(go.Scatter(
        x=periodos,
        y=flujo_acumulado,
        name='Flujo Acumulado',
        mode='lines+markers',
        line=dict(color='#4ECDC4', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title=titulo,
        xaxis_title="Período (mes)",
        yaxis=dict(title="Flujo Mensual (S/.)"),
        yaxis2=dict(title="Flujo Acumulado (S/.)", overlaying='y', side='right'),
        height=400,
        hovermode='x unified'
    )
    
    return fig


def crear_heatmap_sensibilidad(df: pd.DataFrame,
                               x_col: str, y_col: str, valor_col: str,
                               titulo: str = "Análisis de Sensibilidad") -> go.Figure:
    """
    Crea un mapa de calor para análisis de sensibilidad.
    
    Args:
        df: DataFrame con datos
        x_col: Columna para eje X
        y_col: Columna para eje Y
        valor_col: Columna con valores
        titulo: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    pivot = df.pivot(index=y_col, columns=x_col, values=valor_col)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='RdYlGn',
        text=pivot.values,
        texttemplate='%{text:,.0f}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title=titulo,
        xaxis_title=x_col,
        yaxis_title=y_col,
        height=500
    )
    
    return fig


def crear_grafico_distribucion(valores: List[float],
                               titulo: str = "Distribución",
                               nombre: str = "Distribución") -> go.Figure:
    """
    Crea un histograma de distribución.
    
    Args:
        valores: Lista de valores
        titulo: Título del gráfico
        nombre: Nombre de la serie
        
    Returns:
        Figura de Plotly
    """
    fig = go.Figure(data=[
        go.Histogram(x=valores, name=nombre,
                    marker_color='#4ECDC4',
                    nbinsx=30)
    ])
    
    fig.update_layout(
        title=titulo,
        xaxis_title="Valor",
        yaxis_title="Frecuencia",
        showlegend=False,
        height=400
    )
    
    return fig


def crear_grafico_boxplot(datos: Dict[str, List[float]],
                          titulo: str = "Box Plot") -> go.Figure:
    """
    Crea un diagrama de caja (box plot).
    
    Args:
        datos: Diccionario {nombre: valores}
        titulo: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    fig = go.Figure()
    
    for nombre, valores in datos.items():
        fig.add_trace(go.Box(y=valores, name=nombre,
                            marker_color='#4ECDC4'))
    
    fig.update_layout(
        title=titulo,
        yaxis_title="Valor",
        showlegend=True,
        height=400
    )
    
    return fig


def crear_grafico_cascada(categorias: List[str], valores: List[float],
                         titulo: str = "Análisis de Cascada") -> go.Figure:
    """
    Crea un gráfico de cascada (waterfall).
    
    Args:
        categorias: Categorías
        valores: Valores para cada categoría
        titulo: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    fig = go.Figure(go.Waterfall(
        name="Análisis",
        orientation="v",
        measure=["relative"] * (len(valores) - 1) + ["total"],
        x=categorias,
        textposition="outside",
        text=[f"S/. {v:,.0f}" for v in valores],
        y=valores,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title=titulo,
        showlegend=False,
        height=400
    )
    
    return fig


def aplicar_tema_personalizado(fig: go.Figure,
                              color_fondo: str = "#f5f5f5") -> go.Figure:
    """
    Aplica tema personalizado a una figura.
    
    Args:
        fig: Figura de Plotly
        color_fondo: Color de fondo
        
    Returns:
        Figura modificada
    """
    fig.update_layout(
        plot_bgcolor=color_fondo,
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12, color="#333"),
        title_font=dict(size=16, color="#2C3E50"),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig