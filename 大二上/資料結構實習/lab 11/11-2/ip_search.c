#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <windows.h> // Windows 專用高精度計時

// 實驗限制與參數設定
#define MAX_IPS 10000       //  最多不超過 10000 個不同 IP
#define TABLE_SIZE 20011    // 質數，大於 MAX_IPS * 2 以減少碰撞

typedef struct {
    char ip[16]; // 儲存 IP 字串，如 "140.123.1.2"
    int count;   // 計數器
} Entry;

// 全域資料結構
Entry seqArray[MAX_IPS];      // 循序搜尋用的陣列
int seqCount = 0;             // 目前陣列中有幾筆資料
Entry hashTable[TABLE_SIZE];  // 雜湊表 (全域變數預設內容為 0)

// 計時器頻率
long long frequency = 0;

// 初始化計時器
void initTimer() {
    LARGE_INTEGER li;
    QueryPerformanceFrequency(&li);
    frequency = li.QuadPart;
}

// 取得奈秒時間 (Windows)
long long getNanoTime() {
    if (frequency == 0) initTimer();
    LARGE_INTEGER li;
    QueryPerformanceCounter(&li);
    return (li.QuadPart * 1000000000LL) / frequency;
}

// ★★★ 優化後的 Hash 函數 ★★★
// 1. 不使用 sscanf，改用手動解析 (速度快)
// 2. 邏輯：(k1.k2) XOR (k3.k4) [cite: 53]
//    將 k1, k2 視為高低位組合成 16bit 數字，擴大數值範圍避免群聚
unsigned int xorHash(const char* ip) {
    unsigned int parts[4] = {0};
    unsigned int val = 0;
    int idx = 0;
    const char* p = ip;

    // 手動解析字串 "140.111.22.3" -> [140, 111, 22, 3]
    while (*p) {
        if (*p == '.') {
            parts[idx++] = val;
            val = 0;
        } else {
            val = val * 10 + (*p - '0');
        }
        p++;
    }
    parts[idx] = val; // 存入最後一段

    // 實作改良版 XOR 雜湊
    // 讓範圍擴展到 0 ~ 65535，大幅減少碰撞
    unsigned int group1 = (parts[0] << 8) | parts[1]; // k1.k2
    unsigned int group2 = (parts[2] << 8) | parts[3]; // k3.k4
    
    return group1 ^ group2;
}

int main() {
    char ip[32];
    initTimer();

    // 持續讀取 Java 傳來的 IP
    while (scanf("%s", ip) != EOF) {
        // 接收到退出指令
        if (strcmp(ip, "EXIT") == 0) break;

        long long start, end;
        long long seqTime, hashTime;

        // ==========================================
        // 1. 循序搜尋 (Sequential Search) [cite: 46]
        // ==========================================
        start = getNanoTime();
        int found = 0;
        for (int i = 0; i < seqCount; i++) {
            if (strcmp(seqArray[i].ip, ip) == 0) { // [cite: 48] 從頭比對
                seqArray[i].count++; // [cite: 49] 找到則計數++
                found = 1;
                break;
            }
        }
        // [cite: 50] 找不到則新增
        if (!found && seqCount < MAX_IPS) {
            strcpy(seqArray[seqCount].ip, ip);
            seqArray[seqCount].count = 1;
            seqCount++;
        }
        end = getNanoTime();
        seqTime = end - start;

        // ==========================================
        // 2. 雜湊搜尋 (Hash Table) [cite: 52]
        // ==========================================
        start = getNanoTime();
        unsigned int h = xorHash(ip);
        int index = h % TABLE_SIZE; // [cite: 54] 計算 Index
        
        // 處理碰撞：Linear Probing [cite: 56]
        while (hashTable[index].count != 0) {
            if (strcmp(hashTable[index].ip, ip) == 0) {
                break; // 找到了
            }
            index = (index + 1) % TABLE_SIZE; // 往下一格找
        }
        
        if (hashTable[index].count == 0) {
            // 空位置，新增
            strcpy(hashTable[index].ip, ip);
            hashTable[index].count = 1;
        } else {
            // 已存在，計數++
            hashTable[index].count++;
        }
        end = getNanoTime();
        hashTime = end - start;

        // 回傳兩個時間給 Java (奈秒)
        printf("%lld %lld\n", seqTime, hashTime);
        fflush(stdout); // ★重要：清空緩衝區，確保 Java 立刻收到
    }

    return 0;
}