// import javax.swing.*;
// import java.awt.*;
// import java.awt.event.ActionEvent;
// import java.awt.event.ActionListener;
// import java.io.*;
// import java.net.Socket;

// public class MyGUIClient extends JFrame {
//     private static final String ADDRESS = "127.0.0.1";
//     private static final int PORT = 5000;

//     // GUI 元件
//     private JTextArea messageArea; // 顯示訊息區域 (North/Center)
//     private JTextField inputField; // 輸入區域 (South)
//     private JButton sendButton;    // 發送按鈕 (South)

//     // 網路變數
//     private PrintWriter serverWriter;
//     private BufferedReader serverReader;
//     private Socket socket;

//     public MyGUIClient() {
//         super("Echo Client GUI"); // 設定視窗標題

//         // 1. 初始化 GUI 介面
//         initGUI();

//         // 2. 連線到 Server (建議放在建構子或另外的方法)
//         connectToServer();

//         // 3. 設定視窗屬性
//         this.setSize(400, 500);
//         this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
//         this.setVisible(true);
//     }

//     private void initGUI() {
//         this.setLayout(new BorderLayout());

//         // --- 顯示區域 (Center) ---
//         messageArea = new JTextArea();
//         messageArea.setEditable(false); // 使用者不可直接編輯顯示區
//         messageArea.setFont(new Font("Monospaced", Font.PLAIN, 14));
//         // 加上捲軸，以免訊息過長無法顯示
//         JScrollPane scrollPane = new JScrollPane(messageArea);
//         this.add(scrollPane, BorderLayout.CENTER);


//         // --- 輸入區域 (South) ---
//         JPanel bottomPanel = new JPanel();
//         bottomPanel.setLayout(new BorderLayout());

//         inputField = new JTextField();
//         inputField.setFont(new Font("SansSerif", Font.PLAIN, 14));
        
//         sendButton = new JButton("Send");

//         bottomPanel.add(inputField, BorderLayout.CENTER);
//         bottomPanel.add(sendButton, BorderLayout.EAST);

//         this.add(bottomPanel, BorderLayout.SOUTH);

//         // --- 事件監聽 (按下 Enter 或 點擊按鈕) ---
//         ActionListener sendAction = new ActionListener() {
//             @Override
//             public void actionPerformed(ActionEvent e) {
//                 sendMessage();
//             }
//         };

//         inputField.addActionListener(sendAction); // 讓使用者按 Enter 也能送出
//         sendButton.addActionListener(sendAction); // 按按鈕送出
//     }

//     private void connectToServer() {
//         try {
//             messageArea.append("正在連線到 Server...\n");
//             socket = new Socket(ADDRESS, PORT);
            
//             // 建立串流
//             serverWriter = new PrintWriter(socket.getOutputStream(), true);
//             serverReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            
//             messageArea.append("連線成功！\n----------------------\n");

//             // ★關鍵：開啟一個新的背景執行緒來等待 Server 的訊息★
//             // 如果不在新執行緒做，GUI 會因為卡在 readLine() 而當機
//             new Thread(new Runnable() {
//                 @Override
//                 public void run() {
//                     try {
//                         String echoMsg;
//                         // 這裡會持續等待 Server 的回應
//                         while ((echoMsg = serverReader.readLine()) != null) {
//                             // 收到訊息後，顯示在 TextArea
//                             // 因為是在背景執行緒，更新 GUI 最好用 invokeLater (雖不強制但較安全)
//                             String finalMsg = echoMsg;
//                             SwingUtilities.invokeLater(() -> {
//                                 messageArea.append(finalMsg + "\n");
//                                 // 自動捲動到底部
//                                 messageArea.setCaretPosition(messageArea.getDocument().getLength());
//                             });
//                         }
//                     } catch (IOException e) {
//                         messageArea.append("與 Server 斷線: " + e.getMessage() + "\n");
//                     }
//                 }
//             }).start();

//         } catch (IOException e) {
//             messageArea.append("無法連線到 Server: " + e.getMessage() + "\n");
//             inputField.setEditable(false); // 連線失敗就禁止輸入
//             sendButton.setEnabled(false);
//         }
//     }

//     // 發送訊息的方法
//     private void sendMessage() {
//         String text = inputField.getText();
//         if (text != null && !text.trim().isEmpty()) {
//             // 1. 送出給 Server
//             if (serverWriter != null) {
//                 serverWriter.println(text);
//             }
            
//             // 2. 清空輸入框
//             inputField.setText("");
            
//             // (選用) 是否要先在自己畫面顯示 "我: xxx"？
//             // 依照你的題目需求是「Server echo 回來才顯示」，所以這邊通常不先顯示
//         }
//     }

//     public static void main(String[] args) {
//         // 啟動 GUI
//         SwingUtilities.invokeLater(() -> new MyGUIClient());
//     }
// }


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
            serverReader = new BufferedReader(new InputStreamReader(socket.getOutputStream()));

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
                            SwingUtilities.invokeLater(() -> {
                                messageArea.append(echoMsg + "
"); // 這裡不要更改
                                // 自動捲動到底部
                                messageArea.setCaretPosition(messageArea.getDocument().getLength()); // 這裡不要更改
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