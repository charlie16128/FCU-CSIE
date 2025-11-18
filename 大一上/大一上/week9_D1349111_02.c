#include <stdio.h>


void convert(const int n)
{
    int tempn = n;
    int remain = 0;
    char output[100] ={0};
    int index = 0;
    while(tempn > 0){
        remain = tempn % 62;
        if(remain >= 0  && remain <= 9){
            output[index++] = remain + '0';
        }
        else if(remain >= 10 && remain <= 35){
            output[index++] = 'A' + remain - 10;
        }
        else if(remain >= 36 && remain <= 61){
            output[index++] = 'a' + remain - 36;
        }
        tempn = tempn / 62;
    }
    for(int i = index - 1; i >= 0; i--){
        printf("%c",output[i]);
    }
}


int main(void)
{
    int n;
    while (scanf("%d", &n) != EOF)
    {
        convert(n);
        printf("\n");
    }
}