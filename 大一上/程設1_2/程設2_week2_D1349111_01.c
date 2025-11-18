#include <stdio.h>
#include <string.h>

int main() {
    int num;

    while (scanf("%d", &num) && num != 0) {
        char numbers[50][20] = {0};

        for (int i = 0; i < num; i++) {
            scanf("%s", numbers[i]);
        }

        for (int i = 0; i < num - 1; i++) {
            for (int j = 0; j < num - 1 - i; j++) {
                char ab[40] = {0}, ba[40] = {0};
                int len_ab = 0, len_ba = 0;

                //ab
                for (int k = 0; k < strlen(numbers[j]); k++) {
                    ab[len_ab++] = numbers[j][k];
                }
                for (int k = 0; k < strlen(numbers[j + 1]); k++) {
                    ab[len_ab++] = numbers[j + 1][k];
                }
                // ab[len_ab] = '\0';

                //ba
                for (int k = 0; k < strlen(numbers[j + 1]); k++) {
                    ba[len_ba++] = numbers[j + 1][k];
                }
                for (int k = 0; k < strlen(numbers[j]); k++) {
                    ba[len_ba++] = numbers[j][k];
                }
                // ba[len_ba] = '\0';

                if (strcmp(ab, ba) < 0) {
                    char temp[20];
                    strcpy(temp, numbers[j]);
                    strcpy(numbers[j], numbers[j + 1]);
                    strcpy(numbers[j + 1], temp);
                }
            }
        }

        for (int i = 0; i < num; i++) {
            printf("%s", numbers[i]);
        }
        printf("\n");
    }

    return 0;
}

