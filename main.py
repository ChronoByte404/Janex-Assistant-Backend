import os
import sys
import time
import json
import requests
import threading
from http.server import HTTPServer

from Utilities.functions import *
from Utilities.record import *
from Utilities.transcribe import *
from Utilities.server import *
from Utilities.audio_server import *
from Interfaces.discord_bot import *

configuration = loadconfig("./Settings/config.json")

def classify(sentence):
    sentence = sentence.replace("'", "")
    os.system(f"./Utilities/send_request http://localhost:{port} '{sentence}'")

    with open("./short_term_memory/output.txt", "r") as f:
        output = f.read()

    with open("./short_term_memory/current_class.json", "r") as f:
        intent_class = json.load(f)

    DoFunction(intent_class)
    os.system(f'./Utilities/tts "{output}"')

def audio_command():
    Input = Audio()
    AI = speech()

    while True:
        try:
            Input.VoiceCommand()
            url = configuration.get("voip-port")
            url = f"http://localhost:{url}"

            files = {'file': open('short_term_memory/audio.wav', 'rb')}
            response = requests.post(url, files=files)

            if response.status_code == 200:
                response_data = response.json()
                
                ResponseOutput = response_data.get("ResponseOutput")
                intent_class = response_data.get("intent_class")

                print(ResponseOutput)
                tts(ResponseOutput)
                DoFunction(intent_class)
            else:
                print("Failed to receive a valid response from the server.")

        except Exception as e:
            print(f"Error: {e}")

def audio_server():
    flaskapp.run(port=config.get("voip-port"))

def server():
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"{port}")
    httpd.serve_forever()

def both_servers():
    threading.Thread(target=audio_server, args=()).start()
    threading.Thread(target=server, args=()).start()

def discord_server():
    Instance = DiscordBot()
    Instance.activate_bot()

def text_command():
    text = input("You: ")
    classify(text)

if __name__ == "__main__":
    config = loadconfig("./Settings/config.json")
    port = config.get("default-port")

    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = input("Mode (text/audio/server/discord): ")

    if mode.lower() == "audio":
        audio_command()
    elif mode.lower() == "server":
        both_servers()
    elif mode.lower() == "discord":
        discord_server()
    else:
        text_command()
