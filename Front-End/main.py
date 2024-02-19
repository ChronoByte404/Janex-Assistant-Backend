from Internal.framework import *
from Internal.functions import *

import requests

Instance = Interface()

def listen():
    Talokan = 1
    while True:
        try:
            Instance.VoiceCommand()
            ResponseOutput, intent_class = Instance.send_audio()
            DoFunction(intent_class)
            tts(ResponseOutput)
        except Exception as e:
            print(f"Error: {e}")
            quit()

def text():
    Talokan = 2
    while True:
        try:
            Text = input("You: ")
            Instance.send(Text)
            ResponseJson = loadconfig("./local_memory/current_class.json")
            ResponseOutput, intent_class = ResponseJson.get("response"), ResponseJson.get("intent_class")
            DoFunction(intent_class)
            tts(ResponseOutput)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":

    config = loadconfig("./Settings/config.json")
    port = config.get("default-port")

    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = input("Mode (text/audio): ")

    if mode.lower() == "audio":
        listen()
    elif mode.lower() == "text":
        while True:
            try:
                text()
            except Exception as e:
                print(e)
    else:
        print("Usage: python3 main.py text {or} audio")
