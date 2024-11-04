#include <stdio.h>
#include <string.h>

#define GRID_SIZE 6

char grille[GRID_SIZE][GRID_SIZE];

void reverse_rotate() {
    char temp[GRID_SIZE][GRID_SIZE];
    for (int i = 0; i < GRID_SIZE; i++) {
        for (int j = 0; j < GRID_SIZE; j++) {
            temp[i][j] = grille[GRID_SIZE-j-1][i];
        }
    }
    memcpy(grille, temp, sizeof(temp));
}

void print_grille() {
    for (int i = 0; i < GRID_SIZE; i++) {
        for (int j = 0; j < GRID_SIZE; j++) {
            printf("%c", grille[i][j]);
        }
        printf("\n");
    }
}

int main() {
    // Riempie la griglia con la chiave criptata (da sostituire con la tua chiave criptata effettiva)
    const char* encrypted_key = "JSPZZ8U4N554BOWAO6NP6WWS5GGS9M67AZCJ";
    int secret[] = {0, 1, 1, 1, 1, 3, 3, 1, 3, 3, 4, 5, 5, 0, 5, 2, 5, 3};  // Da aggiornare con i tuoi valori reali

    // Simula il popolamento della griglia basandosi sui valori secret
    for (int i = 0; i < 18; i += 2) {
        int row = secret[i];
        int col = secret[i + 1];
        grille[row][col] = encrypted_key[i / 2];
    }

    // Applica la rotazione inversa per riportare la griglia allo stato originale
    for (int i = 0; i < 4; i++) {
        reverse_rotate();
    }

    // Stampa la griglia per verificare se corrisponde alla chiave originale
    print_grille();

    return 0;
}
