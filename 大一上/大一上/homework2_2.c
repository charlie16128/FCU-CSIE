#include <stdio.h>

// 函數用來進行大數乘法
void cross(int a[], int b, int *a_size) {
    int carry = 0;
    for (int i = 0; i < *a_size; i++) {
        int prod = a[i] * b + carry;
        a[i] = prod % 10; // 存放當前位的數字
        carry = prod / 10; // 更新進位
    }

    // 處理剩餘的進位
    while (carry) {
        a[*a_size] = carry % 10;
        carry /= 10;
        (*a_size)++;
    }
}

int main() {
    int n;
    printf("Enter a number: ");
    scanf("%d", &n);

    // 用來存放結果的陣列（假設最多2000位數）
    int a[2000] = {1}; 
    int a_size = 1; // 初始值 1! = 1

    // 逐步計算階乘
    for (int i = 2; i <= n; i++) {
        cross(a, i, &a_size); // 將當前的階乘乘數與結果相乘
    }

    // 從高位到低位輸出結果
    printf("%d! = ", n);
    for (int i = a_size - 1; i >= 0; i--) {
        printf("%d", a[i]);
    }
    printf("\n");

    return 0;
}
