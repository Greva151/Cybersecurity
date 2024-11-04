#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

void win() {
  execve("/bin/sh", NULL, NULL);
}

void setup() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
}

int chal() {
  puts("havce number storage v1.0");
  puts("You have 16 slots to save your data. Use them safely!");

  long long index = LONG_MAX;
  long long storage[16];

  memset(storage, 0, sizeof(storage));

  do {
    int choice = 0;
    index = LONG_MAX;

    while (index >= 16) {
      printf("Enter the index you want to interact with\n> ");
      scanf("%lld", &index);
    }

    for (choice = 0; choice != 1 && choice != 2 ;) {
      printf("What do you want to do?\n1) edit\n2) view\n> ");
      scanf("%d", &choice);
    }

    if (choice == 1) {
      long long prev_content = storage[index];

      printf("Enter the new content: ");
      scanf("%lld", &storage[index]);

      printf("Successfully edited storage[%lld], from 0x%016llx->0x%016llx\n", index, prev_content, storage[index]);
    } else if (choice == 2) {
      printf("Content of storage index: %lld: 0x%016llx\n", index,
             storage[index]);
    }

    for (choice = 0; choice != 1 && choice != 2; ) {
      printf("What do you want to do?\n1) continue\n2) exit\n> ");
      scanf("%d", &choice);
    }

    if (choice == 2) {
      return 0;
    }
  } while (1);
}

int main() {
  setup();

  return chal();  
}
