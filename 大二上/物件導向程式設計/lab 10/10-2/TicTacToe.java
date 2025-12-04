import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class TicTacToe extends JFrame implements ActionListener {

    // 介面元件
    private JButton[][] buttons = new JButton[3][3];
    private JMenuItem resetItem;
    private JMenuItem changeSymbolItem;
    private JLabel statusLabel;

    // 遊戲資料
    private String p1Symbol = "O";
    private String p2Symbol = "X";
    private boolean isP1Turn = true; // true 代表輪到 P1 (O), false 代表 P2 (X)
    private int movesCount = 0; // 計算步數，判斷平手用

    public TicTacToe() {
        super("井字遊戲 Tic-Tac-Toe");
        setSize(400, 450);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null); // 視窗置中
        setLayout(new BorderLayout());

        // --- 1. 建立選單 (包含 Reset 和 Change Symbols) ---
        JMenuBar menuBar = new JMenuBar();
        JMenu optionMenu = new JMenu("Options");

        // 重置選項
        resetItem = new JMenuItem("Reset Game");
        resetItem.addActionListener(this);
        optionMenu.add(resetItem);

        // 更換符號選項
        changeSymbolItem = new JMenuItem("Change Symbols");
        changeSymbolItem.addActionListener(this);
        optionMenu.add(changeSymbolItem);

        menuBar.add(optionMenu);
        setJMenuBar(menuBar);

        // --- 2. 建立遊戲按鈕區 ---
        JPanel boardPanel = new JPanel();
        boardPanel.setLayout(new GridLayout(3, 3));
        
        Font font = new Font("Arial", Font.BOLD, 60);
        
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                buttons[i][j] = new JButton("");
                buttons[i][j].setFont(font);
                buttons[i][j].setFocusPainted(false);
                buttons[i][j].addActionListener(this);
                boardPanel.add(buttons[i][j]);
            }
        }
        add(boardPanel, BorderLayout.CENTER);

        // --- 3. 狀態列 ---
        statusLabel = new JLabel("輪到玩家: " + p1Symbol);
        statusLabel.setHorizontalAlignment(SwingConstants.CENTER);
        statusLabel.setFont(new Font("Microsoft JhengHei", Font.PLAIN, 16));
        statusLabel.setBorder(BorderFactory.createEmptyBorder(10, 0, 10, 0));
        add(statusLabel, BorderLayout.SOUTH);

        setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object source = e.getSource();

        // --- 功能 (2): Reset 選單 ---
        if (source == resetItem) {
            resetGame();
            return;
        }

        // --- 功能 (3): 改變符號機制 ---
        if (source == changeSymbolItem) {
            changeSymbols();
            return;
        }

        // --- 處理棋盤點擊 ---
        // 檢查是否點擊了棋盤按鈕
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (source == buttons[i][j]) {
                    // 如果按鈕已經有字，不做反應
                    if (!buttons[i][j].getText().equals("")) {
                        return;
                    }

                    // 設定符號
                    String currentSymbol = isP1Turn ? p1Symbol : p2Symbol;
                    buttons[i][j].setText(currentSymbol);
                    movesCount++;

                    // 檢查是否獲勝或平手
                    if (checkWin(currentSymbol)) {
                        // --- 功能 (1): 獲勝彈窗 ---
                        JOptionPane.showMessageDialog(this, "玩家 " + currentSymbol + " 獲勝！");
                        resetGame();
                    } else if (movesCount == 9) {
                        // --- 功能 (1): 平手彈窗 ---
                        JOptionPane.showMessageDialog(this, "平手 (Draw)！");
                        resetGame();
                    } else {
                        // 換下一位
                        isP1Turn = !isP1Turn;
                        updateStatus();
                    }
                }
            }
        }
    }

    // 判斷獲勝邏輯
    private boolean checkWin(String symbol) {
        // 檢查橫列
        for (int i = 0; i < 3; i++) {
            if (buttons[i][0].getText().equals(symbol) &&
                buttons[i][1].getText().equals(symbol) &&
                buttons[i][2].getText().equals(symbol)) {
                return true;
            }
        }
        // 檢查直行
        for (int j = 0; j < 3; j++) {
            if (buttons[0][j].getText().equals(symbol) &&
                buttons[1][j].getText().equals(symbol) &&
                buttons[2][j].getText().equals(symbol)) {
                return true;
            }
        }
        // 檢查對角線
        if (buttons[0][0].getText().equals(symbol) &&
            buttons[1][1].getText().equals(symbol) &&
            buttons[2][2].getText().equals(symbol)) {
            return true;
        }
        if (buttons[0][2].getText().equals(symbol) &&
            buttons[1][1].getText().equals(symbol) &&
            buttons[2][0].getText().equals(symbol)) {
            return true;
        }

        return false;
    }

    // 重置遊戲板
    private void resetGame() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                buttons[i][j].setText("");
            }
        }
        isP1Turn = true;
        movesCount = 0;
        updateStatus();
    }

    // 更新下方狀態列文字
    private void updateStatus() {
        String current = isP1Turn ? p1Symbol : p2Symbol;
        statusLabel.setText("輪到玩家: " + current);
    }

    // --- 功能 (3) 實作細節: 改變符號 ---
    private void changeSymbols() {
        // String newP1 = JOptionPane.showInputDialog(this, "請輸入玩家 1 的符號:", p1Symbol);
        

        // String newP2 = JOptionPane.showInputDialog(this, "請輸入玩家 2 的符號:", p2Symbol);



        JPanel panel = new JPanel(new GridLayout(3,2,5,5));

        JLabel label1 = new JLabel("玩家 1 符號(目前:" + p1Symbol + "):" );
        JTextField field1 = new JTextField(String.valueOf(p1Symbol), 5);

        JLabel label2 = new JLabel("玩家 2 符號(目前:" + p2Symbol + "):" );
        JTextField field2 = new JTextField(String.valueOf(p2Symbol), 5);
        
        panel.add(label1);
        panel.add(field1);
        panel.add(label2);
        panel.add(field2);

        int result = JOptionPane.showConfirmDialog(
            this,
            panel,
            "Change Simbel",
            JOptionPane.OK_CANCEL_OPTION,
            JOptionPane.PLAIN_MESSAGE
        );

        String newP1 = field1.getText().trim();
        String newP2 = field2.getText().trim();

        if (newP1 == null || newP1.trim().isEmpty()){
            ShowError(); 
            return; // 取消或空白則不處理
        } 
        if (newP2 == null || newP2.trim().isEmpty()){
            ShowError(); 
            return;
        } 
        
        // 檢查兩者是否相同
        if (newP1.equals(newP2)) {
            JOptionPane.showMessageDialog(this, "錯誤：兩位玩家的符號不能相同！", "錯誤", JOptionPane.ERROR_MESSAGE);
        } else {
            // 更新符號並重置遊戲以示公平
            p1Symbol = newP1;
            p2Symbol = newP2;
            resetGame();
            JOptionPane.showMessageDialog(this, "符號已更新為 " + p1Symbol + " 與 " + p2Symbol + "，遊戲已重置。");
        }
    }
    void ShowError(){
        JOptionPane.showMessageDialog(
            this,
            "符號不能為空",
            "ERROR",
            JOptionPane.ERROR_MESSAGE
        );
    }

    public static void main(String[] args) {
        new TicTacToe();
    }
}