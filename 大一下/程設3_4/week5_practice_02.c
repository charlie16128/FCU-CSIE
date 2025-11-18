// #include <stdio.h>
// #include <string.h>

// int main(){
//     char a[2000], b[2000];
//     while(fgets(a, 2000, stdin) != NULL){
//         fgets(b, 2000, stdin);
//         a[strlen(a) - 1] = '\0';
//         b[strlen(b) - 1] = '\0';
//         int c1[128] = {}, c2[128] = {};
//         int v;
//         for(int i = 0; a[i] != '\0'; i++) c1[a[i]]++;
//         for(int i = 0; b[i] != '\0'; i++) c2[b[i]]++;

//         for(int i = 0; i < 128; i++){ // 用少的
//             if(c1[i] < c2[i]){
//                 v = c1[i];
//             }
//             else{
//                 v = c2[i];
//             }
//             for(;v > 0; v--) putchar(i);
//         }
//         puts("");
//     }
//     return 0;
// }


// #include <stdio.h>
// #include <string.h>

// int main(){
//     char input1[1001] = {}, input2[1001] = {};
//     while(fgets(input1, 1001, stdin) != NULL){
//         fgets(input2, 1001, stdin);
//         input1[strlen(input1) - 1] = '\0';
//         input2[strlen(input2) - 1] = '\0';
//         char f1[128] = {}, f2[128] = {};
//         for(int i = 0; input1[i] != '\0'; i++) f1[input1[i]]++;
//         for(int i = 0; input2[i] != '\0'; i++) f2[input2[i]]++;
//         int times;
//         for(int i = 0; i < 128; i++){
//             if(f1[i] < f2[i]){
//                 times = f1[i];
//             }
//             else{
//                 times = f2[i];
//             }
//             for(;times > 0; times--) printf("%c",i);
//         }
//         printf("\n");
//     }
//     return 0;
// }


// #include <stdio.h>
// #include <string.h>

// int main(){
//     char input1[2001] = {},input2[2001] = {};
//     while(fgets(input1, 2001, stdin) != NULL){
//         fgets(input2, 2001, stdin);
//         input1[strlen(input1) - 1] = '\0';
//         input2[strlen(input2) - 1] = '\0';
//         int f1[128] = {}, f2[128] = {};
//         for(int i = 0; input1[i] != '\0'; i++) f1[input1[i]]++;
//         for(int i = 0; input2[i] != '\0'; i++) f2[input2[i]]++;

//         int times;
//         for(int i = 0; i < 128; i++){
//             if(f1[i] > f2[i]){
//                 times = f2[i];
//             }
//             else{
//                 times = f1[i];
//             }
//             for(; times > 0; times--) printf("%c",i);
//         }
//         printf("\n");
//     } 
//     return 0;
// }


#include <stdio.h>
#include <string.h>

int main(){
    char input1[10000] = {}, input2[10000] = {};
    while(fgets(input1, 10000, stdin) != NULL){
        fgets(input2, 10000, stdin);
        input1[strlen(input1) - 1] = '\0';
        input2[strlen(input2) - 1] = '\0';
        int f1[10000] = {}, f2[10000] = {};
        for(int i = 0; input1[i] != '\0'; i++) f1[input1[i]]++;
        for(int i = 0; input2[i] != '\0'; i++) f2[input2[i]]++;

        int times;
        for(int i = 0; i < 128; i++){
            if(f1[i] > f2[i]){
                times = f2[i];
            }
            else{
                times = f1[i];
            }
            for(;times > 0; times--) printf("%c",i);
        }
        printf("\n");
    }
    return 0;
}