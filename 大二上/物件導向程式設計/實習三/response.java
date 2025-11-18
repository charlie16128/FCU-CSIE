```java
public class PostfixEvaluation {
	public int evaluate(char[] input) {
		MyStack2 stack = new MyStack2(50); 
	
		for (char ch : input) {
			if (Character.isDigit(ch)) {
				stack.push(Character.getNumericValue(ch));
			} else {
				
				int b = stack.pop(); 
				int a = stack.pop(); 
				int result = 0;
			
			switch (ch) {
			case '+':
			result = a + b;
			break;
			case '-':
			result = a - b;
			break;
			case '*':
			result = a * b;
			break;
			case '/':
			if (b == 0) {
			    System.out.println("Division by zero!");
			    return 0;
			}
			result = a / b;
			break;
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
```