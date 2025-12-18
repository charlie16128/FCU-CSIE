import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class MyUDPEchoServer {
    public static void main(String[] args) {
        int portNumber = 5000;
        try (DatagramSocket serverSocket = new DatagramSocket(portNumber)) {
            System.out.println("UDP Server started on port " + portNumber);
            
            byte[] receiveBuffer = new byte[1024];

            while (true) {
                // 1. 準備接收封包的容器
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                
                // 2. 等待接收 (會卡在這裡直到有資料)
                serverSocket.receive(receivePacket);

                // 3. 解析資料
                String msg = new String(receivePacket.getData(), 0, receivePacket.getLength());
                InetAddress clientAddress = receivePacket.getAddress();
                int clientPort = receivePacket.getPort();

                System.out.println("收到來自 " + clientAddress + ":" + clientPort + " 的訊息: " + msg);

                // 4. 回傳 Echo 訊息
                String echoMsg = "Server Echo (UDP): " + msg;
                byte[] sendData = echoMsg.getBytes();
                DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, clientAddress, clientPort);
                
                serverSocket.send(sendPacket);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}