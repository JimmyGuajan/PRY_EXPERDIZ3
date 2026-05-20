"""
Módulo de visualización para el dashboard de Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
import numpy as np


class Dashboard:
    """Clase para crear visualizaciones en Streamlit"""
    
    @staticmethod
    def display_data_info(data_info: Dict[str, Any]):
        """
        Muestra información básica del dataset
        
        Args:
            data_info: Diccionario con información del dataset
        """
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Filas", data_info.get('rows', 0))
        
        with col2:
            st.metric("Columnas", data_info.get('columns', 0))
        
        with col3:
            st.metric("Tamaño (MB)", f"{data_info.get('memory_usage', 0):.2f}")
        
        st.subheader("Columnas")
        cols_df = pd.DataFrame({
            "Nombre": data_info.get('column_names', []),
            "Tipo": [str(data_info.get('column_types', {}).get(col, '')) for col in data_info.get('column_names', [])]
        })
        st.dataframe(cols_df, use_container_width=True)
    
    @staticmethod
    def display_summary_statistics(summary_stats: Dict[str, Any]):
        """
        Muestra estadísticas resumidas
        
        Args:
            summary_stats: Diccionario con estadísticas
        """
        if 'message' in summary_stats:
            st.info(summary_stats['message'])
            return
        
        st.subheader("Estadísticas Descriptivas")
        
        # Convertir a DataFrame para mejor visualización
        stats_df = pd.DataFrame(summary_stats).T
        st.dataframe(stats_df, use_container_width=True)
    
    @staticmethod
    def display_categorical_summary(categorical_summary: Dict[str, Any]):
        """
        Muestra resumen de variables categóricas
        
        Args:
            categorical_summary: Diccionario con resumen categórico
        """
        if not categorical_summary:
            st.info("No hay columnas categóricas")
            return
        
        st.subheader("Variables Categóricas")
        
        for col, info in categorical_summary.items():
            with st.expander(f"{col} ({info['unique_values']} valores únicos)"):
                st.write(f"Valores únicos: {info['unique_values']}")
                st.write("Top valores:")
                top_df = pd.DataFrame(list(info['top_values'].items()), 
                                     columns=['Valor', 'Frecuencia'])
                st.bar_chart(top_df.set_index('Valor'))
    
    @staticmethod
    def display_questions_detected(questions: List[str]):
        """
        Muestra las preguntas detectadas en el dataset
        
        Args:
            questions: Lista de preguntas detectadas
        """
        if not questions:
            st.info("No se detectaron preguntas explícitas en el dataset")
            return
        
        st.subheader("Preguntas Detectadas")
        for i, question in enumerate(questions, 1):
            st.write(f"{i}. {question}")
    
    @staticmethod
    def create_histogram(df: pd.DataFrame, column: str):
        """
        Crea un histograma para una columna numérica
        
        Args:
            df: DataFrame con los datos
            column: Nombre de la columna
        """
        fig = px.histogram(df, x=column, nbins=30, title=f"Distribución de {column}")
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str = ""):
        """
        Crea un gráfico de barras
        
        Args:
            df: DataFrame con los datos
            x_col: Columna para eje X
            y_col: Columna para eje Y
            title: Título del gráfico
        """
        fig = px.bar(df, x=x_col, y=y_col, title=title)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_scatter_plot(df: pd.DataFrame, x_col: str, y_col: str, color_col: str = None):
        """
        Crea un gráfico de dispersión
        
        Args:
            df: DataFrame con los datos
            x_col: Columna para eje X
            y_col: Columna para eje Y
            color_col: Columna para color (opcional)
        """
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col, 
                        title=f"Relación entre {x_col} y {y_col}")
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_pie_chart(df: pd.DataFrame, column: str, title: str = ""):
        """
        Crea un gráfico circular
        
        Args:
            df: DataFrame con los datos
            column: Columna a graficar
            title: Título del gráfico
        """
        value_counts = df[column].value_counts()
        fig = px.pie(values=value_counts.values, names=value_counts.index, 
                    title=title or f"Distribución de {column}")
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def create_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str = ""):
        """
        Crea un gráfico de líneas
        
        Args:
            df: DataFrame con los datos
            x_col: Columna para eje X
            y_col: Columna para eje Y
            title: Título del gráfico
        """
        fig = px.line(df, x=x_col, y=y_col, title=title)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def display_ai_analysis(analysis: str):
        """
        Muestra el análisis generado por la IA
        
        Args:
            analysis: Texto del análisis
        """
        st.subheader("🤖 Análisis de IA para Toma de Decisiones")
        st.markdown(analysis)
    
    @staticmethod
    def display_sample_data(df: pd.DataFrame, n: int = 5):
        """
        Muestra una muestra de los datos
        
        Args:
            df: DataFrame con los datos
            n: Número de filas a mostrar
        """
        st.subheader("Muestra de Datos")
        st.dataframe(df.head(n), use_container_width=True)
    
    @staticmethod
    def create_correlation_heatmap(df: pd.DataFrame):
        """
        Crea un mapa de calor de correlación
        
        Args:
            df: DataFrame con los datos
        """
        numeric_df = df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            st.info("Se necesitan al menos 2 columnas numéricas para el mapa de correlación")
            return
        
        correlation_matrix = numeric_df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=correlation_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlación")
        ))
        
        fig.update_layout(
            title="Mapa de Calor de Correlación",
            width=800,
            height=800
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def generate_auto_report(df: pd.DataFrame):
        """
        Genera un reporte automático con gráficos interesantes basados en los datos
        
        Args:
            df: DataFrame con los datos
        """
        st.header("📊 Reporte Automático de Datos")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not numeric_cols and not categorical_cols:
            st.warning("No hay suficientes datos para generar gráficos")
            return
        
        # Sección 1: Distribuciones de columnas numéricas
        if numeric_cols:
            st.subheader("📈 Distribuciones de Variables Numéricas")
            cols_per_row = 2
            for i in range(0, min(len(numeric_cols), 4), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(numeric_cols[i:i+cols_per_row]):
                    with cols[j]:
                        fig = px.histogram(df, x=col, nbins=20, title=f"Distribución de {col}")
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)
        
        # Sección 2: Top categorías
        if categorical_cols:
            st.subheader("📊 Top Categorías")
            for col in categorical_cols[:3]:  # Máximo 3 columnas categóricas
                value_counts = df[col].value_counts().head(10)
                if len(value_counts) > 0:
                    fig = px.bar(x=value_counts.index, y=value_counts.values, 
                                title=f"Top 10: {col}")
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
        
        # Sección 3: Correlaciones
        if len(numeric_cols) >= 2:
            st.subheader("🔗 Correlaciones entre Variables Numéricas")
            Dashboard.create_correlation_heatmap(df)
        
        # Sección 4: Relaciones entre variables
        if len(numeric_cols) >= 2:
            st.subheader("🔍 Relaciones entre Variables")
            # Mostrar hasta 3 scatter plots
            pairs = []
            for i in range(min(len(numeric_cols) - 1, 3)):
                pairs.append((numeric_cols[i], numeric_cols[i + 1]))
            
            for x_col, y_col in pairs:
                fig = px.scatter(df, x=x_col, y=y_col, 
                               title=f"Relación: {x_col} vs {y_col}",
                               trendline="ols")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Sección 5: Distribuciones por categoría
        if categorical_cols and numeric_cols:
            st.subheader("📊 Distribuciones por Categoría")
            cat_col = categorical_cols[0]
            num_col = numeric_cols[0]
            
            fig = px.box(df, x=cat_col, y=num_col, 
                       title=f"Distribución de {num_col} por {cat_col}")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Sección 6: Resumen estadístico
        st.subheader("📋 Resumen Estadístico")
        if numeric_cols:
            stats_df = df[numeric_cols].describe()
            st.dataframe(stats_df, use_container_width=True)
