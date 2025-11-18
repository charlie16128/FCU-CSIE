#include <stdio.h>
#include <string.h>

int main(){
    int tc, blackline, check = 1;
    scanf("%d",&tc);
    getchar(); // wtf 靠北加了這就ac
    
    char input[100] = {0};
    while(tc--){
        fgets(input,100,stdin); // read the blackline
        fgets(input,100,stdin); 
        input[strcspn(input, "\n")] = 0; // idk
        
        int len = strlen(input);
        for(int i = 1; i <= len; i++){ // min repeat length
            if(len % i == 0){ // 要能整除才能循環
                check = 1;
                for(int k = i; k < len; k++){
                    if(input[k] != input[k % i]){
                        check = 0;
                        break;
                    }
                }
                if(check){
                    printf("%d\n",i);
                    break;
                }
            }
        }

        if(tc != 0){
            printf("\n");
        }
    }    
    return 0;
}