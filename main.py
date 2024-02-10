import os
from Utilities.functions import *

User = input("You: ")
os.system(f"./AI/a.out '{User}'")
with open("short_term_memory/current_class.json", "r") as f:
    intent_class = json.load(f)

DoFunction(intent_class)