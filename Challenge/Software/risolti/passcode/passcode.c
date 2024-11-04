#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void setup() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
}

void print_flag() {
  char buf[0x100];

  FILE* flag = fopen("/home/user/flag", "r");
  if (flag == NULL) {
    perror("fopen");
    exit(EXIT_FAILURE);
  }

  fgets(buf, 0x100, flag);
  fputs(buf, stdout);
}

#define UNAUTHORIZED 0
#define AUTHORIZED 0x13371338

typedef struct {
  char token[64];
  int auth;
} auth_t;

int main() {
  puts("havce password manager v1.0");
  printf("Enter your token here: ");

  char* username = malloc(70);
  if (username == NULL) {
    perror("malloc");
    exit(EXIT_FAILURE);
  }

  fgets(username, 70, stdin);

  auth_t auth = {
    .token = {},
    .auth = UNAUTHORIZED,
  };
 
  strcpy(auth.token, username);
  // TODO: implement proper token validation.

  if (auth.auth == UNAUTHORIZED) {
    puts("You're not authorized. Please retry another time.");
    exit(EXIT_FAILURE);
  }

  print_flag();
}
