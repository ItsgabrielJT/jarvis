import os
import webbrowser
import speech_recognition as sr
from voice_engine import speak
from config import VS_CODE_APP_NAME, YOUTUBE_ACDC_URL

def open_vscode():
    """Ejecuta un comando del sistema para abrir VS Code en macOS."""
    os.system(f"open -a '{VS_CODE_APP_NAME}'")

def play_acdc():
    """Abre el navegador por defecto con la búsqueda de AC/DC."""
    webbrowser.open(YOUTUBE_ACDC_URL)

def execute_special_action():
    """Acción que se dispara al escuchar el doble aplauso."""
    open_vscode()
    play_acdc()

def listen_and_execute():
    """Captura el audio del micrófono, usa SpeechRecognition y despacha acciones."""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        speak("¿Qué deseas ordenar?")
        
        # Ajusta el ruido de fondo rápido
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("\n[Escuchando sub-comando por 5 segundos...]")
        
        try:
            # Espera audio con un timeout
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            # Reconocimiento usando Google (requiere internet, es gratuito)
            print("[Procesando audio...]")
            command = recognizer.recognize_google(audio, language="es-ES").lower()
            print(f"-> Comando capturado: '{command}'")
            
            # Parsing de comandos
            if "google" in command:
                speak("Abriendo Google en tu navegador.")
                webbrowser.open("https://www.google.com")
            
            elif "hora" in command or "tiempo" in command:
                import datetime
                now = datetime.datetime.now().strftime("%H:%M")
                speak(f"La hora actual es {now}.")
                
            elif "broma" in command or "chiste" in command:
                speak("¿Por qué los programadores prefieren el modo oscuro? Porque la luz atrae a los bugs.")
                
            elif "reiniciar" in command or "actualizar" in command or "reinicia" in command:
                import sys
                speak("Aplicando actualizaciones y reiniciando sistemas.")
                print("[Reiniciando proceso...]")
                os.execv(sys.executable, [sys.executable] + sys.argv)
                
            elif "apagar" in command or "detener" in command or "salir" in command or "apágate" in command:
                import sys
                speak("Apagando sistemas por completo. Hasta la próxima.")
                print("[Apagando proceso...]")
                sys.exit(0)
                
            else:
                speak("Aún no he sido programado para ese comando.")
                
        except sr.WaitTimeoutError:
            print("[Ningún comando de voz detectado]")
            speak("No detecté ninguna orden. Regresando a espera.")
        except sr.UnknownValueError:
            print("[No se entendió el audio]")
            speak("No pude entender el sonido, lo siento.")
        except sr.RequestError as e:
            print(f"[Error de conexión con servicio de Google: {e}]")
            speak("Error en la conexión con el servidor de reconocimiento de voz.")
