import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": """
    請完成以下postfixecaluation function，僅輸出PostfixEvaluation和main就好，絕對不要更改main中的任何內容尤其是System.out.println(pe.evaluate("234*+".toCharArray()));完全不要動
    
public class PostfixEvaluation {
	public int evaluate(char[] input) {
		MyStack2 stack = new MyStack2(50); 

		for (char ch : input) {
			if (Character.isDigit(ch)) {
				sstack.push(Character.getNumericValue(ch));
			} else {
				// 遇到運算符號就 pop 兩個數來做運算
				int b = stack.pop(); // 注意順序：先 pop 出來的是右邊的數
				int a = stack.pop(); // 再 pop 出來的是左邊的數
				int result = 0;

				switch (ch) {
					
				}
				stack.push(result); 
			}
		}

		return stack.pop(); 
	}

	public static void main(String args[]) {
		PostfixEvaluation pe = new PostfixEvaluation();

		System.out.println(pe.evaluate("234*+".toCharArray())); 
		System.out.println(pe.evaluate("23*4+".toCharArray())); 
		System.out.println(pe.evaluate("12+7*".toCharArray()));
		System.out.println(pe.evaluate("68*2/".toCharArray())); 
		System.out.println(pe.evaluate("123-4+*51-*3*".toCharArray()));
		System.out.println(pe.evaluate("42/3-4+5*13*-".toCharArray())); 
	}
}




class MyStack2 {
	protected int maxCapacity;
	private int[] stack;
	protected int top;
	
	public static int value = 100;
	
	public MyStack2() {
		/*
		maxCapacity = 5;
		stack = new int[maxCapacity];
		top = -1;
		*/
		this(5);
	}
	
	public MyStack2(int capacity) {
		maxCapacity = capacity;
		stack = new int[maxCapacity];
		top = -1;
	}
	
	public boolean isFull() {
		if(top == maxCapacity - 1) {
			System.out.println("The Stack is FULL!!!");
			return true;
		}
		return false;
	}
	
	public boolean isEmpty() {
		if(top >= 0) {
			return false;
		}
		// System.out.println("The Stack is EMPTY!!!");
		return true;
	}
	
	public void push(int theElement) {
		if(!isFull()) {
			stack[++top] = theElement;
		}
	}
	
	public int pop() {
		if(!isEmpty()) {
			return stack[top--];
		}
		return 0;
	}
	
	public int top() {
		if(!isEmpty()) {
			return stack[top];
		}	
		return 0;
	}
	
	public void popall() {
		while(!isEmpty()) {
			System.out.println(top());
			pop();
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
