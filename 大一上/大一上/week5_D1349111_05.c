#include <stdio.h>

int main() {
    char input;
    int move, encrypt,result;
    while (scanf("%c %d %d", &input, &move, &encrypt) != EOF) {
        int tempinput = (int)input;
        if ( encrypt == 1 ) { 
            result = tempinput + move;
            if (tempinput >= 65 && tempinput <= 90 && result > 90) {  
                //result -= 26;   
                result -= 26;
            }
            else if (tempinput >= 97 && tempinput <= 122 && result > 122) {  
                result -= 26;   
            }
            printf("%c\n", (char)result);
        }else if ( encrypt == 2 ) { 
            result = input - move;
            if (tempinput >= 65 && tempinput <= 90 && result < 65) {   
                result += 26;     
            }
            else if (tempinput >= 97 && tempinput <= 122 && result < 97) {   
                result += 26;     
            }
            printf("%c\n",(char)result);
        }
        input = 0, encrypt = 0; //初始化值
//        input = '\0', result = '\0';
    }
    return 0;
}