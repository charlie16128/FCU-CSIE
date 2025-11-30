public class HeapSelectionSort {
    public static long sort(int[] array) {
        long startTime = System.nanoTime();
        int n = array.length;
        
        // Build heap
        prepareHeap(array, n);
        
        for (int i = 0; i < n - 1; i++) {
            // Swap first element with last unsorted element
            swap(array, 0, n - 1 - i);
            // Heapify down
            heapifyDown(array, 0, n - 1 - i);
        }
        
        long endTime = System.nanoTime();
        return endTime - startTime;
    }
    
    private static void prepareHeap(int[] array, int size) {
        for (int i = size / 2 - 1; i >= 0; i--) {
            heapifyDown(array, i, size);
        }
    }
    
    private static void heapifyDown(int[] array, int index, int size) {
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
            swap(array, index, largest);
            heapifyDown(array, largest, size);
        }
    }
    
    private static void swap(int[] array, int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}
