#include <cstdlib>
#include <ctime>
#include <string>
#include <iostream>
std::string flag = "REDACTED";

void encrypt(std::string& s, int key) {
    for (auto& c: s) {
        c ^= key;
    }
}

int main() {
    std::srand(std::time(nullptr));
    for (std::size_t i = 0; i < 50; ++i) {
        int key = rand();
        encrypt(flag, key);
    }
    for (auto c: flag) {
        std::cout << static_cast<int>(static_cast<unsigned char>(c)) << ",";
    }
}

