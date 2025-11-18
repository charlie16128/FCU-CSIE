class Stack {

    private int[] stack;
    private int top;
    private int capacity;

    public Stack(int capacity) {
        this.capacity = capacity;
        this.stack = new int[capacity];
        this.top = -1;
    }

    public boolean isEmpty() {
        return top == -1;
    }

    public void push(int element) {
        try {
            stack[++top] = element;
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Exception : Index " + top + " out of bounds for length " + capacity);

            capacity *= 2;
            int[] newStack = new int[capacity];
            for (int i = 0; i < stack.length; i++) {
                newStack[i] = stack[i];
            }
            stack = newStack;
            stack[top] = element;
        }
    }

    public int pop() throws Exception {
        if (isEmpty()) {
            throw new Exception("Exception : Index -1 out of bounds for length " + capacity);
        }

        top--;
        return stack[top];
    }

    public int top() {
        if (isEmpty()) {
            return -1; // Or throw an exception if you prefer
        }
        return stack[top];
    }

    public void popAll() {
        while (!isEmpty()) {
            System.out.println(top());
            try {
                pop();
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        }
    }
}

public class MyStack2 {
    public static void main(String args[]) {
        Stack stack = new Stack(3);

        try {
            stack.push(1);
            stack.push(2);
            stack.push(3);
            System.out.println("pop: " + stack.pop());
            stack.push(4);
            stack.push(5);
            stack.push(6);
            stack.push(7);
            stack.push(8);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        try {
            stack.pop();
            stack.popAll();
            stack.pop();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}