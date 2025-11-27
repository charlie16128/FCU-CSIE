import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

class MyJFrame extends JFrame {
	
	public MyJFrame(String title) {
		super(title);
		this.setLocation(0, 0);
		this.setSize(400, 400);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Container contentPane = this.getContentPane();
		contentPane.setBackground(Color.WHITE);
		
		// 改為 3x3 的九宮格
		contentPane.setLayout(new GridLayout(3, 3, 5, 5));
		
		MyActionListener actionListener = new MyActionListener();
		
		// 建立 9 個按鈕
		for(int i = 0; i < 9; i++) {
			JButton button = new JButton("");
			button.setFont(new Font("Arial", Font.BOLD, 60));
			button.setBackground(Color.WHITE);
			button.setOpaque(true);
			button.setBorderPainted(true);
			button.setFocusPainted(false);
			button.addActionListener(actionListener);
			contentPane.add(button);
		}
		
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
	
	public void actionPerformed(ActionEvent event) {
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
		
		// 切換回合
		isOTurn = !isOTurn;
		
		// 如果盤面已填滿（9 步），遊戲結束
		if(moveCount >= 9) {
			JOptionPane.showMessageDialog(null, "遊戲結束！盤面已填滿");
		}
	}
}