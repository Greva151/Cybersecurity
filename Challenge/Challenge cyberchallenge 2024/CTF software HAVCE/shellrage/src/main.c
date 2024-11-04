#include "login.h"
#include "utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

#define BASE_PATH "./data"

void logo() {
  puts("  ██████  ██░ ██ ▓█████  ██▓     ██▓     ██▀███   ▄▄▄        ▄████ "
       "▓█████ ");
  puts("▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    ▓██ ▒ ██▒▒████▄     ██▒ ▀█▒▓█  "
       " ▀ ");
  puts("░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    ▓██ ░▄█ ▒▒██  ▀█▄  "
       "▒██░▄▄▄░▒███   ");
  puts("  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    ▒██▀▀█▄  ░██▄▄▄▄██ ░▓█  ██▓▒▓█ "
       " ▄ ");
  puts("▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒░██▓ ▒██▒ ▓█   "
       "▓██▒░▒▓███▀▒░▒████▒");
  puts("▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ░▒   ▒ ░░ "
       "▒░ ░");
  puts("░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░  ░▒ ░ ▒░  ▒   ▒▒ ░  ░   ░  ░ "
       "░  ░");
  puts("░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░     ░░   ░   ░   ▒   ░ ░   ░    "
       "░   ");
  puts("      ░   ░  ░  ░   ░  ░    ░  ░    ░  ░   ░           ░  ░      ░    "
       "░  ░");
}

void banner() {
  puts("");
  puts("Welcome to the havce shellcode vault!");
  puts("Store your shellcodes and execute them.");
  puts("============================================");
  puts("If you want, after you submit a shellcode,");
  puts("you can share it with your friends, securely.");
}

void show_menu() {
  puts("> 1. Login");
  puts("> 2. Register");
  puts("> 3. Logout");
  printf(">> ");
}

void setup_folder() { mkdir(BASE_PATH, 0700); }

int main(int argc, char **argv) {
  disable_buffering();
  logo();
  banner();
  setup_folder();

  for (;;) {
    show_menu();
    int choice = read_int();
    if (choice == -1) {
      exit(1);
    }

    switch (choice) {
    case 1:
      login();
      break;
    case 2:
      reg();
      break;
    default:
      exit(0);
    }
  }
}
