#include <unistd.h>
#include <stdio.h>

void debug() {
  execve("/bin/sh", NULL, NULL);
}

void setup() {
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);
}

int main() {
  char buf[32];

  setup();

  printf("Come ti chiami? ");
  read(0, buf, 0x100);

  printf("Ho capito bene? Ti chiami ");
  printf(buf);
  puts("");
  read(0, buf, 0x100);

  puts("Ok, ciao!");
  return 0;
}