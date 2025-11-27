# 外部排序程式碼邏輯詳解

## 目錄
1. [方法一：Merge Sort 外部排序](#方法一merge-sort-外部排序)
2. [方法二：Min-Heap 外部排序](#方法二min-heap-外部排序)
3. [Java GUI 程式](#java-gui-程式)

---

## 方法一：Merge Sort 外部排序

### 整體流程圖

```
輸入檔案 (100,000 筆)
    ↓
┌───────────────────────────────────┐
│ 階段 1: 產生 Runs                  │
│ generate_runs()                   │
└───────────────────────────────────┘
    ↓
run0.dat (10,000 筆)
run1.dat (10,000 筆)
run2.dat (10,000 筆)
    ...
run9.dat (10,000 筆)
    ↓
┌───────────────────────────────────┐
│ 階段 2: 多層合併                   │
│ merge_runs()                      │
└───────────────────────────────────┘
    ↓
sorted_merge.dat (100,000 筆)
```

---

### 階段 1：generate_runs() - 產生已排序的區段

```c
int generate_runs(const char *input_file, const char *run_prefix) {
    FILE *fin = fopen(input_file, "r");
    int *buffer = (int*)malloc(MAX_MEMORY * sizeof(int));
    int run_count = 0;
    int count;

    while (1) {
        count = 0;
        // 步驟 1: 讀取資料
        while (count < MAX_MEMORY && fscanf(fin, "%d", &buffer[count]) == 1) {
            count++;
        }

        if (count == 0) break;  // 沒有更多資料了

        // 步驟 2: 在記憶體內排序
        qsort(buffer, count, sizeof(int), compare);

        // 步驟 3: 寫入 run 檔案
        char run_filename[100];
        sprintf(run_filename, "%s%d.dat", run_prefix, run_count);
        FILE *fout = fopen(run_filename, "w");
        for (int i = 0; i < count; i++) {
            fprintf(fout, "%d\n", buffer[i]);
        }
        fclose(fout);
        run_count++;
    }

    free(buffer);
    fclose(fin);
    return run_count;
}
```

#### 逐步解析

**初始化**：
```c
FILE *fin = fopen(input_file, "r");  // 開啟輸入檔案
int *buffer = (int*)malloc(MAX_MEMORY * sizeof(int));  // 分配 10,000 個整數的陣列
int run_count = 0;  // 記錄產生了幾個 run
```

**主迴圈 - 處理每一批資料**：

```c
while (1) {
    // 第 1 步：讀取最多 10,000 筆資料
    count = 0;
    while (count < MAX_MEMORY && fscanf(fin, "%d", &buffer[count]) == 1) {
        buffer[count] = 讀到的數字;
        count++;
    }
    
    // 如果沒讀到任何資料，結束
    if (count == 0) break;
```

**範例執行過程（100,000 筆資料）**：

```
第 1 次迴圈：
  讀取: buffer[0]=67423, buffer[1]=12045, ..., buffer[9999]=88234
  count = 10000
  
第 2 次迴圈：
  讀取: buffer[0]=34567, buffer[1]=98765, ..., buffer[9999]=23456
  count = 10000
  
...

第 10 次迴圈：
  讀取: buffer[0]=45678, buffer[1]=11111, ..., buffer[9999]=99999
  count = 10000
  
第 11 次迴圈：
  讀取: 沒有更多資料
  count = 0 → 跳出迴圈
```

**排序並寫入**：

```c
    // 第 2 步：使用快速排序在記憶體內排序
    qsort(buffer, count, sizeof(int), compare);
    // 排序後：buffer[0] <= buffer[1] <= ... <= buffer[count-1]
    
    // 第 3 步：寫入檔案
    sprintf(run_filename, "%s%d.dat", run_prefix, run_count);
    // 例如：run_filename = "run_merge_0.dat"
    
    FILE *fout = fopen(run_filename, "w");
    for (int i = 0; i < count; i++) {
        fprintf(fout, "%d\n", buffer[i]);  // 一行一個數字
    }
    fclose(fout);
    run_count++;  // 完成一個 run
}
```

**執行結果**：
```
run_merge_0.dat: 包含 0-9999 範圍內的 10,000 個已排序數字
run_merge_1.dat: 包含 10000-19999 範圍內的 10,000 個已排序數字
...
run_merge_9.dat: 包含 90000-99999 範圍內的 10,000 個已排序數字
```

---

### 階段 2：merge_two_files() - 合併兩個已排序檔案

```c
void merge_two_files(const char *file1, const char *file2, 
                     const char *output, int *buffer) {
    FILE *f1 = fopen(file1, "r");
    FILE *f2 = fopen(file2, "r");
    FILE *fout = fopen(output, "w");

    // 將 10,000 陣列分成兩半
    int buffer_size = MAX_MEMORY / 2;  // 5,000
    int *buf1 = buffer;                 // 前 5,000 給 file1
    int *buf2 = buffer + buffer_size;   // 後 5,000 給 file2
    
    int count1 = 0, count2 = 0;  // 當前緩衝區有多少資料
    int pos1 = 0, pos2 = 0;      // 當前處理到哪個位置
    
    // 初始讀取
    while (count1 < buffer_size && fscanf(f1, "%d", &buf1[count1]) == 1) {
        count1++;
    }
    while (count2 < buffer_size && fscanf(f2, "%d", &buf2[count2]) == 1) {
        count2++;
    }
```

#### 記憶體配置圖解

```
buffer[10000] 的使用：

索引:    0                    4999  5000                  9999
        ┌────────────────────────┬────────────────────────┐
        │      buf1[5000]        │      buf2[5000]        │
        │  來自 file1 的緩衝區   │  來自 file2 的緩衝區   │
        └────────────────────────┴────────────────────────┘
```

#### 合併邏輯

```c
    // 主合併迴圈
    while (count1 > 0 || count2 > 0) {
        if (count1 > 0 && (count2 == 0 || buf1[pos1] <= buf2[pos2])) {
            // 情況 1: file1 的值較小（或 file2 已空）
            fprintf(fout, "%d\n", buf1[pos1]);
            pos1++;
            count1--;
            
            // 如果 buf1 用完了，重新填充
            if (count1 == 0 && !feof(f1)) {
                pos1 = 0;
                count1 = 0;
                while (count1 < buffer_size && fscanf(f1, "%d", &buf1[count1]) == 1) {
                    count1++;
                }
            }
        } else if (count2 > 0) {
            // 情況 2: file2 的值較小
            fprintf(fout, "%d\n", buf2[pos2]);
            pos2++;
            count2--;
            
            // 如果 buf2 用完了，重新填充
            if (count2 == 0 && !feof(f2)) {
                pos2 = 0;
                count2 = 0;
                while (count2 < buffer_size && fscanf(f2, "%d", &buf2[count2]) == 1) {
                    count2++;
                }
            }
        }
    }
```

#### 詳細執行範例

假設合併 `run0.dat` (10,000 筆) 和 `run1.dat` (10,000 筆)：

```
【初始狀態】
file1 (run0.dat): 0, 5, 10, 15, 20, ..., 99995
file2 (run1.dat): 2, 7, 12, 17, 22, ..., 99997

buf1 讀入: [0, 5, 10, ..., (前 5,000 個)] count1=5000, pos1=0
buf2 讀入: [2, 7, 12, ..., (前 5,000 個)] count2=5000, pos2=0

【第 1 次比較】
buf1[0]=0, buf2[0]=2
0 < 2 → 輸出 0
pos1++, count1--

【第 2 次比較】
buf1[1]=5, buf2[0]=2
5 > 2 → 輸出 2
pos2++, count2--

【第 3 次比較】
buf1[1]=5, buf2[1]=7
5 < 7 → 輸出 5
pos1++, count1--

... 持續比較並輸出 ...

【buf1 用完】
pos1 到達 5000，count1=0
重新讀取 file1 的下一批 5,000 筆
pos1 重置為 0，count1=5000

... 繼續合併 ...

【最終】
輸出檔案包含所有 20,000 筆，已排序
```

**動畫示意**：
```
Step 1:
buf1: [0, 5, 10, 15, 20]  ← pos1
buf2: [2, 7, 12, 17, 22]  ← pos2
output: []
比較 0 vs 2 → 輸出 0

Step 2:
buf1: [0, 5, 10, 15, 20]     ← pos1
buf2: [2, 7, 12, 17, 22]  ← pos2
output: [0]
比較 5 vs 2 → 輸出 2

Step 3:
buf1: [0, 5, 10, 15, 20]     ← pos1
buf2: [2, 7, 12, 17, 22]     ← pos2
output: [0, 2]
比較 5 vs 7 → 輸出 5

... 繼續 ...
```

---

### 階段 2：merge_runs() - 多層合併

```c
void merge_runs(const char *run_prefix, int run_count, const char *output_file) {
    int current_level = 0;
    int current_count = run_count;  // 當前層有多少個檔案
    
    int *buffer = (int*)malloc(MAX_MEMORY * sizeof(int));

    while (current_count > 1) {  // 直到只剩一個檔案
        int next_count = 0;
        
        // 兩兩配對合併
        for (int i = 0; i < current_count; i += 2) {
            char file1[100], file2[100], output[100];
            
            // 構造檔名
            if (current_level == 0) {
                sprintf(file1, "%s%d.dat", run_prefix, i);
            } else {
                sprintf(file1, "%slevel%d_%d.dat", run_prefix, current_level, i);
            }

            if (i + 1 < current_count) {
                // 有配對的檔案
                if (current_level == 0) {
                    sprintf(file2, "%s%d.dat", run_prefix, i + 1);
                } else {
                    sprintf(file2, "%slevel%d_%d.dat", run_prefix, current_level, i + 1);
                }
                sprintf(output, "%slevel%d_%d.dat", run_prefix, current_level + 1, next_count);
                
                // 合併兩個檔案
                merge_two_files(file1, file2, output, buffer);
                
                remove(file1);
                remove(file2);
            } else {
                // 奇數個檔案，最後一個直接移到下一層
                sprintf(output, "%slevel%d_%d.dat", run_prefix, current_level + 1, next_count);
                rename(file1, output);
            }
            next_count++;
        }
        
        current_level++;
        current_count = next_count;
    }

    // 重新命名最終結果
    char final_file[100];
    sprintf(final_file, "%slevel%d_0.dat", run_prefix, current_level);
    rename(final_file, output_file);
    
    free(buffer);
}
```

#### 合併樹狀圖（10 個檔案）

```
Level 0: 10 個檔案
run0.dat ─┐
run1.dat ─┴→ level1_0.dat ─┐
run2.dat ─┐                │
run3.dat ─┴→ level1_1.dat ─┴→ level2_0.dat ─┐
run4.dat ─┐                │                │
run5.dat ─┴→ level1_2.dat ─┘                │
run6.dat ─┐                                 ├→ level3_0.dat ─┐
run7.dat ─┴→ level1_3.dat ─┐                │                │
run8.dat ─┐                ├→ level2_1.dat ─┘                │
run9.dat ─┴→ level1_4.dat ─┘                                 │
                                                              ├→ sorted_merge.dat
                           level2_2.dat (run9 直接上來) ────→ level3_1.dat ─┘
```

#### 執行過程詳解

```
【Level 0 → Level 1】
current_level = 0, current_count = 10

迴圈 i=0:
  file1 = "run_merge_0.dat"
  file2 = "run_merge_1.dat"
  output = "run_merge_level1_0.dat"
  合併 → next_count = 1

迴圈 i=2:
  file1 = "run_merge_2.dat"
  file2 = "run_merge_3.dat"
  output = "run_merge_level1_1.dat"
  合併 → next_count = 2

... (i=4, 6, 8 同理) ...

結果：5 個檔案
current_level = 1, current_count = 5

【Level 1 → Level 2】
迴圈 i=0:
  file1 = "run_merge_level1_0.dat"
  file2 = "run_merge_level1_1.dat"
  output = "run_merge_level2_0.dat"
  合併 → next_count = 1

迴圈 i=2:
  file1 = "run_merge_level1_2.dat"
  file2 = "run_merge_level1_3.dat"
  output = "run_merge_level2_1.dat"
  合併 → next_count = 2

迴圈 i=4:
  file1 = "run_merge_level1_4.dat"
  沒有 file2（i+1 >= current_count）
  直接移動到 "run_merge_level2_2.dat"
  next_count = 3

結果：3 個檔案
current_level = 2, current_count = 3

【Level 2 → Level 3】
迴圈 i=0:
  合併 level2_0.dat + level2_1.dat → level3_0.dat

迴圈 i=2:
  直接移動 level2_2.dat → level3_1.dat

結果：2 個檔案
current_level = 3, current_count = 2

【Level 3 → 最終】
迴圈 i=0:
  合併 level3_0.dat + level3_1.dat → level4_0.dat

結果：1 個檔案
current_count = 1 → 跳出 while 迴圈

【重新命名】
level4_0.dat → sorted_merge.dat
```

---

## 方法二：Min-Heap 外部排序

### 整體流程圖

```
輸入檔案 (100,000 筆)
    ↓
┌───────────────────────────────────┐
│ 階段 1: 使用 Heap 產生較大 Runs    │
│ generate_runs_with_heap()         │
└───────────────────────────────────┘
    ↓
run_heap_0.dat (~16,667 筆)
run_heap_1.dat (~16,667 筆)
run_heap_2.dat (~16,667 筆)
run_heap_3.dat (~16,667 筆)
run_heap_4.dat (~16,667 筆)
run_heap_5.dat (~16,667 筆)
    ↓
┌───────────────────────────────────┐
│ 階段 2: K-way Merge (一次完成)    │
│ merge_files_with_heap()           │
└───────────────────────────────────┘
    ↓
sorted_heap.dat (100,000 筆)
```

---

### 資料結構：Min-Heap（最小堆）

#### 結構定義

```c
typedef struct HeapNode {
    int value;          // 數值
    int run_index;      // 來自哪個 run（用於合併階段）
    FILE *file;         // 對應的檔案指標（用於合併階段）
} HeapNode;

typedef struct MinHeap {
    HeapNode *nodes;    // 節點陣列
    int size;           // 當前元素數量
    int capacity;       // 容量
} MinHeap;
```

#### 堆的性質

```
最小堆性質：父節點 <= 子節點

        1
       / \
      3   2
     / \ / \
    7  5 4  6

陣列表示：[1, 3, 2, 7, 5, 4, 6]
索引關係：
  - 父節點: (i-1)/2
  - 左子節點: 2*i+1
  - 右子節點: 2*i+2
```

#### 核心操作

**1. heapify_down（向下調整）**

```c
void heapify_down(MinHeap *heap, int idx) {
    int smallest = idx;
    int left = 2 * idx + 1;
    int right = 2 * idx + 2;

    // 找出父、左子、右子中最小的
    if (left < heap->size && heap->nodes[left].value < heap->nodes[smallest].value)
        smallest = left;
    if (right < heap->size && heap->nodes[right].value < heap->nodes[smallest].value)
        smallest = right;

    // 如果最小的不是父節點，交換並繼續調整
    if (smallest != idx) {
        swap(&heap->nodes[idx], &heap->nodes[smallest]);
        heapify_down(heap, smallest);  // 遞迴
    }
}
```

**範例**：
```
初始（違反堆性質）:
        5
       / \
      3   2
     
步驟 1: 比較 5, 3, 2 → 最小是 2
        交換 5 和 2
        2
       / \
      3   5
      
結果：恢復堆性質 ✓
```

**2. heapify_up（向上調整）**

```c
void heapify_up(MinHeap *heap, int idx) {
    while (idx > 0) {
        int parent = (idx - 1) / 2;
        if (heap->nodes[idx].value < heap->nodes[parent].value) {
            swap(&heap->nodes[idx], &heap->nodes[parent]);
            idx = parent;
        } else {
            break;
        }
    }
}
```

**範例**：
```
初始（新插入 1 在最後）:
        2
       / \
      3   4
     / \
    5   1  ← 新插入

步驟 1: 比較 1 和父節點 3 → 1 < 3，交換
        2
       / \
      1   4
     / \
    5   3

步驟 2: 比較 1 和父節點 2 → 1 < 2，交換
        1
       / \
      2   4
     / \
    5   3

結果：恢復堆性質 ✓
```

**3. insert（插入）**

```c
void insert(MinHeap *heap, HeapNode node) {
    heap->nodes[heap->size] = node;  // 放在最後
    heapify_up(heap, heap->size);    // 向上調整
    heap->size++;
}
```

**4. extractMin（取出最小值）**

```c
HeapNode extractMin(MinHeap *heap) {
    HeapNode min = heap->nodes[0];              // 保存根節點
    heap->nodes[0] = heap->nodes[heap->size - 1];  // 最後元素移到根
    heap->size--;
    heapify_down(heap, 0);                      // 向下調整
    return min;
}
```

**範例**：
```
初始:
        1
       / \
      2   3
     / \
    4   5

步驟 1: 取出根節點 1
步驟 2: 最後元素 5 移到根
        5
       / \
      2   3
     /
    4

步驟 3: heapify_down
        2
       / \
      4   3
     /
    5

回傳: 1
```

---

### 階段 1：generate_runs_with_heap() - 產生較大的 Runs

```c
int generate_runs_with_heap(const char *input_file, const char *run_prefix) {
    FILE *fin = fopen(input_file, "r");
    
    // 雙緩衝區
    int *buffer = (int*)malloc(MAX_MEMORY * sizeof(int));
    int *next_buffer = (int*)malloc(MAX_MEMORY * sizeof(int));
    MinHeap *heap = createMinHeap(MAX_MEMORY);
    
    int run_count = 0;
    
    // 讀取第一批資料
    int count = 0;
    while (count < MAX_MEMORY && fscanf(fin, "%d", &buffer[count]) == 1) {
        count++;
    }
    
    int next_count = 0;  // 下一個 run 的資料數量
```

#### 核心演算法：替換選擇排序（Replacement Selection）

```c
    while (count > 0) {
        // 將當前批次資料插入堆
        for (int i = 0; i < count; i++) {
            HeapNode node;
            node.value = buffer[i];
            insert(heap, node);
        }
        
        // 開啟輸出檔案
        char run_filename[100];
        sprintf(run_filename, "%s%d.dat", run_prefix, run_count);
        FILE *fout = fopen(run_filename, "w");
        int last_value = -2147483648;  // INT_MIN
        
        // 處理當前 run
        while (heap->size > 0) {
            HeapNode min = extractMin(heap);
            
            if (min.value >= last_value) {
                // 可以輸出到當前 run
                fprintf(fout, "%d\n", min.value);
                last_value = min.value;
                
                // 嘗試從檔案讀取新值
                int new_val;
                if (fscanf(fin, "%d", &new_val) == 1) {
                    if (new_val >= last_value) {
                        // 新值夠大，可以加入當前 run
                        HeapNode new_node;
                        new_node.value = new_val;
                        insert(heap, new_node);
                    } else {
                        // 新值太小，保存到下一個 run
                        if (next_count < MAX_MEMORY) {
                            next_buffer[next_count++] = new_val;
                        }
                    }
                }
            } else {
                // 此值太小，保存到下一個 run
                if (next_count < MAX_MEMORY) {
                    next_buffer[next_count++] = min.value;
                }
            }
        }
        
        fclose(fout);
        run_count++;
        
        // 交換緩衝區
        int *temp = buffer;
        buffer = next_buffer;
        next_buffer = temp;
        count = next_count;
        next_count = 0;
        
        // 如果 buffer 還有空間，繼續讀取
        while (count < MAX_MEMORY && fscanf(fin, "%d", &buffer[count]) == 1) {
            count++;
        }
    }
```

#### 詳細執行範例

假設有 20 個數字（簡化）：
```
輸入: [15, 3, 20, 8, 1, 18, 25, 12, 5, 30, 
       2, 22, 10, 17, 7, 28, 13, 19, 4, 26]
```

**第一個 Run 的產生過程**：

```
【初始化】
讀取前 10 個到 buffer: [15, 3, 20, 8, 1, 18, 25, 12, 5, 30]
建立堆（最小堆）:
        1
       / \
      3   8
     / \ / \
    15 5 18 20
   / \ /
  12 25 30

last_value = -∞

【Step 1】
extractMin() → 取出 1
1 >= -∞ → 可以輸出
輸出: 1
last_value = 1
讀取新值: 2
2 >= 1 → 插入堆

堆現在:
        2
       / \
      3   8
     / \ / \
    15 5 18 20
   / \ /
  12 25 30

輸出檔案: [1]

【Step 2】
extractMin() → 取出 2
2 >= 1 → 可以輸出
輸出: 2
last_value = 2
讀取新值: 22
22 >= 2 → 插入堆

輸出檔案: [1, 2]

【Step 3】
extractMin() → 取出 3
3 >= 2 → 可以輸出
輸出: 3
last_value = 3
讀取新值: 10
10 >= 3 → 插入堆

輸出檔案: [1, 2, 3]

... 繼續 ...

【Step 10】
extractMin() → 取出 30
30 >= 28 → 可以輸出
輸出: 30
last_value = 30
讀取新值: 26
26 < 30 → 太小！保存到 next_buffer

next_buffer: [26]

【堆空了】
第一個 run 完成！
輸出檔案: [1, 2, 3, 5, 8, 10, 12, 15, 18, 20, 22, 25, 28, 30]
共 14 個數字（比 MAX_MEMORY=10 還多！）
```

**為什麼 Run 會變大？**

關鍵在於：
```
if (new_val >= last_value) {
    插入當前 run 的堆;
} else {
    保存到下一個 run;
}
```

只要新讀入的值 ≥ 最後輸出的值，就能繼續加入當前 run！

**統計特性**：
- 對於隨機資料，約有 50% 的新值能加入當前 run
- 因此平均 run 大小 ≈ 2 × MAX_MEMORY

---

### 階段 2：merge_files_with_heap() - K-way Merge

```c
void merge_files_with_heap(char **filenames, int file_count, const char *output_file) {
    MinHeap *heap = createMinHeap(file_count);
    FILE *files[file_count];
    
    // 開啟所有檔案並初始化堆
    for (int i = 0; i < file_count; i++) {
        files[i] = fopen(filenames[i], "r");
        
        HeapNode node;
        if (fscanf(files[i], "%d", &node.value) == 1) {
            node.run_index = i;
            node.file = files[i];
            insert(heap, node);
        }
    }
    
    FILE *fout = fopen(output_file, "w");
    
    // 主合併迴圈
    while (heap->size > 0) {
        HeapNode min = extractMin(heap);
        fprintf(fout, "%d\n", min.value);
        
        // 從同一個檔案讀取下一個值
        int next_val;
        if (fscanf(min.file, "%d", &next_val) == 1) {
            HeapNode new_node;
            new_node.value = next_val;
            new_node.run_index = min.run_index;
            new_node.file = min.file;
            insert(heap, new_node);
        }
    }
    
    fclose(fout);
    for (int i = 0; i < file_count; i++) {
        if (files[i]) fclose(files[i]);
    }
}
```

#### 詳細執行範例

假設有 3 個已排序檔案：
```
file0: [1, 4, 7, 10]
file1: [2, 5, 8, 11]
file2: [3, 6, 9, 12]
```

**執行過程**：

```
【初始化】
從每個檔案讀取第一個值：
  file0 → 1
  file1 → 2
  file2 → 3

建立堆:
        1 (from file0)
       / \
      2   3
   (file1)(file2)

【Step 1】
extractMin() → {value=1, file=file0}
輸出: 1
從 file0 讀取下一個: 4
插入堆: {value=4, file=file0}

堆:
        2 (file1)
       / \
      4   3
   (file0)(file2)

輸出: [1]

【Step 2】
extractMin() → {value=2, file=file1}
輸出: 2
從 file1 讀取下一個: 5
插入堆: {value=5, file=file1}

堆:
        3 (file2)
       / \
      4   5
   (file0)(file1)

輸出: [1, 2]

【Step 3】
extractMin() → {value=3, file=file2}
輸出: 3
從 file2 讀取下一個: 6
插入堆: {value=6, file=file2}

堆:
        4 (file0)
       / \
      5   6
   (file1)(file2)

輸出: [1, 2, 3]

... 繼續 ...

【最終】
輸出: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
```

**動畫示意**：

```
回合 1:
file0: [1, 4, 7, 10]  ← 讀 1
file1: [2, 5, 8, 11]
file2: [3, 6, 9, 12]
堆: [1, 2, 3]
輸出: []

回合 2:
file0: [1, 4, 7, 10]  ← 讀 4
file1: [2, 5, 8, 11]  ← 讀 2
file2: [3, 6, 9, 12]
堆: [2, 4, 3]
輸出: [1]

回合 3:
file0: [1, 4, 7, 10]
file1: [2, 5, 8, 11]  ← 讀 5
file2: [3, 6, 9, 12]  ← 讀 3
堆: [3, 4, 5]
輸出: [1, 2]

回合 4:
file0: [1, 4, 7, 10]  ← 讀 4
file1: [2, 5, 8, 11]
file2: [3, 6, 9, 12]  ← 讀 6
堆: [4, 5, 6]
輸出: [1, 2, 3]

... 繼續 ...
```

---

## Java GUI 程式

### 整體架構

```
ExternalSortGUI
├── UI Components (Swing)
│   ├── 輸入欄位
│   ├── 按鈕
│   └── 結果顯示區
├── generateData()      → 產生測試資料
├── compileC()          → 編譯 C 程式
├── performSort()       → 執行排序並比較
└── verifyResults()     → 驗證結果
```

### 關鍵方法詳解

#### 1. generateData() - 產生不重複的測試資料

```java
private void generateData() {
    // 讀取參數
    String fileName = fileNameField.getText().trim();
    int dataCount = Integer.parseInt(dataCountField.getText().trim());
    int minValue = Integer.parseInt(minValueField.getText().trim());
    
    // 檢查範圍
    if (maxValue - minValue + 1 < dataCount) {
        // 範圍不足，顯示錯誤
        return;
    }
    
    // 建立包含所有數字的陣列
    int[] numbers = new int[dataCount];
    for (int i = 0; i < dataCount; i++) {
        numbers[i] = minValue + i;
    }
    // 現在 numbers = [0, 1, 2, 3, ..., dataCount-1]
    
    // Fisher-Yates 洗牌演算法
    Random random = new Random();
    for (int i = dataCount - 1; i > 0; i--) {
        int j = random.nextInt(i + 1);
        // 交換 numbers[i] 和 numbers[j]
        int temp = numbers[i];
        numbers[i] = numbers[j];
        numbers[j] = temp;
    }
    // 現在 numbers 被隨機打亂了
    
    // 寫入檔案
    PrintWriter writer = new PrintWriter(new FileWriter(fileName));
    for (int i = 0; i < dataCount; i++) {
        writer.println(numbers[i]);
    }
    writer.close();
}
```

**Fisher-Yates 洗牌演算法範例**：
```
初始: [0, 1, 2, 3, 4]

i=4: j=random(0-4)=2 → 交換 [4] 和 [2]
     [0, 1, 4, 3, 2]

i=3: j=random(0-3)=0 → 交換 [3] 和 [0]
     [3, 1, 4, 0, 2]

i=2: j=random(0-2)=2 → 交換 [2] 和 [2]
     [3, 1, 4, 0, 2]

i=1: j=random(0-1)=1 → 交換 [1] 和 [1]
     [3, 1, 4, 0, 2]

結果: [3, 1, 4, 0, 2] (隨機排列)
```

#### 2. performSort() - 執行排序

```java
private void performSort() {
    // 步驟 1: 編譯 C 程式
    compileC();
    
    // 步驟 2: 執行方法一
    long time1 = executeMergeSort();
    
    // 步驟 3: 執行方法二
    long time2 = executeHeapSort();
    
    // 步驟 4: 比較結果
    resultArea.append(String.format("方法一: %.2f 毫秒\n", time1 / 1000.0));
    resultArea.append(String.format("方法二: %.2f 毫秒\n", time2 / 1000.0));
    
    if (time1 > time2) {
        double ratio = (double) time1 / time2;
        resultArea.append(String.format("方法二快 %.2f 倍\n", ratio));
    }
}
```

#### 3. executeMergeSort() - 執行 C 程式

```java
private long executeMergeSort() throws Exception {
    // 執行 C 程式
    Process process = Runtime.getRuntime().exec(
        "./external_sort_merge " + currentDataFile + " sorted_merge.dat");
    
    // 讀取標準輸出
    BufferedReader reader = new BufferedReader(
        new InputStreamReader(process.getInputStream()));
    String line;
    while ((line = reader.readLine()) != null) {
        resultArea.append(line + "\n");  // 顯示在 GUI
    }
    
    // 等待程式完成
    process.waitFor();
    
    // 讀取時間檔案
    BufferedReader timeReader = new BufferedReader(
        new FileReader("time_merge.txt"));
    String timeStr = timeReader.readLine();
    timeReader.close();
    
    return (long) (Double.parseDouble(timeStr) * 1000);  // 轉換成微秒
}
```

#### 4. verifyResults() - 驗證結果

```java
private void verifyResults() {
    // 驗證方法一
    boolean valid1 = verifySortedFile("sorted_merge.dat");
    resultArea.append("方法一: " + (valid1 ? "✓ 正確" : "✗ 錯誤") + "\n");
    
    // 驗證方法二
    boolean valid2 = verifySortedFile("sorted_heap.dat");
    resultArea.append("方法二: " + (valid2 ? "✓ 正確" : "✗ 錯誤") + "\n");
    
    // 比較兩個檔案
    boolean same = compareFiles("sorted_merge.dat", "sorted_heap.dat");
    resultArea.append("結果相同: " + (same ? "✓ 是" : "✗ 否") + "\n");
}

private boolean verifySortedFile(String fileName) throws Exception {
    BufferedReader reader = new BufferedReader(new FileReader(fileName));
    int prev = Integer.MIN_VALUE;
    int count = 0;
    
    String line;
    while ((line = reader.readLine()) != null) {
        int curr = Integer.parseInt(line.trim());
        if (curr < prev) {
            // 發現逆序！
            reader.close();
            return false;
        }
        prev = curr;
        count++;
    }
    reader.close();
    
    // 檢查資料筆數是否正確
    return count == currentDataCount;
}
```

---

## 總結：兩種方法的核心差異

### 方法一（Merge Sort）

**優點**：
- ✓ 邏輯簡單直觀
- ✓ 嚴格遵守記憶體限制
- ✓ 穩定可靠

**缺點**：
- ✗ 產生較多 runs
- ✗ 需要多層合併
- ✗ I/O 次數較多

**適用場景**：
- 記憶體嚴格受限
- 需要簡單可靠的實作

### 方法二（Min-Heap）

**優點**：
- ✓ 產生較大的 runs（~2x）
- ✓ 只需一次多路合併
- ✓ 效能較優（快 1.3-1.5 倍）

**缺點**：
- ✗ 需要額外的堆結構
- ✗ 實作較複雜

**適用場景**：
- 追求最佳效能
- 可以使用額外資料結構

---

## 關鍵技術總結

### 1. 外部排序的本質
將大檔案分成小塊 → 排序小塊 → 合併小塊

### 2. 記憶體限制的處理
使用緩衝區技術，分批處理資料

### 3. 堆的應用
- 最小堆：快速找到最小值 O(log n)
- K-way merge：同時處理 k 個有序序列

### 4. 替換選擇排序
利用新讀入資料的「機會」，產生更大的 runs

### 5. 雙緩衝技術
當前處理 + 下一批準備，避免資料遺失
