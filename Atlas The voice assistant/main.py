import pyttsx3
import speech_recognition as sr
import pyaudio
import webbrowser
import pygame
import requests

assistant = "Atlas"

api_key_news = "d92bcc710b15477baa4f3232ee841d0f"
api_key_weather = "0915469b30f24ba385e94008241608"

def get_news_headlines(api_key, country):
    base_url = "https://newsapi.org/v2/top-headlines"
    
    params = {
        'apiKey': api_key,
        'pageSize': 3  # Adjust the number of headlines as needed
    }
    
    if country:
        params['country'] = country

    try:
        print("Sending request to News API...")
        response = requests.get(base_url, params=params)
        print(f"Response status code: {response.status_code}")
        
        response.raise_for_status()
        news_data = response.json()

        print(f"API Response: {news_data}")

        if news_data['status'] == 'ok':
            articles = news_data.get('articles', [])
            if articles:
                print(f"Number of articles received: {len(articles)}")
                for i, article in enumerate(articles, 1):
                    headline = article.get('title', 'No headline available')
                    print(f"{i}. {headline}")
            else:
                print("No articles found in the response.")
        else:
            print(f"API returned an error. Status: {news_data.get('status')}")
            if 'message' in news_data:
                print(f"Error message: {news_data['message']}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
    except ValueError as e:
        print(f"An error occurred while parsing the JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_weather(api_key, location):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': location
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        location_name = data['location']['name']
        country = data['location']['country']
        temp_c = data['current']['temp_c']
        condition = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind_kph = data['current']['wind_kph']

        print(f"Weather in {location_name}, {country}:")
        print(f"Temperature: {temp_c}°C")
        speak(f"Temperature: {temp_c}°C")
        print(f"Condition: {condition}")
        speak(f"Condition: {condition}")
        print(f"Humidity: {humidity}%")
        speak(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_kph} km/h")
        speak(f"Wind Speed: {wind_kph} km/h")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def palying_music(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def speak(speech):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
    engine.say(speech)
    engine.runAndWait()

def url_opener(instructions): 
    if instructions.lower().startswith("open"):
        web = instructions.lower().split(" ")[1]
        webbrowser.open(f"https://www.{web}.com")

    elif instructions.lower().startswith("play") and instructions.lower().endswith("on youtube"):  
        list_for_youtube = instructions.lower().split(" ")
        video = list_for_youtube[1:-2]
        webbrowser.open(f"https://www.youtube.com/results?search_query={video}")    
        
    elif instructions.lower().startswith("play") and instructions.lower().endswith("on spotify"):  
        list_for_spotify = instructions.lower().split(" ")
        music = list_for_spotify[1:-2]
        webbrowser.open(f"https://open.spotify.com/search/{music}")

    elif "weather" in instructions.lower():
        list_for_weather = instructions.lower().split(" ")
        location = list_for_weather[-1]
        get_weather(api_key_weather, location)   

    elif "news" in instructions.lower():
        get_news_headlines(api_key_news, "us")


def play(filename):
    pygame.mixer.init(frequency=16000)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def taking_voice_to_wake_assistant():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # play('Atlas The voice assistant/music/level-up-191997.mp3')
        r.dynamic_energy_threshold = True
        r.energy_threshold = 300
        audio = r.listen(source, phrase_time_limit=5)
        command = r.recognize_google(audio)
        print(command)
        return command
    
def taking_voice_to_get_instructions():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        play('Atlas The voice assistant/music/notification-beep-229154.mp3')
        r.dynamic_energy_threshold = True
        r.energy_threshold = 300
        audio = r.listen(source)
        play('Atlas The voice assistant/music/notification-beep-229154.mp3')
        print("Recognizing...")
        command = r.recognize_google(audio)
        print(command)
        return command
    
if __name__ == "__main__":

    # wake word for jarvis

    print(f"Activating {assistant}...")
    speak(f" Activating {assistant}...")
    while True:
        try:
            wake_word = taking_voice_to_wake_assistant()
    
            if wake_word.lower() == f"hello {assistant.lower()}" or wake_word.lower() == f"hey {assistant.lower()}":
                play('Atlas The voice assistant/music/level-up-191997.mp3')
                speak("Yes")

                instructions = taking_voice_to_get_instructions()
                url_opener(instructions)

        except Exception as e:
            pass
            continue

        


    


