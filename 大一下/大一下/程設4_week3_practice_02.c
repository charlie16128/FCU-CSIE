// #include <stdio.h>

// int main(){
//     int j, r;
//     while(scanf("%d %d", &j, &r) == 2){
//         int score[500] = {0};
//         int winner = 0, max = -1;
//         int temp  = 0;
//         for(int i = 0; i < r; i++){
//             for(int k = 1; k <= j; k++){
//                 scanf("%d", &temp);
//                 score[k] += temp;
//                 if(score[k] >= max){
//                     max = score[k];
//                     winner = k; 
//                 }
//             }
//         }
//         printf("%d\n",winner);
//     }
//     return 0;
// }


#include <stdio.h>

int main(){
    int j, r;
    while(scanf("%d %d",&j, &r) == 2){
        int score[505] = {0};
        int winner, temp, max = -1;
        for(int i = 0; i < r; i++){
            for(int k = 1; k <= j; k++){
                scanf("%d", &temp);
                score[k] += temp;
                if(score[k] >= max){
                    max = score[k];
                    winner = k;
                }
            }
        }
        printf("%d\n",winner);
    }
    return 0;
}