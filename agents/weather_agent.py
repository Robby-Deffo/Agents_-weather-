import requests
from speech import speak
from listener import listen

def celsius_to_fahrenheit(c):
    return c * 9/5 + 32

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
}

def extract_number(text, max_valid):
    text = text.lower().strip()
    for word in text.split():
        if word.isdigit():
            num = int(word)
        elif word in NUMBER_WORDS:
            num = NUMBER_WORDS[word]
        else:
            continue
        if 1 <= num <= max_valid:
            return num
    return None

def run():
    MAX_ATTEMPTS = 3
    city = None

    for attempt in range(MAX_ATTEMPTS):
        city = listen()
        if city is not None:
            break
        if attempt < MAX_ATTEMPTS - 1:
            speak("Sorry, I didn't catch that. Could you say the city again?")

    if city is None:
        speak("I'm sorry, I was having trouble understanding you. Could you please type your city instead?")
        city = input("What city do you want the weather for? ")

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_response = requests.get(geo_url, params={"name": city, "count": 3})
    geo_data = geo_response.json()

    if "results" not in geo_data:
        print("Couldn't find that city. Try again with a different spelling.")
        return

    results = geo_data["results"]

    # Sort by population (most populous first), treating unknown population as 0
    results = sorted(results, key=lambda r: r.get("population", 0), reverse=True)

    if len(results) == 1:
        location = results[0]
    else:
        top_population = results[0].get("population", 0)
        second_population = results[1].get("population", 0)

        # If the top match is at least 5x more populous, just go with it
        if top_population > 0 and top_population >= second_population * 5:
            location = results[0]
            print(f"Assuming you meant {location['name']}, {location.get('country', '')} (by far the most populous match).")
        else:
            print("Found a few matches:")
            options_spoken = []
            for i, place in enumerate(results):
                state = place.get("admin1", "")
                country = place.get("country", "")
                print(f"{i + 1}. {place['name']}, {state}, {country}")
                options_spoken.append(f"{i + 1} for {place['name']}, {state}")

            speak("I found a few matches. " + ". ".join(options_spoken) + ". Which one is yours?")

            choice = None
            for attempt in range(MAX_ATTEMPTS):
                answer = listen()
                if answer:
                    choice = extract_number(answer, len(results))
                    if choice:
                        break
                if attempt < MAX_ATTEMPTS - 1:
                    speak("Sorry, I didn't catch a valid number. Please say the number again.")

            if choice is None:
                speak("I'm having trouble understanding. Please type the number instead.")
                choice = int(input("Which one is yours? (type the number): "))

            location = results[choice - 1]

    lat = location["latitude"]
    lon = location["longitude"]
    print(f"Using {location['name']}, {location.get('admin1', '')}, {location.get('country', '')} at ({lat}, {lon})")

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_response = requests.get(weather_url, params={
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,precipitation,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    })
    weather_data = weather_response.json()

    current_c = weather_data["current"]["temperature_2m"]
    current_f = celsius_to_fahrenheit(current_c)

    high_c = weather_data["daily"]["temperature_2m_max"][0]
    low_c = weather_data["daily"]["temperature_2m_min"][0]
    high_f = celsius_to_fahrenheit(high_c)
    low_f = celsius_to_fahrenheit(low_c)

    print(f"\nCurrent temp: {current_c}°C / {round(current_f, 1)}°F")
    print(f"Today's high: {high_c}°C / {round(high_f, 1)}°F")
    print(f"Today's low: {low_c}°C / {round(low_f, 1)}°F")

    weather_summary = f"""
City: {location['name']}, {location.get('admin1', '')}
Current temperature: {current_c}°C / {round(current_f, 1)}°F
Today's high: {high_c}°C / {round(high_f, 1)}°F
Today's low: {low_c}°C / {round(low_f, 1)}°F
"""

    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": f"""You are a friendly, upbeat weather reporter speaking live, out loud, on the radio — not writing an article.
Talk the way a real person talks: use contractions (it's, you're, gonna), casual conversational phrasing, and natural little pauses like "well," or "so yeah."
Bring genuine enthusiasm and energy — sound excited, not flat.
Only include a joke or a funny observation if a genuinely good one comes to mind — don't force it in every time. A weather report with no joke is totally fine; a weak, forced joke is worse than no joke.
Give it 4-5 sentences, like a real local weather personality with some charisma.
Here's the data:\n{weather_summary}""",
            "stream": False
        }
    )

    report = ollama_response.json()["response"]
    print("\n--- Weather Report ---")
    print(report)
    speak(report)