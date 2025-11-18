#include <stdio.h>
int fx(int input){
    int total = 0;
    while(input >= 1){
        total = total + input % 10;
        input = input / 10;
    }
    return total;
}
int main(){
    int input;
    while(scanf("%d",&input)){
        if(input != 0){
            while(input >= 10){
                input = fx(input);
            }
            printf("%d\n",input);
        }
        else if(input == 0){
            break;
        }
    }
    return 0;
}