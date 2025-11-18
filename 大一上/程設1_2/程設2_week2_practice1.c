#include <stdio.h>
#include <string.h>

int main() {
    char input[100001] = {0};
    int frequency[26] = {0};
    char letters[26];
    int type = 0;

    scanf("%s", input);

    for (int i = 0; i < strlen(input); i++){
        frequency[input[i] - 'a']++;
    }

    for (int i = 0; i < 26; i++){
        if (frequency[i] > 0) {     
            letters[type] = 'a' + i; 
            frequency[type] = frequency[i]; 
            type++;
        }
    }

    for (int i = 0; i < type - 1; i++){
        for (int j = 0; j < type - i - 1; j++) {
            if (frequency[j] < frequency[j + 1]){
                int tempFreq = frequency[j];
                frequency[j] = frequency[j + 1];
                frequency[j + 1] = tempFreq;

                char tempLetter = letters[j];
                letters[j] = letters[j + 1];
                letters[j + 1] = tempLetter;
            }
        }
    }
    // //test 
    // for(int i = 0; i < type; i++){
    //     printf("%c : %d, type : %d\n",letters[i],frequency[i],type);
    // }

    int total = 0;
    for (int i = 0; i < type; i++){
        int keyPosition = i / 8;
        total += frequency[i] * (keyPosition + 1);
    }

    printf("%d\n", total);

    return 0;
}