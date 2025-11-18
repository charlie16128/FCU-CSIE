#include <stdio.h>

unsigned long long convert(unsigned long long input) {
    unsigned long long reverse = 0;
    while (input > 0) {
        reverse = reverse * 10 + input % 10;
        input /= 10;
    }
    return reverse;
}

int main() {
    int num;
    scanf("%d", &num);
    for (int i = 0; i < num; i++) {
        unsigned long long input;
        scanf("%llu", &input);

        int counter = 1; 
        input += convert(input);
        unsigned long long reverse = convert(input);

        while (input != reverse) {
            input += reverse;
            reverse = convert(input);
            counter++;
        }
        printf("%d %llu\n", counter, input);
    }
    return 0;
}
