#include <stdio.h>
#include <stdlib.h>

int count_binary_one(int n){
    int count = 0;
    while(n){
        if(n & 1) count++; //check if the last bit is 1 , because computer use binary to store negative number
        n >>= 1; // right shift 1 bit
    }
    return count;
}

int main(){
    int n;
    scanf("%d",&n);

    while(n-- > 0){
        char input[100] = {0};
        scanf("%s",&input);

        int binary_count = count_binary_one(atoi(input)); // atoi convert strign to integer

        int hexa_input = strtol(input, NULL, 16);//先將字串input用16進解析，轉成2進再轉成10進

        int hexa_count = count_binary_one(hexa_input);// convert hexa to binary and count 1
        
        printf("%d %d\n",binary_count, hexa_count);
    }

    return 0;
}