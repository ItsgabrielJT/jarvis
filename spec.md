# JARVIS Voice Assistant – Specification (spec.md)

## Overview

This project defines a personal voice assistant (“Jarvis”) that runs locally on macOS. It listens for a trigger (double clap), activates voice recognition, and executes commands such as opening applications and playing specific content (e.g., YouTube music).

---

## Objectives

* Build a local voice assistant in Python
* Enable hands-free interaction using voice commands
* Implement a **double-clap trigger** to activate listening mode
* Execute system-level and web-based actions
* Provide audio feedback for a “Jarvis-like” experience

---

## Core Features

### 1. Activation Mechanism

* Detect **double clap sound** via microphone input
* Use audio amplitude thresholds and timing logic
* On detection:

  * Activate assistant
  * Play a confirmation sound or voice response

---

### 2. Voice Recognition

* Capture voice input using:

  * `SpeechRecognition`
* Convert speech to text using:

  * Google Speech API or Whisper (optional)

---

### 3. Command Processing

* Parse recognized text
* Match keywords to predefined actions

Example:

```python
if "open google" in command:
    webbrowser.open("https://www.google.com")
```

---

### 4. Actions Supported

#### Application Launching

* Open Visual Studio Code

```python
os.system("open -a 'Visual Studio Code'")
```

#### Web Navigation

* Open websites
* Play YouTube content

Example:

```python
webbrowser.open("https://www.youtube.com/results?search_query=ACDC+Back+in+Black")
```

---

### 5. Voice Feedback

* Respond using:

  * `pyttsx3` (offline)
  * or `ElevenLabs` (high-quality voice)

Example:

```python
engine.say("Opening Visual Studio Code and playing music")
engine.runAndWait()
```

---

## Special Feature (Your Requirement)

### Double Clap → Execute Action

When user claps twice:

1. Open Visual Studio Code
2. Open YouTube with **AC/DC – Back in Black**

Pseudo-flow:

```python
if detect_double_clap():
    speak("Launching your workspace")
    open_vscode()
    play_acdc()
```

---

## Tools & Technologies

* **Python** → Core language
* **SpeechRecognition** → Voice input
* **PyAudio** → Microphone access
* **pyttsx3 / ElevenLabs** → Voice output
* **webbrowser** → Open URLs
* **os / subprocess** → Launch apps
* **numpy / sounddevice** → Clap detection
* **Optional Enhancements**:

  * OpenAI API → smarter conversations
  * Whisper → better speech accuracy
  * LiveKit → real-time voice agents

---

## System Architecture

```
[Microphone Input]
        ↓
[Clap Detection Module] ----→ (Trigger)
        ↓
[Speech Recognition]
        ↓
[Command Processor]
        ↓
[Action Executor]
        ↓
[Voice Response]
```

---

## Clap Detection Logic

* Continuously listen to microphone input
* Detect spikes in sound amplitude
* If two spikes occur within ~0.5–1 second → trigger

Pseudo-code:

```python
if sound_level > threshold:
    register_clap()

if two_claps_detected_within_timeframe:
    trigger_assistant()
```

---

## File Structure

```
jarvis/
│── main.py
│── clap_detector.py
│── voice_engine.py
│── commands.py
│── utils.py
│── config.py
```

---

## Example Command Set

| Command              | Action                |
| -------------------- | --------------------- |
| "Open Google"        | Launch browser        |
| "Open VS Code"       | Open IDE              |
| "Play Back in Black" | Open YouTube          |
| "What time is it?"   | Speak current time    |
| "Tell me a joke"     | AI-generated response |

---

## Challenges & Considerations

* Background noise affecting clap detection
* Voice recognition accuracy
* macOS app path differences
* Latency in speech processing
* Making responses feel natural

---

## Future Enhancements

* Wake word ("Hey Jarvis")
* Context-aware conversations (LLM integration)
* Smart home integration
* Email/calendar automation
* GUI dashboard
* Personalization (voice, tone, memory)

---

## macOS Notes

* Grant microphone permissions
* Install dependencies:

```bash
brew install portaudio
pip install speechrecognition pyaudio pyttsx3 numpy sounddevice
```

---

## Conclusion

This project is a solid foundation for building a personal AI assistant. Starting with simple commands and triggers (like your **double clap → open VS Code + play AC/DC**) gives immediate, tangible results while leaving room for advanced AI capabilities later.

You don’t need to be Iron Man — but this gets you pretty close.
