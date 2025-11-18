#include <stdio.h>

int main() {
    int t;  //case num
    
    scanf("%d", &t); 

    for (int i = 0; i < t; i++) {
        int n;  
        scanf("%d", &n); //shop num

        int shops[200];  
        for (int j = 0; j < n; j++) {
            scanf("%d", &shops[j]); //shops
        }

        int min_pos = shops[0], max_pos = shops[0];

        for (int j = 1; j < n; j++) {
            if (shops[j] < min_pos) {
                min_pos = shops[j];
            }
            if (shops[j] > max_pos) {
                max_pos = shops[j];
            }
        }

        int min_distance = (max_pos - min_pos) * 2;
        printf("%d\n", min_distance);
    }

    return 0;
}
