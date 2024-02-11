#include <cstdlib>

int main() {
    std::system("git rm -rf --cached .");
    std::system("git add .");
    std::system("git add *");
    std::system("git commit -m 'Automation'");
    std::system("git push");
    return 0;
}
