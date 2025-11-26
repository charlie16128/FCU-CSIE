import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.plaf.TextUI;

public class SimpleInputApp extends JFrame {

    // 上方用於顯示結果的文字區域
    private JTextArea displayArea;
    // 下方用於輸入文字的輸入框
    private JTextField inputField;
    // 觸發動作的按鈕
    private JButton submitButton;

    public SimpleInputApp() {
        // 設定視窗標題
        super("簡單輸入應用程式");

        // 1. 初始化元件
        
        // 顯示區域：設定為 5 行 30 列，並讓它不可編輯
        displayArea = new JTextArea(5, 30);
        displayArea.setEditable(true);
        // 使用 JScrollPane 包裹 displayArea，讓文字多時可以滾動
        JScrollPane scrollPane = new JScrollPane(displayArea);
        
        // 輸入框：設定為 20 列寬
        inputField = new JTextField(20);
        
        // 按鈕
        submitButton = new JButton("送出");

        // 2. 建立佈局與容器
        
        // 使用 BorderLayout 佈局管理器 (JFrame 預設就是它)
        // 將顯示區域放在上方 (NORTH)
        
        // 建立一個 Panel 來放置輸入框和按鈕 (使用 FlowLayout 佈局)
        JPanel inputPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 5, 5));
        inputPanel.add(new JLabel("輸入文字:")); // 加入一個標籤
        inputPanel.add(inputField);
        inputPanel.add(submitButton);

        // 3. 將元件加入到 JFrame 視窗中
        this.add(scrollPane, BorderLayout.CENTER); // 將滾動面板放在中央
        this.add(inputPanel, BorderLayout.SOUTH);   // 將輸入面板放在下方

        // 4. 設定視窗屬性
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // 設定關閉按鈕的行為
        this.pack();                                         // 根據元件大小調整視窗大小
        this.setLocationRelativeTo(null);                    // 視窗置中
        this.setVisible(true);                               // 顯示視窗

        // 5. 新增事件監聽器
        
        // 按鈕按下時的動作
        submitButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                processInput();
            }
        });
        
        // 在輸入框中按下 Enter 鍵時的動作
        inputField.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                processInput();
            }
        });
    }
    
    /**
     * 處理輸入框內容並更新顯示區域的方法
     */
    private void processInput() {
        // 取得輸入框中的文字
        String text = inputField.getText();

        if (!text.trim().isEmpty()) {
            // 將文字附加到顯示區域，並換行
            displayArea.append(text + "\n");
            
            // 清空輸入框
            inputField.setText("");
            
            // 讓文字區域自動滾動到最底端 (可選)
            displayArea.setCaretPosition(displayArea.getDocument().getLength());
        }
    }

    // 主方法：啟動應用程式
    public static void main(String[] args) {
        // 確保 GUI 更新是在 AWT 事件調度線程中進行
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                new SimpleInputApp();
            }
        });
    }
}