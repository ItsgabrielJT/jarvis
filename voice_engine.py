import pyttsx3

def init_engine():
    engine = pyttsx3.init()
    # Establecer la velocidad de habla un poco más rápida/normal
    engine.setProperty('rate', 150)
    
    # Intenta seleccionar una voz en español si está disponible en macOS
    voices = engine.getProperty('voices')
    for voice in voices:
        if "ES" in voice.id or "es_" in voice.id or "spanish" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
            
    return engine

engine = init_engine()

def speak(text):
    """Hace que el sistema hable el texto proporcionado de forma síncrona."""
    print(f"\n[Jarvis] -> {text}")
    engine.say(text)
    engine.runAndWait()
