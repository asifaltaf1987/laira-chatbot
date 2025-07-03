import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import tempfile
import os

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        return query
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand your speech."
    except sr.RequestError:
        return "Speech recognition service is unavailable."

def text_to_speech(text):
    try:
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)
        playsound(temp_path)
        os.remove(temp_path)
    except Exception as e:
        print("TTS error:", e)
