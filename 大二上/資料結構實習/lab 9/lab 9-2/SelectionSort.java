public class SelectionSort {
    public static long sort(int[] array) {
        long startTime = System.nanoTime();
        int n = array.length;
        
        for (int i = 0; i < n - 1; i++) {
            int minIndex = i;
            for (int j = i + 1; j < n; j++) {
                if (array[j] < array[minIndex]) {
                    minIndex = j;
                }
            }
            if (minIndex != i) {
                int temp = array[i];
                array[i] = array[minIndex];
                array[minIndex] = temp;
            }
        }
        
        long endTime = System.nanoTime();
        return endTime - startTime;
    }
}
