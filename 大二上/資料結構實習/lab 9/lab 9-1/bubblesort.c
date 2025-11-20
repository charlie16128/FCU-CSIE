#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifdef _WIN32
    #include <windows.h>
    typedef LARGE_INTEGER TimeType;
#else
    #include <time.h>
    typedef struct timespec TimeType;
#endif

void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

void generateRandom(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        arr[i] = rand() % 1000000;
    }
}

void generateGood(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        arr[i] = i;
    }
    // 打亂1%的資料
    int swapCount = n / 100;
    for (int i = 0; i < swapCount; i++) {
        int idx1 = rand() % n;
        int idx2 = rand() % n;
        int temp = arr[idx1];
        arr[idx1] = arr[idx2];
        arr[idx2] = temp;
    }
}

void generateWorst(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        arr[i] = n - i - 1;
    }
}

long long getTimeNs() {
#ifdef _WIN32
    static LARGE_INTEGER frequency;
    static int initialized = 0;
    if (!initialized) {
        QueryPerformanceFrequency(&frequency);
        initialized = 1;
    }
    
    LARGE_INTEGER counter;
    QueryPerformanceCounter(&counter);
    return (long long)((counter.QuadPart * 1000000000LL) / frequency.QuadPart);
#else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (long long)ts.tv_sec * 1000000000LL + ts.tv_nsec;
#endif
}

void testSort(int n, char* dataType, void (*generateFunc)(int[], int)) {
    int* arr = (int*)malloc(n * sizeof(int));
    
    generateFunc(arr, n);
    
    long long startTime = getTimeNs();
    bubbleSort(arr, n);
    long long endTime = getTimeNs();
    
    long long elapsedNs = endTime - startTime;
    
    printf("%d %s: %lld ns\n", n, dataType, elapsedNs);
    
    free(arr);
}

int main() {
    srand((unsigned int)time(NULL));
    
    int sizes[] = {10000, 100000, 1000000};
    
    printf("C語言 Bubble Sort 測試結果 (使用高精度計時器):\n");
    printf("=========================================================\n");
    
    for (int i = 0; i < 3; i++) {
        int n = sizes[i];
        printf("\n資料量: %d\n", n);
        testSort(n, "random", generateRandom);
        testSort(n, "good", generateGood);
        testSort(n, "worst", generateWorst);
    }
    
    return 0;
}
