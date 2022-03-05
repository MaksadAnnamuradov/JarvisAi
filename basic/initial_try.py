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
todo_list = ["go shopping", "clean room", "record video"]


#save notes to file
def save_notes():
    global recognizer
    speaker.say("What file would you like to save your notes to?")
    speaker.runAndWait()

    done = False
    while not done:
        
        try:
            with sr.Microphone() as source:
                # recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source, phrase_time_limit=2)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

                with open(filename + ".txt", "w") as file:
                    for item in todo_list:
                        file.write(item + "\n")
                    done = True
                    speaker.say("Notes saved.")
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
                # recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source, phrase_time_limit=2)

                note_name = recognizer.recognize_google(audio)
                note_name = note_name.lower()

                #check if note already exists in to do list
                if note_name in todo_list:
                    speaker.say("That note already exists.")
                    speaker.runAndWait()
                else:
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
    global recognizer
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
                # recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source, phrase_time_limit=2)

                note_name = recognizer.recognize_google(audio)
                note_name = note_name.lower()


                # check if the note does not exist in to do list
                if note_name not in todo_list:
                    speaker.say("Sorry, that note does not exist.")
                    speaker.runAndWait()
                else:
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


    done = False
    while not done:
        speaker.say("What is the name of to do that you would like to edit?")
        speaker.runAndWait()
        try:
            with sr.Microphone() as source:
                # recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source, phrase_time_limit=2)

                todo_edit = recognizer.recognize_google(audio)
                todo_edit = todo_edit.lower()

                # check if the note does not exist in to do list
                if todo_edit not in todo_list:
                    speaker.say("Sorry, that note does not exist.")
                    speaker.runAndWait()
                else:
                    speaker.say("What would you like to change it to?")
                    speaker.runAndWait()

                    audio = recognizer.listen(source, phrase_time_limit=2)

                    editted_todo = recognizer.recognize_google(audio)
                    editted_todo = editted_todo.lower()

                    todo_list[todo_list.index(todo_edit)] = editted_todo
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
    "save notes": save_notes,
    "add to do": add_todo,
    "show to do": show_todos,
    "remove to do": remove_todo,
    "edit to do": edit_todo,
    "exit": quit,
    "greeting": hello
}

assistant = GenericAssistant('intents.json', model_name = "test_mode", intent_methods = mappings)
# assistant.train_model()
# assistant.save_model()

assistant.load_model("test_mode")

while True:
    try:
        with sr.Microphone() as source:
            speaker.say("How can I help you?")
            speaker.runAndWait()
            # print("Say something!")
            # recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source, phrase_time_limit=2)

            text = recognizer.recognize_google(audio)
            text = text.lower()
            

            print("You said: " + text)

            assistant.request(text)
    except sr.UnknownValueError:
        recognizer = sr.Recognizer()
        print("error")
        speaker.say("Sorry, I didn't get that.")
        speaker.runAndWait()
