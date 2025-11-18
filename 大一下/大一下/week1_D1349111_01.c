#include <stdio.h>

int main(){
    int Empty_cola;
    while(scanf("%d",&Empty_cola) != EOF){
        int total = Empty_cola;

        while(Empty_cola >= 3){ // 3 empty cola can exchange 1 cola
            total += Empty_cola / 3;
            Empty_cola = Empty_cola / 3 + Empty_cola % 3; 
        }

        if(Empty_cola == 2) total++; // 2 empty cola can exchange 1 cola, so can borrow 1 from other and can return 1 
        printf("%d\n",total);
    }
    return 0;
}