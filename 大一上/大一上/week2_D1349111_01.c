#include <stdio.h>
int main(){
    int originword,num;
    char newword;
    scanf("%c %d",&originword,&num);
    if(originword + num > 122){
        newword = originword - 26 + num;
    }
    else{
        newword = originword + num;
    }
    printf("%c",newword);
}