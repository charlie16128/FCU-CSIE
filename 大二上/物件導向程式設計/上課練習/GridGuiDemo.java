import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

// ---------------------------------------------------------
// 1. 這是額外寫的 Class，專門用來處理按鈕動作
// ---------------------------------------------------------
class ButtonClickHandler implements ActionListener {
    
    // 當任何一顆綁定此 Handler 的按鈕被按下，都會執行這裡
    @Override
    public void actionPerformed(ActionEvent e) {
        // 透過 e.getSource() 抓取「到底是哪一顆按鈕」觸發了事件
        JButton clickedBtn = (JButton) e.getSource();
        
        // 取得按鈕目前的文字
        String text = clickedBtn.getText();
        
        // 邏輯處理：在 Console 印出並修改按鈕文字
        System.out.println("外部 Handler 偵測到點擊: " + text);
        
        // 簡單的互動效果：如果還沒被按過，就打勾
        if (!text.equals("✔")) {
            clickedBtn.setText("✔");
        } else {
            // 如果已經是打勾，就復原 (Toggle效果)
            clickedBtn.setText("?");
        }
    }
}

// ---------------------------------------------------------
// 2. 這是主 GUI Class
// ---------------------------------------------------------
public class GridGuiDemo {

    public void init() {
        JFrame frame = new JFrame("外部 Listener 範例");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 400);

        Container cp = frame.getContentPane();
        cp.setLayout(new GridLayout(3, 3, 5, 5));

        // 【關鍵步驟】建立一個 Handler 的實體物件
        // 我們只需要建立一次，就可以給 9 個按鈕共用！
        ButtonClickHandler myHandler = new ButtonClickHandler();

        for (int i = 1; i <= 9; i++) {
            JButton btn = new JButton("按鈕 " + i);
            
            // 【關鍵步驟】把剛剛建立的 handler 註冊給按鈕
            btn.addActionListener(myHandler);
            
            cp.add(btn);
        }

        frame.setVisible(true);
    }

    public static void main(String[] args) {
        GridGuiDemo demo = new GridGuiDemo();
        demo.init();
    }
}