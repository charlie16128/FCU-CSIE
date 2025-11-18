// #include <stdio.h>
// #include <string.h>

// int main(){
//     int tc;
//     scanf("%d",&tc);
//     while(tc--){
//         int k, w;
//         char word[100][100];
//         scanf("%d %d",&k, &w);

//         for(int i = 0; i < w; i++){
//             scanf("%s",word[i]);
//         }
        
//         int total = k;

//         for(int i = 1; i < w; i++){
//             if(strcmp(word[i], word[i - 1]) == 0){
//                 continue;
//             }

//             int repeat = 0;
//             for(int j = 1; j < k; j++){
//                 if(strncmp(word[i - 1] + k - j, word[i], j) == 0){
//                     repeat = j;
//                 }
//             }
//             total += k - repeat;
//         }
//         printf("%d\n",total);
//     }
//     return 0;
// }



// #include <stdio.h>
// #include <string.h>

// int main(){
//     int tc;
//     scanf("%d",&tc);
//     while(tc--){
//         int k, w;
//         scanf("%d %d",&k, &w);
//         char word[105][105];
//         for(int i = 0; i < w; i++){
//             scanf("%s",word[i]);
//         }

//         int total = k;
        
//         for(int i = 1; i < w; i++){
//             if(strcmp(word[i - 1], word[i]) == 0) continue;

//             int repeat = 0;
//             for(int j = 0; j < k; j++){
//                 if(strncmp(word[i - 1] + k - j, word[i], j) == 0) repeat = j;
//             }

//             total += k - repeat;
//         }
//     }

//     return 0;
// }



// #include <stdio.h>
// #include <string.h>

// int main(){
//     int tc;
//     scanf("%d",&tc);
//     while(tc--){
//         int k, w;
//         scanf("%d %d",&k, &w);
//         char word[105][105];
//         for(int i = 0; i < w; i++){
//             scanf("%s",word[i]);
//         }

//         int total = k;
//         for(int i = 1; i < w; i++){
//             if(strcmp(word[i - 1], word[i]) == 0) continue;

//             int repeat = 0;
//             for(int j = 1; j < k; j++){
//                 if(strncmp(word[j - 1] + k - j, word[j], j) == 0) repeat = j;
//             }
//             total += k - repeat;
//         }
//         printf("%d\n",total);
//     }
//     return 0;
// }



#include <stdio.h>
#include <string.h>

int main(){
    int tc;
    scanf("%d",&tc);
    while(tc--){
        int k, w;
        scanf("%d %d",&k, &w);
        char word[105][105];
        for(int i = 0; i < w; i++){
            scanf("%s",word[i]);
        }

        int total = k;
        for(int i = 1; i < w; i++){
            if(strcmp(word[i - 1], word[i]) == 0) continue;

            int repeat = 0;
            for(int j = 1; j < k; j++){
                if(strncmp(word[i - 1] + k - j, word[i], j) == 0) repeat = j;
            }

            total += k - repeat;
        }
        printf("%d\n",total);
    }
    return 0;
}



