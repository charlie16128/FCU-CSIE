import sys
import time

def heapify_down(array, index, size):
    largest = index
    left = 2 * index + 1
    right = 2 * index + 2
    
    if left < size and array[left] > array[largest]:
        largest = left
    if right < size and array[right] > array[largest]:
        largest = right
    
    if largest != index:
        array[index], array[largest] = array[largest], array[index]
        heapify_down(array, largest, size)

def prepare_heap(array, size):
    for i in range(size // 2 - 1, -1, -1):
        heapify_down(array, i, size)

def heap_selection_sort(array):
    start_time = time.perf_counter_ns()
    n = len(array)
    
    prepare_heap(array, n)
    
    for i in range(n - 1):
        array[0], array[n - 1 - i] = array[n - 1 - i], array[0]
        heapify_down(array, 0, n - 1 - i)
    
    end_time = time.perf_counter_ns()
    return end_time - start_time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python heap_selection_sort_v2.py <input_file>")
        sys.exit(1)
    
    # Read data from file
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        size = int(lines[0].strip())
        array = [int(lines[i+1].strip()) for i in range(size)]
    
    time_ns = heap_selection_sort(array)
    print(time_ns)
