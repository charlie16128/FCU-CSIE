import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama9.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": """
    請完成以下程式碼，不要更改main，不需要印出overflow，只需要在push超過5個元素時顯示The Stack is FULL!!!或當stack為空時印出EMPTY符合main下面的輸出
    public class MyStack1 {
	//
	final static int MAX_STACK_SIZE = 5;
	
	public static boolean isFull() {
		System.out.println("The Stack is FULL!!!");
		return true;
	}
	
	public static boolean isEmpty() {
		System.out.println("The Stack is EMPTY!!!");
		return true;
	}
	
	public static void push(int theElement) {
	}
	
	public static void pop() {
	}
	
	public static int top() {
		return 0;
	}
	
	public static void popall() {
		// print the top and then pop it until the stack is empty
	}
	
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
