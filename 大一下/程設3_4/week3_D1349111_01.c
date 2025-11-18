#include <stdio.h>

int square_sum(long long num){
    long long total = 0;
    while(num > 0){
        total += (num % 10) * (num % 10);
        num /= 10;
    }
    return total; 
}
int main(){
    int case_counter = 1, tc;
    long long input, result;
    scanf("%d",&tc);

    while(tc--){
        scanf("%lld",&input);
        result = square_sum(input);

        while(result != 1 && result != 4){
            result = square_sum(result);
        }
        
        if(result == 1){
            printf("Case #%d: %lld is a Happy number.\n",case_counter++, input);
        }
        else{
            printf("Case #%d: %lld is an Unhappy number.\n",case_counter++, input);
        }
    }
    return 0;
}