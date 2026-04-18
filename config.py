# Configuración de Jarvis

# Parámetros de detección de aplausos
CLAP_THRESHOLD = 150  # Umbral más bajo. Ajusta según los valores [DEBUG] que veas en la terminal.
MAX_TIME_BETWEEN_CLAPS = 1.0  # Máximo tiempo (segundos) entre el primer y segundo aplauso
MIN_TIME_BETWEEN_CLAPS = 0.2  # Mínimo tiempo (segundos) para evitar que el eco del primer aplauso cuente como dos

# Configuración de Audio (PyAudio)
CHUNK_SIZE = 1024
RATE = 44100

# Parámetros de las Acciones
VS_CODE_APP_NAME = "Visual Studio Code"
YOUTUBE_ACDC_URL = "https://www.youtube.com/watch?v=pAgnJDJN4VA&list=RDpAgnJDJN4VA&start_radio=1"

# Configuración de la IA Local (LM Studio)
INTERACTIVE_TIMEOUT = 300  # Segundos de silencio antes de que Jarvis regrese a modo espera (300s = 5m)
LM_STUDIO_URL = "http://127.0.0.1:1234/v1"
AI_SYSTEM_PROMPT = """Eres Jarvis, un asistente de IA de voz eficiente y conversacional.
IMPORTANTE: Debido al tipo de modelo de razonamiento que eres, generarás tu proceso de razonamiento interno primero. Sin embargo, tu única salida verbal (que se enviará al sintetizador de voz) debe ir ÚNICAMENTE y ESTRICTAMENTE debajo de la siguiente cadena exacta: ===RESPUESTA_FINAL===

Estructura estricta que debes seguir para TODA respuesta:
Thinking Process:
(tu análisis y razonamiento interno...)
===RESPUESTA_FINAL===
(Aquí tu respuesta final hablada corta hacia el usuario, sin texto de asteriscos, comillas de markdown, ni ninguna otra estructura)

Mapeo de acciones (Solo incluye las etiquetas de acción en la respuesta final hablada si el usuario pidió alguna de estas acciones):
Abrir código -> [ACTION:OPEN_VSCODE]
Música AC/DC -> [ACTION:PLAY_ACDC]
Pausar audio -> [ACTION:PAUSE_MEDIA]
Buscar Google -> [ACTION:SEARCH_GOOGLE]
Apagarte -> [ACTION:SHUTDOWN]
Reiniciar -> [ACTION:RESTART]
"""
