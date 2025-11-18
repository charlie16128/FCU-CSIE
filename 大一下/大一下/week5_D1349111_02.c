#include <stdio.h>
#include <string.h>

int n, array[105][105], ans, total;

int main(){
    while (scanf("%d", &n) == 1){
        for (int i = 1; i <= n; i++){
            for (int j = 1; j <= n; j++){
                scanf("%d", &array[i][j]);
                array[i][j] += array[i][j - 1];
            }
        }
        ans = -100000;
        
        for(int i = 0; i < n; i++){
            for(int j = i + 1; j <= n; j++){
                total = 0;
                for(int k = 1; k <= n; k++){
                    total += array[k][j] - array[k][i];
                    if(total > ans){
                        ans = total;
                    }
                    if(total < 0){
                        total = 0;
                    }
                }
            }
        }
        printf("%d\n", ans);
    }
    return 0;
}
