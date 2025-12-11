import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class MyEchoServer {
    public static void main(String[] args) throws IOException{
        int portNumber = 5000;

		ServerSocket serverSocket = new ServerSocket(portNumber);
		System.out.println("Server started on port " + portNumber);
		while(true){
			try {
				
				System.out.println("等待連線......");
				Socket socket = serverSocket.accept();
				System.out.println("A new client is connected : " + socket);
				
				InputStream in = socket.getInputStream();
				OutputStream out = socket.getOutputStream();
				
				BufferedReader reader = new BufferedReader(new InputStreamReader(in));
				PrintWriter writer = new PrintWriter(out, true);

				String inputLine;

				while ((inputLine = reader.readLine()) != null) {
					System.out.println("收到 Client 訊息: " + inputLine);

					writer.println("Server Echo : " + inputLine);
				}
				
				System.out.println("Client disconnected.");
				socket.close();
			} catch(IOException e) {
				// e.printStackTrace();
				System.out.println("Client 已離線");
			}
		}
    }
}