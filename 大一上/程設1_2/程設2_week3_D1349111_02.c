#include <stdio.h>
#include <string.h>

int main(){
    int guess;
    int higest = 10, lowest = 1;

    while(scanf("%d",&guess) && guess != 0){
        char statement[100] = {0};

        getchar();
        fgets(statement, sizeof(statement), stdin);
        statement[strcspn(statement, "\n")] = 0; 

        if(strcmp(statement, "right on") == 0){
            if(guess >= lowest && guess <= higest){
                printf("Stan may be honest\n");
            }
            else{
                printf("Stan is dishonest\n");
            }
            higest = 10, lowest = 1;
        }
        else if(strcmp(statement, "too high") == 0){
            if(guess - 1 < higest){
                higest = guess - 1;
            }
        }
        else if(strcmp(statement, "too low") == 0){
            if(guess + 1 > lowest){
                lowest = guess + 1;
            }
        }
    }
    return 0;
}