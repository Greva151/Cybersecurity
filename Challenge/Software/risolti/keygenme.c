//Gregorio Maria Vallé 5^C Informatica 22/09/2023

#include <stdio.h>
#include <string.h>

void pairStrings(char *password, char *id0, char *id1, int n);
void makeSerial(char *id, char *password); 

int main(){
    char id[32] = {0}; 
    char password[64] = {0}; 
    
    printf("User id: "); 
    fgets(id, 32, stdin); 

    makeSerial(id, password);

    printf("password: %s", password); 

    return 0; 
}


void pairStrings(char *password, char *id0, char *id1, int n){
    int padding = 0;
    int i = 0;
    int c = 0;

    while ((i < n || (c < n))) {
        if ((padding & 1) == 0) {
            *(padding + password) = *(i + id0);
            padding = padding + 1;
            i = i + 1;
        }
        else {
            *(padding + password) = *(c + id1);
            padding = padding + 1;
            c = c + 1;
        }
    }
}


void makeSerial(char *id, char *password){
    pairStrings(password, id + 18, id + 9, 8);
    pairStrings(password + 16, id, id + 18, 8);
    pairStrings(password + 32, id + 9, id, 8);
    *(password + 48) = 0;
}