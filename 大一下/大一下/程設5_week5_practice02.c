#include <stdio.h>

int main(){
    long long int n, M;
    while(scanf("%lld",&n) && n){
        int count = 0;

        for(int a = 9; a >= 0; --a){
            if(((n - a) % 9) == 0){
                M = (n - a) / 9;
                if(count++) printf(" ");
                
                printf("%lld",n + M);
            }
        }
        printf("\n");
    }
    return 0;
}
/* 求 N , n + M = N
    輸入 n = N - M
    又 N = M × 10 + a(0~9)  兩邊同減M得到 
       n = 9M + a

    若 n - a 若為9倍數，就會有一個合法的M
    n = 9M + a  ->  M = (n - a) / 9
    
*/ 
 


// #include <stdio.h>

// int main(){
//     long long int n, M;
//     while(scanf("%lld",&n) && n){
//         int count = 0;
//         for(int a = 9; a >= 0; a--){
//             if((n - a) % 9 == 0){
//                 if(count++) printf(" ");
//                 M = (n - a) / 9;
//                 printf("%lld",n + M);
//             }
//         }
//         printf("\n");
//     }

//     return 0;
// }


#include <stdio.h>

int main(){
    long long int n, M;
    while(scanf("%lld",&n) && n){
        int count = 0;
        for(int a = 9; a >= 0; a--){
            if((n - a) % 9 == 0){
                if(count++) printf(" ");
                M = (n - a) / 9;
                printf("%lld", n + M);
            }
        }
        printf("\n");
    }
    return 0;
}

//n = N - M
//N = M * 10 + a
//n = 9M + a

