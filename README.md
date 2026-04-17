# Jarvis Voice Assistant

Un asistente de voz rápido y local para macOS, escrito en Python. El sistema se queda monitoreando el entorno esperando un **doble aplauso**, que ejecuta una acción personalizada de manera instantánea y luego abre la escucha para comandos de voz.

## Función Especial (El "Doble Aplauso")
Cuando aplaudes dos veces frente al micrófono (con ~0.5s a 1s de diferencia):
1. **Jarvis dice:** *"Iniciando tu entorno de trabajo"* (Utiliza `pyttsx3` que funciona 100% offline).
2. **Sistema:** Se abre automáticamente Visual Studio Code (`open -a`).
3. **Navegador:** Se redirige y reproduce música (AC/DC - Back in Black en YouTube).
4. **Voz Activa:** Se abre un modo de escucha que puedes utilizar para consultar la hora, pedir un chiste, o abrir google antes de regresar nuevamente a dormir en espera de otro aplauso.

---

## 💻 Requerimientos del Sistema e Instalación en macOS

Para la funcionalidad del micrófono y reconocimiento de voz requieres ciertas librerías del sistema antes de instalar las dependencias de Python.

### 1. Requerimientos del Sistema (`portaudio`)

La librería `pyaudio` lo necesita para acceder al hardware del micrófono limpio.

Abre tu terminal e instala:
```bash
brew install portaudio
```
*(Asumiendo que tienes [Homebrew](https://brew.sh/es/) instalado)*

### 2. Dependencias de Python

Se recomienda crear un entorno virtual, pero puedes instalar directamente a nivel proyecto:

```bash
pip install -r requirements.txt
```

#### Notas sobre dependencias:
- **`SpeechRecognition`**: Se encargará de parsear el audio y enviarlo a reconocimiento (Google Speech AI gratuito sin credenciales).
- **`pyaudio`**: Maneja el buffer de audio en tiempo real para encontrar el ruido del aplauso.
- **`pyttsx3`**: Sintetizador de Text-To-Speech integrado (Siri en el caso de Mac).

---

## 🚀 Uso

Inicia el orquestador principal:

```bash
python main.py
```

1. **Permiso de Micrófono:** La primera vez que el script corra, **macOS lanzará una ventana de seguridad** preguntando "Terminal / Python desea acceder al micrófono". Haz clic en **OK / Permitir**. 
*(Si no te salta o la negaste por error, ve a `System Settings > Privacy & Security > Microphone` y habilita el terminal que uses)*.
2. Da **2 aplausos seguidos**. Verás en la terminal `[*] Primer aplauso detectado!` y el segundo. 
   - *Nota: Dependiendo del micrófono integrado de tu Mac o tus auriculares, podrías necesitar aplaudir fuerte. Si es demasiado insensible o super sensible a otros ruidos, edita `CLAP_THRESHOLD` dentro del archivo `config.py`.*
3. Jarvis hablará y cargará VS Code + YouTube. Luego dirá "¿Qué deseas ordenar?". En ese instante puedes decir en voz alta (ej. *"Qué hora es"* o *"Cuéntame un chiste"*). 
4. Si pasan 5 segundos sin audio claro, cerrará la sesión de voz y volverá al loop infinito de los aplausos silenciosos.

---

## Estructura de Archivos

- `config.py`: Ajustes de latencia, límites y links.
- `clap_detector.py`: Hilo infinito utilizando PyAudio y cálculos Root Mean Square (RMS) para rastrear "picos" de audio en caliente.
- `voice_engine.py`: Encapsulación del sintetizador de sonido offline.
- `commands.py`: Contiene los macros predefinidos y la lógica de Google Speech.
- `main.py`: Arranque del proyecto (Orquestador principal).

---

## 🤖 Cómo mantener a Jarvis siempre activo (en segundo plano)

Si no quieres abrir la terminal manualmente cada vez que enciendes la computadora, tienes dos excelentes opciones en macOS:

### Método 1: Automator (Inicio automático al encender la Mac)
Este método crea una "aplicación" invisible que MacOS lanza al iniciar sesión.

1. Abre la aplicación **Automator** (búscala en Spotlight).
2. Selecciona crear un nuevo documento y elige **Aplicación**.
3. En el buscador de la izquierda, escribe "Ejecutar un script de shell" (*Run Shell Script*) y arrástralo al panel derecho.
4. Pega el siguiente código (asegúrate de que las rutas coincidan con tu computadora):
   ```bash
   # Asegurar la ruta de python de tu entorno virtual si usas venv
   cd /Users/gabrieltates/Desktop/jarvis
   source .venv/bin/activate
   nohup python main.py > jarvis_log.txt 2>&1 &
   ```
5. Guarda la aplicación con `Cmd + S` (ejemplo, llámala "AutoJarvis" y guárdala en tu carpeta de Aplicaciones).
6. Ve a **Configuración del Sistema > General > Ítems de inicio sesión** (*Login Items*) de macOS.
7. Haz clic en el botón `+` en "Abrir al iniciar sesión" y selecciona tu app "AutoJarvis".

> *Nota: Automator también te pedirá permisos de Micrófono la primera vez que se ejecute en segundo plano.*

### Método 2: Terminal con NoHup (Rápido y temporal)
Si solo quieres cerrar la ventana de la terminal actual pero dejar a Jarvis escuchando todo el día:
1. Abre tu terminal en la carpeta del proyecto y activa el entorno:
   ```bash
   source .venv/bin/activate
   ```
2. Lanza el script desvinculado hacia el fondo (background):
   ```bash
   nohup python main.py > jarvis_log.txt 2>&1 &
   ```
3. Ahora puedes cerrar la ventana de terminal tranquilamente. Los aplausos seguirán funcionando.
4. Para detenerlo, tendrías que buscar el proceso:
   ```bash
   pkill -f "python main.py"
   ```
