#include <stdio.h>

int main(){
    int num;
    scanf("%d", &num);

    char input[1000][1000];
    int r, c, n;
    while(num--){
        scanf("%d %d %d", &r, &c, &n);

        for(int i = 0; i < r; i++){
            scanf("%s", input[i]);
        }

        for(int day = 0; day < n; day++){
            char temp[1000][1000];

            for(int i = 0; i < r; i++){
                for(int k = 0; k < c; k++){
                    temp[i][k] = input[i][k];

                    if(i > 0 && ((input[i-1][k] == 'R' && input[i][k] == 'S') || (input[i-1][k] == 'S' && input[i][k] == 'P') || (input[i-1][k] == 'P' && input[i][k] == 'R'))){
                        temp[i][k] = input[i-1][k];
                    }
                    if(i < r - 1 && ((input[i+1][k] == 'R' && input[i][k] == 'S') || (input[i+1][k] == 'S' && input[i][k] == 'P') || (input[i+1][k] == 'P' && input[i][k] == 'R'))){
                        temp[i][k] = input[i+1][k];
                    }
                    if(k > 0 && ((input[i][k-1] == 'R' && input[i][k] == 'S') || (input[i][k-1] == 'S' && input[i][k] == 'P') || (input[i][k-1] == 'P' && input[i][k] == 'R'))){
                        temp[i][k] = input[i][k-1];
                    }
                    if(k < c - 1 && ((input[i][k+1] == 'R' && input[i][k] == 'S') || (input[i][k+1] == 'S' && input[i][k] == 'P') || (input[i][k+1] == 'P' && input[i][k] == 'R'))){
                        temp[i][k] = input[i][k+1];
                    }
                }
            }

            for(int i = 0; i < r; i++){
                for(int k = 0; k < c; k++){
                    input[i][k] = temp[i][k];
                }
            }
        }

        for(int i = 0; i < r; i++){
            printf("%s\n", input[i]);
        }

        printf("\n");
    }
    return 0;
}