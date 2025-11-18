// #include <stdio.h>

// int main(){
//     int num, case_counter = 1;
//     int input[1000];

//     while(scanf("%d",&num) != EOF){
//         for(int i = 0; i < num; i++){
//             scanf("%d",&input[i]);
//         }

//         long long max = 0, temp = 1;
//         for(int i = 0; i < num; i++){
//             temp = 1;
//             for(int k = i; k < num; k++){
//                 temp *= input[k];
//                 if(temp > max){
//                     max = temp;
//                 }
//             }
//         }
//         printf("Case #%d: The maximum product is %lld.\n\n",case_counter++, max);
//     }
//     return 0;
// }


#include <stdio.h>

int main(){
    int tc, counter = 1;
    while(scanf("%d",&tc) != EOF){
        int input[100];
        for(int i = 0; i < tc; i++){
            scanf("%d",&input[i]);
        }   
        long long max = 0, temp = 1;
        for(int i = 0; i < tc; i++){
            temp = 1;
            for(int k = i; k < tc; k++){
                temp *= input[k];
                if(temp > max){
                    max = temp;
                }
            }
        }
        printf("Case #%d: The maximum product is %lld.\n\n",counter++, max);
    }
    return 0;
}