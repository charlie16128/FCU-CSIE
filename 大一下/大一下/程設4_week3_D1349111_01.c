#include <stdio.h>

// 計算最大公因數
long long gcd(long long a, long long b){
    while(b){
        long long temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main(){
    int v1, d1, v2, d2, counter = 1;

    while(scanf("%d %d %d %d", &v1, &d1, &v2, &d2)){
        if(!v1 && !d1 && !v2 && !d2) break;

        printf("Case #%d: ", counter++);

        // 通分
        long long t1 = (long long)d1 * v2; // d1 / v1 上下同成v2
        long long t2 = (long long)d2 * v1; // d2 / v2 上下同成v1

        if(t1 < t2){
            printf("You owe me a beer!\n");
        } else {
            printf("No beer for the captain.\n");
        }

        printf("Avg. arrival time: ");

        long long numerator = t1 + t2; // 分子
        long long denominator = 2LL * v1 * v2; //分母
        // avg = (d1/v1 + d2/v2) / 2 
        //     = d1 * v2 + d2 * v1  /  2 * v1 * v2

        // 約分
        long long g = gcd(numerator, denominator);
        numerator /= g;
        denominator /= g;

        if(denominator == 1){ // 分母為1顯示分子就好
            printf("%lld\n", numerator);
        } 
        else {
            printf("%lld/%lld\n", numerator, denominator);
        }
    }
    return 0;
}