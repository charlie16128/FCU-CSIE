#include <stdio.h>

int main() {
    int n; 
    while (scanf("%d", &n) && n != 0) { 
        int heights[50];  
        int sum = 0, average = 0, answer = 0;
        
        for (int i = 0; i < n; i++) {
            scanf("%d", &heights[i]);
            sum += heights[i]; 
        }
        average = sum / n;  
        for (int i = 0; i < n; i++) {
            if (heights[i] > average) {  
                answer += heights[i] - average;  
            }
        }
        printf("%d\n", answer);  
    }
    return 0;
}
