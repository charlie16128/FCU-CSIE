public class StackWithCapacity {

    private int capacity;
    private int currentSize;
    private int[] stackArray;

    public StackWithCapacity(int capacity) {
        this.capacity = capacity;
        this.currentSize = 0;
        this.stackArray = new int[capacity];
    }

    public boolean isFull() {
        return currentSize == capacity;
    }

    public boolean isEmpty() {
        return currentSize == 0;
    }

    public void push(int value) {
        if (isFull()) {
            System.out.println("The Stack is FULL!!!");
            return;
        }
        stackArray[currentSize] = value;
        currentSize++;
    }

    public int pop() {
        if (isEmpty()) {
            System.out.println("The Stack is EMPTY!!!");
            return -1; // Or throw an exception, depending on desired behavior
        }
        currentSize--;
        return stackArray[currentSize];
    }

    public int top() {
        if (isEmpty()) {
            System.out.println("The Stack is EMPTY!!!");
            return -1; // Or throw an exception
        }
        return stackArray[currentSize - 1];
    }

    public void popall() {
        if (isEmpty()) {
            System.out.println("The Stack is EMPTY!!!");
            return;
        }
        for (int i = currentSize - 1; i >= 0; i--) {
            System.out.print(stackArray[i] + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        StackWithCapacity stack = new StackWithCapacity(5);

        stack.push(1);
        stack.top(); // No output
        stack.pop();
        stack.push(2);
        stack.push(3);
        stack.push(4);
        stack.push(5);
        stack.pop();
        stack.popall();
        stack.pop();
        stack.popall();
    }
}