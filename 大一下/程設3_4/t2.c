#include <stdio.h>
#define MIN_ACERAGE_SCORE 95
#define MAX_ACERAGE_SCORE 99
#define CURRENT_AVERAGE_SCORE 80
#define CURRENT_READ_BOOK 2

int main(){
    for(int i = MIN_ACERAGE_SCORE; i < MAX_ACERAGE_SCORE + 1; i++){ // Changed <= to <
        if(i == 100){
            printf("You have to get 'infinite' 100 score to get the average score %d\n", i);
        }
        else{
            printf("You have to get '%d' 100 score to get the average score %d\n", 
                (CURRENT_READ_BOOK * (i - CURRENT_AVERAGE_SCORE)) / (100 - i), i);
        }
    }
    
    return 0;
}