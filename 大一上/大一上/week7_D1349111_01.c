#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main() {
    char map[] = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./";
    char input[100];  

    while (fgets(input, 100, stdin) != NULL) { 
        for (int i = 0; i < strlen(input); i++) {  
            int pos = 0;  
            for(int k = 0; k < strlen(map); k++) {  
                if(tolower(input[i]) == map[k]) {
                    pos = k;  
                    break;  
                }
            }
            if(pos >= 2) {
                printf("%c", map[pos - 2]);  
            } else {
                printf("%c", input[i]);
            }
        }
    }
    return 0;
}


