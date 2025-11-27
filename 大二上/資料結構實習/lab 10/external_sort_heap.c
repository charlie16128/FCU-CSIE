#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_MEMORY 10000  // 最多只能使用10000個整數的陣列

// 最小堆節點結構
typedef struct HeapNode {
    int value;          // 當前值
    int run_index;      // 來自哪個run
    FILE *file;         // 對應的檔案指標
} HeapNode;

// 最小堆結構
typedef struct MinHeap {
    HeapNode *nodes;
    int size;
    int capacity;
} MinHeap;

// 建立最小堆
MinHeap* createMinHeap(int capacity) {
    MinHeap *heap = (MinHeap*)malloc(sizeof(MinHeap));
    heap->nodes = (HeapNode*)malloc(capacity * sizeof(HeapNode));
    heap->size = 0;
    heap->capacity = capacity;
    return heap;
}

// 交換兩個節點
void swap(HeapNode *a, HeapNode *b) {
    HeapNode temp = *a;
    *a = *b;
    *b = temp;
}

// 向下調整堆
void heapify_down(MinHeap *heap, int idx) {
    int smallest = idx;
    int left = 2 * idx + 1;
    int right = 2 * idx + 2;

    if (left < heap->size && heap->nodes[left].value < heap->nodes[smallest].value)
        smallest = left;
    if (right < heap->size && heap->nodes[right].value < heap->nodes[smallest].value)
        smallest = right;

    if (smallest != idx) {
        swap(&heap->nodes[idx], &heap->nodes[smallest]);
        heapify_down(heap, smallest);
    }
}

// 向上調整堆
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

// 插入節點到堆
void insert(MinHeap *heap, HeapNode node) {
    if (heap->size >= heap->capacity) return;
    heap->nodes[heap->size] = node;
    heapify_up(heap, heap->size);
    heap->size++;
}

// 取出最小值並更新
HeapNode extractMin(MinHeap *heap) {
    HeapNode min = heap->nodes[0];
    heap->nodes[0] = heap->nodes[heap->size - 1];
    heap->size--;
    heapify_down(heap, 0);
    return min;
}

// 替換堆頂元素
void replaceMin(MinHeap *heap, HeapNode new_node) {
    heap->nodes[0] = new_node;
    heapify_down(heap, 0);
}

// 比較函數
int compare(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

// 使用堆產生較大的runs（簡化版，確保不遺失資料）
int generate_runs_with_heap(const char *input_file, const char *run_prefix) {
    FILE *fin = fopen(input_file, "r");
    if (!fin) {
        printf("無法開啟輸入檔案: %s\n", input_file);
        return -1;
    }

    int *buffer = (int*)malloc(MAX_MEMORY * sizeof(int));
    int *next_buffer = (int*)malloc(MAX_MEMORY * sizeof(int));
    MinHeap *heap = createMinHeap(MAX_MEMORY);
    int run_count = 0;
    
    // 讀取第一批資料
    int count = 0;
    while (count < MAX_MEMORY && fscanf(fin, "%d", &buffer[count]) == 1) {
        count++;
    }
    
    if (count == 0) {
        free(buffer);
        free(next_buffer);
        free(heap->nodes);
        free(heap);
        fclose(fin);
        return 0;
    }

    int next_count = 0;  // 下一個run的資料數量
    
    while (count > 0) {
        // 將當前批次資料插入堆
        for (int i = 0; i < count; i++) {
            HeapNode node;
            node.value = buffer[i];
            insert(heap, node);
        }
        
        char run_filename[100];
        sprintf(run_filename, "%s%d.dat", run_prefix, run_count);
        FILE *fout = fopen(run_filename, "w");
        int last_value = -2147483648;  // INT_MIN
        
        // 處理當前run
        while (heap->size > 0) {
            HeapNode min = extractMin(heap);
            
            if (min.value >= last_value) {
                // 輸出到當前run
                fprintf(fout, "%d\n", min.value);
                last_value = min.value;
                
                // 嘗試從檔案讀取新值
                int new_val;
                if (fscanf(fin, "%d", &new_val) == 1) {
                    if (new_val >= last_value) {
                        // 可以加入當前run
                        HeapNode new_node;
                        new_node.value = new_val;
                        insert(heap, new_node);
                    } else {
                        // 保存到下一個run
                        if (next_count < MAX_MEMORY) {
                            next_buffer[next_count++] = new_val;
                        }
                    }
                }
            } else {
                // 保存到下一個run
                if (next_count < MAX_MEMORY) {
                    next_buffer[next_count++] = min.value;
                }
            }
        }
        
        fclose(fout);
        run_count++;
        
        // 交換buffer，準備處理下一個run
        int *temp = buffer;
        buffer = next_buffer;
        next_buffer = temp;
        count = next_count;
        next_count = 0;
        
        // 如果buffer還有空間且檔案還有資料，繼續讀取
        while (count < MAX_MEMORY && fscanf(fin, "%d", &buffer[count]) == 1) {
            count++;
        }
    }
    
    free(buffer);
    free(next_buffer);
    free(heap->nodes);
    free(heap);
    fclose(fin);
    return run_count;
}

// 使用堆合併多個檔案
void merge_files_with_heap(char **filenames, int file_count, const char *output_file) {
    MinHeap *heap = createMinHeap(file_count);
    FILE *files[file_count];
    
    // 開啟所有檔案並初始化堆
    for (int i = 0; i < file_count; i++) {
        files[i] = fopen(filenames[i], "r");
        if (!files[i]) continue;
        
        HeapNode node;
        if (fscanf(files[i], "%d", &node.value) == 1) {
            node.run_index = i;
            node.file = files[i];
            insert(heap, node);
        }
    }
    
    FILE *fout = fopen(output_file, "w");
    
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
    
    free(heap->nodes);
    free(heap);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("用法: %s <input_file> <output_file>\n", argv[0]);
        return 1;
    }

    const char *input_file = argv[1];
    const char *output_file = argv[2];
    const char *run_prefix = "run_heap_";

    clock_t start = clock();

    // 階段1：使用堆產生runs（每個run會比MAX_MEMORY大）
    printf("使用Min-Heap產生排序區段(runs)...\n");
    int run_count = generate_runs_with_heap(input_file, run_prefix);
    if (run_count < 0) {
        return 1;
    }
    printf("產生了 %d 個排序區段\n", run_count);

    // 階段2：使用堆合併所有runs
    printf("使用Min-Heap合併排序區段...\n");
    if (run_count == 1) {
        char run_file[100];
        sprintf(run_file, "%s0.dat", run_prefix);
        rename(run_file, output_file);
    } else {
        char **filenames = (char**)malloc(run_count * sizeof(char*));
        for (int i = 0; i < run_count; i++) {
            filenames[i] = (char*)malloc(100 * sizeof(char));
            sprintf(filenames[i], "%s%d.dat", run_prefix, i);
        }
        
        merge_files_with_heap(filenames, run_count, output_file);
        
        // 清理暫存檔案
        for (int i = 0; i < run_count; i++) {
            remove(filenames[i]);
            free(filenames[i]);
        }
        free(filenames);
    }

    clock_t end = clock();
    double time_spent = ((double)(end - start)) / CLOCKS_PER_SEC * 1000.0;

    printf("排序完成！\n");
    printf("輸出檔案: %s\n", output_file);
    printf("執行時間: %.2f 毫秒\n", time_spent);

    // 將時間寫入檔案供Java讀取
    FILE *time_file = fopen("time_heap.txt", "w");
    fprintf(time_file, "%.2f", time_spent);
    fclose(time_file);

    return 0;
}
