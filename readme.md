# 🌤️ Agents (Weather)

A fully local, voice-activated AI agent system — starting with weather, growing over time. No cloud AI subscriptions, no ongoing API costs. Say "Hey Jarvis," ask for a city, and get a natural-sounding spoken weather report generated entirely on your own machine.

This is agent #1 of a larger multi-agent system being built from scratch as a hands-on learning project by Robby and Ani.

## Features

- 🎙️ **Wake word activation** — hands-free, always listening (currently "Hey Jarvis," a custom "Hey Lisa" wake word is planned)
- 🗣️ **Voice input, with a typed fallback** — speak your answer; after 3 failed attempts, it gracefully offers to let you type instead (built with accessibility in mind — voice isn't accessible to everyone)
- 🌍 **Smart city disambiguation** — automatically picks the most likely match by population (e.g. "Tokyo" just works, no menu), and only asks when it's a genuine toss-up between similarly-sized cities — up to 3 options, answerable by voice or typed number
- 🧠 **Local AI narration** — [Ollama](https://ollama.com) running `llama3.2` turns raw weather data into a natural, enthusiastic, occasionally funny spoken report — entirely offline, prompt-tuned over several iterations for genuinely conversational tone
- 🔊 **Natural voice output** — `edge-tts` neural voices, far more human-sounding than standard robotic TTS
- 🔁 **Runs continuously** — a real standing app: after each report, it goes back to listening for the wake word rather than exiting

## Folder Structure

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

As more agents are added (news, finance, etc.), each will get its own file inside `agents/`, all sharing the same `speech.py` and `listener.py` tools.

## Tech Stack

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
6. Say **"Hey Jarvis"**, then say or type a city name.

## Roadmap

- [ ] Train a custom "Hey Lisa" wake word (via synthetic data generation, once more agents exist)
- [ ] Add a second agent (news, finance, etc.) and build real intent-based routing between agents
- [ ] Desktop GUI — a visual app window instead of the terminal
- [ ] A senior orchestrator agent to route between all specialized agents
- [ ] Average-temperature-during-the-day feature
- [ ] Comparison build using Claude Code, for learning purposes

## Built By

Robby & Ani — learning AI development hands-on, one bug at a time. Follow along for updates as this grows into a full multi-agent system.