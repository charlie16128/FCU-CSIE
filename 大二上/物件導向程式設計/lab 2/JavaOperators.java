public class JavaOperators {

    public static void main(String[] args) {
        int a = 6, b = 3;

        System.out.println("--- +-*/展示---");
        System.out.println("a = 6, b = 3");
        System.out.println("  a + b = " + (a + b));

        System.out.println("  a - b = " + (a - b));

        System.out.println("  a * b = " + (a * b));

        System.out.println("  a / b = " + (a / b)); 


        // if-else
        System.out.println("--- if-else展示---");
        if (a >= b) {
            System.out.println("   a >= b");
        }else {
            System.out.println("   a < b");
        }

        // for 
        System.out.println("\n--- for 迴圈展示 ---");
        System.out.println("從 1 到 5 數數：");
        for (int i = 1; i <= 5; i++) {
            System.out.println("  i = " + i);
        }

        // while
        System.out.println("\n--- while 迴圈展示 ---");
        System.out.println("數到 10 結束：");
        int count = 0;
        while (count < 10) {
            System.out.println("  count = " + count);
            count++;
        }
    }
}