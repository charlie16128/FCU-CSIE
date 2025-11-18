#include <stdio.h>
#include <string.h>

int main() {
    char input[100] = {0};  

    while (fgets(input, 100, stdin) != NULL) { 
        int step = 0;  
        int one_counter = 0; 
        for (int i = 0; input[i] != '\0'; i++) {
            if (input[i] == '1') {
                one_counter++;  
            } 
            else if (input[i] == '0') {
                step += one_counter;  
            }
        }
        printf("%d\n", step); 
    }
    return 0;
}
