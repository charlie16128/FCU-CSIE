#include <stdio.h>

int main() {
    char a, b;
    while (scanf("%c %c", &a, &b) != EOF) {
        int sum = (a - 'A') + (b - 'A');
        char result = ((sum % 26) + 1) + 'A';
        printf("%c\n", result);
        getchar();
    }
    return 0;
}
