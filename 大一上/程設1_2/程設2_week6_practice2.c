#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
int count(int n){
    int num = n;
    while(n){
        num += n % 10;
        n /= 10;
    }
    return num;
}

int count_digit(int n){
    int digit = 0;
    while(n){
        digit++;
        n /= 10;
    }
    return digit;
}

int main() {
    int t;
    scanf("%d", &t);
    while(t--){
        int n;
        scanf("%d", &n);
        bool check = false;
        int digit = count_digit(n);
        for(int i = n - 9 * digit; i <= n; i++){
            if(count(i) == n){ //¦ì¼Æ©M+self
                printf("%d\n", i);
                check = true;
                break;
            }
        }
        
        if(!check){
            printf("0\n");
        }
    }
    return 0;
}