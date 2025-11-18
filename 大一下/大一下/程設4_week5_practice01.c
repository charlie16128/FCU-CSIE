// #include <stdio.h>
// #include <string.h>

// int main() {
//     int tc;
//     scanf("%d", &tc); // 讀取測試案例數量

//     while (tc--) {
//         int n;
//         scanf("%d", &n); // 每組測資中的骨牌數量

//         int count[100] = {0}; // 用來記錄每種骨牌的數量（最多 9*10+9 = 99 種）
//         int pairs = 0; // 最終的答案：等價的骨牌對數

//         for (int i = 0; i < n; i++) {
//             int a, b;
//             scanf("%d %d", &a, &b); // 讀入每塊骨牌的兩個數字

//             // 標準化骨牌：確保小的數在前，這樣 [1,2] 和 [2,1] 會被視為同一種
//             int min_val, max_val;
//             if (a < b) {
//                 min_val = a;
//                 max_val = b;
//             } else {
//                 min_val = b;
//                 max_val = a;
//             }

//             // 把骨牌轉成一個唯一的 key，例如 [1,2] → 12
//             int key = min_val * 10 + max_val;

//             // 對於已經出現過的這種骨牌，每出現一次，就會多一個配對
//             pairs += count[key]; // 如果這個 key 已出現 k 次，這塊就可以與那 k 塊形成 k 對
//             count[key]++; // 把這個 key 的出現次數加 1
//         }
//         printf("%d\n", pairs); // 輸出結果
//     }

//     return 0;
// }

// #include <stdio.h>

// int main(){
//     int tc;
//     scanf("%d",&tc);
//     while(tc--){
//         int n;
//         scanf("%d",&n);

//         int count[100] = {0};
//         int pair = 0;
//         for(int i = 0; i < n; i++){
//             int a, b;
//             scanf("%d %d",&a, &b);

//             int big, small;
//             if(a > b){
//                 big = a;
//                 small = b;
//             }else{
//                 big = b;
//                 small = a;
//             }
//             int key = big * 10 + small;
//             pair += count[key];
//             count[key]++;
//         }
//         printf("%d\n",pair);
//     }
//     return 0;
// }

#include <stdio.h>

int main(){
    int tc;
    scanf("%d",&tc);
    while(tc--){
        int n;
        scanf("%d",&n);

        int count[100] = {0}, pair = 0;
        for(int i = 0; i < n; i++){
            int a, b;
            scanf("%d %d",&a, &b);

            int big, small;
            if(a > b){
                big = a;
                small = b;
            }else{
                small = a;
                big = b;
            }

            int key = big * 10 + small;
            pair += count[key];
            count[key]++;
        }
        printf("%d\n",pair);
    }
    return 0;
}