#include <stdio.h>
#include <string.h>

int main(){
    int field_x, field_y, counter = 1;
    int dir[8][2] = {{-1,-1},{-1,0},{-1,1},{0,-1},{0,1},{1,-1},{1,0},{1,1}};

    while(scanf("%d %d",&field_x, &field_y) && field_x  && field_y){
        char input[1000][1000] = {0};
        for(int i = 0; i < field_x; i++){
            scanf("%s",input[i]);
        }

        if(counter > 1) printf("\n");
        printf("Field #%d:\n",counter++);

        for(int i = 0; i < field_x; i++){
            for(int k = 0; k < field_y; k++){
                if(input[i][k] == '*'){
                    printf("*");
                }else{
                    int cnt = 0;
                    for(int j = 0; j < 8; j++){
                        int x = i + dir[j][0];
                        int y = k + dir[j][1];
                        if(x >= 0 && y >= 0 && x < field_x && y < field_y && input[x][y] == '*'){
                            cnt++;
                        }
                    }
                    printf("%d",cnt);
                }
            }
            printf("\n");
        }
    }
    return 0;
}

/*
#include <stdio.h>

int main(){
    int field_x,field_y, counter = 1;
    int map[8][2] = {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};
    while(scanf("%d %d",&field_x, &field_y) && field_x && field_y){
        char input[110][110];
        for(int m = 0; m < field_x; m++){
            scanf("%s",&input[m]);
        }

        if(counter > 1) printf("\n");
        printf("Field #%d:\n",counter++);

        for(int i = 0; i < field_x; i++){
            for(int k = 0; k < field_y; k++){
                if(input[i][k] == '*'){
                    printf("*");
                }else{
                    int cnt = 0;
                    for(int j = 0; j < 8; j++){
                        int x = i + map[j][0];
                        int y = k + map[j][1];
                        if(x >= 0 && y >= 0 && x < field_x && y < field_y && input[x][y] == '*'){
                            cnt++;
                        }
                    }
                    printf("%d",cnt);
                }
            }
            printf("\n");
        }
    }
    return 0;
}
*/