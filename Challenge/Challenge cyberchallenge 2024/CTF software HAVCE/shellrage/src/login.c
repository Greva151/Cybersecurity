#include "auth.h"
#include "shellcode.h"
#include "utils.h"
#include <errno.h>
#include <limits.h>
#include <linux/limits.h>
#include <stdio.h>
#include <string.h>
#include <sys/random.h>
#include <sys/stat.h>

void reg() {
  char user[BUF_LEN];
  char pass[BUF_LEN];
  char token[BUF_LEN];
  unsigned long long tokint;

  prompt("Insert your username (max 31 chars):");
  fgets(user, sizeof(user), stdin);

  prompt("Insert your password (max 31 chars):");
  fgets(pass, sizeof(pass), stdin);

  // Remove trailing newlines
  user[strcspn(user, "\n")] = 0;
  pass[strcspn(pass, "\n")] = 0;

  // Generate login token, 8 bytes of randomness should be enough.
  getrandom(&tokint, sizeof(tokint), 0);
  snprintf(token, sizeof(token), "%llx", tokint);

  char pathdir[PATH_MAX];
  char pathuser[PATH_MAX];
  char pathpass[PATH_MAX];
  char pathshc[PATH_MAX];
  snprintf(pathdir, sizeof(pathdir), "%s/%s", BASE_PATH, token);
  snprintf(pathuser, sizeof(pathuser), "%s/%s/%s", BASE_PATH, token, "user");
  snprintf(pathpass, sizeof(pathpass), "%s/%s/%s", BASE_PATH, token, "pass");
  snprintf(pathshc, sizeof(pathshc), "%s/%s/%s", BASE_PATH, token, "shc");

  // Better to ask forgiveness than permission.
  if (mkdir(pathdir, 0700) == -1) {
    // Collision?
    perror("mkdir");
    return;
  }

  if (mkdir(pathshc, 0700) == -1) {
    perror("mkdir");
    return;
  }

  FILE *usr, *pss;
  if ((usr = fopen(pathuser, "w+")) == NULL) {
    perror("fopen");
    return;
  }

  if ((pss = fopen(pathpass, "w+")) == NULL) {
    perror("fopen");
    return;
  }

  // Write the username and password inside.
  fputs(user, usr);
  fputs(pass, pss);
  fclose(usr);
  fclose(pss);

  printf("Hi %s, here's your login token: %llu\n", user, tokint);
}

void login() {
  Auth auth_data;

  unsigned long long tokint = 0;

  prompt("Please enter your login token:");
  if (scanf("%llu", &tokint) < 1) {
    puts("Invalid token.");
    return;
  }

  // Encode it to hex.
  snprintf(auth_data.token, sizeof(auth_data.token), "%llx", tokint);

  char pathuser[PATH_MAX];
  char pathpass[PATH_MAX];
  snprintf(pathuser, sizeof(pathuser), "%s/%s/%s", BASE_PATH, auth_data.token,
           "user");
  snprintf(pathpass, sizeof(pathpass), "%s/%s/%s", BASE_PATH, auth_data.token,
           "pass");

  FILE *usr, *pss;
  if ((usr = fopen(pathuser, "r")) == NULL) {
    perror("fopen");
    return;
  }

  if ((pss = fopen(pathpass, "r")) == NULL) {
    perror("fopen");
    return;
  }

  fgets(auth_data.user, sizeof(auth_data.user), usr);
  fclose(usr);

  fgets(auth_data.pass, sizeof(auth_data.pass), pss);
  fclose(pss);

  printf("Welcome back, %s!\n", auth_data.user);

  // Ask user for their password.
  prompt("Insert your password:");
  scanf("%32s", auth_data.pass_to_check);

  if (strncmp(auth_data.pass, auth_data.pass_to_check,
              sizeof(auth_data.pass)) != 0) {
    puts("You're not authorized!");
    return;
  }

  shellcodes(&auth_data);
}