import subprocess

def speak(text):
    """Hace que el sistema hable el texto proporcionado de forma síncrona."""
    print(f"\n[Jarvis] -> {text}")
    try:
        # Usamos el comando nativo 'say' de macOS para garantizar que hable
        subprocess.run(["say", text], check=False)
    except Exception as e:
        print(f"[Error en síntesis de voz]: {e}")
