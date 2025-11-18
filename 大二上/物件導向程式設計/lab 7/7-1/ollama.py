import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": 
    """
    請幫我完成以下程式碼，且popall要印出所有值，pop不用印出，push要滿了加倍，main內的程式不要更動。  
    輸出應該要為 
    pop: 3 
    Exception：Index 3 out of bounds for length 3 
    Exception：Index 6 out of bounds for length 6 
    7 
    6 
    5 
    4 
    2 
    1 
    The Stack is EMPTY!!! 
    Exception：Index -1 out of bounds for length 12 
    
    請確保輸出和跟上面一樣，在main內的程式不要更動的情況下，解釋:push到3時輸出Exception：Index 3 out of bounds for length 3 但會在pop : 3之後，然後容量加倍繼續讀456，到6時跳出Exception：Index 6 out of bounds for length 6，然後容量加倍，接著popall，輸出7 6 5 4 2 1 ，再pop()輸出The Stack is EMPTY!!! Exception: The Stack is EMPTY!!!
    push pop popall要寫exception 其他不用
    
    class Stack {


    public Stack(int capacity) {

    }

    public boolean isEmpty() {
        return top == -1;
    }

    public void push(int element) {
        try {
            stack[++top] = element;
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Exception : Index " + top + " out of bounds for length " + maxCapacity);
 
            maxCapacity *= 2;
            int[] newStack = new int[maxCapacity];
            for (int i = 0; i < stack.length; i++) {
                newStack[i] = stack[i];
            }
            stack = newStack;

            stack[top] = element;
        }
    }

    public int pop() throws Exception {
        if (isEmpty()) {
            
            throw new Exception("Exception : Index -1 out of bounds for length " + maxCapacity);
        }

    }

    public int top() {
    
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
