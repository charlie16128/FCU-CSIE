#include <stdio.h>
#include <string.h>

int main(){
    int tc;
    scanf("%d",&tc);
    getchar();
    while(tc--){
        char input[10000];
        if(fgets(input, sizeof(input), stdin)){
            input[strcspn(input, "\n")] = 0;
            char stack[10000];
            int top = -1;
            int check = 1;

            for(int i = 0; input[i] != '\0'; i++){
                if(input[i] == '(' || input[i] == '['){
                    stack[++top] = input[i];
                }
                else if(input[i] == ')'){
                    if(top == -1  || stack[top] != '('){
                        check = 0;
                        break;
                    }
                    top--;
                }
                else if(input[i] == ']'){
                    if(top == -1 || stack[top] != '['){
                        check = 0;
                        break;
                    }
                    top--;
                }
            }
            if(top != -1) check = 0;

            if(check) printf("Yes\n");
            else printf("No\n");
        }else{
            printf("Yes\n");
        }
    }
    return 0;
}
