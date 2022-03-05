from neuralintents import GenericAssistant
import speech_recognition as sr
import pyttsx3 as tts
import sys

# import nltk
# nltk.download("omw-1.4")

recognizer = sr.Recognizer()

speaker = tts.init()

# voices = speaker.getProperty('voices')
# for voice in voices:
#     if voice.name == "Sophie":
#         speaker.setProperty('voice', gender)
#         break

speaker.setProperty('rate', 150)

#create to do list of string
todo_list = ["Go shopping", "Clean Room", "Record Video"]


def create_note(text):
    global recognizer

    speaker.say("What would you like to call your note?")
    speaker.runAndWait()

    done = False
    while not done:
        
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)

                note_name = recognizer.recognize_google(audio)
                note_name = note_name.lower()

                speaker.say("Choose a file to save your note to.")
                speaker.runAndWait()
                
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(filename, "w") as file:
                file.write(text)
                done = True
                speaker.say("Note created.")
                speaker.runAndWait()
                
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("Sorry, I didn't get that.")
            speaker.runAndWait()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


def add_todo():
    global recognizer

    speaker.say("What would you like to add to your to do list?")
    speaker.runAndWait()

    done = False
    while not done:
        
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)

                note_name = recognizer.recognize_google(audio)
                note_name = note_name.lower()

                todo_list.append(note_name)
                done = True
                speaker.say("Note added.")
                speaker.runAndWait()
                
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("Sorry, I didn't get that.")
            speaker.runAndWait()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def show_todos():
    global speaker
    speaker.say("Here is your to do list.")
    speaker.runAndWait()
    for item in todo_list:
        speaker.say(item)
        speaker.runAndWait()

def remove_todo():
    global recognizer
    speaker.say("What would you like to remove from your to do list?")
    speaker.runAndWait()

    done = False
    while not done:
        
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)

                note_name = recognizer.recognize_google(audio)
                note_name = note_name.lower()

                todo_list.remove(note_name)
                done = True
                speaker.say("Note removed.")
                speaker.runAndWait()
                
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("Sorry, I didn't get that.")
            speaker.runAndWait()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

#create a function to edit to do list
def edit_todo():
    global recognizer
    speaker.say("What would you like to edit on your to do list?")
    speaker.runAndWait()

    done = False
    while not done:
        
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)

                note_name = recognizer.recognize_google(audio)
                note_name = note_name.lower()

                speaker.say("What would you like to change it to?")
                speaker.runAndWait()

                with sr.Microphone() as source:
                    audio = recognizer.listen(source)

                    note_name = recognizer.recognize_google(audio)
                    note_name = note_name.lower()

                    todo_list[todo_list.index(note_name)] = note_name
                    done = True
                    speaker.say("Note edited.")
                    speaker.runAndWait()
                
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("Sorry, I didn't get that.")
            speaker.runAndWait()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def hello():
    global recognizer
    speaker.say("Hello, how can I help you?")
    speaker.runAndWait()

def quit():
    global recognizer
    speaker.say("Goodbye.")
    speaker.runAndWait()
    sys.exit()

mappings = {
    "create note": create_note,
    "add to do": add_todo,
    "show to do": show_todos,
    "remove to do": remove_todo,
    "edit to do": edit_todo,
    "quit": quit,
    "hello": hello
}

assistant = GenericAssistant('intents.json', model_name = "test_mode", intent_methods = mappings)
assistant.train_model()
# assistant.save_model()

# assistant.load_model("test_mode")

while True:
    try:
        with sr.Microphone() as source:
            speaker.say("Welcome!")
            speaker.runAndWait()
            # print("Say something!")
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source)


            text = recognizer.recognize_google(audio)
            text = text.lower()
            

            speaker.say("You said: " + text)

            assistant.request(text)
    except sr.UnknownValueError:
        print("error")
        # speaker.say("Sorry, I didn't get that.")
        recognizer = sr.Recognizer()
        # speaker.runAndWait()
