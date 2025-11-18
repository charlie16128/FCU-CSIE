#include <stdio.h>
#include <string.h>

int main(){
    int tc;
    scanf("%d",&tc);
    getchar();
    while(tc--){
        char input[100] = {};
        fgets(input, 100, stdin);
        int total = 0, score = 1;
        for(int i = 0; i < strlen(input); i++){
            if(input[i] == 'O'){
                total += score;
                score++;
            }else{
                score = 1;
            }
        }
        printf("%d\n",total);
    }
    return 0;
}