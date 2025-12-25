import java.awt.Color;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.SwingUtilities;
import javax.swing.border.LineBorder;

public class ButtonColorExample {

    private static void createAndShowGUI() {
        // Create the JFrame
        JFrame frame = new JFrame("Button Background Color Example");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 300);
        frame.setLayout(null); // Use null layout for absolute positioning

        // Create the JButton
        JButton button = new JButton("Click Me!");
        
        // Set the background color to a specific color (e.g., green)
        button.setBackground(Color.GREEN);
        
        button.setBorder(new LineBorder(Color.red, 2));

        // Ensure the button is opaque so the background color is displayed correctly
        button.setOpaque(true);

        // Optional: set the text color
        button.setForeground(Color.BLACK);

        // Define the button's position and size (x, y, width, height)
        button.setBounds(100, 100, 150, 50);
        
        // Add the button to the frame
        frame.add(button);

        // Make the frame visible
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        // Ensure GUI creation happens on the Event Dispatch Thread (EDT)
        SwingUtilities.invokeLater(ButtonColorExample::createAndShowGUI);
    }
}
