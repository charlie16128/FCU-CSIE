public class MyStack1 {
	//
	final static int MAX_STACK_SIZE = 5;
	
	public static boolean isFull() {
	    if (pushCount == MAX_STACK_SIZE) {
	        System.out.println("The Stack is FULL!!!");
	    }
	    return false;
	}
	
	public static boolean isEmpty() {
	    if (pushCount == 0) {
	        System.out.println("The Stack is EMPTY!!!");
	    }
	    return false;
	}
	
	public static void push(int theElement) {
	    if (pushCount < MAX_STACK_SIZE) {
	        stack.add(theElement);
	        pushCount++;
	    } else {
	        System.out.println("The Stack is FULL!!!");
	        return;
	    }
	}
	
	public static void pop() {
	    if (stack.isEmpty()) {
	        System.out.println("The Stack is EMPTY!!!");
	        return;
	    }
	    stack.remove(stack.size() - 1);
	    pushCount--;
	}
	
	public static int top() {
	    if (stack.isEmpty()) {
	        System.out.println("The Stack is EMPTY!!!");
	        return -1; // Or throw an exception
	    }
	    return stack.get(stack.size() - 1);
	}
	
	public static void popall() {
	    while (!stack.isEmpty()) {
	        System.out.println(stack.remove(stack.size() - 1));
	    }
	}
	
	public static int pushCount = 0;
	public static java.util.Stack<Integer> stack = new java.util.Stack<>();
	
	public static void main(String args[]) {
	
	    // the following codes are used for test
	    // please do not modify the following codes
	    
	    push(1);
	    push(2);
	    push(3);
	    System.out.println(top());
	    pop();
	    push(4);
	    push(5);
	    push(6);
	    push(7);
	    push(8);
	    pop();
	    popall();
	    pop();
	    
	    // Final Output should be like:
	    // 3
	    // The Stack is FULL!!!
	    // The Stack is FULL!!!
	    // 5
	    // 4
	    // 2
	    // 1
	    // The Stack is EMPTY!!!
	    // The Stack is EMPTY!!!
	}
}