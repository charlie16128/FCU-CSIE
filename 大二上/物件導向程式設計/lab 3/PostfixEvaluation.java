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
		sstack.push(result); 
		}
	}
		return sstack.pop(); 
}
	public static void main(String args[]) {
		PostfixEvaluation pe = new PostfixEvaluation();
	
		System.out.println(pe.evaluate("234*+".toCharArray())); 
		System.out.println(pe.evaluate("23*4+".toCharArray())); 
		System.out.println(pe.evaluate("12+7*" + ".toCharArray()));
		System.out.println(pe.evaluate("68*2/" + ".toCharArray())); 
		System.out.println(pe.evaluate("123-4+*51-*3*" + ".toCharArray()));
		System.out.println(pe.evaluate("42/3-4+5*13*-" + ".toCharArray())); 
	}
}