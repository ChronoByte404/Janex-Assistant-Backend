#include <iostream>
#include <cstdlib>

int main() {
    const char* command = "python3 ./Maintenance/training.py";

    int returnCode = system(command);

    return 0;
}