#include <stdio.h>
int main(){
    int num;
    while(scanf("%d",&num) != EOF){
        int temp = num;
        int line = 1;
        while(num - line > 0){
            num -= line;
            line++;
        }
        if(line % 2 == 0){
            printf("TERM %d IS %d/%d\n",temp, num, line + 1 - num);
        }else{
            printf("TERM %d IS %d/%d\n",temp,line + 1 - num, num);
        }
    }
    return 0;
}