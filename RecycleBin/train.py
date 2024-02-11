import random
import spacy
from spacy.lang.en import English
import numpy as np
import json
from JanexUltimate.janexpython import *

def trainvectors():

    nlp = spacy.load("en_core_web_md")
    with open("long_term_memory/intents.json", "r") as f:
        intents = json.load(f)
    
    pattern_vectors = {}
    patterncount = 0
    responsecount = 0
    patterntoks = 0
    responsetoks = 0
    for intent_class in intents["intents"]:
        for pattern in intent_class["patterns"]:
            patterns = tokenize(pattern)
            for token in patterns:
                token_vector = nlp(token).vector
                pattern_vectors[token] = token_vector.tolist()
                patterntoks += 1
            patterncount += 1
            print(f"{token}: {token_vector}")

    with open("long_term_memory/intent_vectors.json", "w") as vectors_file:
        json.dump(pattern_vectors, vectors_file)

    print(f"Code: Training completed. {patterncount} patterns ({patterntoks} tokens) transformed into vectors.")

if __name__ == "__main__":
    trainvectors()