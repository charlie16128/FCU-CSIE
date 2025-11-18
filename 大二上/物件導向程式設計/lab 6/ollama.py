import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": 
"""
請用 Java 撰寫一個名為 BinarySearchTree 的類別並實作介面 MySearchable，使用固定大小為 32 的 int 陣列作為二元搜尋樹的儲存結構，以 Integer.MIN_VALUE 表示空節點，實作 put(int item) 來插入元素（若超出容量則輸出「超出存儲大小限制」）、exist(int item) 來檢查元素是否存在（透過遞迴搜尋）、以及 printTree() 來印出樹中所有節點（空節點顯示為 NULL），其中插入與搜尋均需使用遞迴方式，請依以下架構完成
	不要使用@override、
 
    public class BinarySearchTree implements MySearchable {
    private int[] tree;  // 用 int 陣列儲存二元搜尋樹
    private static final int MAX_SIZE = 32;  // 陣列大小限制為 32

    // 建構子
    public BinarySearchTree() {
        tree = new int[MAX_SIZE];
        // 初始化所有節點為 Integer.MIN_VALUE，表示節點尚未被填入
        for (int i = 0; i < MAX_SIZE; i++) {
            tree[i] = Integer.MIN_VALUE;  // 表示空位置
        }
    }

    // 插入數字
    public void put(int item) {
        // 檢查是否超過陣列大小限制
        if (tree[MAX_SIZE - 1] != Integer.MIN_VALUE) {
            
        }

        // 如果樹是空的，插入根節點
        if (tree[0] == Integer.MIN_VALUE) {

        }

        // 否則從根節點開始插入

    }

    // 遞迴插入數字到二元搜尋樹
    private void insert(int index, int item) {
        // 如果超過陣列範圍，顯示錯誤訊息
        if (index >= MAX_SIZE) {

        }

        if (tree[index] == Integer.MIN_VALUE) {

        } else if (item < tree[index]) {
            // 插入到左子樹

        } else if (item > tree[index]) {
            // 插入到右子樹
            
        }
    }

    // 檢查數字是否存在於樹中
    public boolean exist(int item) {

    }

    // 遞迴搜尋數字是否存在
    private boolean search(int index, int item) {
        
    }

    // 顯示樹的結構
    public void printTree() {
            System.out.print("NULL ");  // 樹的結構中，首先顯示根節點的空位置
            for (int i = 0; i < MAX_SIZE - 1; i++) {
                if (tree[i] == Integer.MIN_VALUE) {
                    System.out.print("NULL ");  // 顯示為 NULL
                } else {
                    System.out.print(tree[i] + " ");  // 顯示節點值
                }
            }
            System.out.println();
        }
}


""",
    "stream": False
}

def get_response():
    r = requests.post(url, json=payload, timeout=600)
    r.raise_for_status()
    data = r.json()
    return data["response"]

if __name__ == "__main__":
    response = get_response()
    print(f'{response}')

    with open("response.java", "w", encoding="utf-8") as f:
        f.write(response)
    print("程式碼存成 response.java")
