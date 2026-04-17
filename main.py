from clap_detector import detect_double_clap
from commands import execute_special_action, listen_and_execute
from voice_engine import speak

def on_double_clap():
    """
    Función que responde al evento de doble aplauso detectado.
    1. Jarvis da la bienvenida.
    2. Ejecuta la macro (Abre VS Code y pone música en YouTube).
    3. Habilita el reconocimiento de voz para comandos extra (opcional).
    """
    print("\n" + "="*40)
    print(" >>> EVENTO: DOBLE APLAUSO ACTIVADO <<<")
    print("="*40)
    
    speak("Iniciando tu entorno de trabajo.")
    
    # 1 y 2: Visual Studio Code + YouTube AC/DC
    execute_special_action()
    
    # 3: Modo interactivo por voz, tras abrir las apps
    # Descomenta la siguiente línea si deseas que después de abrir 
    # VS Code se quede escuchando (ej. "dime la hora").
    listen_and_execute()
    
    print("\n[Regresando al modo silencioso... Esperando doble aplauso para ejecutar de nuevo.]")

if __name__ == "__main__":
    print("="*40)
    print("      SISTEMA JARVIS INICIADO")
    print("="*40)
    
    # Saludo inicial
    speak("Sistemas en línea. Esperando comando de doble palmada.")
    print("\nDa 2 aplausos a una distancia prudente del micrófono (intervalo ~0.5 a 1 segundo).")
    
    try:
        # Inicia loop continuo analizando el micrófono
        detect_double_clap(callback=on_double_clap)
    except KeyboardInterrupt:
        print("\nSistema apagado por el usuario.")
        speak("Apagando sistemas... Hasta luego.")
