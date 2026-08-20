import sounddevice as sd
from openwakeword.model import Model
from speech import speak
from agents.weather_agent import run as run_weather_agent

wake_model = Model(wakeword_models=["hey_jarvis"])
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280

print("Weather agent is now running. Say 'Hey Jarvis' anytime.")

while True:
    detected = False

    def wake_callback(indata, frames, time_info, status):
        global detected
        audio = indata[:, 0]
        prediction = wake_model.predict(audio)
        if prediction["hey_jarvis"] > 0.5:
            detected = True

    with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, blocksize=CHUNK_SIZE, dtype='int16', callback=wake_callback):
        while not detected:
            sd.sleep(100)

    print("Wake word heard!")
    speak("Yes? What city?")

    run_weather_agent()

    print("\nDone! Listening for 'Hey Jarvis' again...\n")