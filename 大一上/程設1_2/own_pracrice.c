#include <stdio.h>

int main(){
    char input_1;
    scanf("%c", &input_1);                  //a = 0110 0001 , A= 0100 0001 in 0x
    printf("%c", input_1 & 0b11011111);   // Convert lowercase to uppercase
    return 0;
}
