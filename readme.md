# Agents (Weather,...)

A fully local, voice-activated AI agent system starting with weather, growing over time. No cloud AI subscriptions, no ongoing API costs. Say "Hey Jarvis," ask for a city, and get a natural-sounding spoken weather report generated entirely on your own machine.

This is agent #1 of a larger system Robby and Ani are building from scratch as a hands-on learning project. The plan is for this to grow into a real multi-agent setup more specialized agents (news, finance, and others) are coming, all sharing the same local infrastructure this weather agent already runs on.

## What it does

Say "Hey Jarvis" and the agent starts listening. Tell it a city, either by voice or by typing, and it fetches live weather data, hands it to a locally run AI model to write up a natural, enthusiastic report, and reads it back to you out loud.

A few things worth knowing about how it behaves: if you ask about somewhere ambiguous like "Springfield," it checks population data first, if one match is clearly the most likely (like Tokyo), it just goes with that instead of asking. If it's a genuine toss-up between similarly-sized cities, it'll ask you to pick, and you can answer that by voice too. If the microphone ever struggles to understand you after a few tries, it falls back to letting you type instead, since voice input isn't accessible to everyone.

The AI narration runs through Ollama using `llama3.2`, entirely offline, with a prompt that's been tuned over several rounds to sound like an actual person talking rather than a script being read aloud. The voice itself uses `edge-tts`, which sounds noticeably more natural than typical robotic text-to-speech.

Once it finishes giving you a report, it goes right back to listening for the wake word it's meant to run continuously in the background, not be started fresh each time.

## Folder structure

```
weather_Agent/
├── fetcher.py              # Entry point — wake word listener, hands off to agents
├── speech.py                 # Text-to-speech (shared across future agents)
├── listener.py                 # Speech-to-text (shared across future agents)
├── .gitignore
├── README.md
├── .env                          # Local secrets, not committed
└── agents/
    ├── __init__.py                # Marks this as a Python package
    └── weather_agent.py            # Weather logic, wrapped in a run() function
```

`speech.py` and `listener.py` sit outside the `agents/` folder on purpose — they're shared tools, not specific to weather. As new agents get added, each one gets its own file inside `agents/`, but they'll all reuse this same voice input/output plumbing rather than duplicating it.

## Tech stack

| Purpose | Tool | Why |
|---|---|---|
| Local LLM | [Ollama](https://ollama.com) + `llama3.2` | Free, offline, no API costs |
| Weather + geocoding data | [Open-Meteo](https://open-meteo.com/) | Free, no API key required |
| Wake word detection | `openWakeWord` | Fully open-source, no account needed |
| Voice output | `edge-tts` | Free, near-human-quality neural voice |
| Voice input | Google Speech Recognition (via `SpeechRecognition`) | Free, accurate, no key |
| Mic recording | `sounddevice` + `scipy` | Chosen over `pyaudio` to avoid a C++ compiler dependency |

## Setup

1. Install [Ollama](https://ollama.com), then pull the model:
   ```
   ollama pull llama3.2
   ```
2. Clone this repo, then create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```
   pip install requests edge-tts sounddevice scipy SpeechRecognition openwakeword python-dotenv
   ```
4. Download the wake word models (one-time):
   ```python
   python
   >>> import openwakeword
   >>> openwakeword.utils.download_models()
   >>> exit()
   ```
5. Run it:
   ```
   python fetcher.py
   ```
6. Say "Hey Jarvis," then say or type a city name.

## What's next

The weather agent works end to end, but it's still just one agent answering to a wake word that isn't even its final name yet. Next up: training a custom "Hey Lisa" wake word, adding a second agent so there's actually something to route between, and building the routing logic itself so the system can tell what you're asking for and hand it to the right agent. Further out, there's a desktop GUI planned instead of the terminal, and eventually a senior orchestrator agent sitting on top of all the specialized ones.

## Built by

Robby Deffo  & Ani harutyunyan — learning AI development hands-on, one bug at a time. Follow along as this grows from one agent into a full system.