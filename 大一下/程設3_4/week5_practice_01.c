// #include <stdio.h>
// #include <string.h>

// int main(){
//     int n, m;
//     while(scanf("%d %d",&n, &m) == 2){
//         int a[1000];
//         int i = 0;
//         if(n < 2 || m < 2){
//             printf("Boring!\n");
//             continue;
//         }
//         while(n > 1){
//             a[i++] = n;
//             if(n % m != 0){
//                 printf("Boring!\n");
//                 break;
//             }
//             n /= m;
//             if(n == 1){
//                 a[i++] = 1;
//                 for(int j = 0; j < i; j++){
//                     // printf("%d%c",a[j], j==i-1?'\n' : ' ');
//                     printf("%d ",a[j]);
//                 }
//                 printf("\n");
//             }
//         }
//     }
//     return 0;
// }



// #include <stdio.h>
// #include <string.h>

// int main(){
//     int a, b;
//     while(scanf("%d %d",&a ,&b) != EOF){
//         if(a < 2 || b < 2){
//             printf("Boring!\n");
//             continue;
//         }
//         int array[1000] = {}, i = 0;
//         while(a > 1){
//             array[i++] = a;
//             if(a % b != 0){
//                 printf("Boring!\n");
//                 break;
//             }
//             a /= b;
//             if(a == 1){
//                 array[i++] = 1; 
//                 for(int k = 0; k < i; k++){
//                     printf("%d ",array[k]);
//                 }
//                 printf("\n");
//             }
//         }
//     }
//     return 0;
// }

// #include <stdio.h>
// #include <string.h>

// int main(){
//     int a, b;
//     while(scanf("%d %d",&a, &b) != EOF){
//         if(a < 2 || b < 2){
//             printf("Boring!\n");
//             continue;
//         }
//         int array[10000] = {}, i = 0;
//         while(a > 1){
//             array[i++] = a;
//             if(a % b != 0){
//                 printf("Boring!\n");
//                 break;
//             }
//             a /= b;
//             if(a == 1){
//                 array[i++] = 1;
//                 for(int k = 0; k < i; k++){
//                     printf("%d%c",array[k], k == i -1 ? '\n' : '');
//                 }
//             }
//         }
//     }
//     return 0;
// }



#include <stdio.h>
#include <string.h>

int main(){
    int a, b;
    while(scanf("%d %d",&a, &b) != EOF){
        int array[10000] = {}, i = 0;
        if(a < 2 || b < 2){
            printf("Boring!\n");
            continue;
        }
        
        while(a > 1){
            array[i++] = a;
            if(a % b != 0){
                printf("Boring!\n");
                break;
            }
            a /= b;
            if(a == 1){
                array[i++] = 1;
                for(int k = 0; k < i; k++){
                    printf("%d%c",array[k], k == i -1 ? '\n' : ' ');
                }
            }
        }
    }
    return 0;
}