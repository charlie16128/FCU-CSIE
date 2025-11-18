#include <stdio.h>
int isnegetiveornot(int input_x , int input_y){
    if(input_x < 0){
        input_x = -(input_x);
    }
    if(input_y < 0){
        input_y = -(input_y);
    }
    return input_x + input_y;
}

int main(){

    int x,y;
    while(scanf("%d %d",&x,&y) != EOF){
        if(x > 0 && y > 0){
            printf("First Quadrant\n%d\n",isnegetiveornot(x,y));
        }
        else if(x < 0 && y > 0){
            printf("Second Quadrant\n%d\n",isnegetiveornot(x,y));
        }
        else if(x < 0 && y < 0){
            printf("Third Quadrant\n%d\n",isnegetiveornot(x,y));
        }
        else if(x > 0 && y < 0){
            printf("Fourth Quadrant\n%d\n",isnegetiveornot(x,y));
        }
        else if(x == 0 || y == 0){
            printf("On Axis\n%d\n",isnegetiveornot(x,y));
        }
    }

    return 0;
}