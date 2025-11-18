#include <stdio.h>

int my_fib(const int n)
{
    if(n == 1){
        return 1;
    }
    else if(n <= 0){
        return 0;
    }
    else if (n > 1){
        return my_fib(n - 1) + my_fib(n - 2);
    }
}


int main(void)
{
    int n;
    while(scanf(" %d",&n) != EOF)
    {
        printf("%d\n",my_fib(n));
    }
}
