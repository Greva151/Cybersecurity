#include "auth.h"
#include <stdlib.h>
#include <string.h>

Auth *duplicate_auth(Auth *auth) {
  Auth *copy = malloc(sizeof(Auth));
  strncpy(copy->token, auth->token, sizeof(copy->token));
  strncpy(copy->user, auth->user, sizeof(copy->user));
  strncpy(copy->pass_to_check, auth->pass_to_check,
          sizeof(copy->pass_to_check));
  strncpy(copy->pass, auth->pass, sizeof(copy->pass));
  return copy;
}