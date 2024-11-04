#include "auth.h"
#include "context.h"
#include "utils.h"
#include <dirent.h>
#include <fcntl.h>
#include <limits.h>
#include <seccomp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

// Only read and write are permitted.
int owner_privileges() {
  int rc = -1;
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL);

  rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  if (rc < 0) {
    goto out;
  }

  rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  if (rc < 0) {
    goto out;
  }

  rc = seccomp_load(ctx);
  if (rc < 0) {
    goto out;
  }

out:
  seccomp_release(ctx);
  return -rc;
}

// Both read and write are permitted, plus the open syscall.
int debug_privileges() {
  int rc = -1;
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL);

  rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
  if (rc < 0) {
    goto out;
  }

  rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  if (rc < 0) {
    goto out;
  }

  rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  if (rc < 0) {
    goto out;
  }

  rc = seccomp_load(ctx);
  if (rc < 0) {
    goto out;
  }

out:
  seccomp_release(ctx);
  return -rc;
}

// Only the open and read syscall is enabled.
int shared_privileges() {
  int rc = -1;
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL);

  rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
  if (rc < 0) {
    goto out;
  }

  rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  if (rc < 0) {
    goto out;
  }

  // No write!

  rc = seccomp_load(ctx);
  if (rc < 0) {
    goto out;
  }
out:
  seccomp_release(ctx);
  return -rc;
}

int drop_privileges(SHCContext *ctx) {
  switch (ctx->privilege_level) {
  case Owner:
    return owner_privileges();
  case Debug:
    return debug_privileges();
  default:
    return shared_privileges();
  }
}

int load_shellcode(SHCContext *ctx, char *path) {
  if ((ctx == NULL) || (path == NULL)) {
    return 0;
  }

  int fd;
  char buf[600];

  if ((fd = open(path, O_RDONLY)) == -1) {
    perror("open");
    return 0;
  }

  if (read(fd, buf, sizeof(buf)) == -1) {
    perror("read");
    return 0;
  }

  strcpy(ctx->shellcode, buf);

  close(fd);

  return 1;
}

void shc_show_menu() {
  puts("> 1. List all shellcodes");
  puts("> 2. Execute a shellcode");
  puts("> 3. Create a shellcode");
  puts("> 4. Execute a friend's shellcode");
  puts("> 5. Exit");
  printf(">> ");
}

void list(Auth *auth) {
  char path[PATH_MAX];
  snprintf(path, sizeof(path), "%s/%s/shc", BASE_PATH, auth->token);
  DIR *d;

  struct dirent *dir;

  puts("This is the list of the currently available shellcodes: ");
  if ((d = opendir(path)) == NULL) {
    perror("opendir");
    return;
  }

  // Iterate over files.
  while ((dir = readdir(d)) != NULL) {
    // Print only files
    if (dir->d_type == DT_REG) {
      printf(" - %s\n", dir->d_name);
    }
  }
  closedir(d);
  putchar('\n');
}

void launch_shc(SHCContext *ctx) {
  pid_t pid, w;

  switch (pid = fork()) {
  case -1:
    perror("fork");
    return;
  case 0:
    printf("Launching the %s shellcode.\n", ctx->path);

    void *code = mmap(0, 0x10000, PROT_EXEC | PROT_READ | PROT_WRITE,
                      MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);

    memcpy(code, ctx->shellcode, sizeof(ctx->shellcode));

    if (drop_privileges(ctx) == -1) {
      puts("Couldn't drop privileges.");
      exit(1);
    }   

    ((void (*)(void))(code))();
    exit(0);
  default:
    w = waitpid(pid, NULL, 0);
    if (w == -1) {
      perror("waitpid");
      return;
    }

    printf("Shellcode %s has finished executing.\n", ctx->path);
  }
}

void execute(Auth *auth) {
  prompt("Which shellcode do you want to execute?");
  int shcn = read_int();

  char path[PATH_MAX];
  snprintf(path, sizeof(path), "%s/%s/shc/%d", BASE_PATH, auth->token, shcn);

  SHCContext *ctx = new_ctx_from_path(auth, path, Owner);

  if (!load_shellcode(ctx, path)) {
    goto out;
  }

  launch_shc(ctx);
out:
  free_ctx(ctx);
}

void execute_shared(Auth *auth) {
  unsigned long long share_token = 0;
  prompt("Enter the share token:");
  scanf("%llu", &share_token);

  prompt("Which shellcode do you want to execute?");
  int shcn = read_int();

  char path[PATH_MAX];
  snprintf(path, sizeof(path), "%s/%llx/shc/%d", BASE_PATH, share_token, shcn);

  SHCContext *ctx = new_ctx_from_path(auth, path, Shared);

  if (!load_shellcode(ctx, path)) {
    goto out;
  }

  launch_shc(ctx);
out:
  free_ctx(ctx);
}

void create(Auth *auth) {
  prompt("Enter the shellcode number you want to create:");
  int shcn = read_int();

  char path[PATH_MAX];
  snprintf(path, sizeof(path), "%s/%s/shc/%d", BASE_PATH, auth->token, shcn);

  int fd;
  if ((fd = open(path, O_RDWR | O_CREAT | O_EXCL, 0777)) == -1) {
    perror("open");
    return;
  }

  char buf[800];
  prompt("Insert the raw bytes of the shellcode:");
  read(STDIN_FILENO, buf, sizeof(buf));
  write(fd, buf, sizeof(buf));

  close(fd);
}

void shellcodes(Auth *auth) {
  for (;;) {
    shc_show_menu();
    int choice = read_int();

    switch (choice) {
    case 1:
      list(auth);
      break;
    case 2:
      execute(auth);
      break;
    case 3:
      create(auth);
      break;
    case 4:
      execute_shared(auth);
      break;
    case 5:
      return;
    default:
      break;
    }
  }
}
