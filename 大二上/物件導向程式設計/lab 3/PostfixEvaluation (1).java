public class PostfixEvaluation {
	public int evaluate(char[] input) {
		MyStack2 stack = new MyStack2(50); // 建立足夠大的 stack

		for (char ch : input) {
			if (Character.isDigit(ch)) {
				stack.push(Character.digit(ch, 10)); // 轉為數字後 push
			} else {
				// 遇到運算符號就 pop 兩個數來做運算
				int b = stack.pop(); // 注意順序：先 pop 出來的是右邊的數
				int a = stack.pop(); // 再 pop 出來的是左邊的數
				int result = 0;

				switch (ch) {
					case '+': result = a + b; break;
					case '-': result = a - b; break;
					case '*': result = a * b; break;
					case '/': result = a / b; break;
					default:
						System.out.println("Invalid operator: " + ch);
						break;
				}
				stack.push(result); // 將結果推回 stack
			}
		}

		return stack.pop(); // 最終結果
	}

	public static void main(String args[]) {
		PostfixEvaluation pe = new PostfixEvaluation();

		System.out.println(pe.evaluate("234*+".toCharArray())); // 2 + (3 * 4) = 14
		System.out.println(pe.evaluate("23*4+".toCharArray())); // (2 * 3) + 4 = 10
		System.out.println(pe.evaluate("12+7*".toCharArray())); // (1 + 2) * 7 = 21
		System.out.println(pe.evaluate("68*2/".toCharArray())); // (6 * 8) / 2 = 24
		System.out.println(pe.evaluate("123-4+*51-*3*".toCharArray())); // Complex
		System.out.println(pe.evaluate("42/3-4+5*13*-".toCharArray())); // Complex
	}
}
