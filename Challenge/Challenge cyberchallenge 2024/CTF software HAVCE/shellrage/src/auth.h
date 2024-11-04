#ifndef AUTH_H
#define AUTH_H
#include "utils.h"

typedef struct {
  char token[BUF_LEN];
  char user[BUF_LEN];
  char pass_to_check[BUF_LEN];
  char pass[BUF_LEN];
} Auth;

Auth *duplicate_auth(Auth *auth);

#endif
