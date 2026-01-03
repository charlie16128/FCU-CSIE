import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;

public class ReversiServer {
    private static final int PORT = 8888;
    // 所有連線
    public static List<ClientHandler> allClients = Collections.synchronizedList(new ArrayList<>());
    // 隨機匹配佇列
    public static Queue<ClientHandler> randomQueue = new ConcurrentLinkedQueue<>();
    // 房間地圖 (房號 -> 房間物件)
    public static Map<String, GameRoom> roomMap = new ConcurrentHashMap<>();

    public static void main(String[] args) {
        System.out.println(">>> 黑白棋伺服器啟動 (Port: " + PORT + ")");
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            while (true) {
                Socket socket = serverSocket.accept();
                ClientHandler client = new ClientHandler(socket);
                allClients.add(client);
                new Thread(client).start();
            }
        } catch (IOException e) { e.printStackTrace(); }
    }

    // 大廳廣播
    public static void broadcastLobby(String msg) {
        synchronized (allClients) {
            for (ClientHandler c : allClients) {
                if (!c.isInGame) c.send(msg);
            }
        }
    }

    static class ClientHandler implements Runnable {
        private Socket socket;
        private PrintWriter out;
        private BufferedReader in;
        public String name;
        public boolean isInGame = false;
        public GameRoom currentRoom = null;

        public ClientHandler(Socket s) { this.socket = s; }

        public void run() {
            try {
                in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                out = new PrintWriter(socket.getOutputStream(), true);
                String line;
                while ((line = in.readLine()) != null) {
                    handleMessage(line);
                }
            } catch (IOException e) {
                System.out.println(name + " 斷線");
            } finally {
                cleanup();
            }
        }

        private void handleMessage(String msg) {
            String[] parts = msg.split("\\|");
            String type = parts[0];

            switch (type) {
                case "LOGIN":
                    this.name = parts[1];
                    broadcastLobby("LOBBY_CHAT|[系統]|歡迎 " + name + " 加入大廳");
                    break;
                case "CHAT":
                    if (isInGame && currentRoom != null) currentRoom.broadcast("GAME_CHAT|" + name + "|" + parts[1]);
                    else broadcastLobby("LOBBY_CHAT|" + name + "|" + parts[1]);
                    break;
                case "MATCH_RANDOM":
                    processRandomMatch();
                    break;
                case "CREATE_ROOM":
                    createPrivateRoom();
                    break;
                case "JOIN_ROOM":
                    if(parts.length > 1) joinPrivateRoom(parts[1]);
                    break;
                case "MOVE":
                    if (isInGame && currentRoom != null) 
                        currentRoom.handleMove(this, Integer.parseInt(parts[1]), Integer.parseInt(parts[2]));
                    break;
                case "EXIT": // 接收到離開/投降指令
                    if (currentRoom != null) currentRoom.playerExit(this);
                  break;
            }
        }

        private void processRandomMatch() {
            if (isInGame) return;
            send("LOBBY_CHAT|[系統]|正在尋找隨機對手...");
            synchronized (randomQueue) {
                if (randomQueue.contains(this)) return;
                if (!randomQueue.isEmpty()) {
                    ClientHandler opponent = randomQueue.poll();
                    GameRoom room = new GameRoom(this); 
                    room.join(opponent); 
                    System.out.println(name + " 和 " + opponent.name + "開始對戰了"); // 印出對戰資訊
                } else {
                    randomQueue.add(this);
                }
            }
        }

        private void createPrivateRoom() {
            if (isInGame) return;
            String roomId;
            do {
                roomId = String.format("%04d", new Random().nextInt(10000));
            } while (roomMap.containsKey(roomId));

            GameRoom room = new GameRoom(this, roomId);
            roomMap.put(roomId, room);
            
            this.currentRoom = room;
            this.isInGame = true; 
            send("ROOM_CREATED|" + roomId); 
            send("LOBBY_CHAT|[系統]|房間 " + roomId + " 已創建，等待對手加入...");
        }

        private void joinPrivateRoom(String roomId) {
            if (isInGame) return;
            GameRoom room = roomMap.get(roomId);
            if (room != null && !room.isFull()) {
                room.join(this);
                roomMap.remove(roomId); 
            } else {
                send("ERROR|房間不存在或已滿");
            }
        }

        public void send(String msg) { out.println(msg); }

        private void cleanup() {
            allClients.remove(this);
            randomQueue.remove(this);
            if (currentRoom != null && currentRoom.roomId != null) {
                roomMap.remove(currentRoom.roomId);
            }
            if (currentRoom != null) currentRoom.playerExit(this);
            try { socket.close(); } catch (IOException e) {}
        }
    }

    static class GameRoom {
        ClientHandler black, white;
        int[][] board = new int[8][8];
        int currentTurn = 1; 
        String roomId = null; 
        boolean gameStarted = false;

        // 創建房間(有ID)
        public GameRoom(ClientHandler host, String roomId) {
            this.black = host;
            this.roomId = roomId;
            host.currentRoom = this;
        }

        // 創建房間(有ID)
        public GameRoom(ClientHandler p1) {
            this.black = p1;
            p1.currentRoom = this;
        }

        public boolean isFull() { return black != null && white != null; }

        // 加入this房間
        public void join(ClientHandler p2) {
            this.white = p2;
            p2.currentRoom = this;
            startGame();
        }

        // 開始遊戲
        private void startGame() {
            this.gameStarted = true;
            black.isInGame = true;
            white.isInGame = true;

            // 初始化棋盤
            board[3][3] = 2; board[4][4] = 2;
            board[3][4] = 1; board[4][3] = 1;

            black.send("START|BLACK|" + white.name);
            white.send("START|WHITE|" + black.name);
            sendUpdate();
        }

        public void broadcast(String msg) {
            if(black!=null) black.send(msg);
            if(white!=null) white.send(msg);
        }

        public synchronized void handleMove(ClientHandler p, int r, int c) {
            if (!gameStarted) return;
            int pColor = (p == black) ? 1 : 2;
            if (pColor != currentTurn) return;

            if (isValidMove(r, c, pColor, true)) {
                board[r][c] = pColor;
                nextTurn();
            }
        }

        private void nextTurn() {
            int nextColor = (currentTurn == 1) ? 2 : 1;
            if (hasValidMove(nextColor)) {
                currentTurn = nextColor;
            } else {
                broadcast("MSG_PASS|" + (nextColor==1?"黑方":"白方"));
                if (!hasValidMove(currentTurn)) {
                    endGame();
                    return;
                }
            }
            sendUpdate();
            if (isFullBoard()) endGame();
        }

        private void sendUpdate() {
            StringBuilder sb = new StringBuilder();
            for(int[] row : board) for(int cell : row) sb.append(cell);
            broadcast("UPDATE|" + sb.toString() + "|" + currentTurn + "|" + count(1) + "|" + count(2));
        }

        private boolean isValidMove(int r, int c, int color, boolean execute) {
            if (board[r][c] != 0) return false;
            int opponent = (color == 1) ? 2 : 1;
            boolean valid = false;
            int[][] dirs = {{-1,0},{1,0},{0,-1},{0,1},{-1,-1},{-1,1},{1,-1},{1,1}};

            for (int[] d : dirs) {
                int i = r + d[0], j = c + d[1];
                boolean sawOpponent = false;
                while (i >= 0 && i < 8 && j >= 0 && j < 8) {
                    if (board[i][j] == opponent) sawOpponent = true;
                    else if (board[i][j] == color) {
                        if (sawOpponent) {
                            valid = true;
                            if (execute) {
                                int tr = r + d[0], tc = c + d[1];
                                while (tr != i || tc != j) {
                                    board[tr][tc] = color;
                                    tr += d[0]; tc += d[1];
                                }
                            }
                        }
                        break;
                    } else break;
                    i += d[0]; j += d[1];
                }
            }
            return valid;
        }

        private boolean hasValidMove(int color) {
            for(int i=0; i<8; i++) for(int j=0; j<8; j++) if(isValidMove(i, j, color, false)) return true;
            return false;
        }

        private boolean isFullBoard() {
            for(int[] row : board) for(int cell : row) if(cell == 0) return false;
            return true;
        }

        private int count(int c) {
            int n = 0;
            for(int[] row : board) for(int cell : row) if(cell == c) n++;
            return n;
        }

        // --- 正常結束 ---
        private void endGame() {
            int b = count(1), w = count(2);
            String winner = (b > w) ? "黑棋" : (w > b) ? "白棋" : "平手";
            String winnerName = (b > w) ? black.name : (w > b) ? white.name : "雙方";
            
            broadcast("GAME_OVER|" + winner + "獲勝 (" + winnerName + ")");
            
            // 廣播戰報
            String report = "戰報: " + black.name + " vs " + white.name + "，由 [" + winnerName + "] 獲勝！(黑:" + b + "/白:" + w + ")";
            ReversiServer.broadcastLobby("LOBBY_CHAT|系統|" + report);

            resetPlayers();
        }

        // --- 玩家投降/離開/斷線 ---
        public void playerExit(ClientHandler p) {
            if (!gameStarted) { 
                 resetPlayers();
                 return;
            }

            String loserName = p.name;
            // 如果走的是黑棋，那白棋贏；反之亦然
            ClientHandler winner = (p == black) ? white : black;
            String winnerName = (winner != null) ? winner.name : "對手";

            // 通知房間內
            broadcast("GAME_OVER|" + loserName + " 已投降/離開，" + winnerName + " 獲勝！");

            // 通知大廳 (系統廣播)
            String report = "戰報: " + loserName + " 投降了，[" + winnerName + "] 不戰而勝！";
            ReversiServer.broadcastLobby("LOBBY_CHAT|系統|" + report);

            resetPlayers();
        }

        private void resetPlayers() {
            if(black!=null) { black.isInGame=false; black.currentRoom=null; }
            if(white!=null) { white.isInGame=false; white.currentRoom=null; }
        }
    }
}
