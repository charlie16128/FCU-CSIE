import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class SimpleCalculator {

    private JFrame frame;
    private JTextField displayField;

    private String currentOperator = "";
    private double firstNumber = 0;
    private boolean isOperatorClicked = false; 

    public void init() {
        frame = new JFrame("My Calculator");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 500);
        frame.setLayout(new BorderLayout());
        frame.setLocation(0, 0);

        // display area
        displayField = new JTextField("");
        displayField.setFont(new Font("Consolas", Font.BOLD, 30));
        displayField.setHorizontalAlignment(JTextField.RIGHT);
        displayField.setEditable(true);
        frame.add(displayField, BorderLayout.NORTH);

        // Setup buttons
        JPanel btnPanel = new JPanel();
        btnPanel.setLayout(new GridLayout(4, 4, 5, 5));

        String[] btnLabels = {
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "C", "0", "=", "+"
        };

        ActionListener listener = new CalculatorListener();

        for (String label : btnLabels) {
            JButton btn = new JButton(label);
            btn.setFont(new Font("Arial", Font.BOLD, 24));
            btn.addActionListener(listener);
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
            String command = e.getActionCommand();

            if (command.matches("[0-9]")) {
                // Handle number inputs
                if (displayField.getText().equals("0") || isOperatorClicked) {
                    displayField.setText(command);
                    isOperatorClicked = false;
                } else {
                    displayField.setText(displayField.getText() + command);
                }

            } else if (command.equals("C")) {
                // Handle clear
                displayField.setText("0");
                firstNumber = 0;
                currentOperator = "";

            } else if (command.equals("=")) {
                double secondNumber = Double.parseDouble(displayField.getText());
                double result = 0;

                switch (currentOperator) {
                    case "+": result = firstNumber + secondNumber; break;
                    case "-": result = firstNumber - secondNumber; break;
                    case "*": result = firstNumber * secondNumber; break;
                    case "/":
                        if (secondNumber == 0) {
                            displayField.setText("Error");
                            return;
                        }
                        result = firstNumber / secondNumber;
                        break;
                }

                displayField.setText(String.valueOf(result));
                firstNumber = result; 

            } else {    // Handle operators (+, -, *, /)
                String currentText = displayField.getText();
                if (!currentText.equals("Error")) {
                     firstNumber = Double.parseDouble(currentText);
                }
                currentOperator = command;
                isOperatorClicked = true;
            }
        }
    }
}