#include <stdio.h>

void soluzione(char *caratteri);

int main(){
    char asciiArray[128];

    for(int i = 0; i < 128; i++) asciiArray[i] = i;

    soluzione(asciiArray); 

    return 0; 
}

void soluzione(char *caratteri){

    printf("%c", 204/2);
    printf("%c", 216/2);
    printf("%c", 194/2);
    printf("%c", 206/2);
    printf("%c", 246/2);
    printf("%c", 200/2);
    printf("%c", 102/2);
    printf("%c", 232/2);
    printf("%c", 202/2);
    printf("%c", 228/2);
    printf("%c", 218/2);
    printf("%c", 210/2);
    printf("%c", 220/2);
    printf("%c", 194/2);
    printf("%c", 220/2);
    printf("%c", 232/2);
    printf("%c", 202/2);
    printf("%c", 190/2);
    printf("%c", 96/2);
    printf("%c", 250/2);

}