import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.net.*;

public class MyUDPClient extends JFrame {
    private static final String ADDRESS = "127.0.0.1";
    private static final int PORT = 5000;

    private JTextArea messageArea;
    private JTextField inputField;
    private JButton sendButton;

    // UDP 變數
    private DatagramSocket socket;
    private InetAddress serverAddress;

    public MyUDPClient() {
        super("UDP Echo Client");
        initGUI();
        initNetwork(); // 建立 UDP Socket
        
        this.setSize(400, 500);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setVisible(true);
    }

    private void initGUI() {
        this.setLayout(new BorderLayout());
        messageArea = new JTextArea();
        messageArea.setEditable(false);
        messageArea.setFont(new Font("Monospaced", Font.PLAIN, 14));
        this.add(new JScrollPane(messageArea), BorderLayout.CENTER);

        JPanel bottomPanel = new JPanel(new BorderLayout());
        inputField = new JTextField();
        inputField.setFont(new Font("SansSerif", Font.PLAIN, 14));
        sendButton = new JButton("Send");

        bottomPanel.add(inputField, BorderLayout.CENTER);
        bottomPanel.add(sendButton, BorderLayout.EAST);
        this.add(bottomPanel, BorderLayout.SOUTH);

        ActionListener sendAction = e -> sendMessage();
        inputField.addActionListener(sendAction);
        sendButton.addActionListener(sendAction);
    }

    private void initNetwork() {
        try {
            socket = new DatagramSocket(); // 自動分配一個可用 port
            serverAddress = InetAddress.getByName(ADDRESS);
            messageArea.append("UDP Socket 已建立，準備發送封包...\n");

            // 啟動背景執行緒接收 Server 回傳的封包
            new Thread(() -> {
                byte[] buf = new byte[1024];
                while (true) {
                    try {
                        DatagramPacket packet = new DatagramPacket(buf, buf.length);
                        socket.receive(packet); // 等待接收
                        String received = new String(packet.getData(), 0, packet.getLength());
                        
                        SwingUtilities.invokeLater(() -> {
                            messageArea.append(received + "\n");
                            messageArea.setCaretPosition(messageArea.getDocument().getLength());
                        });
                    } catch (IOException e) {
                        messageArea.append("接收錯誤: " + e.getMessage() + "\n");
                        break;
                    }
                }
            }).start();

        } catch (Exception e) {
            messageArea.append("無法建立 Socket: " + e.getMessage() + "\n");
        }
    }

    private void sendMessage() {
        String text = inputField.getText();
        if (text != null && !text.trim().isEmpty()) {
            try {
                byte[] data = text.getBytes();
                DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, PORT);
                socket.send(packet);
                inputField.setText("");
            } catch (IOException e) {
                messageArea.append("發送失敗: " + e.getMessage() + "\n");
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(MyUDPClient::new);
    }
}