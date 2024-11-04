#include <stdio.h>

void print_not_bitwise(char *array, size_t size) {
    for (size_t i = 0; i < size; i++) {
        putchar(~array[i]);
    }
    putchar('\n');
}

int main() {
    char array[] = {
        0xbc, 0xbc, 0xb6, 0xab,
        0x84, 0x98, 0x9b, 0x9d,
        0xa0, 0x8b, 0xcf, 0xa0,
        0x8b, 0x97, 0xcc, 0xa0,
        0x8d, 0x9a, 0xca, 0x9c,
        0x8a, 0x9a, 0x82, 0xff
    };
    
    size_t size = sizeof(array) / sizeof(array[0]);
    print_not_bitwise(array, size);
    
    return 0;
}
