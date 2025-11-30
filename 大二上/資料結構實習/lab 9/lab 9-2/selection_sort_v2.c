#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifdef _WIN32
#include <windows.h>

long long get_time_ns() {
    LARGE_INTEGER frequency, counter;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&counter);
    return (long long)((counter.QuadPart * 1000000000LL) / frequency.QuadPart);
}
#else
long long get_time_ns() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (long long)(ts.tv_sec * 1000000000LL + ts.tv_nsec);
}
#endif

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <input_file>\n", argv[0]);
        return 1;
    }
    
    // Read data from file
    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL) {
        printf("Error opening file\n");
        return 1;
    }
    
    int size;
    fscanf(fp, "%d", &size);
    
    int *array = (int*)malloc(size * sizeof(int));
    for (int i = 0; i < size; i++) {
        fscanf(fp, "%d", &array[i]);
    }
    fclose(fp);
    
    // Sort
    long long start_time = get_time_ns();
    
    for (int i = 0; i < size - 1; i++) {
        int min_index = i;
        for (int j = i + 1; j < size; j++) {
            if (array[j] < array[min_index]) {
                min_index = j;
            }
        }
        if (min_index != i) {
            int temp = array[i];
            array[i] = array[min_index];
            array[min_index] = temp;
        }
    }
    
    long long end_time = get_time_ns();
    long long elapsed = end_time - start_time;
    
    printf("%lld\n", elapsed);
    
    free(array);
    return 0;
}
