import os
from time import strftime
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import random
import subprocess
from ecapture import ecapture as ec
import pyautogui  # code added by Pyoush Madan
from time import sleep  # code added by Pyoush Madan
import screen_brightness_control as sbc  # code added by Pyoush Madan
import requests
import pyjokes
from bs4 import BeautifulSoup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


list_of_jokes = ["The three most well known languages in India are English, Hindi, and... JavaScript", "Interviewer... Where were you born?Me in India... Interviewer:.. oh, which part?... Me: What ‘which part’ ..? Whole body was born in India",
                 "how many Indians does it take to fix a lightbulb?Two. One to do the task and other to explain how lightbulbs were actually invented in ancient India", "What do you call bread from India? It's Naan of your business", "Britain: Drive on the left side... Europe and America: Drive on the right side...India: lol what's a 'traffic law'?"]
jokes = len(list_of_jokes)-1
ran_joke = random.randint(0, jokes)


def speak(audio):  # speak audio
    engine.say(audio)
    engine.runAndWait()


def wishMe():  # wishes me
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 3:
        speak("It's Late Night Sir!, You should sleep right now")

    elif hour >= 4 and hour < 12:
        speak("Good Moring Master!")
    elif hour >= 12 and hour < 17:
        speak("Good Afternoon Sir !")
    elif hour >= 17 and hour < 19:
        speak("Good Evening !")
    elif hour >= 19 and hour < 24:
        speak("Good Night Sir!")

    if hour >= 0 and hour <= 4:
        pass
    else:
        speak("I am Your Personal assistant, Jarvis! version 1.0!")


def takeCommand():  # takes microphone inout and returns output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        # Using google for voice recognition
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")  # User query will be printed
    except Exception as e:
        # Say that again will be printed in case of improper voice
        print("Say that again please...")
        return "None"  # None string will be returned
    return query


if __name__ == "__main__":
    wishMe()
    speak("How May I Help You Sir ?")
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching in Wikipedia')
            query = query.replace("according to wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("Accoring to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak("Here We Go")
            webbrowser.open("youtube.com")
        elif 'youtube' in query and 'search' in query:
            speak("What Should I Search Sir ?")
            search_yt = takeCommand()
            search_yt = search_yt.replace(" ", "+")
            speak("Here We Go")
            webbrowser.open(
                f"https://www.youtube.com/results?search_query={search_yt}")
        elif 'open google' in query:
            speak("Here We Go")
            webbrowser.open("google.com")
        elif 'google' in query and 'search' in query:
            speak("What Should I Search Sir ?")
            search_go = takeCommand()
            search_go = search_go.replace(" ", "+")
            speak("Here We Go")
            webbrowser.open(f"https://www.google.com/search?q={search_go}")
        elif 'open instagram' in query:
            speak("Here We Go")
            webbrowser.open("instagram.com")
        elif 'open facebook' in query:
            speak("Here We Go")
            webbrowser.open("facebook.com")
        elif 'open twitter' in query:
            speak("Here We Go")
            webbrowser.open("twitter.com")
        elif 'download youtube videos' in query:
            speak("Here We Go")
            webbrowser.open("en.onlinevideoconverter.pro")
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(strTime)
        elif 'the date' in query:
            today = datetime.date.today()
            speak(today)
        elif query == 'jarvis':
            speak("At Your Service Sir, How can I help you")
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif "volume up" in query:
            pyautogui.press("volumeup")
            speak("volume upped")
            sleep(1)
            speak("anything else for which i may assist you")
        elif "volume down" in query:
            pyautogui.press("volumedown")
            speak("volume lowered")
            sleep(1)
            speak("anything else for which i may assist you")
        elif "mute" in query:
            pyautogui.press("volumemute")
            speak("volume muted")
            sleep(1)
            speak("anything else for which i may assist you")
        elif "brightness" in query:
            try:
                current = sbc.get_brightness()
                bright = int(takecommand())
                set = sbc.set_brightness(bright)
                speak(f"brightness set to {set} percent")
                sleep(1)
                speak("anything else for which i may assist you")
            except Exception as e:
                print(e)
                speak("error")

        elif 'todo' in query or 'to do' in query:
            if 'add' in query or 'create' in query:
                with open('todo.txt', 'a') as f:
                    todo_w = takeCommand()
                    f.write(f"{todo_w}\n")
                speak("To Do is updated successfully !")
            elif 'read' in query or 'tell' in query:
                with open('todo.txt', 'r') as f:
                    todo_r = f.read()
                    if todo_r == "":
                        todo_r = "No Pendning Tasks Sir"
                    speak(todo_r)
            elif 'erase' in query or 'remove all' in query or 'clear' in query:
                with open("todo.txt", "w") as f:
                    f.write("")
                speak("All Tasks has been cleared, Sir !")
        elif 'open spotify' in query:
            speak("Opening spotify")
            webbrowser.open("spotify.com")

        elif "log off" in query or "sign out" in query:
            speak(
                "Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])
        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "robo camera", "img.jpg")
        elif "weather" in query:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name = takeCommand()
            complete_url = base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                speak(" City Not Found ")
        elif "who made you" in query or "who created you" in query or "who discovered you" in query:
            speak("I was built by a Human")
            print("I was built by a Human")

        elif 'jarvis quit' in query or 'exit' in query or 'close' in query:
            speak("Thanks you for using Jarvis Sir")
            exit()
