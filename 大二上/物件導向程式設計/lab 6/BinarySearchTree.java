public class BinarySearchTree implements MySearchable {
    private int[] tree; // 用 int 陣列儲存二元搜尋樹
    private static final int MAX_SIZE = 32; // 陣列大小限制為 32

    // 建構子
    public BinarySearchTree() {
        tree = new int[MAX_SIZE];
        // 初始化所有節點為 Integer.MIN_VALUE，表示節點尚未被填入
        for (int i = 0; i < MAX_SIZE; i++) {
            tree[i] = Integer.MIN_VALUE; // 表示空位置
        }
    }

    // 插入數字
    public void put(int item) {
        // 檢查是否超過陣列大小限制
        if (tree[MAX_SIZE - 1] != Integer.MIN_VALUE) {
            System.out.println("超出存儲大小限制");
            return;
        }

        // 如果樹是空的，插入根節點
        if (tree[0] == Integer.MIN_VALUE) {
            tree[0] = item;
            return;
        }

        // 否則從根節點開始插入
        int index = 0;
        while (index < MAX_SIZE) {
            if (tree[index] == Integer.MIN_VALUE) {
                // 找到空位
                tree[index] = item;
                return;
            } else if (item < tree[index]) {
                index = (index * 2) + 1; // 往左走
            } else if (item > tree[index]) {
                index = (index * 2) + 2; // 往右走
            } else {
                // 元素已存在
                return;
            }
        }
    }

    // 遞迴插入數字到二元搜尋樹
    private void insert(int index, int item) {
        if (index >= MAX_SIZE) {
            System.out.println("超出存儲大小限制");
            return;
        }

        if (tree[index] == Integer.MIN_VALUE) {
            tree[index] = item;
            return;
        } else if (item < tree[index]) {
            insert(index * 2 + 1, item); // 往左走
        } else if (item > tree[index]) {
            insert(index * 2 + 2, item); // 往右走
        }
    }

    // 檢查數字是否存在於樹中
    public boolean exist(int item) {
        return search(0, item);
    }

    // 遞迴搜尋數字是否存在
    private boolean search(int index, int item) {
        if (index >= MAX_SIZE) {
            return false;
        }

        if (tree[index] == Integer.MIN_VALUE) {
            return false;
        }

        if (item == tree[index]) {
            return true;
        } else if (item < tree[index]) {
            return search(index * 2 + 1, item); // 往左走
        } else {
            return search(index * 2 + 2, item); // 往右走
        }
    }

    // 顯示樹的結構
    public void printTree() {
        System.out.print("NULL "); // 樹的結構中，首先顯示根節點的空位置
        for (int i = 0; i < MAX_SIZE - 1; i++) {
            if (tree[i] == Integer.MIN_VALUE) {
                System.out.print("NULL "); // 顯示為 NULL
            } else {
                System.out.print(tree[i] + " "); // 顯示節點值
            }
        }
        System.out.println();
    }
}