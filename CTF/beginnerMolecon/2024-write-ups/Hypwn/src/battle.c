#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdio.h>

void win(); 

typedef struct ally_pokemon
{
    char *name; 
    char *move; 
    int hp; 
    bool burnt; 
    bool can_move; 
    int atk_mul; 
    int has_protected; 

}AllyPokemon;

typedef struct enemy_pokemon 
{
    char *name; 
    char hp; 
    int atk_mul; 
    bool protected; 
}EnemyPokemon; 

/* SNORLAX MOVESET:         LUCARIO MOVESET:                    /* ARCEUS MOVESET:           MEWTWO MOVESET
    - protect                  - CalmMind                        - Judgment                  - Focus Blast
    - recover                  - AuraSphere                       - Flamethrower              - Psychic
    - bottintesta              - GigaImpact                        - Bodypress                 - Ice beam
    - GigaImpact                  - Protect                            - will-o-wisp               - Calm Mind         */

bool check_protect(int val) {
    if (val == 1) {
        int rand_n = rand() % 2; 
        return rand_n == 1; 
    } else if (val == 2) {
        int rand_n = rand() % 10; 
        return rand_n == 1; 
    } else {
        return false; 
    }
}

void battle(AllyPokemon *ally, EnemyPokemon *enemy) {
    char *ally_move = ally->move; 
    int rand_n = -1;  
    int damage; 

    if (!ally->can_move) {
        printf("%s must recover.\n", ally->name); 
        ally->can_move = true;  
    } else if (strcmp(ally->name, "Snorlax") == 0) {
        if (strcmp(ally_move, "Protect") == 0) {
            bool check = true; 
            printf("Snorlax use protect.\n"); 
            if (ally->has_protected) {
                check = check_protect(ally->has_protected); 
            }
            if (check) {
                rand_n = rand() % 2;
                if (strcmp(enemy->name, "Arceus")== 0) {
                    if (!rand_n) printf("Arceus use Flamethrower.\n");
                    else printf("Arceus use Bodypress\n"); 
                } else if (!strcmp(enemy->name, "Mewtwo")) {
                    if (!rand_n) printf("Mewtwo use Psychic!\n"); 
                    else printf("Mewtwo use Focus Blast!\n"); 
                } 
                printf("But Snorlax protect himself!\n"); 
                enemy->protected = true; 
                ally->has_protected++; 
            } else {
                printf("But Snorlax failed to protect himself!\n"); 
                ally->has_protected = 0;
            }
        } else if (!strcmp(ally_move, "Recover")) {
            printf("Snorlax use recover. He recover "); 
            if ((25 + ally->hp) > 100) {
                printf("%d HP!\n", 100-ally->hp); 
                ally->hp = 100; 
            } else {
            ally->hp += 25; 
            printf("25 HP!\n"); 
            }
        } else if (!strcmp(ally_move, "Headbutt")) {
            printf("Snorlax used Headbutt!\n");
            if (!strcmp(enemy->name, "Arceus")) {
                if (ally->burnt) damage = 7; 
                else damage = 15; 
                printf("Arceus loose %d HP!\n", damage);
                enemy->hp -= damage;  
            } else {
                damage = 20; 
                printf("Mewtoo loose 20 HP!\n"); 
                enemy->hp -= damage; 
            }
        } else {
            printf("Snorlax used Gigaimpact!\n"); 
            if (!strcmp(enemy->name, "Arceus")) {
                if (ally->burnt) damage = 20; 
                else damage = 35; 
                printf("Arceus loose %d HP!\n", damage);
            } else {
                damage = 48; 
                printf("Mewtwo loose 48 HP!\n"); 
            }
            enemy->hp -= damage; 
            ally->can_move = false; 
        }
    } else {

        if (strcmp(ally_move, "CalmMind") == 0) {
            printf("Lucario used Calm Mind!\n"); 
            printf("He now deals double the damage.\n"); 
            ally->atk_mul *= 2; 
        } else if (strcmp(ally_move, "AuraSphere") == 0) {
            printf("Lucario used Aura Sphere!\n"); 
            if (!strcmp(enemy->name, "Arceus")) {
                damage = 22 * ally->atk_mul; 
                if (ally->burnt) damage = damage / 2; 
                printf("Arceus loose %d HP!\n", damage); 
                printf("It's supereffective!\n"); 
                enemy->hp -= damage; 
            } else {
                damage = 10 * ally->atk_mul; 
                if (ally->burnt) damage = damage / 2; 
                printf("Mewtwo loose %d HP!\n", damage); 
                printf("But it is not very effective...\n"); 
                enemy->hp -= damage; 
            }
        } else if (!strcmp(ally_move, "Protect")) {
            printf("Lucario used Protect!\n"); 
            bool check = true; 
            if (ally->has_protected) {
                check = check_protect(ally->has_protected); 
            }
            if (check) {
                rand_n = rand() % 2; 
                if (strcmp(enemy->name, "Arceus") == 0) {
                    if (rand_n) printf("Arceus used Will-O-Wisp!\n"); 
                    else printf("Arceus used Flamethrower!\n"); 
                    printf("But Lucario protects himself!\n"); 
                    enemy->protected = true; 
                    ally->has_protected++;
                } else {
                    if (enemy->atk_mul == 1){
                        if (rand_n) {
                            printf("Mewtwo used Psychic!\n"); 
                            printf("But Lucario protects himself!\n"); 
                        } else {
                            printf("Mewtwo used Calm Mind!\n"); 
                            printf("He now deals double the damage.\n"); 
                            enemy->atk_mul *= 2; 
                        }
                        enemy->protected = true; 
                        ally->has_protected++;
                    } else {
                        printf("Mewtwo used Psychic!\n"); 
                        printf("But Lucario protects himself!\n");
                        enemy->protected = true;
                        ally->has_protected++;
                    }
                }
            } else {
                printf("But Lucario failed to protect himself!\n"); 
                ally->has_protected = 0; 
            }
        } else {
            printf("Lucario used Giga Impact!\n"); 
            if (strcmp(enemy->name, "Arceus") == 0) {
                damage = 20 * ally->atk_mul; 
                if (ally->burnt) damage /= 2; 
                printf("Arceus loose %d HP!\n", damage);
                enemy->hp -= damage; 
            } else {
                damage = 24 * ally->atk_mul; 
                printf("Mewtwo loose %d HP!\n", damage); 
                enemy->hp -= damage;
            }
            ally->can_move = false; 
        }
    }

    if(strcmp(ally->move, "Protect") != 0) {
        ally->has_protected = 0; 
    }

    if (enemy->hp <= 0) {
        printf("%s defeated %s!Congrats, here your prize!\n", ally->name, enemy->name); 
        win(); 
    }

    if (!enemy->protected) {

        if (!strcmp(enemy->name, "Arceus")) {
            if (!strcmp(ally->name, "Snorlax")) {
                if (!ally->burnt) {
                    printf("Arceus used Will-O-Wisp!\n"); 
                    printf("Snorlax is now burnt.\n"); 
                    ally->burnt = true; 
                } else {
                    printf("Arceus used Bodypress!\n"); 
                    printf("Snorlax loose 35 HP!\n"); 
                    printf("It's supereffective!\n"); 
                    ally->hp -= 35; 
                }
            } else if (!strcmp(ally->name, "Lucario")) {
                rand_n = rand() % 2;
                if (rand_n) {
                    printf("Arceus used Flamethrower!\n"); 
                    printf("Lucario loose 35 HP!\n"); 
                    printf("It's supereffective!\n"); 
                    ally->hp -= 35; 
                    rand_n = rand() % 2;
                    if (rand_n) {
                        printf("Lucario is now burnt!\n");
                        ally->burnt = true;
                    }
                } else {
                    printf("Arceus used Judgement!\n"); 
                    printf("Lucario loose 45 HP!\n"); 
                    ally->hp -= 45; 
                }
            }
        } else {
            if (!strcmp(ally->name, "Snorlax")) {
                if (enemy->atk_mul == 1) {
                    rand_n = rand() % 2; 
                    if (rand_n) {
                        printf("Mewtwo used Calm Mind!\n");
                        printf("He now deals double the damage.\n");
                        enemy->atk_mul *= 2;
                    } else {
                        printf("Mewtwo used Focus Blast!\n"); 
                        rand_n = rand() % 10; 
                        if (rand_n == 1) {
                            printf("But Snorlax dodged the attack!\n");
                        } else {
                            damage = 60 * enemy->atk_mul; 
                            ally->hp -= damage; 
                            printf("Snorlax loose %d HP!\n", damage); 
                        }
                    }
                    
                } else {
                    printf("Mewtwo used Focus Blast!\n"); 
                    rand_n = rand() % 10; 
                    if (rand_n == 1) {
                        printf("But Snorlax dodged the attack!\n");
                    } else {
                        damage = 60 * enemy->atk_mul; 
                        ally->hp -= 60; 
                        printf("Snorlax loose %d HP!\n", damage); 
                    }
                }
            } else if (!strcmp(ally->name, "Lucario")) {
                    if (enemy->atk_mul == 1) {
                        rand_n = rand() % 2;
                        if (rand_n) {
                            printf("Mewtwo used Calm Mind!\n");
                            printf("He now deals double the damage.\n");
                            enemy->atk_mul *= 2;
                        } else {
                            printf("Mewtwo used Psychic!\n"); 
                            damage = 45 * enemy->atk_mul; 
                            ally->hp -= damage; 
                            printf("Lucario loose %d HP!\n", damage); 
                        }
                    }
                    else {
                        printf("Mewtwo used Psychic!\n"); 
                        damage = 45 * enemy->atk_mul; 
                        ally->hp -= damage; 
                        printf("Lucario loose %d HP!\n", damage); 
                    }
            } 
        }

    }   

    if (!strcmp(enemy->name, "Arceus")) {
        printf("Arceus recover 3 HP from leftovers!\n"); 
        enemy->hp += 3;
    }

    if (ally->burnt) {
        printf("%s loose 5 HP for the burn!\n", ally->name);
        ally->hp -= 5;
    }

    if (ally->hp <= 0) {
        printf("%s fainted! Game over!\n", ally->name); 
        printf("GAME OVER\n");
    }
    if (enemy->hp <= 0) {
        printf("%s defeated %s! Congrats, here your prize!\n",ally->name, enemy->name); 
        win(); 
    } else {
        printf("%s: %d, %d, %d, %d, %d\n", ally->name, ally->hp, ally->burnt, ally->can_move, ally->atk_mul, ally->has_protected);
        printf("%s: %d, %d\n", enemy->name, enemy->hp, enemy->atk_mul);
    }

    printf("END\n"); 
}

void win() {
    FILE *file;
    char ch;

    file = fopen("flag.txt", "r");
    if (file == NULL) {
        perror("Errore nell'apertura del file");
        return;
    }

    while ((ch = fgetc(file)) != EOF) {
        putchar(ch);
    }

    printf("\n\n\n"); 

    fclose(file);
}

int main(int argc, char *argv[])
{
    if (argc != 11) {
        printf("Usage: %s ally_name, ally_hp, ally_burnt, ally_can_move, ally_atk_mul, ally_hasprotected, ally_move , enemy_name, enemy_hp, enemy_atk_mul\n", argv[0]);
        return 1;
    }

    AllyPokemon *ally = malloc(sizeof(AllyPokemon));
    EnemyPokemon *enemy = malloc(sizeof(EnemyPokemon));

    ally->name = argv[1];
    ally->hp = atoi(argv[2]);
    ally->burnt = atoi(argv[3]);
    ally->can_move = atoi(argv[4]);
    ally->atk_mul = atoi(argv[5]);
    ally->has_protected = atoi(argv[6]);
    ally->move = argv[7];

    enemy->name = argv[8];
    enemy->hp = atoi(argv[9]);
    enemy->atk_mul = atoi(argv[10]);
    enemy->protected = false; 

    battle(ally, enemy);


    return 0;
}
