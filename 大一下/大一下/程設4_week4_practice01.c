// #include <stdio.h>

// void swap(int *a, int *b){
//     int temp = *a;
//     *a = *b;
//     *b = temp;
// }

// int main() {
//     int s1[1000], s2[1000];
//     int n, m, match;
//     char c;

//     while(1){
//         n = 0;
//         while(scanf("%d%c", &s1[n], &c) == 2){
//             n++;
//             if(c == '\n') break;
//         }
//         if (n == 0) break;

//         m = 0;
//         while(scanf("%d%c", &s2[m], &c) == 2){
//             m++;
//             if(c == '\n') break;
//         }

//         for(int i = 0; i < n - 1; i++){
//             for(int j = 0; j < n - i - 1; j++){
//                 if(s1[j] > s1[j + 1]){
//                     swap(&s1[j], &s1[j + 1]);
//                 }
//             }
//         }

//         for(int i = 0; i < m - 1; i++){
//             for(int j = 0; j < m - i - 1; j++){
//                 if(s2[j] > s2[j + 1]){
//                     swap(&s2[j], &s2[j + 1]);
//                 }
//             }
//         }

//         int i = 0, j = 0;
//         match = 0;
//         while(i < n && j < m){
//             if(s1[i] == s2[j]){
//                 match++;
//                 i++;
//                 j++;
//             } 
//             else if (s1[i] < s2[j]){
//                 i++;
//             } 
//             else{
//                 j++;
//             }
//         }

//         if (match == n && match == m) {
//             printf("A equals B\n");
//         } else if (match == 0) {
//             printf("A and B are disjoint\n");
//         } else if (match == n) {
//             printf("A is a proper subset of B\n");
//         } else if (match == m) {
//             printf("B is a proper subset of A\n");
//         } else {
//             printf("I'm confused!\n");
//         }
//     }
//     return 0;
// }


// #include <stdio.h>

// void swap(int *a, int *b){
//     int temp = *a;
//     *a = *b;
//     *b = temp;
// }

// int main(){
//     int s1[1000], s2[1000];
//     int n, m;
//     char c;

//     while(1){
//         n = 0;
//         while(scanf("%d%c", &s1[n], &c) == 2){
//             n++;
//             if(c == '\n') break;
//         }
//         if(n == 0) break;

//         m = 0;
//         while(scanf("%d%c", &s2[m], &c) == 2){
//             m++;
//             if(c == '\n') break;
//         }

//         for(int i = 0; i < n - 1; i++){
//             for(int j = 0; j < n - i - 1; j++){
//                 if(s1[j] > s1[j + 1]) swap(&s1[j], &s1[j + 1]);
//             }
//         }

//         for(int i = 0; i < m - 1; i++){
//             for(int j = 0; j < m - i - 1; j++){
//                 if(s2[j] > s2[j + 1]) swap(&s2[j], &s2[j + 1]);
//             }
//         }

//         int i = 0, j = 0;
//         int match = 0;
//         while(i < n && j < m){
//             if(s1[i] == s2[j]){
//                 match++;
//                 i++;
//                 j++;
//             }
//             else if(s1[i] < s2[j]){
//                 i++;
//             }
//             else{
//                 j++;
//             }
//         }

//         if(match == n && match == m) printf("A equals B\n");
//         else if(match == 0) printf("A and B are disjoint\n");
//         else if(match == n) printf("A is a proper subset of B\n");
//         else if(match == m) printf("B is a proper subset of A\n");
//         else printf("I'm confused!\n");
//     }
//     return 0;
// }

// #include <stdio.h>

// void swap(int *a, int *b){
//     int temp = *a;
//     *a = *b;
//     *b = temp;
// }

// int main(){
//     int a[10000], b[10000];
//     char c;
//     while(1){
//         int ia = 0, ib = 0;
//         while(scanf("%d%c", &a[ia], &c) == 2){
//             ia++;
//             if(c == '\n') break;
//         }
//         if(ia == 0) break;

//         while(scanf("%d%c",&b[ib], &c) == 2){
//             ib++;
//             if(c == '\n') break;
//         }

//         for(int i = 0; i < ia - 1; i++){
//             for(int j = 0; j < ia - i - 1; j++){
//                 if(a[j] > a[j + 1]) swap(&a[j], &a[j + 1]);
//             }
//         }

//         for(int i = 0; i < ib - 1; i++){
//             for(int j = 0; j < ib - i - 1; j++){
//                 if(b[j] > b[j + 1]) swap(&b[j], &b[j + 1]);
//             }
//         }   

//         int m = 0, n = 0, match = 0;
//         while(m < ia && n < ib){
//             if(a[m] == b[n]){
//                 match++;
//                 m++;
//                 n++;
//             }
//             else if(a[m] > b[n]){
//                 n++;
//             }
//             else{
//                 m++;
//             }
//         }

//         if(match == ia && match == ib) printf("A equals B\n");
//         else if(match == 0) printf("A and B are disjoint\n");
//         else if(match == ia) printf("A is a proper subset of B\n");
//         else if(match == ib) printf("B is a proper subset of A\n");
//         else printf("I'm confused!\n");
//     }
//     return 0;
// }

#include <stdio.h>

void swap(int *a, int *b){
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main(){
    while(1){
        int a[100000] = {0}, b[100000] = {0};
        int ai = 0, bi = 0;
        char c;
        while(scanf("%d%c", &a[ai], &c) == 2){
            ai++;
            if(c == '\n') break;
        }
        if(ai == 0) break;

        while(scanf("%d%c", &b[bi], &c) == 2){
            bi++;
            if(c == '\n') break;
        }

        for(int i = 0; i < ai - 1; i++){
            for(int j = 0; j < ai - i - 1; j++){
                if(a[j] > a[j + 1]) swap(&a[j], &a[j + 1]);
            }
        }
        
        for(int i = 0; i < bi - 1; i++){
            for(int j = 0; j < bi - i - 1; j++){
                if(b[j] > b[j + 1]) swap(&b[j], &b[j + 1]);
            }
        }

        int m = 0, n = 0, match = 0;
        while(m < ai && n < bi){
            if(a[m] == b[n]){
                match++;
                m++;
                n++;
            }
            else if(a[m] > b[n]){
                n++;
            }
            else{
                m++;
            }
        }

        if(match == ai && match == bi){
            printf("A equals B\n");
        }else if(match == 0){
            printf("A and B are disjoint\n");
        }else if(match == ai){
            printf("A is a proper subset of B\n");
        }else if(match == bi){
            printf("B is a proper subset of A\n");
        }else{
            printf("I'm confused!\n");
        }
    }
    return 0;
}