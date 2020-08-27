import sympy
import random

template = """
#include <iostream>
#include <string>
#include <fstream>
#include <gmpxx.h>

uint8_t magic1[] = {
//MAGIC1
};

uint8_t magic2[] = {
//MAGIC2
};

int main() {
    std::cout << "Enter password: ";
    std::string password;
    std::cin >> password;
    mpz_class input(password);
    uint8_t acc = 0;
    for (size_t i = 0; i < std::size(magic1); ++i) {
        acc += input % mpz_class(magic1[i]) != mpz_class(magic2[i]);
    }
    if (acc) {
        std::cout << "Wrong...\\n";
    } else {
        std::ifstream flag_file("flag.txt");
        std::string flag;
        flag_file >> flag;
        std::cout << "The flag is CTF{" << flag << "}\\n";
    }
}
"""

path = 'confucius.cpp'
#flag = 7443246654783499190067509233131646577648579454569457633

block_size = 8

#primes = list(sympy.primerange(0,256))[:40] + list()
chosen_primes = random.sample(list(sympy.primerange(128, 256)), 8)
rest = list(set(range(2,256)).difference(chosen_primes))
primes = [random.choice(rest) for _ in range(256)]+ chosen_primes
assert len(primes) == 256+8
#assert flag < sympy.prod(primes)
password = random.randrange(sympy.prod(primes))
encoded = [password % p for p in primes]
bad_x = next(i for i,p in enumerate(primes) if p not in chosen_primes)
encoded[bad_x] = random.randrange(primes[bad_x])
assert encoded[bad_x] != password % primes[bad_x]
indices = list(range(len(primes)))
random.shuffle(indices)
primes = [primes[i] for i in indices]
encoded = [encoded[i] for i in indices]
l1 = []
l2 = []
for i in range(0, len(primes), block_size):
    l1.append(' '*4 + ', '.join(f'0x{x:02x}' for x in primes[i:i+block_size]))
    l2.append(' '*4 + ', '.join(f'0x{x:02x}' for x in encoded[i:i+block_size]))

#data = open(path_template).read()
data = template
data = data.replace('//MAGIC1', ',\n'.join(l1)).replace('//MAGIC2', ',\n'.join(l2))
with open(path, 'w') as f:
    f.write(data)
