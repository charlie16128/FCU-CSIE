// #include <stdio.h>
// #include <string.h>
// #include <ctype.h>

// char *compare(char stdinput[][125], int n, char teaminput[][125], int m){
//     if (n == m) {
//         int accepted = 1;
//         for (int i = 0; i < n; i++) {
//             if (strcmp(stdinput[i], teaminput[i])) {
//                 accepted = 0;
//                 break;
//             }
//         }
//         if (accepted) {
//             return "Accepted";
//         }
//     }

//     char stdnum[120], teamnum[120];
//     int si = 0, ti = 0;
//     // 提取標準答案的數字
//     for (int i = 0; i < n; i++) {
//         for (int j = 0; stdinput[i][j] != '\0'; j++) {
//             if (isdigit(stdinput[i][j])) {
//                 stdnum[si++] = stdinput[i][j];
//             }
//         }
//     }
//     stdnum[si] = '\0';
    
//     // 提取團隊輸出的數字
//     for (int i = 0; i < m; i++) {
//         for (int j = 0; teaminput[i][j] != '\0'; j++) {
//             if (isdigit(teaminput[i][j])) {
//                 teamnum[ti++] = teaminput[i][j];
//             }
//         }
//     }
//     teamnum[ti] = '\0';

//     if (strcmp(stdnum, teamnum) == 0) {
//         return "Presentation Error";
//     } 
//     else {
//         return "Wrong Answer";
//     }
// }

// int main(){
//     int n, counter = 1;
//     while (scanf("%d", &n) && n) {
//         getchar(); 
//         char stdinput[105][125];
//         for (int i = 0; i < n; i++) {
//             fgets(stdinput[i], 125, stdin);
//         }
    
//         int m;
//         scanf("%d", &m);
//         getchar(); 
//         char teaminput[105][125];
//         for (int i = 0; i < m; i++) {
//             fgets(teaminput[i], 125, stdin);
//         }
        
//         printf("Run #%d: ",counter++);
//         printf("%s\n",compare(stdinput, n, teaminput, m));
//     }
    
//     return 0;
// }



#include <stdio.h>
#include <string.h>
#include <ctype.h>

char *compare(char stdinput[105][125], int n, char teaminput[105][125], int m){
    if(n == m){
        int ac = 1;
        for(int i = 0; i < n; i++){
            if(strcmp(stdinput[i], teaminput[i]) != 0){
                ac = 0;
                break;
            }
        }
        if(ac){
            return "Accepted";
        } 
    }
    char stdnum[125], teamnum[125];
    int si = 0, ti = 0;
    for(int i = 0; i < n; i++){
        for(int j = 0; stdinput[i][j] != '\0'; j++){
            if(isdigit(stdinput[i][j])) stdnum[si++] = stdinput[i][j];
        }
    }
    stdnum[si] = '\0';

    for(int i = 0; i < m; i++){
        for(int j = 0; teaminput[i][j] != '\0'; j++){
            if(isdigit(teaminput[i][j])) teamnum[ti++] = teaminput[i][j];
        }
    }
    teamnum[ti] = '\0';

    if(strcmp(stdnum, teamnum) == 0){
        return "Presentation Error";
    }
    else{
        return "Wrong Answer";
    } 
}

int main(){
    int n, counter = 1;
    while(scanf("%d",&n) && n){
        char stdinput[105][125];        
        getchar();
        for(int i = 0; i < n; i++){
            fgets(stdinput[i], 125, stdin);
        }

        int m;
        char teaminput[105][125];
        scanf("%d",&m);
        getchar();
        for(int i = 0; i < m; i++){
            fgets(teaminput[i], 125, stdin);
        }

        printf("Run #%d: ", counter++);
        printf("%s\n", compare(stdinput, n, teaminput, m));
    }
    return 0;
}


// #include <stdio.h>
// #include <string.h>
// #include <ctype.h>

// char *compare(char stdinput[105][125], int n, char teaminput[105][125], int m){
//     if(n == m){
//         int ac = 1;
//         for(int i = 0; i < n; i++){
//             if(strcmp(stdinput[i], teaminput[i]) != 0){
//                 ac = 0;
//                 break;
//             }
//         }
//         if(ac) return "Accepted";
//     }
//     char stdnum[125], teamnum[125];
//     int si = 0, ti = 0;
//     for(int i = 0; i < n; i++){
//         for(int j = 0; stdinput[i][j] != '\0'; j++){
//             if(isdigit(stdinput[i][j])) stdnum[si++] = stdinput[i][j];
//         }
//     }
//     stdnum[si] = '\0';
    
//     for(int i = 0; i < n; i++){
//         for(int j = 0; teaminput[i][j] != '\0'; j++){
//             if(isdigit(teaminput[i][j])) teamnum[ti++] = teaminput[i][j];
//         }
//     }
//     teamnum[ti] = '\0';
    
//     if(strcmp(stdnum, teamnum) == 0){
//         return "Presentation Error";
//     }
//     else{
//         return "Wrong Answer";
//     }
// }

// int main(){
//     int n, counter = 1;
//     while(scanf("%d",&n) && n){
//         char stdinput[105][125];
//         getchar();
//         for(int i = 0; i < n; i++){
//             fgets(stdinput[i], 125, stdin);
//         }

//         int m;
//         char teaminput[105][125];
//         scanf("%d", &m);
//         getchar();
//         for(int i = 0; i < m; i++){
//             fgets(teaminput[i], 125, stdin);
//         }

//         printf("Run #%d: ",counter++);
//         printf("%s\n",compare(stdinput, n, teaminput, m));
//     }
//     return 0;
