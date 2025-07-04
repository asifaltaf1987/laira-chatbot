import tempfile
from gtts import gTTS
import os
import platform

def recognize_speech():
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎙️ Listening... Please speak.")
            audio = r.listen(source)
        query = r.recognize_google(audio)
        return query
    except Exception as e:
        st.warning("⚠️ Voice input is not available in this environment.")
        return ""

def text_to_speech(text):
    try:
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)

        # Optionally play the audio without showing it (not in Streamlit)
        if platform.system() != "Linux":
            # Optional: use local player when run outside Codespaces
            import playsound
            playsound.playsound(temp_path)

        os.remove(temp_path)
    except Exception as e:
        print("TTS error:", e)