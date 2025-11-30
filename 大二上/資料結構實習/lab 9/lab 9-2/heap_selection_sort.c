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

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void heapify_down(int array[], int index, int size) {
    int largest = index;
    int left = 2 * index + 1;
    int right = 2 * index + 2;
    
    if (left < size && array[left] > array[largest]) {
        largest = left;
    }
    if (right < size && array[right] > array[largest]) {
        largest = right;
    }
    
    if (largest != index) {
        swap(&array[index], &array[largest]);
        heapify_down(array, largest, size);
    }
}

void prepare_heap(int array[], int size) {
    for (int i = size / 2 - 1; i >= 0; i--) {
        heapify_down(array, i, size);
    }
}

long long heap_selection_sort(int array[], int size) {
    long long start_time = get_time_ns();
    
    prepare_heap(array, size);
    
    for (int i = 0; i < size - 1; i++) {
        swap(&array[0], &array[size - 1 - i]);
        heapify_down(array, 0, size - 1 - i);
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
    
    long long time_ns = heap_selection_sort(array, size);
    printf("%lld\n", time_ns);
    
    free(array);
    return 0;
}
