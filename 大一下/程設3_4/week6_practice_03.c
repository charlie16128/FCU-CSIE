#include <stdio.h>
#include <stdlib.h>

int main(){
    int n;
    while(scanf("%d",&n) && n){
        printf("%d : ", n);
        int ans = 0;
        for(int i = 2; i * i < n; i++){
            if(n % i == 0){
                while(n % i == 0){
                    n /= i;
                }
                ans++;
            }
        }
        if(n > 1) ans++;
        printf("%d\n",ans);
    }
    return 0;
}


// #include <stdio.h>

// int main(){
//     int n;
//     while(scanf("%d",&n) && n){
//         printf("%d : ", n);
//         int ans = 0;
//         for(int i = 2; i * i < n; i++){
//             if(n % i == 0){
//                 while(n % i == 0){
//                     n /= i;
//                 }
//                 ans++;
//             }
//         }
//         if(n > 1) ans++;
//         printf("%d\n", ans);
//     }
//     return 0;
// }

// #include <stdio.h>

// int main(){
//     int n;
//     while(scanf("%d", &n) && n){
//         printf("%d : ", n);
//         int ans = 0;
//         for(int i = 2; i * i < n; i++){
//             if(n % i == 0){
//                 while(n % i == 0){
//                     n /= i;
//                 }
//                 ans++;
//             }
//         }
//         // if(n > 1) ans++;
//         printf("%d\n",ans);
//     }
//     return 0;
// }

// #include <stdio.h>

// int main(){
//     int n;
//     while(scanf("%d", &n) && n){
//         printf("%d : ",n);
//         int ans = 0;
//         for(int i = 2; i * i < n; i++){
//             if(n % i == 0){
//                 while(n % i == 0){
//                     n /= i;
//                 }
//                 ans++;
//             }
//         }
//         if(n > 1) ans++;
//         printf("%d\n",ans);
//     }
//     return 0;
// }

// #include <stdio.h>

// int main(){
//     int n;
//     while(scanf("%d",&n) && n){
//         printf("%d : ",n);
//         int ans = 0;
//         for(int i = 2; i * i < n; i++){
//             if(n % i == 0){
//                 while(n % i == 0){
//                     n /= i;
//                 }
//                 ans++;
//             }
//         }
//         if(n > 1) ans++;
//         printf("%d\n", ans);
//     }
//     return 0;
// }