#include <stdio.h>
#include <string.h>

int main() {
    int scent[51][51] = {0}; 
    int border_x, border_y;
    scanf("%d %d", &border_x, &border_y);

    int x, y;
    char face;
    char command[105] = {0};

    while(scanf("%d %d %c", &x, &y, &face) != EOF){
        getchar();
        fgets(command, 105, stdin);

        int islost = 0;

        for(int i = 0; command[i] != '\0' && command[i] != '\n'; i++){
            if(command[i] == 'L'){
                if (face == 'N') face = 'W';
                else if (face == 'W') face = 'S';
                else if (face == 'S') face = 'E';
                else if (face == 'E') face = 'N';
            } 
            else if(command[i] == 'R'){
                if (face == 'N') face = 'E';
                else if (face == 'E') face = 'S';
                else if (face == 'S') face = 'W';
                else if (face == 'W') face = 'N';
            } 
            else if(command[i] == 'F'){
                int prev_x = x, prev_y = y;
                if (face == 'N') y++;
                else if (face == 'S') y--;
                else if (face == 'E') x++;
                else if (face == 'W') x--;

                if(x < 0 || x > border_x || y < 0 || y > border_y){
                    if(scent[prev_x][prev_y] == 0){
                        scent[prev_x][prev_y] = 1;
                        x = prev_x;
                        y = prev_y;
                        islost = 1;
                        break;
                    } 
                    else{ 
                        x = prev_x;
                        y = prev_y;
                    }
                }
            }
        }

        if(islost == 1){
            printf("%d %d %c LOST\n", x, y, face);
        } 
        else{
            printf("%d %d %c\n", x, y, face);
        }
    }
    return 0;
}