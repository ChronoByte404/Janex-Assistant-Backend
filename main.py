
# Built-in Python libraries
import os
import time
import requests

# Internal directory libraries
from Utilities.functions import *
from Utilities.record import *
from Utilities.transcribe import *
from Utilities.server import *
#from Utilities.audio_server import *

from Interfaces.discord_bot import *

# Config (tbimported to json)

config = loadconfig("./Settings/config.json")
port = config.get("default-port")

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
            text = AI.transcribe()
            classify(text)
        except:
            pass

def server():
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"{port}")
    httpd.serve_forever()

def discord_server():
    Instance = DiscordBot()
    Instance.activate_bot()

def text_command():
    text = input("You: ")
    classify(text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = input("Mode (text/audio/server): ")

    if mode.lower() == "audio":
        audio_command()
    elif mode.lower() == "server":
        server()
    elif mode.lower() == "discord":
        discord_server()
    else:
        text_command()