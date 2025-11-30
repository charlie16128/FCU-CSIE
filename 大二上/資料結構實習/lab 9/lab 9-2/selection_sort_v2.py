import sys
import time

def selection_sort(array):
    start_time = time.perf_counter_ns()
    n = len(array)
    
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if array[j] < array[min_index]:
                min_index = j
        if min_index != i:
            array[i], array[min_index] = array[min_index], array[i]
    
    end_time = time.perf_counter_ns()
    return end_time - start_time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python selection_sort_v2.py <input_file>")
        sys.exit(1)
    
    # Read data from file
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        size = int(lines[0].strip())
        array = [int(lines[i+1].strip()) for i in range(size)]
    
    time_ns = selection_sort(array)
    print(time_ns)
