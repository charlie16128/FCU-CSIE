#include <stdio.h>
#include <string.h>

int main() {
    int num, count = 1;
    scanf("%d", &num);
    while(num--){
        char link[10][101];
        int relevance[10];
        int max = 0;

        for(int i = 0; i < 10; i++){
            scanf("%s %d", link[i], &relevance[i]);
            if(relevance[i] > max){
                max = relevance[i];
            }
        }

        printf("Case #%d:\n", count++);
        for (int i = 0; i < 10; i++) {
            if (relevance[i] == max) {
                printf("%s\n", link[i]);
            }
        }
    }
    return 0;
}