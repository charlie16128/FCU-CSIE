

public class SearchDemo {
    public static void main(String[] args) {
        // 檢查是否有輸入參數
        if (args.length < 2) {
            System.out.println("請輸入至少兩個數字：第一個為搜尋目標，後面為資料。");
            return;
        }

        // 第一個數字是搜尋目標
        int target = Integer.parseInt(args[0]);

        // 建立 BinarySearchTree 實例
        BinarySearchTree bst = new BinarySearchTree();

        // 從第二個數字開始插入到樹中
        for (int i = 1; i < args.length; i++) {
            int num = Integer.parseInt(args[i]);
            bst.put(num);
        }

        // 印出樹的內容
        System.out.println("建立的 BinarySearchTree 陣列內容：");
        bst.printTree();

        // 執行搜尋
        boolean found = bst.exist(target);
        System.out.println("搜尋 " + target + " 的結果為 " + (found ? "true" : "false"));
    }
}
