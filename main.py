
# Built-in Python libraries
import os
import time
import requests

# Internal directory libraries
from Utilities.functions import *
from Utilities.record import *
from Utilities.transcribe import *
from server import *

# Config (tbimported to json)

port = 8000

def classify(sentence):
    os.system(f"./Utilities/send_request http://localhost:{port} '{sentence}'")

    with open("./short_term_memory/output.txt", "r") as f:
        output = f.read()
    
    with open("./short_term_memory/current_class.json", "r") as f:
        intent_class = json.load(f)
    
    os.system(f"./Utilities/tts '{output}'")
    DoFunction(intent_class)

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

def text_command():
    text = input("You: ")
    classify(text)

if __name__ == "__main__":
    mode = input("Mode: ")
    if mode.lower() == "audio":
        audio_command()
    elif mode.lower() == "server":
        server()
    else:
        text_command()