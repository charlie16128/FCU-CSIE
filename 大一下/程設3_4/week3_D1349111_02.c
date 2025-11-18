#include <stdio.h>

void swap(int *a, int *b){
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main(){
    int tc;
    while(scanf("%d",&tc) != EOF){
        int input[1000];
        for(int i = 0; i < tc; i++){
            scanf("%d",&input[i]);
        }

        int counter = 0;
        for(int i = 0; i < tc - 1 ; i++){
            for(int k = 0; k < tc - i - 1; k++){
                if(input[k] > input[k + 1]){
                    swap(&input[k], &input[k + 1]);
                    counter++;
                }
            }
        }
        printf("Minimum exchange operations : %d\n", counter);
    }
    return 0;
}