#include <stdio.h>
#include <stdlib.h>
#include <string.h> 

int main(){
	char password[20];
	char input[20];  

	
	memset(password, 0, sizeof(password)); 
	memset(input, 0, sizeof(input)); 

	int var =  rand(); 
	
	printf("rand = %d", var); 

	var = var % 0x10 + 5; 

	for(int i = 0; i < var+1; i++){
		int r = rand();
		printf("\n%d", r);  
		password[i] = r + (r/0x2a)*(-0x2a) + '0'; 
	} 

	printf("\n%s\n", password); 

	scanf("%s", input); 

	printf("%d", strncmp(password, input, strlen(password))); 
	


	return 0; 
}
