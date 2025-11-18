#include <stdio.h>

int main(){
    int num, k, list[50] = {0}; 
    int max = 0, count = 0;

    scanf("%d %d", &num, &k);

    for(int i = 0; i < num; i++){
        scanf("%d", &list[i]);
        if(list[i] > max){
            max = list[i];
        }
    }

    for(int i = 0; i < num; i++){
        int max_count = 0;
        for(int j = i; j < num; j++){
            if(list[j] == max){
                max_count++;
            }
            if(max_count >= k){
                count++;
            }
        }
    }

    printf("%d\n", count);
    return 0;
}
