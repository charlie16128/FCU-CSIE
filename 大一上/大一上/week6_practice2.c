#include <stdio.h>

int main(){
    int n, k, num;
    while(scanf("%d %d", &n, &k) != EOF){
        num = n;  // 一開始的糖果數
        while(n >= k){  // 當糖果紙數量可以兌換糖果時
            num += n / k;  // 兌換的新糖果數累加到 num
            n = n % k + n / k;  // 剩餘的糖果紙數和新換的糖果紙數
        }
        printf("%d\n", num);
    }
    return 0;
}
