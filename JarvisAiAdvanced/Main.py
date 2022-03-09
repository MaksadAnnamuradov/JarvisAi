from types import coroutine
import pyttsx3
import speech_recognition as sr
from Features import GoogleSearch

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[1].id)

def Speak(audio):
    print(" ")
    print(f": {audio}")
    engine.say(audio)
    engine.runAndWait()
    print(" ")

def TakeCommand():

    r = sr.Recognizer()
    
    # if(wake_up(query)):
    #     print("Jarvis is here")
    #     Speak("How can I help you?")

    with sr.Microphone() as source:

        print(": Listening....")
        r.adjust_for_ambient_noise(source, duration = 1)
        
        # r.pause_threshold = 1

        audio = r.listen(source, phrase_time_limit = 2)

    query = ""
    try:

        print(": Recognizing...")

        query = r.recognize_google(audio)

        print(f": Your Command : {query}\n")

    except sr.UnknownValueError:
            Speak("Sorry, I didn't get that.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


    return query.lower()

#write function to wake up assistant
def wake_up(message):
    if 'hey jarvis' in message:
        return True
    else:
        return False

def TaskExe():

    while True:

        query = TakeCommand()

        if 'google search' in query:
            GoogleSearch(query)

        elif 'chrome' in query:
            from Automations import ChromeAuto
            ChromeAuto(query)

        elif 'youtube' in query:
            from Automations import YouTubeAuto
            YouTubeAuto(query)
        
        elif 'youtube search' in query:
            Query = query.replace("jarvis","")
            query = Query.replace("youtube search","")
            from Features import YouTubeSearch
            YouTubeSearch(query)

        elif 'set alarm' in query:
            from Features import Alarm
            Alarm(query)

        elif 'download' in query:
            from Features import DownloadYouTube
            DownloadYouTube()
            
        elif 'speed test' in query:
            from Features import SpeedTest
            SpeedTest()

        elif 'where is' in query:

            from Automations import GoogleMaps
            Place = query.replace("where is ","")
            Place = Place.replace("jarvis" , "")
            GoogleMaps(Place)

        elif 'write a note' in query:

            from Automations import Notepad

            Notepad()

        elif 'dismiss' in query:

            from Automations import CloseNotepad

            CloseNotepad()


        elif 'corona cases' in query:

            from Features import CoronaVirus

            Speak("Which Country's Information ?")

            cccc = TakeCommand()

            CoronaVirus(cccc)

        else:

            from DataBase.ChatBot.ChatBot import ChatterBot

            reply = ChatterBot(query)

            Speak(reply)

            if 'bye' in query:

                break

            elif 'exit' in query:

                break

            elif 'go' in query:

                break
    

TaskExe()



