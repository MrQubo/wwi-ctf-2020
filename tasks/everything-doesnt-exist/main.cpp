#include "aes.hpp"
#include <iostream>
#include <unistd.h>
#include <vector>
#include <sys/syscall.h>

#define CHECK(sysnum, retval) do {\
    if (syscall((sysnum)) != (retval)) {\
        std::cerr << "Return value is not " << (retval) << "\n";\
        exit(1);\
    }\
    key.push_back(retval);\
    } while (0)

uint8_t enc[] = {4, 49, 128, 215, 77, 196, 69, 46, 8, 119, 206, 154, 22, 36, 68, 32, 19, 168, 179, 60, 90, 21, 161, 122, 47, 9, 143, 247, 109, 54, 215, 166};

int main() {
    std::vector<uint8_t> key;
    CHECK(SYS_getpid, 55);
    CHECK(SYS_bind, 227);
    CHECK(SYS_ptrace, 236);
    CHECK(SYS_epoll_create, 1);
    CHECK(SYS_msync, 2);
    CHECK(SYS_munmap, 151);
    CHECK(SYS_lchown, 53);
    CHECK(SYS_stat, 232);
    CHECK(SYS_prlimit64, 247);
    CHECK(SYS_semop, 251);
    CHECK(SYS_vmsplice, 138);
    CHECK(SYS_mknod, 55);
    CHECK(SYS_ioctl, 255);
    CHECK(SYS_getrusage, 208);
    CHECK(SYS_getcwd, 193);
    CHECK(SYS_getppid, 157);
    AES_ctx ctx;
    AES_init_ctx(&ctx, key.data());
    AES_ECB_decrypt(&ctx, enc);
    AES_ECB_decrypt(&ctx, enc+16);
    syscall(SYS_write, 1, enc, sizeof(enc));
}
