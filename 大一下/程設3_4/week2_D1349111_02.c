#include <stdio.h>
#include <ctype.h>

int main(){
    int tc, counter = 1;
    scanf("%d",&tc);

    while(tc--){
        char input[1000] = {0};
        scanf("%s",input);
        printf("Case %d: ",counter++);

        int index = 0;
        while(input[index] != '\0'){
            int count = 0;
            char a = input[index++]; //字母

            while(isdigit(input[index]) != 0){
                count = count * 10 + (input[index] - '0'); //how many times
                index++;
            }

            for(int i = 0; i < count; i++){
                printf("%c",a);
            }
        }
        printf("\n");
    }
    return 0;
}
