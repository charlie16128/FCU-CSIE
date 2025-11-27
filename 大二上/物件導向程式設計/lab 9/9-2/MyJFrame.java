import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

class MyJFrame extends JFrame {
	
	public MyJFrame(String title) {
		super(title);
		this.setLocation(150, 250);
		this.setSize(400, 400);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		Container contentPane = this.getContentPane();
		contentPane.setBackground(Color.BLACK);
		
		// 改為 3x3 的九宮格
		contentPane.setLayout(new GridLayout(3, 3, 5, 5));
		
		MyActionListener actionListener = new MyActionListener();
		
		// 建立 9 個按鈕
		JButton[] buttons = new JButton[9];
		for(int i = 0; i < 9; i++) {
			buttons[i] = new JButton("");
			buttons[i].setFont(new Font("Arial", Font.BOLD, 60));
			buttons[i].setBackground(Color.GRAY);
			buttons[i].setOpaque(true);
			buttons[i].setBorderPainted(true);
			buttons[i].setFocusPainted(false);
			buttons[i].addActionListener(actionListener);
			contentPane.add(buttons[i]);
		}
		
		// 將按鈕陣列和 contentPane 傳給 ActionListener
		actionListener.setButtons(buttons);
		actionListener.setContentPane(contentPane);
		
		this.setVisible(true);
		
	}
	
	public static void main(String[] args) {
		// 設定系統預設的 Look and Feel
		try {
			UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());
		} catch (Exception e) {
			e.printStackTrace();
		}
		MyJFrame frame1 = new MyJFrame("井字遊戲");
	}
}

class MyActionListener implements ActionListener {
	private boolean isOTurn = true; // true 代表 O 的回合，false 代表 X 的回合
	private int moveCount = 0; // 記錄已下的棋子數
	private JButton[] buttons; // 儲存所有按鈕的參考
	private boolean gameOver = false; // 遊戲是否結束
	private Container contentPane; // 儲存 contentPane 的參考
	
	public void setButtons(JButton[] buttons) {
		this.buttons = buttons;
	}
	
	public void setContentPane(Container contentPane) {
		this.contentPane = contentPane;
	}
	
	public void actionPerformed(ActionEvent event) {
		// 如果遊戲已結束，不處理點擊
		if(gameOver) {
			return;
		}
		
		JButton clickedButton = (JButton) event.getSource();
		String buttonText = clickedButton.getText();
		
		// 如果按鈕已經有文字（已經被下過棋），則不做任何動作
		if(!buttonText.equals("")) {
			return;
		}
		
		// 根據當前回合放置 O 或 X，並設定顏色
		if(isOTurn) {
			clickedButton.setText("O");
			clickedButton.setForeground(Color.BLUE);
		} else {
			clickedButton.setText("X");
			clickedButton.setForeground(Color.RED);
		}
		
		// 移除 ActionListener 防止再次點擊
		clickedButton.removeActionListener(this);
		
		// 增加移動計數
		moveCount++;
		
		// 檢查是否有人獲勝
		if(checkWin()) {
			gameOver = true;
			contentPane.setBackground(Color.WHITE); // 改變背景為白色
			String winner = isOTurn ? "O" : "X";
			JOptionPane.showMessageDialog(null, winner + " 獲勝！");
			resetGame(); // 重新開始遊戲
			return;
		}
		
		// 切換回合
		isOTurn = !isOTurn;
		
		// 如果盤面已填滿（9 步），遊戲結束，平手
		if(moveCount >= 9) {
			gameOver = true;
			contentPane.setBackground(Color.WHITE); // 改變背景為白色
			JOptionPane.showMessageDialog(null, "遊戲結束！平手");
			resetGame(); // 重新開始遊戲
		}
	}
	
	// 檢查是否有人獲勝
	private boolean checkWin() {
		// 定義所有可能的獲勝組合（8 種）
		int[][] winPatterns = {
			{0, 1, 2}, // 第一橫排
			{3, 4, 5}, // 第二橫排
			{6, 7, 8}, // 第三橫排
			{0, 3, 6}, // 第一直排
			{1, 4, 7}, // 第二直排
			{2, 5, 8}, // 第三直排
			{0, 4, 8}, // 左上到右下對角線
			{2, 4, 6}  // 右上到左下對角線
		};
		
		// 檢查每一種獲勝組合
		for(int[] pattern : winPatterns) {
			String pos1 = buttons[pattern[0]].getText();
			String pos2 = buttons[pattern[1]].getText();
			String pos3 = buttons[pattern[2]].getText();
			
			// 如果三個位置都有相同的符號（且不是空的），則獲勝
			if(!pos1.equals("") && pos1.equals(pos2) && pos2.equals(pos3)) {
				// 將獲勝的三個按鈕背景設為綠色
				buttons[pattern[0]].setBackground(Color.GREEN);
				buttons[pattern[1]].setBackground(Color.GREEN);
				buttons[pattern[2]].setBackground(Color.GREEN);
				return true;
			}
		}
		
		return false;
	}
	
	// 重新開始遊戲
	private void resetGame() {
		// 重置遊戲狀態
		isOTurn = true;
		moveCount = 0;
		gameOver = false;
		
		// 將背景改回黑色	
		contentPane.setBackground(Color.BLACK);
		
		// 重置所有按鈕
		for(JButton button : buttons) {
			button.setText("");
			button.setBackground(Color.GRAY);
			button.setForeground(Color.BLACK);
			// 重新加入 ActionListener
			button.addActionListener(this);
		}
	}
}