#include <stdio.h>

int isPerfectSquare(unsigned int n){
    if(n == 0){
        return 0;
    }
    unsigned int left = 1, right = n;
    while(left <= right){
        unsigned int mid = left + (right - left) / 2;
        unsigned long long square = (unsigned long long)mid * mid;
        if(square == n){
            return 1;
        }
        else if(square < n){
            left = mid + 1;
        }
        else{
            right = mid - 1;
        }
    }
    return 0;
}

int main(){
    unsigned int n;
    while(scanf("%u", &n) && n != 0){
        if(isPerfectSquare(n)){
            printf("yes\n");
        }
        else{
            printf("no\n");
        }
    }
    return 0;
}



/*
1 2 3 4
1 1 1 1
1 0 1 0
1 0 0 1
1 0 0 1
*/

