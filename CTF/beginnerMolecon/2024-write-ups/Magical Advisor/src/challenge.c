#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

void read_flag(char *s) {
    FILE *fp = fopen("./flag.txt", "r");
    fread(s, 1, 100, fp);
    fclose(fp);
}

void challenge(char secret[100]) {
    bool r[8];
    long int A[8][8] = {
        {1368, 1772, 1577, 1536, 1343, 1193, 1039, 1336},
        {1540, 1864, 1263, 1009, 1257, 1901, 1031, 1071},
        {1418, 1995, 1692, 1533, 1330, 1866, 1065, 1619},
        {1890, 1717, 1396, 1880, 1145, 1790, 1351, 1917},
        {1262, 1537, 1748, 1375, 1927, 1056, 1633, 1573},
        {1099, 1954, 1606, 1640, 1345, 1689, 1984, 1427},
        {1078, 1583, 1507, 1640, 1287, 1113, 1275, 1798},
        {1518, 1057, 1703, 1696, 1642, 1532, 1921, 1210}
    };
    long int b[8] = {38229434, 37289959, 42779314, 45094892, 41480368, 43384348, 38797458, 41751617};
    long int rows[8], x[8];

    printf("Give me 8 numbers: ");
    scanf("%ld %ld %ld %ld %ld %ld %ld %ld", &x[0], &x[1], &x[2], &x[3], &x[4], &x[5], &x[6], &x[7]);

    for (int i=0; i<8; i++) {
        rows[i] = 0;
        for (int j=0; j<8; j++) rows[i] += A[i][j] * x[j];

        r[i] = rows[i] == b[i];
    }

    if (r[0] && r[1] && r[2] && r[3] && r[4] && r[5] && r[6] && r[7]) {
        printf("Here's your flag: %s\n", secret);
    } else {
        printf("Wrong, try again.\n");

        srand(time(NULL));
        int advice_index = rand() % 15;
        switch (advice_index)
        {
        case 0:
            printf("Hint: Add 45 to the 4th input.\n");
            break;
        case 1:
            printf("Hint: Multiply the 6th input by 34.\n");
            break;
        case 2:
            printf("Hint: Subtract 12 from the 2nd input.\n");
            break;
        case 3:
            printf("Hint: Divide the 8th input by 6.\n");
            break;
        case 4:
            printf("Hint: Add 1031 to the 1st input.\n");
            break;
        case 5:
            printf("Hint: Subtract 176 from the 3rd input.\n");
            break;
        case 6:
            printf("Hint: Multiply the 9th input by 6.\n");
            break;
        case 7:
            printf("Hint: Add 297 to the 5th input.\n");
            break;
        case 8:
            printf("Hint: Divide the 10th input by 4.\n");
            break;
        case 9:
            printf("Hint: Multiply the 2nd input by 15.\n");
            break;
        case 10:
            printf("Hint: Add 58 to the 7th input.\n");
            break;
        case 11:
            printf("Hint: Subtract 258 from the 8th input.\n");
            break;
        case 12:
            printf("Hint: Add 333 to the 6th input.\n");
            break;
        case 13:
            printf("Hint: Divide the 4th input by 65.\n");
            break;
        case 14:
            printf("Hint: Subtract 487 from the 1st input.\n");
            break;
        }
    }
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    char secret[100];
    memset(secret, 0, 100);

    read_flag(secret);

    challenge(secret);
}
