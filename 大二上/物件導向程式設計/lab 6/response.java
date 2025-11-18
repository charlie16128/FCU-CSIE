```java
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
            int mid = (index + MAX_SIZE / 2) % MAX_SIZE; // 計算中間索引，避免越界
            if (tree[mid] == Integer.MIN_VALUE) {
                // 找到空節點，插入到這裡
                tree[mid] = item;
                return;
            } else if (item < tree[mid]) {
                index = mid;
            } else {
                index = (mid + MAX_SIZE / 2) % MAX_SIZE; // 尋找右子樹
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
            insert((index + MAX_SIZE / 2) % MAX_SIZE, item); // 尋找左子樹
        } else {
            insert((index + MAX_SIZE / 2) % MAX_SIZE, item); // 尋找右子樹
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

        if (tree[index] == item) {
            return true;
        } else if (item < tree[index]) {
            return search((index + MAX_SIZE / 2) % MAX_SIZE, item); // 尋找左子樹
        } else {
            return search((index + MAX_SIZE / 2) % MAX_SIZE, item); // 尋找右子樹
        }
    }

    // 顯示樹的結構
    public void printTree() {
        System.out.print("NULL ");
        for (int i = 0; i < MAX_SIZE - 1; i++) {
            if (tree[i] == Integer.MIN_VALUE) {
                System.out.print("NULL ");
            } else {
                System.out.print(tree[i] + " ");
            }
        }
        System.out.println();
    }
}

// 介面，方便測試
interface MySearchable {
    void put(int item);
    boolean exist(int item);
    void printTree();
}
```

**程式碼說明：**

1.  **`BinarySearchTree` 類別：**
    *   `tree`：一個 `int[]` 陣列，用來儲存二元搜尋樹的節點。
    *   `MAX_SIZE`：二元搜尋樹的陣列大小限制為 32。
    *   **建構子：** 初始化 `tree` 陣列，所有節點都設定為 `Integer.MIN_VALUE`，表示空節點。
    *   **`put(int item)`：**
        *   檢查是否超出陣列大小限制。
        *   如果樹是空的，則將 `item` 插入到根節點（索引 0）。
        *   否則，從根節點開始，使用遞迴方式尋找空節點，並將 `item` 插入到該節點。
    *   **`insert(int index, int item)`：**
        *   如果索引超出陣列範圍，則表示超出存儲大小限制。
        *   如果節點為空，則將 `item` 插入到該節點。
        *   否則，根據 `item` 與節點值的比較，尋找左子樹或右子樹，並使用遞迴方式插入 `item`。
    *   **`exist(int item)`：** 呼叫 `search()` 方法，並傳遞根節點索引 0。
    *   **`search(int index, int item)`：**
        *   如果索引超出陣列範圍，則表示沒有找到 `item`。
        *   如果節點為空，則表示沒有找到 `item`。
        *   如果節點值等於 `item`，則表示找到 `item`。
        *   否則，根據 `item` 與節點值的比較，尋找左子樹或右子樹，並使用遞迴方式搜尋 `item`。
    *   **`printTree()`：**
        *   印出根節點（空節點顯示為 `NULL`）。
        *   然後，從根節點開始，印出每個節點的值（空節點顯示為 `NULL`）。

2.  **`MySearchable` 介面：**
    *   定義了 `put()`, `exist()`, `printTree()` 三個方法，方便測試和使用。

**使用範例：**

```java
public class Main {
    public static void main(String[] args) {
        BinarySearchTree bst = new BinarySearchTree();

        bst.put(5);
        bst.put(3);
        bst.put(7);
        bst.put(1);
        bst.put(9);
        bst.put(2);
        bst.put(4);
        bst.put(6);
        bst.put(8);
        bst.put(10);

        bst.printTree();

        System.out.println("是否存在 5？ " + bst.exist(5));
        System.out.println("是否存在 11？ " + bst.exist(11));

        bst.put(15); // 測試超出存儲大小限制
    }
}
```

**注意事項：**

*   這個實現使用陣列來模擬二元搜尋樹，因此搜尋的效率可能不如真正的二元搜尋樹。
*   `MAX_SIZE` 的值可以根據需要調整。
*   在 `put()` 方法中，如果超出陣列大小限制，會輸出錯誤訊息。
*   `printTree()` 方法會顯示所有節點（包括空節點）。

這個程式碼提供了一個使用 Java 實現二元搜尋樹的基礎。你可以根據需要進行修改和擴展。