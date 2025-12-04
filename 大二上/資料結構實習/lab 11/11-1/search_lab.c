#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define DATA_SIZE 1000000
#define TABLE_SIZE 1500007 // 使用質數減少碰撞

// 交易結構
typedef struct {
    long id;
    char date[16];
    char custId[16];
    char itemName[32];
    double price;
} Transaction;

// Hash Table 節點
typedef struct Node {
    Transaction *data;
    struct Node *next;
} Node;

Transaction *dataset; // 動態配置
Node **hashTable;     // Hash Table

// ------------------- 讀取與建構 -------------------

void loadData(const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        printf("ERROR: Cannot open %s\n", filename);
        exit(1);
    }

    dataset = (Transaction*)malloc(sizeof(Transaction) * DATA_SIZE);
    if (!dataset) { printf("Memory Error\n"); exit(1); }

    char buffer[256];
    int i = 0;
    while (fgets(buffer, sizeof(buffer), fp) && i < DATA_SIZE) {
        // 解析 CSV
        sscanf(buffer, "%ld,%[^,],%[^,],%[^,],%lf", 
               &dataset[i].id, dataset[i].date, dataset[i].custId, dataset[i].itemName, &dataset[i].price);
        i++;
    }
    fclose(fp);
}

int hashCode(long key) {
    return key % TABLE_SIZE;
}

void buildHashTable() {
    hashTable = (Node**)malloc(sizeof(Node*) * TABLE_SIZE);
    for (int i = 0; i < TABLE_SIZE; i++) hashTable[i] = NULL;
    
    for (int i = 0; i < DATA_SIZE; i++) {
        int index = hashCode(dataset[i].id);
        Node *newNode = (Node*)malloc(sizeof(Node));
        newNode->data = &dataset[i];
        newNode->next = hashTable[index];
        hashTable[index] = newNode;
    }
}

// ------------------- 搜尋演算法 -------------------

// 1. 線性搜尋
int linearSearch(long key) {
    for (int i = 0; i < DATA_SIZE; i++) {
        if (dataset[i].id == key) return i;
    }
    return -1;
}

// 2. 二分搜尋
int binarySearch(long key) {
    int left = 0, right = DATA_SIZE - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (dataset[mid].id == key) return mid;
        if (dataset[mid].id < key) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// 3. 插補搜尋 (優化版：減少記憶體讀取)
int interpolationSearch(long key) {
    int low = 0, high = DATA_SIZE - 1;
    
    // 預先讀取邊界值，減少迴圈內的記憶體存取次數 (Cache Optimization)
    long lowVal = dataset[low].id;
    long highVal = dataset[high].id;

    // 提早檢查範圍 (若不在範圍內直接回傳)
    if (key < lowVal || key > highVal) return -1;

    while (low <= high && key >= lowVal && key <= highVal) {
        
        if (low == high) {
            return (lowVal == key) ? low : -1;
        }
        
        // 公式：預測位置
        // 使用暫存變數運算，避免重複存取 dataset[high] 或 dataset[low]
        long long numerator = (long long)(key - lowVal) * (high - low);
        long long denominator = highVal - lowVal;
        
        if (denominator == 0) return (lowVal == key) ? low : -1;
        
        int pos = low + (int)(numerator / denominator);
        
        // 防止索引越界
        if (pos < 0 || pos >= DATA_SIZE) return -1;

        long posVal = dataset[pos].id; // 這是迴圈內唯一一次讀取 dataset

        if (posVal == key) return pos;
        
        if (posVal < key) {
            low = pos + 1;
            // 更新下邊界的值，供下一次迴圈使用
            if (low < DATA_SIZE) lowVal = dataset[low].id; 
        } else {
            high = pos - 1;
            // 更新上邊界的值
            if (high >= 0) highVal = dataset[high].id;
        }
    }
    return -1;
}

// 4. 雜湊搜尋
int hashSearch(long key) {
    int index = hashCode(key);
    Node *curr = hashTable[index];
    while (curr != NULL) {
        if (curr->data->id == key) return 1; // Found
        curr = curr->next;
    }
    return -1;
}

// ------------------- 測試邏輯 -------------------

long checkSum = 0; // 防止編譯器優化

double measureTime(const char* name, int type, long keys[], int count, int repeat) {
    clock_t start = clock();
    
    for (int r = 0; r < repeat; r++) {
        for (int i = 0; i < count; i++) {
            int result = -1;
            switch(type) {
                case 0: result = linearSearch(keys[i]); break;
                case 1: result = binarySearch(keys[i]); break;
                case 2: result = interpolationSearch(keys[i]); break;
                case 3: result = hashSearch(keys[i]); break;
            }
            checkSum += result; 
        }
    }
    
    clock_t end = clock();
    double totalSec = ((double)(end - start)) / CLOCKS_PER_SEC;
    return (totalSec * 1000000000.0) / (count * repeat); 
}

int main() {
    // 關閉輸出緩衝
    setvbuf(stdout, NULL, _IONBF, 0);

    loadData("data.csv");
    buildHashTable();

    long existKeys[10];
    long nonExistKeys[10];
    srand(time(NULL));

    // 1. 產生存在的 Key
    for(int i=0; i<10; i++) {
        existKeys[i] = dataset[rand() % DATA_SIZE].id;
    }
    
    // 2. 產生「不存在」的 Key (修正版)
    // 我們尋找資料間的空隙 (Gap)，確保這些 Key 位於資料範圍內，但剛好沒被使用
    // 這樣插補搜尋才不會在第一行邊界檢查就直接 return，能真正測試出演算法效能
    int count = 0;
    for (int i = 0; i < DATA_SIZE - 1 && count < 10; i++) {
        // 如果前後兩個 ID 差超過 1，代表中間有空號
        if (dataset[i+1].id > dataset[i].id + 1) {
            nonExistKeys[count] = dataset[i].id + 1; // 取中間的空號
            count++;
            i += 50000; // 跳過一大段，讓測試 Key 分散一點
        }
    }
    // 萬一空隙不夠 (機率很低)，用舊方法補滿
    while (count < 10) {
        nonExistKeys[count++] = dataset[DATA_SIZE-1].id + (rand() % 10000) + 1;
    }

    int repeat_slow = 20;     
    int repeat_fast = 500000; 

    // Linear
    double t_lin_e = measureTime("Linear", 0, existKeys, 10, repeat_slow);
    double t_lin_n = measureTime("Linear", 0, nonExistKeys, 10, repeat_slow);
    printf("Linear %.2f %.2f\n", t_lin_e, t_lin_n);

    // Binary
    double t_bin_e = measureTime("Binary", 1, existKeys, 10, repeat_fast);
    double t_bin_n = measureTime("Binary", 1, nonExistKeys, 10, repeat_fast);
    printf("Binary %.2f %.2f\n", t_bin_e, t_bin_n);

    // Interpolation
    double t_int_e = measureTime("Interpolation", 2, existKeys, 10, repeat_fast);
    double t_int_n = measureTime("Interpolation", 2, nonExistKeys, 10, repeat_fast);
    printf("Interpolation %.2f %.2f\n", t_int_e, t_int_n);

    // Hash
    double t_hash_e = measureTime("Hash", 3, existKeys, 10, repeat_fast);
    double t_hash_n = measureTime("Hash", 3, nonExistKeys, 10, repeat_fast);
    printf("Hash %.2f %.2f\n", t_hash_e, t_hash_n);

    return 0;
}