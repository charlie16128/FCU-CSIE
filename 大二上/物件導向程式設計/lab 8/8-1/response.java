```java
import java.util.ArrayList;

class MyStack<T> {
    private ArrayList<T> stack;

    public MyStack() {
        this.stack = new ArrayList<>();
    }

    public void push(T item) {
        this.stack.add(item);
    }

    public T pop() {
        if (this.isEmpty()) {
            return null; // Or throw an exception, depending on desired behavior
        }
        return this.stack.remove(this.stack.size() - 1);
    }

    // 检查栈是否为空
    public boolean isEmpty() {
        return this.stack.isEmpty();
    }

    // 返回栈中的元素数量
    public int size() {
        return this.stack.size();
    }
}

public class StackExample {
    public static void main(String[] args) {
        MyStack<Integer> stack = new MyStack<>();
        //do some test if needed
    }
}

// 以下 Person 不可修改（照你要求保持原樣）
/**
 * --------------------------------------------------------------
 * class Person {
 *    private String name;
 *    private int age;
 *    public Person(String name, int age) {
 *        this.name = name;
 *        this.age = age;
 *    }
 *    @Override
 *    public String toString() {
 *        return "Person{name='" + name + "', age=" + age + "}";
 *    }
 * }
 * --------------------------------------------------------------
 */
```