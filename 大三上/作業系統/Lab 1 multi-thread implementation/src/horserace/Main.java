package horserace;

import javax.swing.SwingUtilities;

/** Application entry point. */
public final class Main {
    private Main() { }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override public void run() {
                new RaceFrame().setVisible(true);
            }
        });
    }
}
