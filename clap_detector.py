import pyaudio
import struct
import math
import time
from config import CLAP_THRESHOLD, MAX_TIME_BETWEEN_CLAPS, MIN_TIME_BETWEEN_CLAPS, CHUNK_SIZE, RATE

def get_rms(block):
    """Calcula el RMS (Root Mean Square) del bloque de audio para medir la amplitud."""
    count = len(block) / 2
    if count == 0:
        return 0
    format_str = "%dh" % count
    try:
        shorts = struct.unpack(format_str, block)
    except struct.error:
        # En caso de que el tamaño del buffer no coincida, omitimos
        return 0

    sum_squares = 0.0
    for sample in shorts:
        # Normalizar el valor
        n = sample * (1.0 / 32768.0)
        sum_squares += n * n
    return math.sqrt(sum_squares / count) * 1000  # Multiplicamos para que sea más fácil leer (ej. 10 a 1000)

def detect_double_clap(callback):
    """Bucle infinito que captura audio mediante pyaudio y reporta un doble aplauso."""
    p = pyaudio.PyAudio()
    
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE)
    except Exception as e:
        print(f"Error al abrir el micrófono: {e}")
        print("Asegúrate de que tienes 'portaudio' instalado (brew install portaudio) y diste permisos.")
        return

    claps = 0
    last_clap_time = 0
    
    try:
        while True:
            try:
                # Leer stream (non-blocking para evitar overflow crashes si es posible)
                data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            except IOError:
                continue
            
            amplitude = get_rms(data)
            
            # --- DEBUGGING: Te ayuda a ver si el micro está captando ---
            if 50 < amplitude < CLAP_THRESHOLD:
                # print(f"[DEBUG] Ruido detectado: {amplitude:.1f} (Umbral actual para aplauso: {CLAP_THRESHOLD})")
                # Lo imprimo con carriage return para no inundar la pantalla
                print(f"\r[DEBUG] Volumen actual: {amplitude:.1f} / Umbral: {CLAP_THRESHOLD}   ", end="")

            # Comparamos si el volumen actual es un ruido fuerte (un posible aplauso)
            if amplitude > CLAP_THRESHOLD:
                current_time = time.time()
                time_since_last_clap = current_time - last_clap_time
                
                # Prevenir doble-conteo por el "eco" del mismo aplauso muy rápido
                if time_since_last_clap > MIN_TIME_BETWEEN_CLAPS:
                    
                    if time_since_last_clap <= MAX_TIME_BETWEEN_CLAPS:
                        # ¡Segundo aplauso detectado en el rango de tiempo correcto!
                        claps += 1
                        print(f"[*] ¡Segundo aplauso detectado! (Volumen: {amplitude:.1f})")
                        
                        # Ejecutar acción
                        callback()
                        
                        # Reset
                        claps = 0
                        last_clap_time = time.time()
                        
                        # Pequeño cooldown para que no siga captando aplausos inmediatamente
                        time.sleep(1)
                        
                    else:
                        # Si pasó demasiado tiempo desde el último aplauso, iniciamos la cuenta de nuevo
                        claps = 1
                        print(f"[*] Primer aplauso detectado! (Volumen: {amplitude:.1f})")
                
                last_clap_time = current_time

    except KeyboardInterrupt:
        print("\nSaliendo de la detección de aplausos...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
