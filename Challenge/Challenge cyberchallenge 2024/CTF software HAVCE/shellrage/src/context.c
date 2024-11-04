#include "context.h"
#include <stdlib.h>
#include <string.h>

void free_ctx(SHCContext *ctx) {
  free(ctx->path);
  free(ctx->auth);
  free(ctx);
}

SHCContext *new_ctx_from_path(Auth *auth, char *path, Level level) {
  if ((auth == NULL) || (path == NULL)) {
    return NULL;
  }

  SHCContext *ctx = malloc(sizeof(SHCContext));

  ctx->auth = duplicate_auth(auth);
  ctx->privilege_level = level;
  ctx->path = strdup(path);

  return ctx;
}