#include <stdio.h>
#include <string.h>

int main(){
    char input1[10000] = {0}, input2[10000] = {0};
    while(scanf("%s %s",input1,input2) != EOF){
        int a = 0, b = 0;

        while(input1[a] !=  '\0' && input2[b] != '\0'){
            if(input1[a] == input2[b]){
                a++;
                b++;
            }
            else{
                b++;
            }
        }
        if(input1[a] == '\0'){
            printf("Yes\n");
        }
        else{
            printf("No\n");
        }
    }
    return 0;
}


/* 
#include <stdio.h>
#include <string.h>

int main(){
    char first[100000] = {0};
    char second[100000] = {0};

    while(scanf("%s %s", first, second) != EOF){
        int i = 0, j = 0;
        int if_found = 0;

        while(first[i] != '\0' && second[j] != '\0'){
            if(first[i] == second[j]){
                i++;
            }
            j++;
        }

        if(first[i] == '\0'){
            if_found = 1;
        }
        else if(second[j] == '\0'){
            if_found = 0;
        }

        if(if_found == 1){
            printf("Yes\n");
        }
        else{
            printf("No\n");
        }
    }
    return 0;
}
*/


#include <stdio.h>

int main(){
    char input1[100] = {0}, input2[100] = {0};
    while(scanf("%s %s",input1, input2) != EOF){
        int a = 0, b = 0;
        while(input1[a] != '\0' && input2[b] != '\0'){
            if(input1[a] == input2[b]){
                a++;
            }
            b++;
        }
        
        if(input1[a] == '\0'){
            printf("Yes\n");
        }
        else{
            printf("No\n");
        }
    }
    return 0;
}