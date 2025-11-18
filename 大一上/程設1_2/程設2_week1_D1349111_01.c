#include <stdio.h>
#include <math.h>
#include <stdlib.h>
int get_Quadrant(int x, int y){
    if(x > 0 && y > 0) return 1;
    if(x < 0 && y > 0) return 2;
    if(x < 0 && y < 0) return 3;
    if(x > 0 && y < 0) return 4;
}

int if_switch(int x1, int y1, int x2, int y2) {
    int dist1 = abs(x1) + abs(y1); 
    int dist2 = abs(x2) + abs(y2); 

    if (dist1 != dist2) 
        return dist1 < dist2;

    if (abs(x1) != abs(x2)) 
        return abs(x1) < abs(x2);
        
    if (abs(y1) != abs(y2)) 
        return abs(y1) < abs(y2);

    return get_Quadrant(x1, y1) < get_Quadrant(x2, y2);
}

int main(){
    int num = 0;
    scanf("%d",&num);

    int coord[10000][2];
    for(int i = 0; i < num; i++){
        scanf("%d%d",&coord[i][0],&coord[i][1]);
    }

    for(int i = 0; i < num - 1; i++){
        for(int k = 0; k < num - 1 - i; k++){
            int x1 = coord[k][0],y1 = coord[k][1];
            int x2 = coord[k + 1][0],y2 = coord[k + 1][1];
            if(if_switch(x1,y1,x2,y2) == 1){
                int temp_x = coord[k][0];
                int temp_y = coord[k][1];
                coord[k][0] = coord[k + 1][0];
                coord[k][1] = coord[k + 1][1];
                coord[k + 1][0] = temp_x;
                coord[k + 1][1] = temp_y;
            }
        }
    }

    for(int i = 0; i < num; i++){
        printf("%d %d\n",coord[i][0],coord[i][1]);
    }
    printf("%d",if_switch(2,2,-2,2));
    return 0;
}