#include <stdio.h>

int main() {
    int num;

    while(1){
        scanf("%d", &num);
        if (num == 0){
            break;
        }

        int input[5000] = {0};
        int max = 0;
        for (int i = 0; i < num; i++) {
            scanf("%d", &input[i]);
            if(input[i] > max){
                max = input[i];
            }
        }
        //¤j¨ì¤p
        for (int i = 0; i < num - 1; i++) {
            for (int j = 0; j < num - i - 1; j++) {
                if (input[j] < input[j + 1]) {
                    int temp = input[j];
                    input[j] = input[j + 1];
                    input[j + 1] = temp;
                }
            }
        }

        int hIndex = 0;
        int k = 0;
        for (int i = 0; i < num; i++){
            if(input[i] >= k + 1){
                hIndex = k + 1; 
            } 
            else{
                break; 
            }
            k++;
        }

        printf("%d\n", hIndex);
    }

    return 0;
}
