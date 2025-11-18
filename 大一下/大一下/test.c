#include <stdio.h>
#include <windows.h>

void p(int *a){
    for(int i = 0; i < *a; i++){
        printf("=");
    }
    printf("\n");

}

int main(){
    int a;
    while(scanf("%d",&a)){
        p(&a);
    }
    return 0;
}