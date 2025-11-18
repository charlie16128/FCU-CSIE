#include<stdio.h>

int main(){
    int v,t;
    while(scanf("%d %d",&v,&t) != EOF) {
        if(t == 0){
            printf("0\n");
            continue;
        }
        double a;
        a = (double)v/t;
        t = t*2;
        double s = 0.5*a*t*t;
        printf("%.0f\n" ,s);
    }
    return 0;
}
