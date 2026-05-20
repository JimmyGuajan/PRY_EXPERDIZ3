"""
Módulo de análisis y generación de decisiones
"""

from typing import Dict, Any, List
from .data_processor import DataProcessor
from .ai_service import AzureOpenAIService


class DecisionEngine:
    """Motor para análisis de datos y generación de decisiones"""
    
    def __init__(self, ai_service: AzureOpenAIService):
        """
        Inicializa el motor de decisiones
        
        Args:
            ai_service: Servicio de Azure OpenAI
        """
        self.ai_service = ai_service
        self.data_processor = DataProcessor()
        self.last_analysis = None
    
    def load_data(self, file_path: str) -> Dict[str, Any]:
        """
        Carga y analiza los datos del archivo
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Diccionario con información de los datos
        """
        try:
            self.data_processor.load_file(file_path)
            info = self.data_processor.get_data_info()
            return {
                "success": True,
                "info": info,
                "sample": self.data_processor.get_data_sample(5).to_dict('records')
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_decision_analysis(self) -> Dict[str, Any]:
        """
        Genera un análisis completo para toma de decisiones
        
        Returns:
            Diccionario con el análisis y sugerencias
        """
        if self.data_processor.data is None:
            return {
                "success": False,
                "error": "No hay datos cargados"
            }
        
        try:
            # Preparar datos para la IA
            data_text = self.data_processor.prepare_data_for_ai()
            
            # Generar análisis
            analysis = self.ai_service.analyze_data_for_decisions(data_text)
            
            self.last_analysis = {
                "data_info": self.data_processor.get_data_info(),
                "summary_stats": self.data_processor.get_summary_statistics(),
                "categorical_summary": self.data_processor.get_categorical_summary(),
                "questions_detected": self.data_processor.detect_questions(),
                "ai_analysis": analysis
            }
            
            return {
                "success": True,
                "analysis": self.last_analysis
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """
        Realiza una pregunta específica sobre los datos
        
        Args:
            question: Pregunta del usuario
            
        Returns:
            Respuesta de la IA
        """
        if self.data_processor.data is None:
            return {
                "success": False,
                "error": "No hay datos cargados"
            }
        
        try:
            data_text = self.data_processor.prepare_data_for_ai()
            answer = self.ai_service.answer_question_about_data(data_text, question)
            
            return {
                "success": True,
                "question": question,
                "answer": answer
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_visualization_suggestions(self) -> Dict[str, Any]:
        """
        Obtiene sugerencias de visualizaciones para el dashboard
        
        Returns:
            Sugerencias de visualizaciones
        """
        if self.data_processor.data is None:
            return {
                "success": False,
                "error": "No hay datos cargados"
            }
        
        try:
            data_text = self.data_processor.prepare_data_for_ai()
            suggestions = self.ai_service.generate_dashboard_suggestions(data_text)
            
            return {
                "success": True,
                "suggestions": suggestions
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_data_overview(self) -> Dict[str, Any]:
        """
        Obtiene una vista general de los datos cargados
        
        Returns:
            Información general de los datos
        """
        if self.data_processor.data is None:
            return {
                "success": False,
                "error": "No hay datos cargados"
            }
        
        return {
            "success": True,
            "info": self.data_processor.get_data_info(),
            "summary_stats": self.data_processor.get_summary_statistics(),
            "categorical_summary": self.data_processor.get_categorical_summary(),
            "questions_detected": self.data_processor.detect_questions(),
            "sample": self.data_processor.get_data_sample(5).to_dict('records')
        }
