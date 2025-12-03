import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;

public class TicTacToe extends JFrame implements ActionListener {

    private JButton[] buttons = new JButton[9];
    private String currentPlayer = "X";
    private boolean gameOver = false;

    public TicTacToe() {
        super("Tic Tac Toe");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(400, 400);
        setLayout(new GridLayout(3, 3));

        buttons = new JButton[9];
        for (int i = 0; i < 9; i++) {
            buttons[i] = new JButton("");
            buttons[i].setFont(new Font("Arial", Font.BOLD, 60));
            buttons[i].setFocusPainted(false);
            buttons[i].addActionListener(this); // 這裡需要類別 implements ActionListener 才能運作
            add(buttons[i]);
        }
        setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        JButton clickedBtn = (JButton) e.getSource();

        if (gameOver) {
            return;
        }

        if (!clickedBtn.getText().equals("")) {
            return;
        }

        clickedBtn.setText(currentPlayer);

        if (checkWin()) {
            JOptionPane.showMessageDialog(this, "Player " + currentPlayer + " wins!");
            gameOver = true;
        } else if (checkTie()) {
            JOptionPane.showMessageDialog(this, "It's a tie!");
            gameOver = true;
        } else {
            switchPlayer();
        }
    }

    private boolean checkWin() {
        int[][] winConditions = {
                {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
                {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
                {0, 4, 8}, {2, 4, 6}
        };

        for (int[] c : winConditions) {
            String b1 = buttons[c[0]].getText();
            String b2 = buttons[c[1]].getText();
            String b3 = buttons[c[2]].getText();

            if (!b1.equals("") && b1.equals(b2) && b2.equals(b3)) {
                return true;
            }
        }

        return false;
    }

    private boolean checkTie() {
        for (int i = 0; i < buttons.length; i++) {
            if (buttons[i].getText().equals("")) {
                return false;
            }
        }
        return true;
    }

    private void switchPlayer() {
        currentPlayer = (currentPlayer.equals("X")) ? "O" : "X";
    }

    public static void main(String[] args) {
        new TicTacToe();
    }
}