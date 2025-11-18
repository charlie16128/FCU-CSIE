#include <stdio.h>
#include <string.h>

int main(){
    int num;
    char input[1000];
    int output[150] = {0};
    int counter = 0;
    
    scanf("%d",&num);
    getchar();
    
    while(fgets(input,1000,stdin) && num-- > 0){
        for(int i = 0; input[i] != '\0'; i++){
            if((char)input[i] != ' ' && (char)input[i] != '\n'){
                if(output[input[i]] == 0){
                    counter++;
                }
                output[input[i]]++;
            }
        }
    }
    
    printf("%d\n",counter);

    for(int i = 0; i < 128; i++){
        if(output[i] != 0){
            printf("%c %d\n",i,output[i]);
        }
    }

    return 0;
}