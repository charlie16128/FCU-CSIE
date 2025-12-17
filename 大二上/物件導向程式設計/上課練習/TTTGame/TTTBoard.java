import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class TTTBoard extends JFrame {
    private static final int FRAME_WIDTH = 350;
    private static final int FRAME_HEIGHT = 330;
    private static final int NUMBER_CELLS = 9;
    
    // 遊戲狀態變數
    private JButton[] cells = new JButton[NUMBER_CELLS];
    private String currentPlayer; // "X" 或 "O"
    private boolean gameOver;
    private TTTHandler handler;

    public TTTBoard() {
        super("Tic Tac Toe Game");

        // 1. 設定視窗屬性 (修復了原本的語法錯誤)
        this.setSize(FRAME_WIDTH, FRAME_HEIGHT);
        this.setResizable(false); // 建議設為 false 以維持版面
        this.setLocation(100, 100); // 這裡也可以用 setLocationRelativeTo(null) 居中
        this.setDefaultCloseOperation(EXIT_ON_CLOSE);

        // 2. 設定版面配置
        Container contentPane = getContentPane();
        contentPane.setLayout(new GridLayout(3, 3));

        // 3. 初始化 Handler
        handler = new TTTHandler();

        // 4. 創建按鈕並加入監聽器 (修復了原本迴圈從 9 開始的錯誤)
        for (int i = 0; i < NUMBER_CELLS; i++) {
            cells[i] = new JButton();
            cells[i].setFont(new Font("Arial", Font.BOLD, 60)); // 設定字體大小讓 X/O 清楚顯示
            cells[i].setFocusPainted(false); // 去除點擊時的焦點框
            cells[i].addActionListener(handler); // 加入點擊事件
            this.add(cells[i]);
        }
        
        // 5. 初始化遊戲狀態
        init();
        
        this.setVisible(true); // 記得讓視窗顯示
    }

    // 初始化或重置遊戲
    public void init() {
        currentPlayer = "O";
        gameOver = false;
        for (int i = 0; i < NUMBER_CELLS; i++) {
            cells[i].setText("");
            cells[i].setBackground(null); // 清除贏家的顏色標記
            cells[i].setEnabled(true);
        }
        this.setTitle("現在輪到: " + currentPlayer);
    }

    // 內部類別：處理按鈕點擊事件
    private class TTTHandler implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            JButton clickedBtn = (JButton) e.getSource();

            // 如果遊戲結束或格子已經被佔用，則不動作
            if (gameOver || !clickedBtn.getText().equals("")) {
                return;
            }

            // 設定文字 (X 或 O)
            clickedBtn.setText(currentPlayer);
            
            // 檢查輸贏
            if (checkWin()) {
                gameOver = true;
                setTitle("遊戲結束! 贏家是: " + currentPlayer);
                JOptionPane.showMessageDialog(TTTBoard.this, "贏家是 " + currentPlayer + "!");
                init(); // 重新開始
            } else if (checkDraw()) {
                gameOver = true;
                setTitle("遊戲結束! 平手");
                JOptionPane.showMessageDialog(TTTBoard.this, "平手!");
                init(); // 重新開始
            } else {
                // 交換玩家
                currentPlayer = currentPlayer.equals("X") ? "O" : "X";
                setTitle("現在輪到: " + currentPlayer);
            }
        }
    }

    // 檢查是否有贏家
    private boolean checkWin() {
        // 所有贏法組合 (索引)
        int[][] winCombinations = {
            {0, 1, 2}, {3, 4, 5}, {6, 7, 8}, // 橫列
            {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, // 直行
            {0, 4, 8}, {2, 4, 6}             // 對角線
        };

        for (int[] combo : winCombinations) {
            JButton b1 = cells[combo[0]];
            JButton b2 = cells[combo[1]];
            JButton b3 = cells[combo[2]];

            // 檢查三個格子是否相同且不為空
            if (!b1.getText().isEmpty() &&
                b1.getText().equals(b2.getText()) &&
                b1.getText().equals(b3.getText())) {
                
                // 標記贏家顏色
                Color winColor = Color.GREEN;
                b1.setBackground(winColor);
                b2.setBackground(winColor);
                b3.setBackground(winColor);
                return true;
            }
        }
        return false;
    }

    // 檢查是否平手 (格子滿了但沒人贏)
    private boolean checkDraw() {
        for (JButton cell : cells) {
            if (cell.getText().isEmpty()) {
                return false; // 還有空格，尚未平手
            }
        }
        return true;
    }

    // Main 方法執行程式
    public static void main(String[] args) {
        // 使用 Event Dispatch Thread 啟動 Swing 程式較為安全
        SwingUtilities.invokeLater(() -> new TTTBoard());
    }
}