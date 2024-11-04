#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int rating = 10;

void setup() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
}

int main() {
  setup();
  
  puts("Welcome to havce new show business format!");
  puts("Enter a joke and we will rate it out of ten.");

  char buf[0x100];

  printf("Tell us your joke here: ");
  fgets(buf, sizeof(buf), stdin);

  printf(buf);

  if (rating == 10) {
    puts("Nice joke! We rate it 10 out of 10.");
    return 0;
  }

  if (rating == 0x1337) {
    puts("This was 1337! Here's your shell.");
    execve("/bin/sh", NULL, NULL);
  }
}
