import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr

def listen():
    duration = 4  # seconds to record
    sample_rate = 44100

    print("Listening... say the city name")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # waits until recording is finished

    write("mic_input.wav", sample_rate, recording)

    recognizer = sr.Recognizer()
    with sr.AudioFile("mic_input.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that. Try typing instead.")
        return None
    except sr.RequestError:
        print("Couldn't reach the speech service — check your internet connection.")
        return None