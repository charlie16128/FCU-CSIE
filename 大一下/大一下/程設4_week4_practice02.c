// #include <stdio.h>
// #include <string.h>

// int main() {
//     int n, cases = 0;

//     while (scanf("%d", &n) != EOF) {
//         int ret = 0;  // cool word count for this case
//         char s[32];

//         for (int i = 0; i < n; i++) {
//             scanf("%s", s);

//             int cnt[128] = {0};     // character count
//             int mcnt[10001] = {0};  // map from frequency to count of that frequency
//             int unique_letter = 0;
//             int same = 0;

//             // Count each character
//             for (int j = 0; s[j]; j++) {
//                 cnt[(int)s[j]]++;
//             }

//             // Check frequency uniqueness
//             for (int j = 'a'; j <= 'z'; j++) {
//                 if (cnt[j]) {
//                     if (mcnt[cnt[j]] > 0) {
//                         same = 1;
//                         break;
//                     }
//                     mcnt[cnt[j]]++;
//                     unique_letter++;
//                 }
//             }

//             if (unique_letter >= 2 && same == 0) {
//                 ret++;
//             }
//         }
//         printf("Case %d: %d\n", ++cases, ret);
//     }
//     return 0;
// }


// #include <stdio.h>
// #include <string.h>

// int main(){
//     int n, cases = 0;
//     while(scanf("%d", &n) != EOF){
//         int ret = 0;
//         char s[32];
//         for(int i = 0; i < n; i++){
//             scanf("%s", s);

//             int cnt[128] = {0};
//             int fcnt[10001] = {0};
//             int unique_letter = 0;
//             int same = 0;

//             for(int j = 0; s[j]; j++){
//                 cnt[(int)s[j]]++;
//             }
//             for(int j = 'a'; j <= 'z'; j++){
//                 if(cnt[j]){
//                     if(fcnt[cnt[j]] != 0){
//                         same = 1;
//                         break;
//                     }
//                     fcnt[cnt[j]]++;
//                     unique_letter++;
//                 }
//             }
//             if(unique_letter >= 2 && same == 0){
//                 ret++;
//             }
//         }
//         printf("Case %d: %d\n", ++cases, ret);
//     }
//     return 0;
// }

// #include <stdio.h>
// #include <string.h>

// int main(){
//     int n, cases = 0;
//     while(scanf("%d", &n) != EOF){
//         int cool_word = 0;
//         char s[32];
        
//         for(int i = 0; i < n; i++){
//             scanf("%s", s);

//             int cnt[150] = {0}, fcnt[10005] = {0};
//             int same = 0, unique = 0;
//             for(int j = 0; s[j] != '\0'; j++){
//                 cnt[(int)s[j]]++;
//             }
            
//             for(int j = 'a'; j <= 'z'; j++){
//                 if(cnt[j]){
//                     if(fcnt[cnt[j]] != 0){
//                         same = 1;
//                         break;
//                     }
//                     fcnt[cnt[j]]++;
//                     unique++;
//                 }
//             }
            
//             if(unique >= 2 && same == 0){
//                 cool_word++;
//             }
//         }
//         printf("Case %d: %d\n",++cases, cool_word);
//     }
//     return 0;
// }


#include <stdio.h>
#include <string.h>

int main(){
    int n, cases = 0;
    while(scanf("%d", &n) != EOF){
        int cool_word = 0;
        char s[35];
        for(int i = 0; i < n; i++){
            scanf("%s", s);

            int cnt[150] = {0};
            int fcnt[10001] = {0};
            for(int j = 0; s[j] != '\0'; j++){
                cnt[(int)s[j]]++;
            }
            
            int same = 0, unique = 0;
            for(int j = 'a'; j <= 'z'; j++){
                if(cnt[j]){
                    if(fcnt[cnt[j]] != 0){
                        same = 1;
                        break;
                    }
                    fcnt[cnt[j]]++;
                    unique++;
                }
            }

            if(same == 0 && unique >= 2){
                cool_word++;
            }
        }
        printf("Case %d: %d\n", ++cases, cool_word);
    }
    return 0;
}
