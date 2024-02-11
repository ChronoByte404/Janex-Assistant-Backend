import numpy as np
import json
from JanexUltimate.janexpython import *  # contains cosine similarity and tokenize
import spacy

def pattern_compare(input_string):
    with open("long_term_memory/intent_vectors.json", "r") as vector_file:
        pattern_vectors = json.load(vector_file)
    
    with open("long_term_memory/intents.json", "r") as intent_file:
        intents = json.load(intent_file)
    
    highest_similarity = 0
    most_similar_pattern = None
    threshold = 0.085
    vector_dim = 300  # Change vector_dim to 300
    nlp = spacy.load("en_core_web_sm")

    input_tokens = tokenize(input_string)
    input_vector = np.zeros(vector_dim)

    for token in input_tokens:
        token_vector = pattern_vectors.get(token)
        if token_vector is None:
            token_vector = nlp(token).vector
        token_vector = np.resize(token_vector, vector_dim)  # Resize token_vector
        input_vector += token_vector

    input_vector /= np.linalg.norm(input_vector)  # Normalize input vector

    for intent_class in intents["intents"]:
        patterns = intent_class.get("patterns", [])
        for pattern in patterns:
            if pattern:
                pattern_vector = pattern_vectors.get(pattern)
                if pattern_vector is not None:
                    pattern_vector = np.array(pattern_vector)
                    pattern_vector /= np.linalg.norm(pattern_vector)  # Normalize pattern vector
                    similarity = calculate_cosine_similarity(input_vector, pattern_vector)

                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        most_similar_pattern = intent_class

    if highest_similarity > threshold and most_similar_pattern:
        return most_similar_pattern

if __name__ == "__main__":
    input_string = input("You: ")
    pattern = pattern_compare(input_string)
    if pattern:
        print("Classified as:", pattern["tag"])
    else:
        print("Unable to classify.")

