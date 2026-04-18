import os
import sys
import webbrowser
import speech_recognition as sr
from voice_engine import speak
from config import VS_CODE_APP_NAME, YOUTUBE_ACDC_URL, LM_STUDIO_URL, AI_SYSTEM_PROMPT, INTERACTIVE_TIMEOUT
from openai import OpenAI

# Inicializar cliente de OpenAI apuntando al servidor local
try:
    openai_client = OpenAI(base_url=LM_STUDIO_URL, api_key="lm-studio", timeout=30.0)
except Exception as e:
    print(f"[Aviso] No se pudo inicializar OpenAI client: {e}")
    openai_client = None

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

def pause_media():
    """Intenta pausar la reproducción en aplicaciones y navegadores (Chrome/Safari/Spotify/Music)."""
    # Apple Music y Spotify
    os.system("osascript -e 'tell application \"Music\" to pause' 2>/dev/null")
    os.system("osascript -e 'tell application \"Spotify\" to pause' 2>/dev/null")
    
    # Navegadores
    os.system("osascript -e 'tell application \"Google Chrome\" to execute javascript \"document.querySelectorAll(\\\"video, audio\\\").forEach(v => v.pause())\" in active tab of first window' 2>/dev/null")
    os.system("osascript -e 'tell application \"Safari\" to do JavaScript \"document.querySelectorAll(\\\"video, audio\\\").forEach(v => v.pause())\" in document 1' 2>/dev/null")


import re

def process_ai_response(response_text):
    """Procesa la respuesta de la IA, extrae comandos y habla el texto limpio."""
    text_to_speak = response_text
    
    # Extraer estrictamente el texto DESPUÉS de ===RESPUESTA_FINAL===
    if "===RESPUESTA_FINAL===" in text_to_speak:
        parts = text_to_speak.split("===RESPUESTA_FINAL===")
        if len(parts) > 1:
            text_to_speak = parts[-1].strip()
        else:
            text_to_speak = ""
    else:
        # Fallback si olvida el separador y solo imprime Thinking Process (truncamiento)
        if "Thinking Process:" in text_to_speak:
            text_to_speak = ""
        elif "<think>" in text_to_speak:
            text_to_speak = re.sub(r'<think>.*?</think>', '', text_to_speak, flags=re.DOTALL)
                
    # Limpiar asteriscos y formato markdown residual
    text_to_speak = text_to_speak.replace('*', '').strip()
    
    # Evaluar acciones
    if "[ACTION:OPEN_VSCODE]" in response_text:
        text_to_speak = text_to_speak.replace("[ACTION:OPEN_VSCODE]", "").strip()
        open_vscode()
        
    if "[ACTION:PLAY_ACDC]" in response_text:
        text_to_speak = text_to_speak.replace("[ACTION:PLAY_ACDC]", "").strip()
        play_acdc()
        
    if "[ACTION:PAUSE_MEDIA]" in response_text:
        text_to_speak = text_to_speak.replace("[ACTION:PAUSE_MEDIA]", "").strip()
        pause_media()
        
    if "[ACTION:SEARCH_GOOGLE]" in response_text:
        text_to_speak = text_to_speak.replace("[ACTION:SEARCH_GOOGLE]", "").strip()
        webbrowser.open("https://www.google.com")
        
    if "[ACTION:RESTART]" in response_text:
        text_to_speak = text_to_speak.replace("[ACTION:RESTART]", "").strip()
        speak(text_to_speak)
        print("[Reiniciando proceso...]")
        os.execv(sys.executable, [sys.executable] + sys.argv)
        
    if "[ACTION:SHUTDOWN]" in response_text:
        text_to_speak = text_to_speak.replace("[ACTION:SHUTDOWN]", "").strip()
        speak(text_to_speak)
        print("[Apagando proceso...]")
        sys.exit(0)
        
    # Hablar el resto del texto
    if text_to_speak:
        speak(text_to_speak)

def listen_and_execute():
    """Captura el audio del micrófono, usa SpeechRecognition y consulta a la IA local."""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        speak("¿En qué te puedo ayudar, señor? Estaré pendiente a tus órdenes.")
        
        # Configuración avanzada para el micrófono
        recognizer.dynamic_energy_threshold = True
        recognizer.dynamic_energy_ratio = 1.5  # Bajamos el ratio para no requerir tanta fuerza
        
        # AUMENTAMOS EL TIEMPO DE PAUSA PARA ORACIONES LARGAS
        recognizer.pause_threshold = 3.0  # Cuánto tiempo de silencio se necesita para considerar terminada la frase
        recognizer.non_speaking_duration = 2.5 # Cuánto silencio "puro" antes de apagar
        
        recognizer.adjust_for_ambient_noise(source, duration=1.5)
        
        while True:
            print(f"\n[Escuchando... El modo interactivo se apagará tras {INTERACTIVE_TIMEOUT//60} minutos de silencio]")
            
            try:
                # Quitamos phrase_time_limit para que no te corte si te extiendes hablando mucho
                audio = recognizer.listen(source, timeout=INTERACTIVE_TIMEOUT, phrase_time_limit=None)
                
                print("[Procesando audio (Speech to Text)...]")
                command_text = recognizer.recognize_google(audio, language="es-ES").lower()
                print(f"-> Has dicho: '{command_text}'")
                
                # Despertador por palabra clave
                if "jarvis" not in command_text:
                    print("[Wake word 'Jarvis' no detectada. Ignorando...]")
                    continue
                    
                # Ejecución RÁPIDA de comandos conocidos sin usar la IA
                if "abre google" in command_text or "busca en google" in command_text:
                    speak("Abriendo Google.")
                    webbrowser.open("https://www.google.com")
                    continue
                elif "pausa" in command_text or "detén la música" in command_text or "silencio" in command_text:
                    speak("Pausando el audio.")
                    pause_media()
                    continue
                elif "visual studio" in command_text or "editor" in command_text or "código" in command_text:
                    speak("Abriendo entorno de desarrollo.")
                    open_vscode()
                    continue
                elif ("música" in command_text or "ac/dc" in command_text) and "pon" in command_text:
                    speak("Reproduciendo AC/DC.")
                    play_acdc()
                    continue
                elif "reiniciar" in command_text or "actualizar" in command_text:
                    speak("Reiniciando sistemas...")
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                elif "apagar" in command_text or "detener" in command_text or "salir" in command_text:
                    speak("Apagando Jarvis. Hasta luego.")
                    sys.exit(0)
                
                # Si no es un comando rápido conocido, pasarle la pregunta/prompt a la IA local
                if openai_client:
                    print("[Consultando a la IA local (LM Studio)...]")
                    user_command_with_rule = command_text + "\n(Recuerda tu separador ===RESPUESTA_FINAL===)"
                    
                    completion = openai_client.chat.completions.create(
                        model="local-model",
                        messages=[
                            {"role": "system", "content": AI_SYSTEM_PROMPT},
                            {"role": "user", "content": user_command_with_rule}
                        ],
                        temperature=0.7,
                        max_tokens=1500
                    )
                    
                    ai_response = completion.choices[0].message.content
                    print(f"\n[Jarvis AI RAW OUTPUT] ->\n{ai_response}\n")
                    
                    if not ai_response.strip():
                        speak("Error interno en la generación del modelo.")
                    else:
                        process_ai_response(ai_response)
                        
                else:
                    speak("El cliente de inteligencia artificial no está inicializado.")
                    
            except sr.WaitTimeoutError:
                print(f"[{INTERACTIVE_TIMEOUT//60} minutos sin comandos detectados]")
                speak("Como no hay más órdenes, regresaré a mi modo de espera.")
                break
            except sr.UnknownValueError:
                print("[No se entendió el audio, siguiendo a la espera...]")
                pass
            except sr.RequestError as e:
                print(f"[Error de conexión en reconocimiento de voz: {e}]")
                speak("Error en la conexión con el servidor de reconocimiento de voz. Regresando a espera.")
                break
            except Exception as e:
                print(f"[Error de la IA o sistema: {e}]")
                speak("Ocurrió un error al procesar tu solicitud.")
                pass
