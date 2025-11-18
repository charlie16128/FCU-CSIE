// #include <stdio.h>
// #include <ctype.h>

// int main() {
//     int letterFrequency[256] = {0};
//     int n;
//     char str[1000];

//     scanf("%d", &n);
//     getchar();

//     while (n > 0) {
//         fgets(str, 1000, stdin);
//         for (int i = 0; str[i] != '\0'; i++) {
//             if (isalpha(str[i])) {
//                 letterFrequency[toupper(str[i])]++;
//             }
//         }
//         n--;
//     }

//     for (int freq = 256; freq > 0; freq--) {
//         for (int asciiValue = 65; asciiValue <= 90; asciiValue++) {
//             if (letterFrequency[asciiValue] == freq) {
//                 printf("%c %d\n", asciiValue, letterFrequency[asciiValue]);
//             }
//         }
//     }

//     return 0;
// }
#include <stdio.h>
#include <ctype.h>

int main() {
    int letterFrequency[256] = {0};
    int n;
    char str[1000];

    scanf("%d", &n);
    getchar();

    while (fgets(str, 1000, stdin) != NULL) { //§ï¤F³o
    
        for (int i = 0; str[i] != '\0'; i++) {
            if (isalpha(str[i])) {
                letterFrequency[toupper(str[i])]++;
            }
        }
    }

    for (int freq = 256; freq > 0; freq--) {
        for (int asciiValue = 65; asciiValue <= 90; asciiValue++) {
            if (letterFrequency[asciiValue] == freq) {
                printf("%c %d\n", asciiValue, letterFrequency[asciiValue]);
            }
        }
    }

    return 0;
}
