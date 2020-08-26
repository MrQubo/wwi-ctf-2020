#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sodium.h>

#define STATE_SIZE 0x100
#define KEY_SIZE 8

#define FLAG_FILE "flag.txt"

static uint8_t get_random_byte() {
    uint8_t array[STATE_SIZE];
    uint8_t key[KEY_SIZE];
    uint8_t i = 0, j = 0, temp;

    randombytes_buf(key, KEY_SIZE);
    for (size_t i = 0; i < STATE_SIZE; ++i) {
        array[i] = i;
    }
    for (size_t i = 0; i < STATE_SIZE; ++i) {
        j += array[i] + key[i % KEY_SIZE];
        temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    i += 1;
    j = array[i];
    temp = array[i];
    array[i] = array[j];
    array[j] = temp;
    i += 1;
    j += array[i];
    temp = array[i];
    array[i] = array[j];
    array[j] = temp;
    return array[(array[i] + array[j]) & 0xFF];
}

static void encrypt(uint8_t* output, uint8_t const* input, size_t size) {
    for (size_t i = 0; i < size; ++i) {
        output[i] = get_random_byte() ^ (uint8_t)(i+1) ^ input[i];
    }
}

static long get_file_size(FILE* stream) {
    // tutaj nie ma co szukać, po prostu poznaję długość pliku 
    fseek(stream, 0, SEEK_END);
    long size = ftell(stream);
    rewind(stream);
    return size;
}

int main() {
    FILE* flag_file = fopen(FLAG_FILE, "r");
    if (flag_file == NULL) {
        printf("Skontaktuj się z adminami, bo coś ewidentnie nie działa\n");
        exit(1);
    }
    long size = get_file_size(flag_file);
    uint8_t *flag = malloc(size);
    uint8_t *encrypted_flag = malloc(size);
    fread((char*)flag, sizeof *flag, size, flag_file);
    while (getchar() != EOF) {
        encrypt(encrypted_flag, flag, size);
        for (long i = 0; i < size; ++i) {
            printf("%02X", encrypted_flag[i]);
        }
        printf("\n");
    }
    free(flag);
    free(encrypted_flag);
}
