import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class MyServer {
    private static final int PORT = 5487;

    public static void main(String[] args) {
        System.out.println("=== Server 啟動中 (Port: " + PORT + ") ===");

        // 1. ServerSocket 建立一次就好，不用放在迴圈裡
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {

            // 2. 最外層加一個 while(true)，讓 Server 永遠活著
            while (true) {
                System.out.println("等待 Client 連線中...");

                // 3. accept() 會停在這裡等，直到有新的 Client 連上來
                try (Socket client = serverSocket.accept()) {
                    System.out.println("Client 已連線: " + client.getInetAddress());

                    // 設定串流
                    BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
                    PrintWriter out = new PrintWriter(client.getOutputStream(), true);

                    String inputLine;

                    // 4. 與「當前」Client 溝通的迴圈
                    while ((inputLine = in.readLine()) != null) {
                        System.out.println("收到: " + inputLine);
                        out.println("Server Echo: " + inputLine);
                    }
                    
                    // 當 in.readLine() 回傳 null，代表 Client 斷線了
                    System.out.println("Client 已斷線，準備等待下一位...");

                } catch (IOException e) {
                    System.out.println("與 Client 連線發生錯誤: " + e.getMessage());
                }
                // 這裡會自動關閉 client socket (因為 try-with-resources)，然後回到最上面的 while(true)
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}