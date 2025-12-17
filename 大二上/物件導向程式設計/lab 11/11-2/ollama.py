import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": 
    """
    請根據我提供的 Java 程式碼骨架完成填空任務，實現一個功能正確的 Echo Client。在【填空 A】請定義 Socket、PrintWriter (serverWriter) 與 BufferedReader (serverReader)；在【填空 B】將 JTextArea 封裝進 JScrollPane 並加入視窗的 BorderLayout.CENTER 位置；在【填空 C】將 inputField 放在底面板中央，sendButton 放在底面板東方 (EAST)，並將面板置於視窗南方；在【填空 D】使用 addActionListener 為輸入框與按鈕綁定發送動作；在【填空 E】使用 127.0.0.1 和 5000 埠號建立 Socket，並正確初始化 serverWriter (需開啟 autoFlush) 與 serverReader；在【填空 F】必須開啟一個獨立 Thread，在 while 迴圈中使用 readLine() 監聽伺服器訊息，收到訊息後利用 SwingUtilities.invokeLater 附加文字至 messageArea，並利用 setCaretPosition 確保捲軸自動滾動到底部；最後在【填空 G】實作 sendMessage 邏輯，取得 inputField 文字後若不為空則透過 serverWriter 送出並呼叫 setText("") 清空輸入框。請直接輸出完整的程式碼，確保邏輯嚴謹且不使用任何自定義或非標準庫類別。
    程式要能執行，要能編譯，已經有的程式碼絕對不能更改、更動 要完全一模一樣
    
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

    public MyGUIClient() {
        super("Echo Client GUI");
        // 【填空 B：初始化介面、設定視窗屬性並啟動連線方法，確保不重複初始化】
    }

    private void initGUI() {
        this.setLayout(new BorderLayout());

        messageArea = new JTextArea();
        messageArea.setEditable(false);
        // 【填空 C：將 messageArea 放入 JScrollPane 並加入 JFrame 的中央 (CENTER)】

        JPanel bottomPanel = new JPanel(new BorderLayout());
        inputField = new JTextField();
        sendButton = new JButton("Send");
        // 【填空 D：佈局 bottomPanel，並將其加入視窗的南方 (SOUTH)】

        ActionListener sendAction = e -> sendMessage();
        // 【填空 E：為 inputField 與 sendButton 註冊 sendAction 監聽器】
    }

    private void connectToServer() {
        try {
            messageArea.append("正在連線到 Server...\n");// 不要換行
            socket = new Socket(ADDRESS, PORT);
            
            // 建立串流
            serverWriter = new PrintWriter(socket.getOutputStream(), true);
            serverReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            
            messageArea.append("連線成功！\n----------------------\n"); // 不要換行

            // ★關鍵：開啟一個新的背景執行緒來等待 Server 的訊息★
            // 如果不在新執行緒做，GUI 會因為卡在 readLine() 而當機
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        String echoMsg;
                        // 這裡會持續等待 Server 的回應
                        while ((echoMsg = serverReader.readLine()) != null) {
                            // 收到訊息後，顯示在 TextArea
                            // 因為是在背景執行緒，更新 GUI 最好用 invokeLater (雖不強制但較安全)
                            String finalMsg = echoMsg;
                            SwingUtilities.invokeLater(() -> {
                                messageArea.append(finalMsg + "\n"); // 這裡不要更改 // 不要換行
                                // 自動捲動到底部
                                messageArea.setCaretPosition(messageArea.getDocument().getLength()); // 這裡不要更改 // 不要換行
                            });
                        }
                    } catch (IOException e) {
                        messageArea.append("與 Server 斷線: " + e.getMessage() + "\n"); // 不要換行
                    }
                }
            }).start();
            
        } catch (IOException e) {
            messageArea.append("無法連線: " + e.getMessage() + "\n");// 不要換行
            inputField.setEditable(false);
            sendButton.setEnabled(false);
        }
    }

    private void sendMessage() {
        // 【填空 H：取得文字、判斷非空值後發送並清空輸入框】
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new MyGUIClient());
    }
}
    """,
    "stream": False
}

def get_response():
    r = requests.post(url, json=payload, timeout=600)
    r.raise_for_status()
    data = r.json()
    return data["response"]

if __name__ == "__main__":
    response = get_response()
    print(f'{response}')

    with open("response.java", "w", encoding="utf-8") as f:
        f.write(response)
    print("程式碼存成 response.java")
