#include <locale.h>
#include <stdio.h>
#include <stdlib.h>

int main(){
  int prova; 
  void *a = malloc(0x20);
  void* b = malloc(0x20); 
  free(a);
  free(b);   
  return 0; 

}

