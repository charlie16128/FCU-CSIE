import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": 
    """
請幫我完成以下程式碼，要通過我的junit test，你不用回傳junit測試程式碼，你需要保留class person完全不要更改
import java.util.LinkedList;

class MyQueue<T> {
    private LinkedList<T> queue;

    public MyQueue() {
        queue = new LinkedList<>();
    }

    public void enqueue(T item) {
    }

    public T dequeue() {
        if (queue.isEmpty()) {
        }
    }

    public boolean isEmpty() {
    }

    public int size() {
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

//我的Junit測試會測這個Object，這邊以下請不要修改
//---------------------------------------------------------------------------------
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
//---------------------------------------------------------------------------------

以下是junit測試的程式碼，確保你回覆給我的程式能通過以下測試
import org.junit.*;

public class QueueTest {

    @Test
    public void testEnqueueAndDequeueInteger() {
        MyQueue<Integer> intQueue = new MyQueue<>();
        intQueue.enqueue(10);
        intQueue.enqueue(20);
        intQueue.enqueue(30);

        Assert.assertEquals(3, intQueue.size());
        Assert.assertEquals(Integer.valueOf(10), intQueue.dequeue());
        Assert.assertEquals(Integer.valueOf(20), intQueue.dequeue());
        Assert.assertEquals(Integer.valueOf(30), intQueue.dequeue());
        Assert.assertTrue(intQueue.isEmpty());
    }

    @Test
    public void testEnqueueAndDequeueString() {
        MyQueue<String> stringQueue = new MyQueue<>();
        stringQueue.enqueue("Hello");
        stringQueue.enqueue("World");

        Assert.assertEquals(2, stringQueue.size());
        Assert.assertEquals("Hello", stringQueue.dequeue());
        Assert.assertEquals("World", stringQueue.dequeue());
        Assert.assertTrue(stringQueue.isEmpty());
    }

    @Test
    public void testIsEmpty() {
        MyQueue<Integer> intQueue = new MyQueue<>();
        Assert.assertTrue(intQueue.isEmpty());
        intQueue.enqueue(1);
        Assert.assertFalse(intQueue.isEmpty());
        intQueue.dequeue();
        Assert.assertTrue(intQueue.isEmpty());
    }

    @Test
    public void testSize() {
        MyQueue<Integer> intQueue = new MyQueue<>();
        Assert.assertEquals(0, intQueue.size());
        intQueue.enqueue(1);
        intQueue.enqueue(2);
        Assert.assertEquals(2, intQueue.size());
        intQueue.dequeue();
        Assert.assertEquals(1, intQueue.size());
    }

    @Test
    public void testQueueWithObjects() {
        MyQueue<Person> personQueue = new MyQueue<>();
        Person alice = new Person("Alice", 25);
        Person bob = new Person("Bob", 30);

        personQueue.enqueue(alice);
        personQueue.enqueue(bob);

        Assert.assertEquals(alice, personQueue.dequeue());
        Assert.assertEquals(bob, personQueue.dequeue());
        Assert.assertTrue(personQueue.isEmpty());
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
