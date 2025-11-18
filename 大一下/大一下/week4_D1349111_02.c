#include <stdio.h>

void bangla(long long input){
    if(input >= 10000000){
        bangla(input / 10000000);
        printf(" kuti");
        input %= 10000000;
    }
    if(input >= 100000){
        printf(" %lld lakh",input / 100000);
        input %= 100000;
    }
    if(input >= 1000){
        printf(" %lld hajar",input / 1000);
        input %= 1000;
    }
    if(input >= 100){
        printf(" %lld shata",input / 100);
        input %= 100;
    } 
    if(input > 0){
        printf(" %lld",input);
    }
}

int main(){
    long long input;
    int cnt = 1;
    while(scanf("%lld",&input) != EOF){
        printf("%4d.",cnt++);
        if(input == 0){
            printf(" 0");
        }
        else{
            bangla(input);
        }    
        printf("\n");
    }
    return 0;
} 

