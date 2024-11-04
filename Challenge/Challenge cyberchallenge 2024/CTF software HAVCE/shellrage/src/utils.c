#include "utils.h"
#include <stdio.h>

void prompt(char *prompt) {
  puts(prompt);
  printf("%s", "> ");
}

void disable_buffering() {
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);
}

int read_int() {
  int out;
  if (scanf("%d", &out) == EOF) {
    return -1;
  }

  char c = 'a';

  while (c != '\n') {
    c = fgetc(stdin);
  }
  return out;
}
