#include <stdio.h>
#include <string.h>

int main(){
    char dacrip[] = {0x70, 0x4e, 0x34, 0xbb, 0xff, 0x99, 0xf3, 0xfe}; 
    char criptato[] = {0x6c, 0x00, 0xfa, 0xd8, 0xae, 0x0d, 0x60, 0x15};
    unsigned char chiave[9];
    memset(chiave, 0, 9);
    char dadecriptare[] = {0x50 , 0x2f , 0xee , 0x11 , 0x38 , 0xe7 , 0xe3 , 0x84 , 0x6f , 0x3a , 0xaf , 0x43, 0x34 , 0xb3 , 0xb3 , 0x8a , 0x7a , 0x28 , 0xab , 0x11 , 0x3c , 0xf5 , 0xe7 , 0x82 , 0x6a , 0x2f , 0xe2 , 0x43, 0x30 , 0xf3 , 0xf6 , 0x85 , 0x68 , 0x2b , 0xee , 0x53 , 0x29 , 0xa0 , 0xa1 , 0xc7 , 0x3c , 0x27 , 0xa2 , 0x43, 0x22 , 0xe1 , 0xfc , 0xcb , 0x6c , 0x27 , 0xaf , 0x0d , 0x3e , 0xb4 , 0xe0 , 0x8e , 0x71 , 0x2c , 0xbc , 0x02, 0x71 , 0xe4 , 0xf6 , 0x99 , 0x7a , 0x2b , 0xba , 0x17 , 0x3e , 0xb8 , 0xb3 , 0x87 , 0x7d , 0x6e , 0xaf , 0x16, 0x25 , 0xfb , 0xe1 , 0x82 , 0x66 , 0x34 , 0xa7 , 0x02 , 0x3c , 0xfb , 0xb3 , 0x8a , 0x3c , 0x3e , 0xbc , 0x0c, 0x32 , 0xf1 , 0xf7 , 0x8e , 0x6e , 0x2b , 0xe0 , 0x69 , 0x5b , 0xf2 , 0xff , 0x8a , 0x7b , 0x35 , 0xa6 , 0x53, 0x0e , 0xf8 , 0xa7 , 0xb4 , 0x6e , 0x7f , 0xfb , 0x13 , 0x61 , 0xa1 , 0xa4 , 0xdf , 0x30 , 0x11 , 0xa3 , 0x57, 0x0e , 0xe5 , 0xe6 , 0xdf , 0x70 , 0x11 , 0xfd , 0x3c , 0x3d , 0xa0 , 0xcc , 0x8f , 0x2c , 0x23 , 0xfa , 0x0d, 0x35 , 0xa0 , 0xac , 0x96 , 0x16 , 0x44 , 0x0a , 0x46 , 0x69 , 0x6e , 0x65 , 0x20 , 0x63 , 0x6f , 0x6d , 0x75, 0x6e , 0x69 , 0x63 , 0x61 , 0x7a , 0x69 , 0x6f , 0x6e , 0x65 , 0x0a}; 
     

    for(int i = 0; i < 9; ++i){
        chiave[i] = dacrip[i] ^ criptato[i];  
    }

    int c = 0; 
    for(int i = 0; i < strlen(dadecriptare); i++, c++){
        if(i % 8 == 0) c = 0; 
        printf("%c", dadecriptare[i] ^ chiave[c]); 
    }

    return 0; 
}

