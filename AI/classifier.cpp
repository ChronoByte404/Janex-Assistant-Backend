#include <iostream>
#include <fstream>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string.hpp>
#include <regex> // Include regex library for pattern matching

using namespace std;
using namespace boost::property_tree;


// Function to calculate similarity between two strings
double similarity(const string& input, const string& pattern) {
    // Remove punctuation symbols (including full stops) from both strings
    string inputProcessed = regex_replace(input, regex("[[:punct:].]"), "");
    string patternProcessed = regex_replace(pattern, regex("[[:punct:].]"), "");

    // Convert both processed strings to lowercase for case-insensitive comparison
    string inputLower = inputProcessed;
    string patternLower = patternProcessed;
    boost::algorithm::to_lower(inputLower);
    boost::algorithm::to_lower(patternLower);

    // Calculate similarity using a simple approach (e.g., exact match)
    return (inputLower == patternLower) ? 1.0 : 0.0;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cout << "Usage: " << argv[0] << " \"Your message\"" << endl;
        return 1;
    }

    ptree pt;

    try {
        // Load the JSON file into the property tree
        read_json("long_term_memory/intents.json", pt);

        string userInput = argv[1]; // Get the input from command-line argument

        double maxSimilarity = 0.0;
        ptree bestMatchIntent;

        // Accessing 'intents' array and iterating over its elements
        for (const auto& intent : pt.get_child("intents")) {
            // Accessing 'patterns' array within each intent
            for (const auto& pattern : intent.second.get_child("patterns")) {
                double similarityScore = similarity(userInput, pattern.second.get_value<string>());
                if (similarityScore > maxSimilarity) {
                    maxSimilarity = similarityScore;
                    bestMatchIntent = intent.second; // Save the entire intent's dictionary
                }
            }
        }

        if (maxSimilarity > 0.0) {
            cout << "Intent: " << bestMatchIntent.get<string>("tag") << " (Similarity: " << maxSimilarity << ")" << endl;
        } else {
            cout << "No matching intent found." << endl;
            // Construct a ptree with "tag" set to "none"
            bestMatchIntent.put("tag", "none");
        }

        // Write the best match intent or "None" to current_class.json in short_term_memory directory
        ofstream outputFile("short_term_memory/current_class.json");
        if (outputFile.is_open()) {
            write_json(outputFile, bestMatchIntent); // Write the entire intent's dictionary or "None"
            outputFile.close();
            cout << "Current class written to short_term_memory/current_class.json" << endl;
        } else {
            cerr << "Error: Unable to open file for writing." << endl;
        }

    } catch (const std::exception& ex) {
        cerr << "Error: " << ex.what() << endl;
        return 1;
    }

    return 0;
}
