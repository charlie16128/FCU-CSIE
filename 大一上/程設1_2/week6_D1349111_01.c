#include <stdio.h>
#include <stdbool.h>

int main(){
    int start,end;
    bool determine = true;
    scanf("%d %d",&start,&end);
    for(int i = start; i <= end; i++){ //2 10
        for(int k = 2 ; k < i; k++){// 2
            if(i % k == 0){
                determine = false;
            }
        }
        if(determine == true){
            printf("%d\n",i);
        }
        determine = true;
    }
    return 0;

}