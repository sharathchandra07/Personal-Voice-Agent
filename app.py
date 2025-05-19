import speech_recognition as sr
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
import pyttsx3
import webbrowser
import subprocess


r = sr.Recognizer()
model = ChatOllama(model="phi")
engine = pyttsx3.init()

apps = {
    "notepad": "notepad",
    "calculator": "calc",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "vs code": "C:\\Users\\Sharath Chandra\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "file manager": "explorer"
    #Add Remaining paths
}


def chatwithollama(audio_input):
    response = model.invoke(audio_input)
    parser = StrOutputParser()

    output = parser.invoke(response)

    print(output)
    engine.say(output)
    engine.runAndWait()
    return

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()
    return

def open_application(app):
    if app in apps:
        text = "Sure sir. Here you go"
        speak(text)
        subprocess.Popen(apps[app], shell=True)
    else:
        open_website(app)
    return


def open_website(site):
    text = "Sure sir. Here you go"
    speak(text)
    url = f"https://{site}.com"
    webbrowser.open(url)
    return
    


with sr.Microphone() as src:
    welcome_text = "Hello sir. This is Jarvis, your voice agent. How can i help you today?"
    engine.say(welcome_text)

    print(welcome_text)

    engine.runAndWait()
    count=1


    while(1):
        speak("I am listening sir.")
        try:
            audio = r.listen(src, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            if (count == 3):
                text = "Sorry sir, I am unable to catch you."
                speak(text)
                break
            else:
                text = "Sorry sir, I didn't catch that. Please repeat again."
                count=count+1
                speak(text)
                continue
        
        try:
            audio_input = r.recognize_google(audio).lower()
            audio_input = audio_input + ' '
            print(audio_input)

            lst = []
            words = ""
            for i in audio_input:
                if (i == ' '):
                    lst.append(words)
                    words=""
                else:
                    words = words+i
            print(lst)
        except sr.UnknownValueError:
            text = "Sorry sir, I am unable to catch you."
            speak(text)
            break

        if (audio_input == "exit "):
            text = "Good bye sir."
            speak(text)
            break

        
        if 'open' in lst:
            idx = lst.index('open')+1
            if (idx < len(lst)):
                application = lst[idx]
                open_application(application)
            else:
                chatwithollama(audio_input)

        else:
            chatwithollama(audio_input)

