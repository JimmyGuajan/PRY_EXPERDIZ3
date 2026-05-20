"""
Módulo para procesamiento de datos de archivos Excel/CSV
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import os


class DataProcessor:
    """Clase para procesar y analizar datos de archivos"""
    
    def __init__(self):
        self.data = None
        self.file_path = None
        self.file_type = None
    
    def load_file(self, file_path: str) -> pd.DataFrame:
        """
        Carga un archivo Excel o CSV
        
        Args:
            file_path: Ruta del archivo a cargar
            
        Returns:
            DataFrame con los datos cargados
        """
        self.file_path = file_path
        file_ext = os.path.splitext(file_path)[1].lower()
        self.file_type = file_ext
        
        try:
            if file_ext in ['.xlsx', '.xls']:
                self.data = pd.read_excel(file_path)
            elif file_ext == '.csv':
                self.data = pd.read_csv(file_path)
            else:
                raise ValueError(f"Formato no soportado: {file_ext}")
            
            return self.data
        except Exception as e:
            raise Exception(f"Error al cargar archivo: {str(e)}")
    
    def get_data_info(self) -> Dict[str, Any]:
        """
        Obtiene información básica sobre el dataset
        
        Returns:
            Diccionario con información del dataset
        """
        if self.data is None:
            return {}
        
        return {
            "rows": len(self.data),
            "columns": len(self.data.columns),
            "column_names": self.data.columns.tolist(),
            "column_types": self.data.dtypes.astype(str).to_dict(),
            "memory_usage": self.data.memory_usage(deep=True).sum() / 1024**2,  # MB
            "null_counts": self.data.isnull().sum().to_dict(),
            "file_type": self.file_type
        }
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas resumidas de las columnas numéricas
        
        Returns:
            Diccionario con estadísticas
        """
        if self.data is None:
            return {}
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return {"message": "No hay columnas numéricas"}
        
        return self.data[numeric_cols].describe().to_dict()
    
    def get_categorical_summary(self) -> Dict[str, Any]:
        """
        Obtiene resumen de columnas categóricas
        
        Returns:
            Diccionario con resumen de categorías
        """
        if self.data is None:
            return {}
        
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        summary = {}
        
        for col in categorical_cols:
            summary[col] = {
                "unique_values": self.data[col].nunique(),
                "top_values": self.data[col].value_counts().head(10).to_dict()
            }
        
        return summary
    
    def detect_questions(self) -> List[str]:
        """
        Detecta posibles preguntas en el dataset basándose en nombres de columnas
        que contengan palabras clave de preguntas
        
        Returns:
            Lista de posibles preguntas detectadas
        """
        if self.data is None:
            return []
        
        question_keywords = ['pregunta', 'question', 'qué', 'que', 'cuál', 'cual', 
                           'cuándo', 'cuando', 'dónde', 'donde', 'por qué', 'porque',
                           'cómo', 'como', 'evaluación', 'evaluacion', 'respuesta']
        
        questions = []
        for col in self.data.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in question_keywords):
                questions.append(col)
        
        return questions
    
    def get_data_sample(self, n: int = 5) -> pd.DataFrame:
        """
        Obtiene una muestra de los datos
        
        Args:
            n: Número de filas a mostrar
            
        Returns:
            DataFrame con la muestra
        """
        if self.data is None:
            return pd.DataFrame()
        
        return self.data.head(n)
    
    def prepare_data_for_ai(self, sample_rows: int = 20) -> str:
        """
        Prepara los datos en formato texto para ser enviados a la IA
        Solo usa las primeras N filas para no sobrecargar el contexto
        
        Args:
            sample_rows: Número de filas a incluir en el análisis (default: 20)
            
        Returns:
            String con los datos formateados
        """
        if self.data is None:
            return ""
        
        info = self.get_data_info()
        summary = self.get_summary_statistics()
        categorical = self.get_categorical_summary()
        
        text = f"""
INFORMACIÓN DEL DATASET:
- Filas totales: {info.get('rows', 0)}
- Columnas: {info.get('columns', 0)}
- Columnas: {', '.join(info.get('column_names', []))}
- Tipo de archivo: {info.get('file_type', 'unknown')}
- Filas analizadas: {min(sample_rows, info.get('rows', 0))} (muestra representativa)

ESTADÍSTICAS DE COLUMNAS NUMÉRICAS:
{summary if 'message' not in summary else 'No hay columnas numéricas'}

RESUMEN DE COLUMNAS CATEGÓRICAS:
{categorical if categorical else 'No hay columnas categóricas'}

PREGUNTAS DETECTADAS:
{self.detect_questions() if self.detect_questions() else 'No se detectaron preguntas explícitas'}

MUESTRA DE DATOS (primeras {sample_rows} filas):
{self.get_data_sample(sample_rows).to_string(index=False)}
"""
        return text
    
    def filter_data(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Filtra los datos según criterios especificados
        
        Args:
            filters: Diccionario con criterios de filtro
            
        Returns:
            DataFrame filtrado
        """
        if self.data is None:
            return pd.DataFrame()
        
        filtered_data = self.data.copy()
        
        for col, value in filters.items():
            if col in filtered_data.columns:
                if isinstance(value, list):
                    filtered_data = filtered_data[filtered_data[col].isin(value)]
                else:
                    filtered_data = filtered_data[filtered_data[col] == value]
        
        return filtered_data
