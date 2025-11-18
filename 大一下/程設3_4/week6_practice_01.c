#include <stdio.h>
#include <stdbool.h>

int main(){
    int n;
    while(scanf("%d",&n) && n){
        int count = 0;
        bool arr[10000] = {false};
        while(1){
            if(arr[n]) break;
            arr[n] = true;
            n = (n * n / 100) % 10000;
            count++;
        }
        printf("%d\n",count);
    }
    return 0;
}

// #include <stdio.h>
// #include <stdbool.h>

// int main(){
//     int n;
//     while(scanf("%d", &n) && n){
//         bool arr[10000] = {false};
//         int counter = 0;
//         while(1){
//             if(arr[n] == true) break;
//             arr[n] = true;
//             n = (n * n / 100) % 10000;
//             counter++;
//         }
//         printf("%d\n", counter);
//     }   
//     return 0;
// }


// #include <stdio.h>
// #include <stdbool.h>

// int main(){
//     int n;
//     while(scanf("%d", &n) && n){
//         bool arr[10000] = {false};
//         int counter = 0;
//         while(1){
//             if(arr[n] == true) break;
//             arr[n] = true;
//             n = (n * n / 100) % 10000;
//             counter++;
//         }
//         printf("%d\n",counter);
//     }
//     return 0;
// }

// #include <stdio.h>
// #include <stdbool.h>

// int main(){
//     int n;

//     while(scanf("%d",&n) && n){
//         int counter = 0;
//         bool arr[10000] = {false};
//         while(1){
//             if(arr[n] == true) break;
//             arr[n] = true;
//             n = (n * n / 100) % 10000;
//             counter++;
//         }
//         printf("%d\n",counter);
//     }
//     return 0;
// }