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
