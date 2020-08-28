#include <fstream>
#include <iostream>
#include <string>
#include <cstring>

class Base {
    public:
    virtual void print() = 0;
};

class Derived1 : public Base {
    public:
    void print() {
        std::ifstream flag("flag.txt");
        std::string s;
        flag >> s;
        std::cerr << s << "\n";
    }
};

class Derived2 : public Base {
    public:
    void print() {
        std::cout << "Hello!\n";
    }
};

void call(Base* b) {
    b->print();
}

void conditional_run(Base* b, int r) {
    if (r)
        b->print();
}

int main() {
    Derived1 d1;
    Derived2 d2;
    conditional_run(&d1, 0);
    char buf[sizeof(d2)];
    std::cin.read(buf, sizeof(d2));
    std::memcpy(&d2, buf, sizeof(d2));
    call(&d2);
}
