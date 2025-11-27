#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_MEMORY 10000  // 最多只能使用10000個整數的陣列

// 比較函數，用於qsort
int compare(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

// 階段1：將大檔案分割成多個已排序的小檔案(runs)
int generate_runs(const char *input_file, const char *run_prefix) {
    FILE *fin = fopen(input_file, "r");
    if (!fin) {
        printf("無法開啟輸入檔案: %s\n", input_file);
        return -1;
    }

    int *buffer = (int*)malloc(MAX_MEMORY * sizeof(int));
    int run_count = 0;
    int count;

    while (1) {
        count = 0;
        // 讀取最多 MAX_MEMORY 筆資料
        while (count < MAX_MEMORY && fscanf(fin, "%d", &buffer[count]) == 1) {
            count++;
        }

        if (count == 0) break;

        // 在記憶體內排序
        qsort(buffer, count, sizeof(int), compare);

        // 寫入run檔案
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

// 合併兩個已排序的檔案
void merge_two_files(const char *file1, const char *file2, const char *output) {
    FILE *f1 = fopen(file1, "r");
    FILE *f2 = fopen(file2, "r");
    FILE *fout = fopen(output, "w");

    int val1, val2;
    int has1 = (fscanf(f1, "%d", &val1) == 1);
    int has2 = (fscanf(f2, "%d", &val2) == 1);

    while (has1 && has2) {
        if (val1 <= val2) {
            fprintf(fout, "%d\n", val1);
            has1 = (fscanf(f1, "%d", &val1) == 1);
        } else {
            fprintf(fout, "%d\n", val2);
            has2 = (fscanf(f2, "%d", &val2) == 1);
        }
    }

    while (has1) {
        fprintf(fout, "%d\n", val1);
        has1 = (fscanf(f1, "%d", &val1) == 1);
    }

    while (has2) {
        fprintf(fout, "%d\n", val2);
        has2 = (fscanf(f2, "%d", &val2) == 1);
    }

    fclose(f1);
    fclose(f2);
    fclose(fout);
}

// 階段2：多路合併所有runs
void merge_runs(const char *run_prefix, int run_count, const char *output_file) {
    int current_level = 0;
    int current_count = run_count;

    while (current_count > 1) {
        int next_count = 0;
        
        for (int i = 0; i < current_count; i += 2) {
            char file1[100], file2[100], output[100];
            
            if (current_level == 0) {
                sprintf(file1, "%s%d.dat", run_prefix, i);
            } else {
                sprintf(file1, "%slevel%d_%d.dat", run_prefix, current_level, i);
            }

            if (i + 1 < current_count) {
                if (current_level == 0) {
                    sprintf(file2, "%s%d.dat", run_prefix, i + 1);
                } else {
                    sprintf(file2, "%slevel%d_%d.dat", run_prefix, current_level, i + 1);
                }
                sprintf(output, "%slevel%d_%d.dat", run_prefix, current_level + 1, next_count);
                
                merge_two_files(file1, file2, output);
                
                // 刪除已合併的檔案
                remove(file1);
                remove(file2);
            } else {
                // 奇數個檔案，最後一個直接複製到下一層
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
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("用法: %s <input_file> <output_file>\n", argv[0]);
        return 1;
    }

    const char *input_file = argv[1];
    const char *output_file = argv[2];
    const char *run_prefix = "run_merge_";

    clock_t start = clock();

    // 階段1：產生runs
    printf("開始產生排序區段(runs)...\n");
    int run_count = generate_runs(input_file, run_prefix);
    if (run_count < 0) {
        return 1;
    }
    printf("產生了 %d 個排序區段\n", run_count);

    // 階段2：合併runs
    printf("開始合併排序區段...\n");
    if (run_count == 1) {
        // 只有一個run，直接重新命名
        char run_file[100];
        sprintf(run_file, "%s0.dat", run_prefix);
        rename(run_file, output_file);
    } else {
        merge_runs(run_prefix, run_count, output_file);
    }

    clock_t end = clock();
    double time_spent = ((double)(end - start)) / CLOCKS_PER_SEC * 1000.0;

    printf("排序完成！\n");
    printf("輸出檔案: %s\n", output_file);
    printf("執行時間: %.2f 毫秒\n", time_spent);

    // 將時間寫入檔案供Java讀取
    FILE *time_file = fopen("time_merge.txt", "w");
    fprintf(time_file, "%.2f", time_spent);
    fclose(time_file);

    return 0;
}
