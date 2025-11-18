// #include <stdio.h>

// int main(){
//     int list[10001], lt = 0;
//     int p[1001] = {1}, pt = 1;
//     int n, c, i, j;

//     for(i = 2; i < 1001; i++){
//         int flag = 1;
//         for(j = 2; j * j <= i; j++){
//             if(i % j == 0){
//                 flag = 0;
//                 break;
//             }
//         }
//         if(flag) p[pt++] = i;
//     }

//     while(scanf("%d %d",&n, &c) == 2){
//         lt = 0;
//         for(i = 0; i < pt; i++){
//             if(p[i] <= n){
//                 list[lt++] = p[i];
//             }
//             else{
//                 break;
//             }
//         }
//         printf("%d %d:",n, c);
//         if(lt & 1){
//             c = c * 2 - 1;
//         }
//         else{
//             c = c * 2;
//         }
//         if(c > lt) c = lt;
//         for(i = lt / 2 - c / 2, j = 0; j < c; j++, i++){
//             printf(" %d", list[i]);
//         }
//         printf("\n\n"); 
//     }
//     return 0;
// }

// #include <stdio.h>

// int main(){
//     int list[10001], lt = 0;
//     int p[1001] = {1}, pt = 1;
//     int n, c;
//     for(int i = 2; i < 1001; i++){
//         int flag = 1;
//         for(int j = 2; j * j <= i; j++){
//             if(i % j == 0){
//                 flag = 0;
//                 break;
//             }
//         }
//         if(flag) p[pt++] = i;
//     }

//     while(scanf("%d %d",&n, &c) == 2){
//         lt = 0;
//         for(int i = 0; i < pt; i++){
//             if(p[i] <= n){
//                 list[lt++] = p[i];
//             }
//             else{
//                 break;
//             }
//         }
//         printf("%d %d:",n, c);
//         if(lt & 1){ // 奇數
//             c = c * 2 - 1;
//         }
//         else{
//             c = c * 2;
//         }
//         if(c > lt) c = lt;

//         int i = lt / 2 - c / 2;
//         for(int j = 0; j < c; j++){
//             printf(" %d", list[i++]);
//         }
//         printf("\n\n");
//     }
//     return 0;
// }

// #include <stdio.h>

// int main(){
//     int n, c;
//     int p[10001] = {1}, pi = 1;
//     int list[1001] = {0}, li = 0;
//     for(int i = 2; i < 10001; i++){
//         int flag = 1;
//         for(int j = 2; j * j <= i; j++){
//             if(i % j == 0){
//                 flag = 0;
//                 break;
//             }
//         }
//         if(flag) p[pi++] = i; 
//     }

//     while(scanf("%d %d", &n, &c) == 2){
//         li = 0;
//         for(int i = 0; i <= pi; i++){
//             if(p[i] <= n){
//                 list[li++] = p[i];
//             }
//             else{
//                 break;
//             }
//         }

//         printf("%d %d:",n, c);
//         if(n % 2 == 1){
//             c = c * 2 - 1;
//         }else{
//             c = 2 * c;
//         }
//         if(c > li) c = li;
//         int index = li / 2 - c / 2;
//         for(int i = 0; i < c; i++){
//             printf(" %d",list[index++]);
//         }
//         printf("\n\n");
//     }
//     return 0;
// }

#include <stdio.h>

int main(){ 
    int n, c;
    int p[1001] = {1}, pi = 1, list[1001] = {0}, li = 0;
    for(int i = 2; i < 1001; i++){
        int flag = 1;
        for(int j = 2; j * j <= i; j++){
            if(i % j == 0){
                flag = 0;
                break;
            }
        }
        if(flag) p[pi++] = i;
    }

    while(scanf("%d %d",&n, &c) == 2){
        printf("%d %d:", n, c);
        li = 0;
        for(int i = 0; i <= pi; i++){
            if(p[i] <= n){
                list[li++] = p[i];
            }
            else{
                break;
            }
        }

        if(n % 2 == 1){
            c = c * 2 - 1;
        }else{
            c = c * 2;
        }
        if(c > li) c = li;
        int index = li / 2 - c / 2;
        
        for(int i = 0; i < c; i++){
            printf(" %d",list[index++]);
        }
        printf("\n\n");
    } 
    return 0;
}