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

long long selection_sort(int array[], int size) {
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
    return elapsed;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <size> <data...>\n", argv[0]);
        return 1;
    }
    
    int size = atoi(argv[1]);
    int *array = (int*)malloc(size * sizeof(int));
    
    for (int i = 0; i < size; i++) {
        array[i] = atoi(argv[i + 2]);
    }
    
    long long time_ns = selection_sort(array, size);
    printf("%lld\n", time_ns);
    
    free(array);
    return 0;
}
