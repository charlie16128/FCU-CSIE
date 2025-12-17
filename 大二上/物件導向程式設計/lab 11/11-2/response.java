```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.Socket;

public class MyGUIClient extends JFrame {
    private static final String ADDRESS = "127.0.0.1";
    private static final int PORT = 5000;

    private JTextArea messageArea;
    private JTextField inputField;
    private JButton sendButton;

    // 【填空 A：定義成員變數 Socket, PrintWriter, BufferedReader】
    private Socket socket;
    private PrintWriter serverWriter;
    private BufferedReader serverReader;

    public MyGUIClient() {
        super("Echo Client GUI");
        // 【填空 B：初始化介面、設定視窗屬性並啟動連線方法，確保不重複初始化】
        initGUI();
    }

    private void initGUI() {
        this.setLayout(new BorderLayout());

        messageArea = new JTextArea();
        messageArea.setEditable(false);

        // 【填空 C：將 messageArea 放入 JScrollPane 並加入 JFrame 的中央 (CENTER)】
        JScrollPane scrollPane = new JScrollPane(messageArea);
        this.add(scrollPane, BorderLayout.CENTER);

        JPanel bottomPanel = new JPanel(new BorderLayout());
        inputField = new JTextField();
        sendButton = new JButton("Send");

        // 【填空 D：佈局 bottomPanel，並將其加入視窗的南方 (SOUTH)】
        bottomPanel.add(inputField, BorderLayout.SOUTH);
        bottomPanel.add(sendButton, BorderLayout.EAST);
        this.add(bottomPanel, BorderLayout.SOUTH);

        ActionListener sendAction = e -> sendMessage();
        // 【填空 D：佈局 bottomPanel，並將其加入視窗的南方 (SOUTH)】
        inputField.addActionListener(sendAction);
        sendButton.addActionListener(sendAction);
    }

    private void connectToServer() {
        try {
            messageArea.append("正在連線到 Server...
");
            socket = new Socket(ADDRESS, PORT);

            // 建立串流
            serverWriter = new PrintWriter(socket.getOutputStream(), true);
            serverReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            messageArea.append("連線成功！
----------------------
");

            // ★關鍵：開啟一個新的背景執行緒來等待 Server 的訊息★
            // 如果不在新執行緒做，GUI 會因為卡在 readLine() 而當機
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        String echoMsg;
                        while ((echoMsg = serverReader.readLine()) != null) {
                            // 收到訊息後，顯示在 TextArea
                            String finalMsg = echoMsg;
                            SwingUtilities.invokeLater(() -> {
                                messageArea.append(finalMsg + "
");
                                // 自動捲動到底部
                                messageArea.setCaretPosition(messageArea.getDocument().getLength());
                            });
                        }
                    } catch (IOException e) {
                        messageArea.append("與 Server 斷線: " + e.getMessage() + "
");
                    }
                }
            }).start();

        } catch (IOException e) {
            messageArea.append("無法連線: " + e.getMessage() + "
");
            inputField.setEditable(false);
            sendButton.setEnabled(false);
        }
    }

    private void sendMessage() {
        // 【填空 H：取得文字、判斷非空值後發送並清空輸入框】
        String text = inputField.getText();
        if (!text.isEmpty()) {
            serverWriter.println(text);
            inputField.setText("");
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new MyGUIClient());
    }
}
```