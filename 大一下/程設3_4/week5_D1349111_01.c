#include <stdio.h>
#include <stdbool.h>
#include <string.h>

void check(int *a, int *b){
    if(*b < *a){
        int temp = *b;
        *b = *a;
        *a = temp;
    }
}

int main(){
    int tc, counter = 1;
    char input[1000005] = {0};
    while(scanf("%s",input) != EOF){ 
        printf("Case %d:\n",counter++);
        scanf("%d", &tc);
        if(tc < 0) break;
        
        int q1, q2;
        for(int i = 0; i < tc; i++){
            scanf("%d %d",&q1, &q2);
            check(&q1, &q2);

            bool same = true;
            char temp = input[q1];
            for(int k = q1; k <= q2; k++){
                if(input[k] != temp){
                    same = false;
                    break;
                }
            }
            //output
            if(same){
                printf("Yes\n");
            }else{
                printf("No\n");
            }
        }
    }
    return 0;
}

