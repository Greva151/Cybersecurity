#include <stdio.h>

int main(){
    char str[] = "\x95\x63\x7f\x9d\x33\xb2\xd9\x57\x3c\xe3\x34\xec\x70\x63\x30\x2c\xb6\x9f\x44\x70\xa0\xbe\x78\xf7\xb9\0";
    char flag[] = "flag{";
    for(int i = 0; i < 5; i++)
        printf("%x\n", flag[i] ^ (str[i] & 0xff));
    return 0; 
}