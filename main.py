import os
from Utilities.functions import *
import time

User = input("You: ")
os.system(f"./AI/classifier.out '{User}'")
with open("short_term_memory/current_class.json", "r") as f:
    intent_class = json.load(f)

time.sleep(1)

os.system(f"./AI/choose_response.out '{User}'")

DoFunction(intent_class)