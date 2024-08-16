import pyttsx3
import speech_recognition as sr
import pyaudio
import webbrowser
import pygame

assistant = "atlas"

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
        video = instructions.lower().split(" ")[1]
        webbrowser.open(f"https://www.youtube.com/results?search_query={video}")    
        
    elif instructions.lower().startswith("play") and instructions.lower().endswith("on spotify"):  
        music = instructions.lower().split(" ")[1]
        webbrowser.open(f"https://open.spotify.com/search/{music}")

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
            play('Atlas The voice assistant/music/level-up-191997.mp3')
            wake_word = taking_voice_to_wake_assistant()
    
            if wake_word.lower() == f"hello {assistant}" or wake_word.lower() == f"hey {assistant}":
                play('Atlas The voice assistant/music/level-up-191997.mp3')
                print(f"Hello, I am {assistant}. How may I help you?")

                play('Atlas The voice assistant/music/notification-beep-229154.mp3')
                instructions = taking_voice_to_get_instructions()
                url_opener(instructions)

        except Exception as e:
            pass
            continue

        


    


