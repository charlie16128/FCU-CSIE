import java.util.Random;

public class BubbleSortTimer {
    
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
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
    
    public static int[] generateRandom(int n) {
        Random rand = new Random();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = rand.nextInt(1000000);
        }
        return arr;
    }
    
    public static int[] generateGood(int n) {
        Random rand = new Random();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = i;
        }
        // 打亂1%的資料
        int swapCount = n / 100;
        for (int i = 0; i < swapCount; i++) {
            int idx1 = rand.nextInt(n);
            int idx2 = rand.nextInt(n);
            int temp = arr[idx1];
            arr[idx1] = arr[idx2];
            arr[idx2] = temp;
        }
        return arr;
    }
    
    public static int[] generateWorst(int n) {
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = n - i - 1;
        }
        return arr;
    }
    
    public static void testSort(int n, String dataType, java.util.function.Function<Integer, int[]> generateFunc) {
        int[] arr = generateFunc.apply(n);
        
        // 使用 System.nanoTime() 進行高精度計時
        long startTime = System.nanoTime();
        bubbleSort(arr);
        long endTime = System.nanoTime();
        
        long elapsedNs = endTime - startTime;
        
        System.out.printf("%d %s: %d ns%n", n, dataType, elapsedNs);
    }
    
    public static void main(String[] args) {
        int[] sizes = {10000, 100000, 1000000};
        
        System.out.println("Java Bubble Sort 測試結果 (使用 System.nanoTime()):");
        System.out.println("=========================================================");
        
        for (int n : sizes) {
            System.out.println("\n資料量: " + n);
            testSort(n, "random", BubbleSortTimer::generateRandom);
            testSort(n, "good", BubbleSortTimer::generateGood);
            testSort(n, "worst", BubbleSortTimer::generateWorst);
        }
    }
}