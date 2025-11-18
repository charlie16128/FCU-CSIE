#include <stdio.h>
#include <stdlib.h>

int main(){
    long long n;
    while(scanf("%lld",&n) && n >= 0){
        printf("%lld\n",n*(n + 1) / 2 + 1);
    }
    return 0;
}

// #include <stdio.h>

// int main(){
//     long long n;
//     while(scanf("%lld",&n) && n >= 0){
//         printf("%lld\n",n * (n + 1) / 2 + 1); 
//     }
//     return 0;
// }

// #include <stdio.h>

// int main(){
//     long long n;
//     while(scanf("%lld",&n) && n >= 0){
//         printf("%lld\n",n * (n + 1) / 2 + 1);
//     }
//     return 0;
// }