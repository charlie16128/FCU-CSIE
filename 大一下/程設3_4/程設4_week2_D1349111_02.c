#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int c_asc(const void *a, const void *b){
    return (*(char *)a) - (*(char *)b);
}

int c_des(const void *a, const void *b){
    return (*(char *)b) - (*(char *)a);
}

int main(){
    char num[50];
    while(scanf("%s",num) && strcmp(num, "0") != 0){
        printf("Original number was %s\n", num);

        int counter = 0;
        int appeared[1000];
        while(1){
            char asc[50], des[50];
            strcpy(asc, num);
            strcpy(des, num);

            qsort(asc, strlen(asc), sizeof(char), c_asc);
            qsort(des, strlen(des), sizeof(char), c_des);

            int num_asc = atoi(asc);
            int num_des = atoi(des);
            int next = num_des - num_asc;

            printf("%d - %d = %d\n",num_des, num_asc, next);

            int found = 0;
            for(int i = 0; i < counter; i++){
                if(appeared[i] == next){
                    found = 1;
                    break;
                }
            }
            appeared[counter++] = next;
            
            if(found){
                printf("Chain length %d\n\n", counter);
                break;
            }

            sprintf(num, "%d", next);
        }
    }
    return 0;
}