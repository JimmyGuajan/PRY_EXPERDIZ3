"""
Módulo de integración con Google AI Studio (Gemini)
"""

import requests
import json
from typing import Dict, Any, Optional
import yaml
import os


class GoogleAIService:
    """Clase para interactuar con Google AI Studio (Gemini)"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Inicializa el servicio de Google AI Studio
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        self.config = self._load_config(config_path)
        self.api_key = self.config.get('google_ai', {}).get('api_key')
        self.model = self.config.get('google_ai', {}).get('model', 'gemini-1.5-pro')
        self.temperature = self.config.get('app', {}).get('temperature', 0.7)
        self.max_tokens = self.config.get('app', {}).get('max_tokens', 2000)
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Carga la configuración desde archivo YAML
        
        Args:
            config_path: Ruta al archivo de configuración
            
        Returns:
            Diccionario con la configuración
        """
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                # Valores por defecto si no existe config.yaml
                return {
                    'google_ai': {
                        'api_key': '',
                        'model': 'gemini-1.5-pro'
                    },
                    'app': {
                        'temperature': 0.7,
                        'max_tokens': 2000
                    }
                }
        except Exception as e:
            print(f"Error cargando configuración: {str(e)}")
            return {}
    
    def generate_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Genera una respuesta usando Google AI Studio (Gemini)
        
        Args:
            prompt: Prompt del usuario
            system_prompt: Prompt del sistema (opcional)
            
        Returns:
            Respuesta generada por la IA
        """
        if not self.api_key:
            return "Error: No se han configurado las credenciales de Google AI Studio. Por favor configura el archivo config/config.yaml"
        
        # Construir el contenido del mensaje
        content_parts = []
        
        if system_prompt:
            content_parts.append({
                "text": f"INSTRUCCIONES DEL SISTEMA: {system_prompt}\n\n"
            })
        
        content_parts.append({
            "text": prompt
        })
        
        # URL de la API de Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": content_parts
                }
            ],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
                else:
                    return "Error: No se recibió respuesta del modelo"
            else:
                return f"Error en la API: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "Error: La solicitud tardó demasiado tiempo. Por favor intenta nuevamente."
        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"
    
    def analyze_data_for_decisions(self, data_info: str) -> str:
        """
        Analiza los datos y genera sugerencias para toma de decisiones
        
        Args:
            data_info: Información del dataset en formato texto
            
        Returns:
            Análisis y sugerencias de la IA
        """
        system_prompt = """Eres un experto en análisis de datos y toma de decisiones. 
Tu tarea es analizar la información proporcionada y generar:
1. Un resumen de los datos
2. Insights clave y patrones identificados
3. Sugerencias específicas para toma de decisiones
4. Recomendaciones accionables basadas en los datos

Responde en español de manera clara y estructurada."""
        
        prompt = f"""Analiza la siguiente información de un dataset y proporciona recomendaciones para toma de decisiones:

{data_info}

Por favor proporciona:
1. **Resumen Ejecutivo**: Breve descripción de los datos
2. **Insights Clave**: Patrones o tendencias importantes
3. **Sugerencias de Decisión**: Recomendaciones específicas basadas en los datos
4. **Próximos Pasos**: Acciones concretas a tomar
"""
        
        return self.generate_completion(prompt, system_prompt)
    
    def answer_question_about_data(self, data_info: str, question: str) -> str:
        """
        Responde una pregunta específica sobre los datos
        
        Args:
            data_info: Información del dataset en formato texto
            question: Pregunta del usuario
            
        Returns:
            Respuesta de la IA
        """
        system_prompt = """Eres un analista de datos experto. 
Responde preguntas específicas sobre los datos proporcionados de manera clara y precisa.
Si la información no es suficiente para responder, indícalo claramente."""
        
        prompt = f"""Basándote en la siguiente información del dataset:

{data_info}

Responde a esta pregunta: {question}
"""
        
        return self.generate_completion(prompt, system_prompt)
    
    def generate_dashboard_suggestions(self, data_info: str) -> str:
        """
        Genera sugerencias sobre qué visualizaciones crear para el dashboard
        
        Args:
            data_info: Información del dataset en formato texto
            
        Returns:
            Sugerencias de visualizaciones
        """
        system_prompt = """Eres un experto en visualización de datos y dashboards.
Sugiere qué tipos de gráficos y visualizaciones serían más útiles para los datos proporcionados."""
        
        prompt = f"""Basándote en la siguiente información del dataset:

{data_info}

Sugiere qué visualizaciones (gráficos de barras, líneas, pastel, etc.) serían más útiles para analizar estos datos.
Para cada visualización, indica:
1. Tipo de gráfico
2. Qué columnas usar
3. Qué insights podría mostrar
"""
        
        return self.generate_completion(prompt, system_prompt)
