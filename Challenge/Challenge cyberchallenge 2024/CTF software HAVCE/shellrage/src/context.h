#ifndef CONTEXT_H
#define CONTEXT_H
#include "auth.h"

typedef enum {
  Owner = 0xdeadbeef,
  Shared = 0xcafebabe,
  Debug = 0x13371337
} Level;

typedef struct {
  Auth *auth;
  char *path;
  char shellcode[500];
  Level privilege_level;
  char unused[100];
} SHCContext;

// free_ctx frees the resources associated with the context.
void free_ctx(SHCContext *ctx);

// new_ctx creates a new shellcode context based on a path and
// a level of permissions.
SHCContext *new_ctx_from_path(Auth *auth, char *path, Level level);
#endif