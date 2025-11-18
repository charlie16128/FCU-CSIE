#include <stdio.h>
#include <stdlib.h>

int main(){
    int l, h, r;
    int height[10000] = {0};
    int rightmost = 0, leftmost = 10000;
    while(scanf("%d %d %d",&l, &h, &r) != EOF){
        if(l < leftmost) leftmost = l;
        if(r > rightmost) rightmost = r;

        for(int i = l; i < r; i++){
            if(h > height[i]) height[i] = h;
        }
    }
    printf("%d %d", leftmost, height[leftmost]);
    for(int i = leftmost + 1; i <= rightmost; i++){
        if(height[i] != height[i - 1]){
            printf(" %d %d",i ,height[i]);
        }
    }
    printf("\n");
    return 0;
}



// #include <stdio.h>

// int main(){
//     int l, h, r;
//     int height[10000] = {0};
//     int rightmost = 0, leftmost = 1000;
//     while(scanf("%d %d %d",&l, &h, &r) != EOF){
//         if(l < leftmost) leftmost = l;
//         if(r > rightmost) rightmost = r;

//         for(int i = l; i < r; i++){
//             if(h > height[i]) height[i] = h;
//         }
//     }
//     printf("%d %d",leftmost, height[leftmost]);
//     for(int i = leftmost + 1; i <= rightmost; i++){
//         if(height[i] != height[i - 1]){
//             printf(" %d %d",i, height[i]);
//         }
//     }
//     return 0;
// }


// #include <stdio.h>

// int main(){
//     int l, h, r;
//     int leftmost = 10000, rightmost = 0;
//     int height[10000] = {0};
//     while(scanf("%d %d %d",&l, &h, &r) != EOF){
//         if(l < leftmost) leftmost = l;
//         if(r > rightmost) rightmost = r;

//         for(int i = l; i < r; i++){
//             if(h > height[i]) height[i] = h;
//         }
//     }
//     printf("%d %d", leftmost, height[leftmost]);
//     for(int i = leftmost + 1; i <= rightmost; i++){
//         if(height[i] != height[i - 1])  printf(" %d %d", i, height[i]);
//     }
//     return 0;
// }

// #include <stdio.h>

// int main(){
//     int l, h, r;
//     int rightmost = 0, leftmost = 10000;
//     int height[10000] = {0};
//     while(scanf("%d %d %d",&l, &h, &r) != EOF){
//         if(l < leftmost) leftmost = l;
//         if(r > rightmost) rightmost = r;

//         for(int i = 2; i < r; i++){
//             if(h > height[i]) height[i] = h;
//         }
//     }
//     printf("%d %d",leftmost, height[leftmost]);
//     for(int i = leftmost + 1; i <= rightmost; i++){
//         if(height[i] != height[i - 1]) printf(" %d %d",i ,height[i]);
//     }
//     return 0;
// }


// #include <stdio.h>

// int main(){
//     int l, h, r;
//     int leftmost = 10000, rightmost = 0;
//     int height[10000] = {0};
//     while(scanf("%d %d %d",&l, &h, &r) != EOF){
//         if(l < leftmost) leftmost = l;
//         if(r > rightmost) rightmost = r;

//         for(int i = l; i < r; i++){
//             if(h > height[i]) height[i] = h;
//         }
//     }
//     printf("%d %d",leftmost, height[leftmost]);
//     for(int i = leftmost + 1; i <= rightmost; i++){
//         if(height[i] != height[i - 1]) printf(" %d %d", i, height[i]);
//     }
//     return 0;
// }