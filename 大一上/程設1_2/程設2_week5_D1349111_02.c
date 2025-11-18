#include <stdio.h>

int main() {
    int num;
    scanf("%d", &num);

    while (num-- > 0){
        int n;
        scanf("%d", &n);

        int scores[n];
        for(int i = 0; i < n; i++){
            scanf("%d", &scores[i]);
        }

        int max_diff = -100000;
        int min_score = scores[n - 1];

        for(int i = n - 2; i >= 0; i--){
            if(scores[i] - min_score > max_diff){
                max_diff = scores[i] - min_score;
            }
            if(scores[i] < min_score){
                min_score = scores[i];
            }
        }

        printf("%d\n", max_diff);
    }
    return 0;
}
