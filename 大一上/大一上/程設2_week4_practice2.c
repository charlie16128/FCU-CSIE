#include <stdio.h>

int main(){
    int num, ans, input[1000][2];

    while(scanf("%d",&num) != EOF){
        ans = 0;
        for(int i = 0; i < num; i++){
            scanf("%d %d",&input[i][0], &input[i][1]);
        }
        
        for(int i = 0; i < num; i++){
            if(input[i][0] > 0){
                for(int k = 0; k < num; k++){
                    if(i != k && input[i][0] == input[k][1] && input[i][1] == input[k][0]){
                        ans++;
                        input[i][0] = -1;
                        input[i][1] = -1;
                        input[k][0] = -1;
                        input[k][1] = -1;
                        break;
                    }
                }
            }
        }

        printf("%d\n",ans);

    }
    return 0;
}





//¦Û¤v¼g
#include <stdio.h>

int main(){
    int num;
    while(scanf("%d",&num) != EOF){
        int input[1000][1000] = {0};
        for(int i = 0; i < num; i++){
            scanf("%d %d", &input[i][0], &input[i][1]);
        }

        int counter = 0;
        for(int i = 0; i < num; i++){
            if(input[i][0] != -1){
                for(int k = 0; k < num; k++){
                    if(i != k && input[i][0] == input[k][1] && input[i][1] == input[k][0]){
                        input[i][0] = -1;
                        input[i][1] = -1;
                        input[k][0] = -1;
                        input[k][1] = -1;
                        counter++;
                        break;
                    }
                }
            }
        }
        printf("%d\n",counter);
    }
    return 0;
}