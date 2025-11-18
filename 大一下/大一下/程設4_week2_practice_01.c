// #include <stdio.h>
// #include <stdlib.h>

// int main(){
//     int n, case_counter = 1;
//     while(scanf("%d", &n) && n){
//         int n1[1005] = {0};
//         for(int i = 0; i < n; i++){
//             scanf("%d",&n1[i]);
//         }

//         int m, m1[50] = {0};
//         scanf("%d",&m);
//         for(int i = 0; i < m; i++){
//             scanf("%d",&m1[i]);
//         }

        
//         int array[50] = {0};
//         for(int j = 0; j < m; j++){
//             int closeset_sum = n1[0] + n1[1];
//             for(int i = 0; i < n; i++){
//                 for(int k = 0; k < n; k++){
//                     int sum = n1[i] + n1[k];
//                     // if(i == k) continue;
//                     if(i != k && (abs(sum - m1[j]) < abs(closeset_sum - m1[j]))) closeset_sum = sum;
//                 }
//             }
//             array[j] = closeset_sum;
//         }    

//         // output
//         printf("Case %d:\n",case_counter++);
//         for(int i = 0; i < m; i++){
//             printf("Closest sum to %d is %d.\n",m1[i],array[i]);
//         }
//     }
//     return 0;
// }



// #include <stdio.h>
// #include <stdlib.h>

// int main(){
//     int n, counter = 1;
//     while(scanf("%d",&n) && n){
//         int n1[1005] = {0};
//         for(int i = 0; i < n; i++){
//             scanf("%d",&n1[i]);
//         }

//         int m, m1[50] = {0}; 
//         scanf("%d",&m);
//         for(int i = 0; i < m; i++){
//             scanf("%d",&m1[i]);
//         }

//         int array[50] = {0};
//         for(int i = 0; i < m; i++){
//             int closest = n1[0] + n1[1];
//             for(int j = 0; j < n; j++){
//                 for(int k = 0; k < n; k++){
//                     int sum = n1[j] + n1[k];
//                     if(j != k && (abs(sum - m1[i]) < abs(closest - m1[i]))) closest = sum;
//                 }
//             }
//             array[i] = closest;    
//         }

//         printf("Case %d:\n",counter++);
//         for(int i = 0; i < m; i++){
//             printf("Closest sum to %d is %d.\n",m1[i], array[i]);
//         }
//     }
//     return 0;
// }



#include <stdio.h>
#include <stdlib.h>

int main(){
    int n, counter = 1;
    while(scanf("%d",&n) && n){
        int n1[1005] = {};
        for(int i = 0; i < n; i++){
            scanf("%d",&n1[i]);
        }

        int m, m1[50] = {};
        scanf("%d",&m);
        for(int i = 0; i < m; i++){
            scanf("%d",&m1[i]);
        }

        int array[50] = {};
        for(int i = 0; i < m; i++){
            int closest = n1[0] + n1[1];
            for(int j = 0; j < n; j++){
                for(int k = 0; k < n; k++){
                    int sum = n1[j] + n1[k];
                    if(j != k && (abs(sum - m1[i]) < abs(closest - m1[i]))) closest = sum;
                }
            }
            array[i] = closest;
        }

        printf("Case %d:\n", counter++);
        for(int i = 0; i < m; i++){
            printf("Closest sum to %d is %d.\n",m1[i], array[i]);
        }
    }
    return 0;
}
