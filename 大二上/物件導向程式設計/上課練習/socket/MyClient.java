import java.io.*;
import java.net.Socket;
import java.util.Scanner;

public class MyClient {
    private static final String ADDRESS = "127.0.0.1";
    private static final int PORT = 5487;

    public static void main(String[] args) {
        try {
            // 1. 連線到 Server
            Socket client = new Socket(ADDRESS, PORT);
            System.out.println("=== 已連線到 Server，請開始輸入文字 ===");

            // 2. 設定網路串流
            // AutoFlush = true 很重要，不然資料會卡在 Buffer 出不去
            PrintWriter out = new PrintWriter(client.getOutputStream(), true);
            BufferedReader serverReader = new BufferedReader(new InputStreamReader(client.getInputStream()));

            // 3. 設定鍵盤輸入
            Scanner keyboard = new Scanner(System.in);

            while (true) {
                System.out.print("輸入: ");
                String input = keyboard.nextLine();

                if ("exit".equalsIgnoreCase(input)) {
                    System.out.println("結束連線...");
                    break;
                }

                // 4. 發送給 Server (必須用 println 以送出換行符號)
                out.println(input);

                // 5. 等待並讀取 Server 的 Echo 回應
                // 如果 Server 沒送回換行符號，程式會卡在這裡
                String response = serverReader.readLine();
                System.out.println(response);
            }

            // 關閉資源
            client.close();
            keyboard.close();

        } catch (IOException e) {
            System.out.println("無法連線至 Server，請確認 Server 是否已啟動。");
            e.printStackTrace();
        }
    }
}