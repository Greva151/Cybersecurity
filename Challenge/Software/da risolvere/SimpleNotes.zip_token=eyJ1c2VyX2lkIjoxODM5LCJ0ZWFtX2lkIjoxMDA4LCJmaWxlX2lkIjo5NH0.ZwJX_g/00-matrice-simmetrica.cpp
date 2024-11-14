#include <iostream>
using namespace std; 

int main(){	
	int n; 

	do{
		cout << "Inserisci la dimensione della matrice (N*N): "; 
		cin >> n; 

		if(n < 2)
			cout << "Errore: dimensione non valida" << endl; 
	}while(n < 2); 

	int matrice[n][n];

	for(int i = 0; i < n; i++)
		for(int j = 0; j < n; j++){
			cout << "Inserisci il valore (" << i << ", " << j << ") della matrice: "
			cin >> matrice[i][j]; 
		} 

	bool flag = true; 

	for(int i = 0; i < n; i++)
		for(int j = 0; j < n; j++)
			if(matrice[i][j] != matrice[j][i]){
				flag = false; 
				break; 
			}
	
	if(flag)
		cout << "la matrice è simmetrica" << endl;
	else
		cout << "la matrice non è simmetrica" << endl; 

	return 0; 
}