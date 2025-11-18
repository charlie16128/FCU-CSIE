#include<stdio.h>

int main(){
    int a,b,c,d,e,f;
    scanf("%d/%d/%d",&a,&b,&c); //abc為當前月/日/年
    scanf("%d/%d/%d",&d,&e,&f); //def為出生月/日/年
    int age = c-f;
    if(f > c || (f == c && e>b) || (f == c && e == b && d>a)){
        printf("Invalid birth date\n");
        return 0;
    }
    if(b < e || (b == e && a < d)){ //還沒到生日,月還沒到或同月天還沒到
        age--;
    }
    if(age > 130){  // 2000/1/1 1870/1/2
        printf("Check birth date\n");
    }
    else{
        printf("%d\n",age);
    }
    return 0;
}