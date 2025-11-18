class MyQueue {

    private int[] queue;
    private int front;
    private int rear;
    private int size;
    private int capacity;

    public MyQueue(int capacity) {
        this.capacity = capacity;
        this.queue = new int[capacity];
        this.front = 0;
        this.rear = 0;
        this.size = 0;
    }

    public void addQ(int item) {
        try {
            if (size == capacity) {
                System.out.println("Excception : Queue is full.  Doubling capacity.");
                int newCapacity = capacity * 2;
                int[] newQueue = new int[newCapacity];
                for (int i = 0; i < size; i++) {
                    newQueue[i] = queue[front + i];
                }
                queue = newQueue;
                capacity = newCapacity;
                front = 0;
                rear = size;
                queue[rear] = item;
                rear++;
                size++;
            } else {
                queue[rear] = item;
                rear++;
                size++;
            }
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Excception : Index " + rear + " out of bounds for length " + capacity);
            // --- 正確擴充邏輯 ---
            int newCapacity = capacity * 2;
            int[] newQueue = new int[newCapacity];
            for (int i = 0; i < size; i++) {
                newQueue[i] = queue[front + i];
            }
            queue = newQueue;
            capacity = newCapacity;
            front = 0;
            rear = size;
            queue[rear] = item;
            rear++;
            size++;
        }
    }

    public int deleteQ() throws Exception {

        if (size == 0) {
            throw new Exception("Excception : Queue is empty");
        }

        if (front == rear) {
            throw new Exception("Excception : Index -1 out of bounds for length " + capacity);
        }

        int item = queue[front];
        front++;
        size--;
        return item;
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
        queue.addQ(6); // 會觸發 Exception：Index 5 out of bounds for length 5
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
         Excception：Index 5 out of bounds for length 5
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