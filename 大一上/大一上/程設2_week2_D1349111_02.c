#include <stdio.h>

int main() {
    int num;
    scanf("%d", &num);

    while (num-- > 0) { 
        int input[1000] = {0};
        int size = 0; //size

        while (scanf("%d", &input[size++])){
            char c = getchar(); 
            if (c == '\n') {
                break;
            } 
        }
        
        //bbsort
        for (int i = 0; i < size - 1; i++){
            for (int j = 0; j < size - 1 - i; j++) {
                if (input[j] < input[j + 1]) {
                    int temp = input[j];
                    input[j] = input[j + 1];
                    input[j + 1] = temp;
                }
            }
        }

        /* test
        for(int i = 0; i < size; i++){
            printf("%d ",input[i]);
        }
        printf("\n");
        */

        int output[1000] = {0};
        int left = 0, right = size - 1; 

        for (int i = 0; i < size; i++){
            if(i % 2 == 0){
                output[left++] = input[i];
            }
            else if(i % 2 == 1){
                output[right--] = input[i];
            }
        }

        for (int i = 0; i < size; i++) {
            printf("%d", output[i]);
            if (i < size - 1){
                printf(" ");
            }
        }
        printf("\n");
    }
    return 0;
}