
# Built-in Python libraries
import os
import time

# Internal directory libraries
from Utilities.functions import *
from Utilities.record import *
from Utilities.transcribe import *


def classify(text):
    os.system(f"./AI/classifier.out '{text}'")
    with open("short_term_memory/current_class.json", "r") as f:
        intent_class = json.load(f)
    time.sleep(1)
    os.system(f"./AI/choose_response.out '{text}'")
    DoFunction(intent_class)
    with open("./short_term_memory/output.txt", "r") as f:
        output = f.read()
        os.system(f"./Utilities/tts '{output}'")

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

def text_command():
    text = input("You: ")
    classify(text)

if __name__ == "__main__":
    mode = input("Mode: ")
    if mode.lower() == "audio":
        audio_command()
    else:
        text_command()