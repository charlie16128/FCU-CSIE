#include <stdio.h>

int main(){
    int num;
    scanf("%d", &num);

    int stack[100000]; 
    int top = -1;

    for(int i = 0; i < num; i++){
        int card;
        scanf("%d", &card);
        
        //至少一張牌
        if(top >= 0 && (stack[top] + card) % 2 == 0){
            top--;
        }
        else{
            stack[++top] = card;
        }
    }
    printf("%d\n", top + 1);
    return 0;
}
