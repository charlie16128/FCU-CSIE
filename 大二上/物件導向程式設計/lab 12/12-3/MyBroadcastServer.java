import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class MyBroadcastServer {
    // 使用執行緒安全的 List 來儲存所有 Client 的輸出串流
    private static List<PrintWriter> allWriters = Collections.synchronizedList(new ArrayList<>());

    public static void main(String[] args) throws IOException {
        int portNumber = 5000;
        ServerSocket serverSocket = new ServerSocket(portNumber);
        System.out.println("Broadcast Server started on port " + portNumber);

        while (true) {
            Socket socket = serverSocket.accept();
            System.out.println("新成員加入: " + socket);
            
            // 每一個連線都開一條執行緒
            new ChatHandler(socket).start();
        }
    }

    // 廣播方法：把 message 傳給清單中的所有人
    private static void broadcast(String message) {
        synchronized (allWriters) {
            for (PrintWriter writer : allWriters) {
                writer.println(message);
            }
        }
    }

    private static class ChatHandler extends Thread {
        private Socket socket;
        private PrintWriter writer;

        public ChatHandler(Socket socket) {
            this.socket = socket;
        }

        @Override
        public void run() {
            try {
                BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                writer = new PrintWriter(socket.getOutputStream(), true);

                // 1. 將此 Client 的輸出串流加入全域清單
                allWriters.add(writer);
                
                // (選用) 告訴大家有新人加入
                // broadcast("--- 伺服器公告：有新使用者加入 ---");

                String inputLine;
                while ((inputLine = reader.readLine()) != null) {
                    System.out.println("收到廣播訊息: " + inputLine);
                    // 2. 收到的訊息不再是 Echo 給自己，而是廣播給所有人
                    // 為了區別是誰傳的，通常 Client 端可以傳送 "Name: Message"，或 Server 簡單加上前綴
                    broadcast(socket + "說: " + inputLine);
                }
            } catch (IOException e) {
                System.out.println("連線中斷");
            } finally {
                // 3. 斷線時，務必從清單移除
                if (writer != null) {
                    allWriters.remove(writer);
                }
                try {
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                System.out.println("成員離開: " + socket);
            }
        }
    }
}