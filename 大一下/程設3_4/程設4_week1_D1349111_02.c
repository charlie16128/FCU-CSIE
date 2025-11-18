#include <stdio.h>

void sortarray(int array[], int size){
    for(int i = 0; i < size - 1; i++){
        for(int k = 0; k < size - i - 1; k++){
            if(array[k] < array[k + 1]){
                int temp = array[k];
                array[k] = array[k + 1];
                array[k + 1] = temp;
            }
        }
    }
}

int main(){
    int tc;
    scanf("%d",&tc);
    while(tc--){
        int list[100], buy;
        int index = 0;
        while(scanf("%d",&buy) && buy){
            list[index++] = buy;
        }
        sortarray(list, index);

        long long temptotal, total = 0;
        for(int i = 0; i < index; i++){
            temptotal = 1;
            for(int pow = 0; pow <= i; pow++){
                if(temptotal > 5000000) break;
                temptotal *= list[i];
            }
            total += 2 * temptotal;
        }

        if(total < 5000000){
            printf("%lld\n",total);
        }
        else{
            printf("Too expensive\n");
        }
    }
    return 0;
}