from colorama import Fore,Style
from wikipedia.wikipedia import random
print(Fore.BLUE + "A.I Bot " + Fore.RED+"By " + Fore.YELLOW+"Mausam Kaushal." + Fore.RED+f''' No copyrights, Use it as you want. Thanks for using my
Project.{Fore.GREEN} Share it with your friends to see more future updates''' + Style.RESET_ALL)

import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os

import smtplib
from youtubesearchpython import VideosSearch
import pafy
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Krish Sir. Please tell me how may I help you")       


def takeCommand():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(to, content)
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open' in query:
            site = query.split(maxsplit=1)
            speak("opening" + site[1])
            webbrowser.open(site[1])

        elif 'youtube' in query:
            split = query.split(maxsplit=1)
            try:
                search = split[1]
            except IndexError:
                search = split[0]
            result = [video['link'] for video in VideosSearch(search, limit=1).result()['result']]
            print(result[0])
            webbrowser.open_new_tab(result[0])
        
        elif 'video' in query:
            split = query.split(maxsplit=1)
            search = split[1]
            result = [video['link'] for video in VideosSearch(search, limit=1).result()['result']]
            f_result = result[0]
            print(f_result)
            speak("downloading video")
            url = pafy.new(f_result)
            vid = url.getbest()
            vid.download()
        elif 'audio' in query:
            split = query.split(maxsplit=1)
            search = split[1]
            result = [video['link'] for video in VideosSearch(search, limit=1).result()['result']]
            f_result = result[0]
            print(f_result)
            
            url = pafy.new(f_result)
            vid = url.getbestaudio()
            vid.download()
        elif 'speak' in query:
            query = query.split(maxsplit=1)
            speak(query[1])

        elif 'play music' in query:
            music_dir = 'C:/Users/HPSEDC/Downloads/Audio'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        
        elif 'truths' in query:
            import v1.tods as tods
            t = tods.truths
            truth = random.choice(t)
            print(truth)
            speak(truth)
        
        elif 'dares' in query:
            import v1.tods as tods
            d = tods.dares
            dare = random.choice(d)
            print(dare)
            print(dare)
        
        elif 'help' in query:
            import v1.help
            help.commands

        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "someone"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Uhh, i can not send that")