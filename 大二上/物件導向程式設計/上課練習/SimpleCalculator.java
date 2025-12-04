import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class SimpleCalculator {

    private JFrame frame;
    private JTextField displayField; // 顯示螢幕

    private String currentOperator = ""; // 目前的運算符號 (+, -, *, /)
    private double firstNumber = 0;      // 儲存第一個輸入的數字
    private boolean isOperatorClicked = false; // 判斷是否剛按過運算符號

    public void init() {
        frame = new JFrame("My Calculator");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 500);
        frame.setLayout(new BorderLayout());
        frame.setLocation(0, 0);

        // --- 2. 介面設計 (View) ---
        
        // A. 上方顯示區 (North)
        displayField = new JTextField("");
        displayField.setFont(new Font("Consolas", Font.BOLD, 30));
        displayField.setHorizontalAlignment(JTextField.RIGHT); // 數字靠右對齊
        displayField.setEditable(true); // 禁止鍵盤直接輸入，強制用按鈕
        frame.add(displayField, BorderLayout.NORTH);

        // B. 按鈕區 (Center)
        JPanel btnPanel = new JPanel();
        btnPanel.setLayout(new GridLayout(4, 4, 5, 5)); // 4x4 的格子

        // 定義按鈕標籤陣列，這樣可以用迴圈建立，不用寫16行程式碼
        String[] btnLabels = {
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "C", "0", "=", "+"
        };

        // 建立監聽器物件 (稍後定義邏輯)
        ActionListener listener = new CalculatorListener();

        // 迴圈建立按鈕
        for (String label : btnLabels) {
            JButton btn = new JButton(label);
            btn.setFont(new Font("Arial", Font.BOLD, 24));
            btn.addActionListener(listener); // 綁定監聽器
            btnPanel.add(btn);
        }

        frame.add(btnPanel, BorderLayout.CENTER);
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new SimpleCalculator().init();
        });
    }


    private class CalculatorListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            String command = e.getActionCommand(); // 取得按鈕上的文字 (例如 "1", "+", "=")

            // 判斷按鈕類型
            if (command.matches("[0-9]")) { 
                // === 情況一：按了數字鍵 (0-9) ===

                if (displayField.getText().equals("0") || isOperatorClicked) {
                    displayField.setText(command);
                    isOperatorClicked = false; // 重置旗標
                } else {
                    displayField.setText(displayField.getText() + command);
                }

            } else if (command.equals("C")) {
                // === 情況二：按了清除鍵 ===
                displayField.setText("0");
                firstNumber = 0;
                currentOperator = "";
                
            } else if (command.equals("=")) {
                // === 情況三：按了等號 ===
                
                // 1. 取得現在螢幕上的數字 (這時候螢幕上顯示的是第二個數字)
                double secondNumber = Double.parseDouble(displayField.getText());
                double result = 0;

                // 2. 判斷要做什麼運算
                switch (currentOperator) {
                    case "+":
                        result = firstNumber + secondNumber;
                        break;
                    case "-":
                        result = firstNumber - secondNumber;
                        break;
                    case "*":
                        result = firstNumber * secondNumber;
                        break;
                    case "/":
                        if(secondNumber == 0){
                            displayField.setText("Error");
                            return;
                        }
                        result = firstNumber / secondNumber;
                        break;
                }

                // 3. 將結果顯示回螢幕 (把 double 轉回 String)
                displayField.setText(String.valueOf(result));
                
                // 運算完後，把這個結果當作下一次運算的「第一個數字」
                firstNumber = result; 
                // isOperatorClicked = true;
            } else {
                // === 情況四：按了運算符號 (+, -, *, /) ===
                
                // 1. 把螢幕上目前的文字轉成數字，存入 firstNumber
                String currentText = displayField.getText();
                firstNumber = Double.parseDouble(currentText);
                
                // 2. 記錄按下的符號 (例如 "+")
                currentOperator = command;
                
                // 3. 設定旗標為 true，這樣下次按數字時，程式就知道要先把螢幕清空
                isOperatorClicked = true;
                
                System.out.println("已暫存第一數: " + firstNumber + ", 運算符: " + currentOperator);
                
                System.out.println("按了運算符: " + command); // (除錯用)
            }
        }
    }
}