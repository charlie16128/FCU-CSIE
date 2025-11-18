#include <stdio.h>
int main(){
    int money,count10,count5,count1,sum;
    scanf("%d",&money);
    count10 = money / 10;
    money = money - 10 * count10;

    count5 = money / 5;
    money = money - 5 * count5;
    
    count1 = money / 1;

    sum = count10 + count5 + count1;

    printf("%d",sum);
    return 0;
}