import sounddevice as sd
import time
from openwakeword.model import Model

model = Model(wakeword_models=["hey_jarvis"])

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280

last_detection_time = 0
COOLDOWN_SECONDS = 2

print("Listening for 'Hey Jarvis'... (press Ctrl+C to stop)")

def callback(indata, frames, time_info, status):
    global last_detection_time
    audio = indata[:, 0]
    prediction = model.predict(audio)
    score = prediction["hey_jarvis"]

    if score > 0.5:
        now = time.time()
        if now - last_detection_time > COOLDOWN_SECONDS:
            print(f"Wake word detected! (confidence: {score:.2f})")
            last_detection_time = now

with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, blocksize=CHUNK_SIZE, dtype='int16', callback=callback):
    while True:
        sd.sleep(100)