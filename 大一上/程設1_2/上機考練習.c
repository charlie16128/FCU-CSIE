#include <stdio.h>
#include <stdlib.h>

int main(){
    int input;
    printf("PERFECTION OUTPUT\n");
    while(scanf("%d",&input) && input != 0){
        int total = 0;
        for(int i = 1; i < input; i++){
            if(input % i == 0){
                total += i;
            }
        }

        if(total == input){
            printf("%5d  PERFECT\n",input);
        }
        else if(total > input){
            printf("%5d  ABUNDANT\n",input);
        }
        else if(total < input){
            printf("%5d  DEFICIENT\n",input);
        }
    }
    printf("END OF OUTPUT");
    return 0;
}
