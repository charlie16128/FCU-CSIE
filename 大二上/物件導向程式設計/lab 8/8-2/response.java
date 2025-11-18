```java
import java.util.LinkedList;

class MyQueue<T> {
    private LinkedList<T> queue;

    public MyQueue() {
        queue = new LinkedList<>();
    }

    public void enqueue(T item) {
        queue.add(item);
    }

    public T dequeue() {
        if (!queue.isEmpty()) {
            return queue.removeFirst();
        } else {
            return null; // Or throw an exception if you prefer
        }
    }

    public boolean isEmpty() {
        return queue.isEmpty();
    }

    public int size() {
        return queue.size();
    }
}

public class QueueExample {
    public static void main(String[] args) {
        MyQueue<Integer> intQueue = new MyQueue<>();
        intQueue.enqueue(10);
        intQueue.enqueue(20);
        System.out.println(intQueue.dequeue()); // 10
    }
}

//我的Juniit測試會測這個Object，這邊以下請不要修改
/**
 * 測試 Person 類別的 toString() 方法。
 */
class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }
}
```