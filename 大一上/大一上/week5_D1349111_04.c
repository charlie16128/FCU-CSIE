#include <stdio.h>
void is_it_a_triangle(int x , int y , int z){
    if(x + y > z && y + z > x && z + x > y){
        if(x == y && y == z){
            printf("Equilateral Triangle\n");
        }
        else if(x*x + y*y == z*z || y*y + z*z == x*x || z*z + x*x == y*y){
            printf("Right Triangle\n");
        }
        else if(x == y || y == z || z == x){
            printf("Isosceles Triangle\n");
        }
        else{
            printf("Scalene Triangle\n");
        }
    }
    else{
        printf("Not a Triangle\n");
    }
}
int main(){
    int x,y,z;
    while(scanf("%d %d %d",&x,&y,&z) != EOF){
        is_it_a_triangle(x,y,z);
    }
    return 0;
}