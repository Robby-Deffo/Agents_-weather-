import asyncio
import os
import edge_tts
from playsound import playsound

VOICE = "en-US-AriaNeural"

async def _generate_audio(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save("report.mp3")

def speak(text):
    asyncio.run(_generate_audio(text))
    playsound("report.mp3")
    os.remove("report.mp3")