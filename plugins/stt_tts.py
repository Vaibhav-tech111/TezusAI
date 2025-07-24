# plugins/stt_tts.py

import speech_recognition as sr
import pyttsx3

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def listen() -> str:
    """
    Listens to microphone input and returns transcribed text.
    """
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError as e:
        return f"STT error: {e}"

def speak(text: str):
    """
    Converts text to speech and plays it.
    """
    print(f"🧠 Tezus says: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()
