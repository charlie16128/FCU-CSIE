import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": 
    """
    請依照下面的程式框架完成queue實作，原本就有的程式碼一定要保留如try catch等，且在不更改main的情況下參考註解內的範例輸出要確保一致，並且當 Queue 滿時，再置入 item，或當 Queue 已空時，仍然嘗試從 Queue 中取出 item 要丟出 Exception
    且當addq滿時要印出Exception，然後將容量加倍。
    
    
    class MyQueue {


    public MyQueue(int capacity) {

    }

    public void addQ(int item) {
        try {
            
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Exception : Index " + rear + " out of bounds for length " + capacity);

            // --- 正確擴充邏輯 ---
            int newCapacity = capacity * 2;
            int[] newQueue = new int[newCapacity];
            for (int i = 0; i < size; i++) {
                newQueue[i] = queue[front + i];
            }
            queue = newQueue;
            capacity = newCapacity;
            // 更新 front / rear
            front = 0;
            rear = size;

            // 再放入新元素
            queue[rear] = item;
            rear++;
            size++;
        }
    }

    public int deleteQ() throws Exception {
        
        throw new Exception("Exception : Index -1 out of bounds for length " + capacity);
        
    }

    public void deleteAll() {
        while (size > 0) {
            try {
                System.out.println(deleteQ());
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        }
    }

    public int size() {
        return size;
    }
}

public class QueueDemo {
    public static void main(String[] args) {
        MyQueue queue = new MyQueue(5);

        queue.addQ(1);
        queue.addQ(2);
        queue.addQ(3);
        System.out.println("size: " + queue.size());

        try {
            System.out.println("deleteQ: " + queue.deleteQ());
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        queue.addQ(4);
        queue.addQ(5);
        queue.addQ(6);  // 會觸發 Exception：Index 5 out of bounds for length 5
        queue.addQ(7);
        queue.addQ(8);

        try {
            queue.deleteQ();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        queue.deleteAll();

        try {
            queue.deleteQ();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        /*
        預期輸出：
        size: 3
        deleteQ: 1
        Exception：Index 5 out of bounds for length 5
        3
        4
        5
        6
        7
        8
        The Queue is EMPTY!!!
        Exception：Index -1 out of bounds for length 10
        */
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
