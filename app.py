"""
Aplicación principal de Streamlit para Dashboard de Toma de Decisiones
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_processor import DataProcessor
from src.ai_service import AzureOpenAIService
from src.google_ai_service import GoogleAIService
from src.decision_engine import DecisionEngine
from src.dashboard import Dashboard


# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Toma de Decisiones",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título de la aplicación
st.title("📊 Dashboard de Toma de Decisiones con IA")
st.markdown("---")

# Sidebar para configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Verificar si existe config.yaml
    config_exists = os.path.exists("config/config.yaml")
    
    if not config_exists:
        st.warning("⚠️ No se encontró config.yaml")
        st.info("Por favor copia config/config_template.yaml a config/config.yaml y completa tus credenciales")
        st.stop()
    
    # Selector de proveedor de IA
    st.subheader("🤖 Proveedor de IA")
    ai_provider = st.selectbox(
        "Selecciona el proveedor de IA:",
        ["Azure OpenAI", "Google AI Studio (Gemini)"],
        index=0
    )
    
    # Inicializar servicios
    try:
        azure_service = AzureOpenAIService()
        google_service = GoogleAIService()
        
        # Determinar qué servicio usar basado en la selección
        if ai_provider == "Azure OpenAI":
            decision_engine = DecisionEngine(azure_service=azure_service)
        else:
            decision_engine = DecisionEngine(google_service=google_service)
        
        dashboard = Dashboard()
        st.success(f"✅ Servicios inicializados correctamente ({ai_provider})")
    except Exception as e:
        st.error(f"❌ Error al inicializar servicios: {str(e)}")
        st.stop()
    
    st.markdown("---")
    st.header("📁 Cargar Datos")
    
    # Upload de archivo
    uploaded_file = st.file_uploader(
        "Sube tu archivo de datos",
        type=['xlsx', 'xls', 'csv'],
        help="Formatos soportados: Excel (.xlsx, .xls) y CSV"
    )
    
    st.markdown("---")
    st.markdown("### 📖 Instrucciones")
    st.markdown("""
    1. Carga un archivo Excel o CSV
    2. Explora los datos en la pestaña 'Datos'
    3. Genera análisis con IA en la pestaña 'Análisis IA'
    4. Haz preguntas específicas en la pestaña 'Preguntar'
    5. Visualiza los datos en la pestaña 'Visualizaciones'
    6. Genera un reporte automático en la pestaña 'Reporte Automático'
    """)

# Estado de la sesión
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'current_file' not in st.session_state:
    st.session_state.current_file = None

# Procesar archivo cargado
if uploaded_file is not None:
    # Guardar archivo temporalmente
    temp_dir = "data"
    os.makedirs(temp_dir, exist_ok=True)
    
    file_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Cargar datos
    with st.spinner("Cargando y analizando datos..."):
        result = decision_engine.load_data(file_path)
        
        if result['success']:
            st.session_state.data_loaded = True
            st.session_state.current_file = uploaded_file.name
            st.success(f"✅ Archivo '{uploaded_file.name}' cargado exitosamente")
        else:
            st.error(f"❌ Error al cargar archivo: {result['error']}")
            st.session_state.data_loaded = False

# Mostrar contenido principal si hay datos cargados
if st.session_state.data_loaded:
    # Pestañas de navegación
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Datos", "🤖 Análisis IA", "❓ Preguntar", "📈 Visualizaciones", "📋 Reporte Automático"])
    
    with tab1:
        st.header("Exploración de Datos")
        
        # Obtener vista general
        overview = decision_engine.get_data_overview()
        
        if overview['success']:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                dashboard.display_data_info(overview['info'])
            
            with col2:
                dashboard.display_sample_data(decision_engine.data_processor.data)
            
            st.markdown("---")
            
            col3, col4 = st.columns(2)
            
            with col3:
                dashboard.display_summary_statistics(overview['summary_stats'])
            
            with col4:
                dashboard.display_categorical_summary(overview['categorical_summary'])
            
            st.markdown("---")
            dashboard.display_questions_detected(overview['questions_detected'])
    
    with tab2:
        st.header("Análisis con IA para Toma de Decisiones")
        
        st.info("🤖 La IA analizará tus datos y generará sugerencias específicas para la toma de decisiones.")
        
        if st.button("🚀 Generar Análisis", type="primary"):
            with st.spinner("Generando análisis con IA..."):
                result = decision_engine.generate_decision_analysis()
                
                if result['success']:
                    dashboard.display_ai_analysis(result['analysis']['ai_analysis'])
                else:
                    st.error(f"❌ Error: {result['error']}")
        
        # También mostrar sugerencias de visualizaciones
        st.markdown("---")
        st.subheader("💡 Sugerencias de Visualizaciones")
        
        if st.button("📊 Obtener Sugerencias de Visualizaciones"):
            with st.spinner("Generando sugerencias..."):
                result = decision_engine.get_visualization_suggestions()
                
                if result['success']:
                    st.markdown(result['suggestions'])
                else:
                    st.error(f"❌ Error: {result['error']}")
    
    with tab3:
        st.header("Preguntar a la IA sobre tus Datos")
        
        st.info("❓ Haz preguntas específicas sobre tus datos y obtén respuestas basadas en la información del archivo.")
        
        question = st.text_input(
            "Escribe tu pregunta:",
            placeholder="Ejemplo: ¿Cuál es el promedio de ventas por región?",
            key="question_input"
        )
        
        if st.button("🔍 Enviar Pregunta", type="primary"):
            if question:
                with st.spinner("Procesando pregunta..."):
                    result = decision_engine.ask_question(question)
                    
                    if result['success']:
                        st.subheader("Respuesta:")
                        st.markdown(result['answer'])
                    else:
                        st.error(f"❌ Error: {result['error']}")
            else:
                st.warning("⚠️ Por favor escribe una pregunta")
        
        # Preguntas sugeridas
        st.markdown("---")
        st.subheader("💡 Preguntas Sugeridas")
        
        overview = decision_engine.get_data_overview()
        if overview['success']:
            questions_detected = overview['questions_detected']
            
            if questions_detected:
                for q in questions_detected:
                    if st.button(f"¿{q}?", key=f"suggested_{q}"):
                        with st.spinner("Procesando pregunta..."):
                            result = decision_engine.ask_question(f"¿Qué puedes decirme sobre {q}?")
                            if result['success']:
                                st.markdown(result['answer'])
                            else:
                                st.error(f"❌ Error: {result['error']}")
    
    with tab4:
        st.header("Visualizaciones Interactivas")
        
        df = decision_engine.data_processor.data
        
        # Selección de tipo de gráfico
        chart_type = st.selectbox(
            "Selecciona el tipo de visualización:",
            ["Histograma", "Gráfico de Barras", "Gráfico de Líneas", "Gráfico Circular", "Diagrama de Dispersión", "Mapa de Calor de Correlación"]
        )
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if chart_type == "Histograma":
            if numeric_cols:
                col = st.selectbox("Selecciona columna numérica:", numeric_cols)
                dashboard.create_histogram(df, col)
            else:
                st.warning("No hay columnas numéricas disponibles")
        
        elif chart_type == "Gráfico de Barras":
            if categorical_cols and numeric_cols:
                x_col = st.selectbox("Columna categórica (eje X):", categorical_cols)
                y_col = st.selectbox("Columna numérica (eje Y):", numeric_cols)
                dashboard.create_bar_chart(df, x_col, y_col, f"{y_col} por {x_col}")
            else:
                st.warning("Se necesita al menos una columna categórica y una numérica")
        
        elif chart_type == "Gráfico de Líneas":
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("Columna para eje X:", numeric_cols)
                y_col = st.selectbox("Columna para eje Y:", numeric_cols)
                dashboard.create_line_chart(df, x_col, y_col, f"{y_col} vs {x_col}")
            else:
                st.warning("Se necesitan al menos 2 columnas numéricas")
        
        elif chart_type == "Gráfico Circular":
            if categorical_cols:
                col = st.selectbox("Selecciona columna categórica:", categorical_cols)
                dashboard.create_pie_chart(df, col, f"Distribución de {col}")
            else:
                st.warning("No hay columnas categóricas disponibles")
        
        elif chart_type == "Diagrama de Dispersión":
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("Columna para eje X:", numeric_cols)
                y_col = st.selectbox("Columna para eje Y:", numeric_cols)
                color_col = st.selectbox("Columna para color (opcional):", ["Ninguna"] + categorical_cols + numeric_cols)
                color_col = None if color_col == "Ninguna" else color_col
                dashboard.create_scatter_plot(df, x_col, y_col, color_col)
            else:
                st.warning("Se necesitan al menos 2 columnas numéricas")
        
        elif chart_type == "Mapa de Calor de Correlación":
            dashboard.create_correlation_heatmap(df)
    
    with tab5:
        st.header("📋 Reporte Automático")
        
        st.info("🚀 Presiona el botón para generar un reporte automático con gráficos interesantes basados en tus datos.")
        
        if st.button("🎯 Generar Reporte Automático", type="primary"):
            with st.spinner("Generando reporte automático..."):
                df = decision_engine.data_processor.data
                dashboard.generate_auto_report(df)

else:
    # Mensaje cuando no hay datos cargados
    st.info("👆 Por favor carga un archivo de datos desde la sidebar para comenzar.")
    
    # Mostrar ejemplo de uso
    st.markdown("---")
    st.header("📖 Ejemplo de Uso")
    st.markdown("""
    ### Formatos de Archivo Soportados:
    - **Excel (.xlsx, .xls)**: Hojas de cálculo de Microsoft Excel
    - **CSV**: Archivos de valores separados por comas
    
    ### Características:
    - 🤊 Análisis automático de datos
    - 🤖 Sugerencias de IA para toma de decisiones
    - ❓ Preguntas específicas sobre tus datos
    - 📈 Visualizaciones interactivas
    - 📊 Estadísticas descriptivas automáticas
    """)
