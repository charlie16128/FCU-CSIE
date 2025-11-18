#include <stdio.h>

int count = 0;
void bin(int n){
    if(n == 0){
        return 0;
    }
    bin(n / 2);
    if(n % 2 == 1){
        count++;
    }
    printf("%d",n % 2);
}

int main(){
    int i;
    while(scanf("%d",&i) && i != 0){
        printf("The parity of ");
        count = 0;
        bin(i);
        printf(" is %d (mod 2).\n",count);
    }
    return 0;
}


/*
#include <stdio.h>

void bin(int n,int *count){
    if(n == 0){
        return;
    }
    bin(n / 2, count);
    if(n % 2 == 1){
        (*count)++;
    }
    printf("%d",n % 2);
}

int main(){
    int i;
    while(scanf("%d",&i) && i){
        printf("The parity of ");
        int count = 0;
        bin(i, &count);
        printf(" is %d (mod 2).\n",count);
    }
    return 0;
}
*/