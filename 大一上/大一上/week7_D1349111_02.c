// #include <stdio.h>

// int main() {
//     int tcnum;
//     scanf("%d", &tcnum);  
//     for (int t = 0; t < tcnum; t++) {
//         int size,symmetric = 1;
//         int ; 
//         scanf("%d", &size);
    
//         int matrix[size][size];  

//         for (int i = 0; i < size; i++) { //input 
//             for (int j = 0; j < size; j++) {
//                 scanf("%d", &matrix[i][j]);
//             }
//         }

//         for (int i = 0; i < size; i++) { //ÀË¬d
//             for (int j = 0; j < size; j++) {
//                 if (matrix[i][j] != matrix[size - 1 - i][size - 1 - j]) {
//                     symmetric = 0;
//                 }
//             }
//         }

//         if (symmetric == 1) {
//             printf("Symmetric\n");
//         } else {
//             printf("Non-symmetric\n");
//         }
//     }
//     return 0;
// }



#include <stdio.h>
#include <string.h>

int main(){
    int testnum;
    scanf("%d",&testnum);
    for(int counter = 0; counter < testnum; counter++){
        int size = 0;
        scanf("%d",&size);

        int m[100][100];
        int input;

        for(int i = 0; i < size; i++){
            for(int k = 0; k < size; k++){
                scanf("%d",&input);
                m[i][k] = input;
            }
        }
        
        int judge = 1;
        for(int i = 0; i < size; i++){
            for(int k = 0; k < size; k++){
                if(m[i][k] != m[size -1 - i][size - 1 - k]){
                    judge = 0;
                    break;
                }
            }
        }

        if(judge == 1){
            printf("Symmetric\n");
        }
        else if (judge == 0){
            printf("Non-symmetric\n");
        }
    }

    return 0;    
}



