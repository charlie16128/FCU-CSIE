import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class SimpleInputApp extends JFrame {

    private JTextArea displayArea;
    private JTextField inputField;
    private JButton submitButton;

    public SimpleInputApp() {
        super("簡單輸入應用程式");

        // --- 1. 初始化元件 ---
        displayArea = new JTextArea(5, 30);
        displayArea.setEditable(false); // 通常顯示區建議設為不可編輯
        JScrollPane scrollPane = new JScrollPane(displayArea);
        
        inputField = new JTextField(20);
        submitButton = new JButton("送出");

        // --- 2. 佈局設定 ---
        JPanel inputPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 5, 5));
        inputPanel.add(new JLabel("輸入文字:"));
        inputPanel.add(inputField);
        inputPanel.add(submitButton);

        this.add(scrollPane, BorderLayout.CENTER);
        this.add(inputPanel, BorderLayout.SOUTH);

        // --- 3. 設定視窗屬性 ---
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.pack();
        this.setLocationRelativeTo(null);
        this.setVisible(true);

        // --- 4. 【關鍵修改】使用外部的 Handler ---
        
        // 建立 Handler 物件，並把上面的 displayArea 和 inputField 傳進去
        // 這樣 Handler 才有權限去控制這些元件
        InputEventHandler myHandler = new InputEventHandler(displayArea, inputField);
        
        // 將同一個 handler 綁定給「按鈕」和「輸入框(Enter鍵)」
        submitButton.addActionListener(myHandler);
        inputField.addActionListener(myHandler);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                new SimpleInputApp();
            }
        });
    }
}

class InputEventHandler implements ActionListener {
    // 定義我們需要操作的元件變數
    private JTextArea displayArea;
    private JTextField inputField;

    // 【關鍵步驟】透過建構子，把 GUI 上的元件傳進來
    public InputEventHandler(JTextArea displayArea, JTextField inputField) {
        this.displayArea = displayArea;
        this.inputField = inputField;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        // 這裡的邏輯是從原本的 processInput() 搬過來的
        
        // 1. 取得輸入框中的文字 (直接操作傳進來的 inputField)
        String text = inputField.getText();

        if (!text.trim().isEmpty()) {
            // 2. 將文字附加到顯示區域
            displayArea.append(text + "\n");
            
            // 3. 清空輸入框
            inputField.setText("");
            
            // 4. 讓文字區域自動滾動到最底端 (UX 優化)
            displayArea.setCaretPosition(displayArea.getDocument().getLength());
            
            // 測試用：印在 Console 確認
            System.out.println("Handler 處理輸入: " + text);
        }
    }
}