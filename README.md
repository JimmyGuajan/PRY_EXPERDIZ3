# 📊 Dashboard de Toma de Decisiones con IA

Sistema de dashboard interactivo para toma de decisiones basado en análisis de datos con inteligencia artificial usando Azure OpenAI, Google AI Studio (Gemini) y Streamlit.

## 🚀 Características

- **Carga de Datos**: Soporte para archivos Excel (.xlsx, .xls) y CSV
- **Análisis Automático**: Estadísticas descriptivas y resumen de datos
- **IA para Decisiones**: Análisis inteligente con sugerencias accionables
- **Preguntas Interactivas**: Haz preguntas específicas sobre tus datos
- **Visualizaciones**: Múltiples tipos de gráficos interactivos
- **Detección de Preguntas**: Identifica automáticamente columnas con preguntas
- **Múltiples Proveedores de IA**: Soporte para Azure OpenAI y Google AI Studio (Gemini)
- **Reporte Automático**: Generación automática de dashboards con gráficos interesantes

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. **Clonar o descargar el proyecto**

2. **Crear entorno virtual** (opcional pero recomendado):
```bash
python -m venv venv
```

3. **Activar entorno virtual**:
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

1. **Copiar el archivo de configuración de ejemplo**:
```bash
copy config\config_template.yaml config\config.yaml
```

2. **Editar `config/config.yaml`** con tus credenciales:

**Para Azure OpenAI:**
```yaml
azure_openai:
  api_key: "tu_api_key_azure_aqui"
  api_endpoint: "https://openaiinteligenciainformacion.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
  deployment_name: "gpt-4o"
  api_version: "2024-08-01-preview"
```

**Para Google AI Studio (Gemini):**
```yaml
google_ai:
  api_key: "tu_api_key_gemini_aqui"
  model: "gemini-1.5-pro"
```

**Obtener API Key de Google AI Studio:**
1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Crea un nuevo proyecto o selecciona uno existente
3. Genera una API Key
4. Copia la API Key en tu archivo `config/config.yaml`

⚠️ **IMPORTANTE**: El archivo `config/config.yaml` está en `.gitignore` para proteger tus credenciales. No lo commits al repositorio.

## 🎯 Uso

1. **Ejecutar la aplicación**:
```bash
streamlit run app.py
```

2. **Abrir el navegador**: La aplicación se abrirá automáticamente en `http://localhost:8501`

3. **Cargar un archivo**: Sube un archivo Excel o CSV desde la sidebar

4. **Seleccionar proveedor de IA**: Elige entre Azure OpenAI o Google AI Studio (Gemini) en la sidebar

5. **Explorar las funcionalidades**:
   - **Pestaña Datos**: Explora la información general de tus datos
   - **Pestaña Análisis IA**: Genera análisis inteligentes para toma de decisiones
   - **Pestaña Preguntar**: Haz preguntas específicas sobre tus datos
   - **Pestaña Visualizaciones**: Crea gráficos interactivos
   - **Pestaña Reporte Automático**: Genera un reporte automático con gráficos interesantes

## 📁 Estructura del Proyecto

```
PRY_EXPERDIZ3/
├── .gitignore              # Archivos ignorados por Git
├── README.md              # Este archivo
├── requirements.txt       # Dependencias de Python
├── app.py                # Aplicación principal de Streamlit
├── config/               # Configuración
│   ├── config_template.yaml  # Plantilla de configuración
│   └── config.yaml         # Configuración real (no en Git)
├── data/                 # Archivos de datos temporales
│   └── .gitkeep
└── src/                  # Módulos del sistema
    ├── __init__.py
    ├── data_processor.py    # Procesamiento de datos
    ├── ai_service.py        # Integración con Azure OpenAI
    ├── google_ai_service.py # Integración con Google AI Studio
    ├── decision_engine.py  # Motor de decisiones
    └── dashboard.py         # Visualizaciones
```

## 🔐 Seguridad

- Las credenciales de API se almacenan en `config/config.yaml`
- Este archivo está excluido del control de versiones por `.gitignore`
- Nunca compartas tu archivo `config/config.yaml`
- Usa `config/config_template.yaml` como plantilla

## 📊 Formatos de Archivo Soportados

- **Excel (.xlsx, .xls)**: Hojas de cálculo de Microsoft Excel
- **CSV**: Archivos de valores separados por comas

## 🤖 Funcionalidades de IA

El sistema soporta múltiples proveedores de IA:

**Azure OpenAI (GPT-4o):**
1. **Análisis de Datos**: Genera resúmenes ejecutivos y insights clave
2. **Sugerencias de Decisión**: Proporciona recomendaciones accionables
3. **Respuestas a Preguntas**: Responde preguntas específicas sobre los datos
4. **Sugerencias de Visualización**: Recomienda los mejores gráficos para tus datos

**Google AI Studio (Gemini):**
1. **Análisis de Datos**: Genera resúmenes ejecutivos y insights clave
2. **Sugerencias de Decisión**: Proporciona recomendaciones accionables
3. **Respuestas a Preguntas**: Responde preguntas específicas sobre los datos
4. **Sugerencias de Visualización**: Recomienda los mejores gráficos para tus datos

Puedes cambiar entre proveedores desde la sidebar de la aplicación.

## 📈 Tipos de Visualizaciones

- Histogramas
- Gráficos de barras
- Gráficos de líneas
- Gráficos circulares (pie charts)
- Diagramas de dispersión
- Mapas de calor de correlación

## 🐛 Solución de Problemas

### Error: "No se encontró config.yaml"
- Asegúrate de copiar `config_template.yaml` a `config.yaml`
- Completa tus credenciales en el archivo copiado

### Error: "No se han configurado las credenciales"
- Verifica que `config/config.yaml` tenga tu API key y endpoint
- Asegúrate de que el archivo YAML esté bien formateado

### Error al cargar archivo
- Verifica que el archivo sea Excel o CSV
- Asegúrate de que el archivo no esté corrupto
- Verifica que el archivo no esté abierto en otro programa

## 📝 Notas

- Los archivos subidos se guardan temporalmente en la carpeta `data/`
- La carpeta `data/` está en `.gitignore` para no comprometer datos de usuarios
- La aplicación se ejecuta localmente en tu máquina

## 🤝 Contribuciones

Este es un proyecto para uso personal/educativo. Si deseas mejorarlo, siéntete libre de hacerlo.

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal.

## 👤 Autor

Creado para análisis de datos y toma de decisiones asistida por IA.
