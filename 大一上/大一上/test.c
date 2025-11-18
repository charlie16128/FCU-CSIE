// #include <stdio.h>

// int main() {
//     char str[1000];
//     // 從標準輸入讀取最多 999 個字符的字符串
//     fgets(str, 1000, stdin);
//     printf("讀取到的字符串: %s", str);
//     return 0;
// }


// #include <stdio.h>
// #include <string.h>

// int main() {
//     char ch[100]; // 用於存儲字符的陣列
//     int i = 0;    // 記錄讀取到的字符數

//     // 每次讀取一個字符，直到 EOF 或達到陣列容量
//     while (i < sizeof(ch) - 1 && (ch[i] = getchar()) != EOF) {
//         i++;
//     }
//     ch[i] = '\0'; // 在陣列末尾加上終止符

//     printf("%s", ch);

//     return 0;
// }

// #include <stdio.h>
// int main(){
//     int n;
//     int count[10] = {0};
//     while(scanf("%d", &n) != EOF && n < 10){
//         count[n]++;
//     }
//     for(int i = 0; i < 10; i++){
//         printf("%d:%d\n", i, count[i]);
//     }
//     return 0;
// }

#include <stdio.h>

int main() {
    int num;
    scanf("%d", &num);
    
    int input[num];
    for (int i = 0; i < num; i++) {
        scanf("%d", &input[i]);
    }

    int search;
    scanf("%d", &search);

    // lower_bound
    int left = 0, right = num;
    while (left < right) {
        int mid = left + (right - left) / 2; // 避免溢位
        if (input[mid] < search) {
            left = mid + 1;
        } 
        else {
            right = mid;
        }
    }
    printf("lower_bound: %d\n", left);

    // upper_bound
    left = 0, right = num; // 重置左右界限
    while (left < right) {
        int mid = left + (right - left) / 2; // 避免溢位
        if (input[mid] <= search) {
            left = mid + 1;
        } 
        else {
            right = mid;
        }
    }
    printf("upper_bound: %d\n", left);

    return 0;
}




