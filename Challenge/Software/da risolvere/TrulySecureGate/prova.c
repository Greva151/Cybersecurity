#include <stdio.h>
#include <string.h>

int pack4(char* parametro1); 
void superalgoritm_block_next(char* array); 
void superalgoritm_init_block(char* array, char* parametro2, char* parametro3, int parametro4);
void superalgoritm_xor(char* array, char* parametro2, int parametro3);
unsigned int rotl32(unsigned int array,char parametro2); 

int main(){
	char array[192]; 
	memset(array, 0, 192);
	
	char parametro2[] = {0x61, 0x70, 0x65, 0x68, 0x74, 0x74, 0x6f, 0x6e, 0x6f, 0x6c, 0x64, 0x72, 0x6f, 0x77, 0x73, 0x73}; 
	char parametro3[] = {0x70, 0x61, 0x6c, 0x65, 0x63, 0x6e, 0x6f, 0x6e, 0x64, 0x72, 0x6f, 0x77, 0x73, 0x73, 0x61}; 
	char parametro4[] = {0x7d, 0x07, 0x82, 0x84, 0xc6, 0xb8, 0x0d, 0x13, 0xf5, 0x60, 0x2b, 0xdc, 0x98, 0x9a, 0x43, 0x57, 0xe0, 0xbc, 0x35, 0xb1, 0x87, 0x98, 0xba, 0x92, 0x72, 0xa3};
	
	superalgoritm_init_block(array, parametro2, parametro3, 0); 
	superalgoritm_xor(array, parametro4, 0x1b);

	for(int i = 0; i < 0x1a; i++){
		printf("%x ", parametro4[i]);
	}

	return 0; 
}

int pack4(char* parametro1){
	return *parametro1; 	
}

void superalgoritm_init_block(char* array, char* parametro2, char* parametro3, int parametro4){
	int uVar1;
	
	memcpy((void *)(array + 0x48),parametro2,0x20);
	memcpy((void *)(array + 0x68),parametro3,0xc);
	uVar1 = pack4("this is not magic");
	*(array + 0x80) = uVar1;
	uVar1 = pack4(" is not magic");
	*(array + 0x84) = uVar1;
	uVar1 = pack4("not magic");
	*(array + 0x88) = uVar1;
	uVar1 = pack4("magic");
	*(array + 0x8c) = uVar1;
	uVar1 = pack4(parametro2);
	*(array + 0x90) = uVar1;
	uVar1 = pack4(parametro2 + 4);
	*(array + 0x94) = uVar1;
	uVar1 = pack4(parametro2 + 8);
	*(array + 0x98) = uVar1;
	uVar1 = pack4(parametro2 + 0xc);
	*(array + 0x9c) = uVar1;
	uVar1 = pack4(parametro2 + 0x10);
	*(array + 0xa0) = uVar1;
	uVar1 = pack4(parametro2 + 0x14);
	*(array + 0xa4) = uVar1;
	uVar1 = pack4(parametro2 + 0x18);
	*(array + 0xa8) = uVar1;
	uVar1 = pack4(parametro2 + 0x1c);
	*(array + 0xac) = uVar1;
	*(array + 0xb0) = 0;
	uVar1 = pack4(parametro3);
	*(array + 0xb4) = uVar1;
	uVar1 = pack4(parametro3 + 4);
	*(array + 0xb8) = uVar1;
	uVar1 = pack4(parametro3 + 8);
	*(array + 0xbc) = uVar1;
	memcpy((void *)(array + 0x68),parametro3,0xc); 

	*(array + 0xb0) = parametro4;

	*(array + 0xb4) = *(array + 0x68); 

	*(array + 0x78) = parametro4;
  	*(array + 0x40) = 0x40;

}

unsigned int rotl32(unsigned int array,char parametro2){
  return array << (parametro2 & 0x1f) | array >> 0x20 - (parametro2 & 0x1f);
}


void superalgoritm_block_next(char* array){
	int uVar1; 

	for (int i = 0; i < 0x10; i++) {
		array[i] = array[i + 0x20];
	}

	for(int q = 0; q < 10; q++){
		*array = *array + array[4];
		uVar1 = rotl32(*array ^ array[0xc],0x10);
		array[0xc] = uVar1;
		array[8] = array[8] + array[0xc];
		uVar1 = rotl32(array[8] ^ array[4],0xc);
		array[4] = uVar1;
		*array = *array + array[4];
		uVar1 = rotl32(*array ^ array[0xc],8);
		array[0xc] = uVar1;
		array[8] = array[8] + array[0xc];
		uVar1 = rotl32(array[8] ^ array[4],7);
		array[4] = uVar1;
		array[1] = array[1] + array[5];
		uVar1 = rotl32(array[1] ^ array[0xd],0x10);
		array[0xd] = uVar1;
		array[9] = array[9] + array[0xd];
		uVar1 = rotl32(array[9] ^ array[5],0xc);
		array[5] = uVar1;
		array[1] = array[1] + array[5];
		uVar1 = rotl32(array[1] ^ array[0xd],8);
		array[0xd] = uVar1;
		array[9] = array[9] + array[0xd];
		uVar1 = rotl32(array[9] ^ array[5],7);
		array[5] = uVar1;
		array[2] = array[2] + array[6];
		uVar1 = rotl32(array[2] ^ array[0xe],0x10);
		array[0xe] = uVar1;
		array[10] = array[10] + array[0xe];
		uVar1 = rotl32(array[10] ^ array[6],0xc);
		array[6] = uVar1;
		array[2] = array[2] + array[6];
		uVar1 = rotl32(array[2] ^ array[0xe],8);
		array[0xe] = uVar1;
		array[10] = array[10] + array[0xe];
		uVar1 = rotl32(array[10] ^ array[6],7);
		array[6] = uVar1;
		array[3] = array[3] + array[7];
		uVar1 = rotl32(array[3] ^ array[0xf],0x10);
		array[0xf] = uVar1;
		array[0xb] = array[0xb] + array[0xf];
		uVar1 = rotl32(array[0xb] ^ array[7],0xc);
		array[7] = uVar1;
		array[3] = array[3] + array[7];
		uVar1 = rotl32(array[3] ^ array[0xf],8);
		array[0xf] = uVar1;
		array[0xb] = array[0xb] + array[0xf];
		uVar1 = rotl32(array[0xb] ^ array[7],7);
		array[7] = uVar1;
		*array = *array + array[5];
		uVar1 = rotl32(*array ^ array[0xf],0x10);
		array[0xf] = uVar1;
		array[10] = array[10] + array[0xf];
		uVar1 = rotl32(array[10] ^ array[5],0xc);
		array[5] = uVar1;
		*array = *array + array[5];
		uVar1 = rotl32(*array ^ array[0xf],8);
		array[0xf] = uVar1;
		array[10] = array[10] + array[0xf];
		uVar1 = rotl32(array[10] ^ array[5],7);
		array[5] = uVar1;
		array[1] = array[1] + array[6];
		uVar1 = rotl32(array[1] ^ array[0xc],0x10);
		array[0xc] = uVar1;
		array[0xb] = array[0xb] + array[0xc];
		uVar1 = rotl32(array[0xb] ^ array[6],0xc);
		array[6] = uVar1;
		array[1] = array[1] + array[6];
		uVar1 = rotl32(array[1] ^ array[0xc],8);
		array[0xc] = uVar1;
		array[0xb] = array[0xb] + array[0xc];
		uVar1 = rotl32(array[0xb] ^ array[6],7);
		array[6] = uVar1;
		array[2] = array[2] + array[7];
		uVar1 = rotl32(array[2] ^ array[0xd],0x10);
		array[0xd] = uVar1;
		array[8] = array[8] + array[0xd];
		uVar1 = rotl32(array[8] ^ array[7],0xc);
		array[7] = uVar1;
		array[2] = array[2] + array[7];
		uVar1 = rotl32(array[2] ^ array[0xd],8);
		array[0xd] = uVar1;
		array[8] = array[8] + array[0xd];
		uVar1 = rotl32(array[8] ^ array[7],7);
		array[7] = uVar1;
		array[3] = array[3] + array[4];
		uVar1 = rotl32(array[3] ^ array[0xe],0x10);
		array[0xe] = uVar1;
		array[9] = array[9] + array[0xe];
		uVar1 = rotl32(array[9] ^ array[4],0xc);
		array[4] = uVar1;
		array[3] = array[3] + array[4];
		uVar1 = rotl32(array[3] ^ array[0xe],8);
		array[0xe] = uVar1;
		array[9] = array[9] + array[0xe];
		uVar1 = rotl32(array[9] ^ array[4],7);
		array[4] = uVar1;
	}

	for (int i = 0; i < 0x10; i++) {
    	array[i] = array[i] + array[i + 0x20];
  	}
	int* puVar2; 
	puVar2 = (unsigned int *)array + 0x2c;
  	*puVar2 = *puVar2 + 1;
	array[0x2d] = array[0x2d] + 1; 
}


void superalgoritm_xor(char* array, char* parametro2, int parametro3){
	for(int i = 0; i < parametro3; i++){
		if('?' < *(array + 0x40)){
			superalgoritm_block_next(array);
			*(array + 0x40) = 0; 
		}
		
		*(i + parametro2) = *(i + parametro2) ^ *(array + *(array + 0x40)); 
		*(array + 0x40) = *(array + 0x40) + 1;
	}
}
