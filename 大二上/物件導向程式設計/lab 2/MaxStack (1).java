import java.util.Stack;

public class MaxStack {

    private Stack<Integer> stack = new Stack<>();
    private int maxSize = 5;

    // isFull: 檢查堆疊是否已滿
    public boolean isFull() {
        return stack.size() == maxSize;
    }

    // isEmpty: 檢查堆疊是否為空
    public boolean isEmpty() {
        return stack.isEmpty();
    }

    // push: 將元素推入堆疊
    public void push(int value) {
        if (isFull()) {
            System.out.println("The Stack is FULL!!!");
            return; // 堆疊已滿，不允許推入
        }
        stack.push(value);
    }

    // pop: 彈出堆疊頂端元素
    public void pop() {
        if (isEmpty()) {
            System.out.println("The Stack is EMPTY!!!");
            return; // 堆疊為空，不允許彈出
        }
        stack.pop();
    }

    // top: 取得堆疊頂端元素，但不彈出
    public int top() {
        if (isEmpty()) {
            System.out.println("The Stack is EMPTY!!!");
            return -1; // 堆疊為空，返回 -1
        }
        return stack.peek();
    }

    // popall: 彈出堆疊所有元素
    public void popall() {
        while (!stack.isEmpty()) {
            System.out.println(stack.pop());
        }
    }

    public static void main(String[] args) {
        MaxStack stack = new MaxStack();

        // 測試資料
        stack.push(1); // 1
        stack.push(2); // 2
        stack.push(3); // 3

        System.out.println(stack.top()); // 顯示 3

        stack.pop(); // 彈出 3

        stack.push(4); // 4
        stack.push(5); // 5

        stack.push(6); // 嘗試推入超過容量的元素
        stack.push(7); // 嘗試推入超過容量的元素
        stack.push(8); // 嘗試推入超過容量的元素

        stack.pop(); // 彈出 5
        stack.popall(); // 預計會顯示 4, 2, 1

        stack.pop(); // 嘗試彈出空堆疊，應該顯示 "The Stack is EMPTY!!!"

        // 再次檢查堆疊是否為空
        if (stack.isEmpty()) {
            System.out.println("The Stack is EMPTY!!!");
        }
    }
}
