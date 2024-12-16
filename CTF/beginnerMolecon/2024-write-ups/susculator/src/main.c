#include <stdio.h>
#include <stdlib.h>

#define RED "\e[0;31m"
#define GRN "\e[0;32m"
#define YEL "\e[0;33m"
#define BLU "\e[0;34m"
#define MAG "\e[0;35m"
#define CYN "\e[0;36m"

#define reset "\e[0m"

unsigned int hash(unsigned int x) {
    x = ((x >> 16) ^ x) * 0xd0b75cd2;
    x = ((x >> 16) ^ x) * 0xd0b75cd2;
    x = (x >> 16) ^ x;
    return x;
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    unsigned int hashvalue = 2740211888;
    printf(RED"\n\n  /$$$$$$  /$$   /$$  /$$$$$$   /$$$$$$  /$$   /$$ /$$        /$$$$$$  /$$$$$$$$ /$$$$$$  /$$$$$$$ \n"
           " /$$__  $$| $$  | $$ /$$__  $$ /$$__  $$| $$  | $$| $$       /$$__  $$|__  $$__//$$__  $$| $$__  $$\n"
           "| $$  \\__/| $$  | $$| $$  \\__/| $$  \\__/| $$  | $$| $$      | $$  \\ $$   | $$  | $$  \\ $$| $$  \\ $$\n"
           "|  $$$$$$ | $$  | $$|  $$$$$$ | $$      | $$  | $$| $$      | $$$$$$$$   | $$  | $$  | $$| $$$$$$$/\n"
           " \\____  $$| $$  | $$ \\____  $$| $$      | $$  | $$| $$      | $$__  $$   | $$  | $$  | $$| $$__  $$\n"
           " /$$  \\ $$| $$  | $$ /$$  \\ $$| $$    $$| $$  | $$| $$      | $$  | $$   | $$  | $$  | $$| $$  \\ $$\n"
           "|  $$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$/| $$$$$$$$| $$  | $$   | $$  |  $$$$$$/| $$  | $$\n"
           " \\______/  \\______/  \\______/  \\______/  \\______/ |________/|__/  |__/   |__/   \\______/ |__/  |__/\n"
           "                                                                                                   \n\n"reset);

    printf(CYN" !!!!This may look like a normal calculator program, and it actually is lol!!!!\n\n"reset);
    printf("1: addition (+)\n");
    printf("2: subtraction (-)\n");
    printf("3: multipliation (*)\n");
    printf("4: division (/)\n\n/>");

    unsigned int scelta;

    scanf("%ud", &scelta);

    if(scelta < 1 || scelta > 4){
        if(scelta == 1337){
            printf("Nice, an easter egg!!\n");
            exit(0);
        }
        if((hash(scelta) != hashvalue)){
		printf(RED"Incorrect input!\n"reset);
		exit(0);
        }else{
            printf(RED "O" GRN "M" YEL "G" BLU " " MAG "U" CYN " " RED "R" GRN "L" YEL "Y"
                   BLU " " MAG "A" CYN " " RED "h" GRN "4" YEL "c" BLU "k" MAG "3" CYN "r"
                   RED "z" "\n"reset);
            FILE *flag;
            flag = fopen("flag.txt", "r");
            if (flag == NULL){
                printf("You need to ha ve a file called 'flag.txt' in the same folder as this executable!\n");
                exit(1);
            }
            char stringa[50];
            fscanf(flag, "%s", stringa);
            printf("%s \n", stringa);
            exit(0);
        }
    }

    float num1 = 0;
    float num2 = 0;

    printf(MAG"Please, insert the 2 numbers this way: <num1> <num2>\n/>"reset);


    if (scanf("%f %f", &num1, &num2) != 2) {
        printf("Error: insert two numbers in the calculator prompt.\n");
        exit(1);
    }
    float result;

    switch(scelta) {
        case 1:
            result = num1 + num2;
            break;

        case 2:
            result = num1 - num2;
            break;

        case 3:
            result = num1 * num2;
            break;

        case 4:
            if (num2 == 0) {
                printf("You tought you could do that, cowboy?\n");
                exit(0);
            }
            result = num1 / num2;
            break;
    }
    printf("Here the result %.4f \n", result);
    return 0;
}
