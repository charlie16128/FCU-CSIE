import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class Lab2_TCPServer {
    public static void main(String[] args) throws IOException {
        int port = 5000;
        ServerSocket serverSocket = new ServerSocket(port);
        System.out.println("【TCP 多執行緒 Server】已啟動，Port: " + port);

        while (true) {
            // 主迴圈只負責接受連線
            Socket socket = serverSocket.accept();
            System.out.println("新 Client 連入: " + socket);

            // 每一個連線都丟給一個新的 Thread 處理
            new ClientHandler(socket).start();
        }
    }

    // 處理單一客戶端的執行緒
    private static class ClientHandler extends Thread {
        private Socket socket;

        public ClientHandler(Socket socket) {
            this.socket = socket;
        }

        @Override
        public void run() {
            try {
                BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                PrintWriter writer = new PrintWriter(socket.getOutputStream(), true);

                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println("收到: " + line);
                    writer.println("Server Echo: " + line);
                }
            } catch (IOException e) {
                System.out.println("Client 斷線");
            }
        }
    }
}