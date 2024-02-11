#include <cstdlib>

int main() {
    try {
        std::system("git pull");
    } catch (...) {
        std::system("git stash");
        std::system("git pull");
    }
    return 0;
}
