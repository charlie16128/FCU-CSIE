import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": 
    """
    請幫我完成以下程式碼，要通過我的junit test，你不用回傳junit測試程式碼，你需要保留class person完全不要更改

import java.util.ArrayList;

class MyStack<T> {

    private ArrayList<T> stack; 

    public MyStack() {
    }

    public void push(T item) {
    }

    public T pop() {

    }

    // 检查栈是否为空
    public boolean isEmpty() {
    }

    // 返回栈中的元素数量
    public int size() {
    }
}

public class StackExample{
    public static void main(String[] args) {
        MyStack<Integer> stack = new MyStack<>();
        //do some test if needed
    }
}

// 以下 Person 不可修改（照你要求保持原樣）
//--------------------------------------------------------------
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
//--------------------------------------------------------------

以下是junit測試的程式碼，確保你回覆給我的程式能通過以下測試
import org.junit.*;

public class StackTest {

    @Test
    public void testPushAndPopInteger() {
        MyStack<Integer> stack = new MyStack<>();
        stack.push(10);
        stack.push(20);
        stack.push(30);

        Assert.assertEquals(Integer.valueOf(30), stack.pop());
        Assert.assertEquals(Integer.valueOf(20), stack.pop());
        Assert.assertEquals(Integer.valueOf(10), stack.pop());
        Assert.assertTrue(stack.isEmpty());
    }

    @Test
    public void testPushAndPopString() {
        MyStack<String> stack = new MyStack<>();
        stack.push("Hello");
        stack.push("World");

        Assert.assertEquals("World", stack.pop());
        Assert.assertEquals("Hello", stack.pop());
        Assert.assertTrue(stack.isEmpty());
    }

    @Test
    public void testSize() {
        MyStack<Integer> intStack = new MyStack<>();
        Assert.assertEquals(0, intStack.size());
        intStack.push(1);
        intStack.push(2);
        Assert.assertEquals(2, intStack.size());
        intStack.pop();
        Assert.assertEquals(1, intStack.size());
    }

    @Test
    public void testStackWithObjects() {
        MyStack<Person> personStack = new MyStack<>();
        Person alice = new Person("Alice", 25);
        Person bob = new Person("Bob", 30);

        personStack.push(alice);
        personStack.push(bob);

        Assert.assertEquals(bob, personStack.pop());
        Assert.assertEquals(alice, personStack.pop());
        Assert.assertTrue(personStack.isEmpty());
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
