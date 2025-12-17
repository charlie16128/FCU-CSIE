import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class MyTTTgame extends JFrame {
    private static final int FRAME_WIDTH = 350;
    private static final int FRAME_HEIGHT = 330;
    private static final int NUMBER_CELLS = 9;

    private JButton[] cells = new JButton[NUMBER_CELLS];
    private String CurPlayer;
    private boolean GameOver;
    private TTTHandler handler;

    public MyTTTgame(){
        super("My fucing game");
        
        this.setSize(FRAME_WIDTH, FRAME_HEIGHT);
        this.setResizable(false);
        this.setLocation(100,100);
        this.setDefaultCloseOperation(EXIT_ON_CLOSE);

        Container contentpane = getContentPane();
        contentpane.setLayout(new GridLayout(3,3));

        handler = new TTTHandler();

        for(int i = 0; i < NUMBER_CELLS; i++){
            cells[i] = new JButton();
            cells[i].setFont(new Font("Arial", Font.BOLD, 60));
            cells[i].setFocusPainted(false);
            cells[i].addActionListener(handler);
            this.add(cells[i]);           
        }

    }  

    private class TTTHandler implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e){
            
        }
    }
}
