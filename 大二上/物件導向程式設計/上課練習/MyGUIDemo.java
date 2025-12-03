import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class MyGUIDemo {
    
    public void init(){
        JFrame frame = new JFrame("Test");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400,400);

        Container cp = frame.getContentPane();
        cp.setLayout(new GridLayout(3,3));

        ButtonClickHandler myHandler = new ButtonClickHandler();
        for(int i = 1; i <= 9; i++){
            JButton btn = new JButton("按鈕" + i);
            btn.addActionListener(myHandler);
            cp.add(btn);
        }
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        MyGUIDemo demo = new MyGUIDemo();
        demo.init();
    }
}

class ButtonClickHandler implements ActionListener {
    @Override
    public void actionPerformed(ActionEvent e){
        JButton clickedBtn = (JButton)e.getSource();

        String text = clickedBtn.getText();

        System.out.println("按鈕 :" + text + "被點擊");
    }
}
