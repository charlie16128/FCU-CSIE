public class BasicArithmeticAndLoops {

    public static void main(String[] args) {

        // 運算子範例
        System.out.println("運算子範例:");
        int a = 10;
        int b = 5;
        int sum = a + b;
        int difference = a - b;
        double product = a * b;
        double quotient = (double)a / b; // 確保除法是浮點數

        System.out.println("加法: " + sum);
        System.out.println("減法: " + difference);
        System.out.println("乘法: " + product);
        System.out.println("除法: " + quotient);

        // if-else 判斷範例
        System.out.println("\nif-else 判斷範例:");
        int score = 75;

        if (score >= 90) {
            System.out.println("成績: 優異");
        } else if (score >= 60) {
            System.out.println("成績: 及格");
        } else {
            System.out.println("成績: 不及格");
        }

        // for 迴圈範例 (從 1 數到 5)
        System.out.println("\nfor 迴圈範例 (從 1 數到 5):");
        for (int i = 1; i <= 5; i++) {
            System.out.println("迴圈次數: " + i);
        }

        // while 迴圈範例 (從 0 數到 9)
        System.out.println("\nwhile 迴圈範例 (從 0 數到 9):");
        int count = 0;
        while (count <= 9) {
            System.out.println("迴圈次數: " + count);
            count++;
        }
    }
}