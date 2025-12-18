import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.*;
import java.net.Socket;

public class Lab2_TCPClient extends JFrame {
    private JTextArea messageArea;
    private JTextField inputField;
    private PrintWriter serverWriter;

    public Lab2_TCPClient() {
        super("TCP Client (Multi-thread Test)");
        initGUI();
        connectToServer(); // 嘗試連線 TCP Server
        
        this.setSize(400, 500);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setVisible(true);
    }

    private void connectToServer() {
        new Thread(() -> {
            try {
                Socket socket = new Socket("127.0.0.1", 5000);
                SwingUtilities.invokeLater(() -> messageArea.append("已連線到 TCP Server！\n"));
                
                serverWriter = new PrintWriter(socket.getOutputStream(), true);
                BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                
                String line;
                while ((line = reader.readLine()) != null) {
                    String finalMsg = line;
                    SwingUtilities.invokeLater(() -> messageArea.append(finalMsg + "\n"));
                }
            } catch (IOException e) {
                SwingUtilities.invokeLater(() -> messageArea.append("無法連線 (請確認 Server 已啟動且是 TCP 版本)\n"));
            }
        }).start();
    }

    private void initGUI() {
        this.setLayout(new BorderLayout());
        messageArea = new JTextArea();
        messageArea.setEditable(false);
        this.add(new JScrollPane(messageArea), BorderLayout.CENTER);

        JPanel bottom = new JPanel(new BorderLayout());
        inputField = new JTextField();
        JButton sendBtn = new JButton("Send");
        bottom.add(inputField, BorderLayout.CENTER);
        bottom.add(sendBtn, BorderLayout.EAST);
        this.add(bottom, BorderLayout.SOUTH);

        Action sendAction = new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (serverWriter != null && !inputField.getText().isEmpty()) {
                    serverWriter.println(inputField.getText());
                    inputField.setText("");
                }
            }
        };
        inputField.addActionListener(sendAction);
        sendBtn.addActionListener(sendAction);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(Lab2_TCPClient::new);
    }
}