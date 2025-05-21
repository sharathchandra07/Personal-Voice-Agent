import speech_recognition as sr
from langchain_core.output_parsers import StrOutputParser
# from langchain_community.chat_models import ChatOllama
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import pyttsx3
import os
import webbrowser
import subprocess
import time
from dotenv import load_dotenv



load_dotenv()

groq_api_key =  os.getenv("groq_api_key")
r = sr.Recognizer()
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)
engine = pyttsx3.init()

# voices = engine.getProperty('voices')      To change voice Male -> Female
# engine.setProperty('voice', voices[0].id)


app_status = {
    "notepad": 0,
    "calculator": 0,
    "chrome": 0,
    "steam": 0,
    "whatsapp": 0,
    "telegram": 0,
    "linkedin": 0,
    "mail": 0,
    "calendar": 0,
    "camera": 0,
    "clock": 0,
    "one note": 0,
    "maps": 0,
    "skype": 0,
    "photos": 0,
    "solitaire": 0,
    "copilot": 0,
    "microsoft store": 0,
    "black notepad": 0,
    "media player": 0,
    "idle": 0
}


apps = {
    "notepad": "notepad",
    "calculator": "calc",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "steam": "D:\\Staem\\Steam.exe",
    #Add all the Remaining paths
}


def chatwithollama(audio_input, config1): 
    response = history.invoke(
    [HumanMessage(content=audio_input)],
    config=config1)

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
        app_status[app] = 1
        time.sleep(3)
    else:
        open_website(app)
    return

def close_application(app):
    if app_status.get(app) == 1:
        text = "Sure sir. Here you go"
        speak(text)
        subprocess.run(f"taskkill /f /im {app}.exe", shell=True)
        app_status[app] = 0
    else:
        speak(f"{app} is not yet opened sir.")
    return




def open_website(site):
    text = "Sure sir. Here you go"
    speak(text)
    url = f"https://{site}"
    webbrowser.open(url)
    return

def start_jarvis(src, config):
    while(1):
        speak("Do you have any questions sir?")
        print("Listening")
        try:
            audio = r.listen(src)
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

            if "jarvis" in lst:
                lst.remove("jarvis")

            print(lst)
        except sr.UnknownValueError:
            text = "Sorry sir, I am unable to catch you."
            speak(text)
            continue
        except sr.WaitTimeoutError:
            text = "Come again sir"
            speak(text)
            continue

        if "goodbye " in audio_input:
            text = "Good bye sir."
            speak(text)
            start_app()

        
        if 'open' in lst or 'close' in lst:
            if 'open' in lst:
                idx = lst.index('open')+1
                if (idx < len(lst)):
                    application = lst[idx]
                    open_application(application)
                    continue
                else:
                    chatwithollama(audio_input, config)
            elif 'close' in lst:
                idx = lst.index('close')+1
                if (idx < len(lst)):
                    application = lst[idx]
                    close_application(application)
                    continue
                else:
                    chatwithollama(audio_input, config)

        else:
            chatwithollama(audio_input, config)


    
store = {}

def set_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
        store[session_id].add_message(SystemMessage(content="You are Jarvis, an intelligent and loyal AI assistant. You must always refer to yourself as Jarvis. When asked 'who are you', say 'I am Jarvis, your AI voice agent. I am ready to help you in performing various tasks.'"))
        store[session_id].add_message(SystemMessage(content="You are Jarvis, an intelligent and loyal AI assistant. You must always refer to yourself as Jarvis. When asked 'what is your name', say 'My name is Jarvis. I am your AI voice agent.'"))
    return store[session_id]

history = RunnableWithMessageHistory(model, set_history)


def start_app():
    with sr.Microphone() as src:
        while (True):
            # print("Waiting for wake word")
            try:
                wake_audio = r.listen(src, timeout=10)
                wake_word = r.recognize_google(wake_audio).lower()
                # print(wake_word)

                if "hey jarvis" in wake_word:
                    welcome_text = "Hello sir. This is Jarvis, your voice agent. I am here to help you."
                    engine.say(welcome_text)

                    print(welcome_text)

                    engine.runAndWait()

                    r.adjust_for_ambient_noise(src)
                    config = {"configurable":{"session_id":"chat1"}}

                    break
                elif wake_word == "exit":
                    exit(0)
                
            except sr.UnknownValueError:
                continue
            except sr.WaitTimeoutError:
                continue
        start_jarvis(src, config)




if __name__ == "__main__":
    start_app()



