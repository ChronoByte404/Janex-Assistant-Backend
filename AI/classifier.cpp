#include <iostream>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string.hpp>

using namespace std;
using namespace boost::property_tree;

// Function to calculate similarity between two strings
double similarity(const string& input, const string& pattern) {
    // Convert both strings to lowercase for case-insensitive comparison
    string inputLower = input;
    string patternLower = pattern;
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
        string bestMatchTag;

        // Accessing 'intents' array and iterating over its elements
        for (const auto& intent : pt.get_child("intents")) {
            // Accessing 'patterns' array within each intent
            for (const auto& pattern : intent.second.get_child("patterns")) {
                double similarityScore = similarity(userInput, pattern.second.get_value<string>());
                if (similarityScore > maxSimilarity) {
                    maxSimilarity = similarityScore;
                    bestMatchTag = intent.second.get<string>("tag");
                }
            }
        }

        if (maxSimilarity > 0.0) {
            cout << "Intent: " << bestMatchTag << " (Similarity: " << maxSimilarity << ")" << endl;
        } else {
            cout << "No matching intent found." << endl;
        }

    } catch (const std::exception& ex) {
        cerr << "Error: " << ex.what() << endl;
        return 1;
    }

    return 0;
}
