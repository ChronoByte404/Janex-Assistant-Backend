#include <iostream>
#include <cstdlib>

int main(int argc, char *argv[]) {
    if (argc > 2) {
        std::cerr << "Usage: " << argv[0] << " [argument]" << std::endl;
        return 1;
    }

    std::string argument;
    if (argc == 2) {
        // If an argument is provided, use it
        argument = argv[1];
    } else {
        // If no argument is provided, set a default value or leave it empty
        argument = ""; // You can set a default value here if needed
    }

    // Construct the command to run the Python script
    std::string command = "python3 main.py " + argument;

    // Execute the command
    int result = std::system(command.c_str());

    // Check if the command executed successfully
    if (result != 0) {
        std::cerr << "Error executing Python script" << std::endl;
        return 1;
    }

    return 0;
}
