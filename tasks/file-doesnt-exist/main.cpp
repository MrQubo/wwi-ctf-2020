#include <string>
#include <fmt/core.h>


static std::string FLAG_ENC = "\220\237X\240gS8w\rYRmD\237\226\215\321\306";
static std::string KEY = "\xd3\xcb\x1e\xdb\x52\x07\x4a\x43\x6e\x1c\x7f\x0b\x10\xc8\xbb\xb7\x95\xbb";

int main () {
    std::string FLAG_DEC = "";

    for (unsigned int i = 0; i < FLAG_ENC.size(); i++) {
        FLAG_DEC += FLAG_ENC[i] xor KEY[i % KEY.size()];
    }

    FILE *file;
    file = fopen(FLAG_DEC.c_str(), "r");

    if (file) {
        fclose(file);
        fmt::print("file exists\n");
    } else {
        fmt::print("file doesn't exist\n");
    }

    return 0;
}
