import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.Socket;
import javax.swing.*;
import javax.swing.border.EmptyBorder;

public class ReversiClient extends JFrame {
    private Socket socket;
    private PrintWriter out;
    private BufferedReader in;
    private String myName;

    private CardLayout cardLayout = new CardLayout();
    private JPanel mainPanel = new JPanel(cardLayout);
    
    // 大廳元件
    private JTextArea lobbyChat = new JTextArea();
    private JTextField lobbyInput = new JTextField();
    
    // 遊戲元件
    private JButton[][] boardBtns = new JButton[8][8];
    private JLabel statusInfo = new JLabel("準備中...");
    private JLabel scoreInfo = new JLabel("黑: 2 | 白: 2");
    private JTextArea gameChat = new JTextArea();
    private JTextField gameInput = new JTextField();
    
    private int[][] localBoard = new int[8][8];
    private int myColor = 0; 
    private int turnColor = 0;

    // 狀態
    private JDialog waitingDialog; 

    public static void main(String[] args) {
        // try { UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName()); } catch(Exception e){}
        SwingUtilities.invokeLater(() -> new ReversiClient());
    }

    public ReversiClient() {
        setTitle("黑白棋大戰 (Java版)");
        setSize(1000, 750);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        initLobby();
        initGame();
        this.add(mainPanel);
        this.setVisible(true);
        connect();
    }

    private void initLobby() {
        JPanel lobby = new JPanel(new BorderLayout(10, 10));
        lobby.setBorder(new EmptyBorder(20, 20, 20, 20));
        
        JLabel title = new JLabel("黑白棋 - 遊戲大廳", SwingConstants.CENTER);
        title.setFont(new Font("微軟正黑體", Font.BOLD, 30));
        lobby.add(title, BorderLayout.NORTH);

        lobbyChat.setEditable(false);
        lobbyChat.setFont(new Font("Monospaced", Font.PLAIN, 16));
        lobby.add(new JScrollPane(lobbyChat), BorderLayout.CENTER);

        JPanel bottom = new JPanel(new BorderLayout(10, 0));
        
        JPanel inputPanel = new JPanel(new BorderLayout());
        inputPanel.add(lobbyInput, BorderLayout.CENTER);
        JButton sendBtn = new JButton("聊天發送");
        inputPanel.add(sendBtn, BorderLayout.EAST);
        
        JButton startBtn = new JButton("開始遊戲");
        startBtn.setFont(new Font("微軟正黑體", Font.BOLD, 24));
        startBtn.setBackground(new Color(255, 140, 0)); 
        startBtn.setForeground(Color.WHITE);
        startBtn.setOpaque(true);
        startBtn.setBorderPainted(false); 
        startBtn.setPreferredSize(new Dimension(0, 60));

        JPanel controlPanel = new JPanel(new BorderLayout(0, 10));
        controlPanel.add(inputPanel, BorderLayout.NORTH);
        controlPanel.add(startBtn, BorderLayout.SOUTH);

        bottom.add(controlPanel, BorderLayout.CENTER);
        lobby.add(bottom, BorderLayout.SOUTH);

        startBtn.addActionListener(e -> showStartGameMenu());
        
        ActionListener sendAction = e -> {
            if(!lobbyInput.getText().trim().isEmpty()){
                out.println("CHAT|" + lobbyInput.getText());
                lobbyInput.setText("");
            }
        };
        sendBtn.addActionListener(sendAction);
        lobbyInput.addActionListener(sendAction);

        mainPanel.add(lobby, "LOBBY");
    }

    private void showStartGameMenu() {
        Object[] options = {"隨機匹配", "創建房間", "加入房間"};
        int n = JOptionPane.showOptionDialog(this,
                "請選擇遊戲模式",
                "開始遊戲",
                JOptionPane.YES_NO_CANCEL_OPTION,
                JOptionPane.QUESTION_MESSAGE,
                null,
                options,
                options[0]);

        if (n == 0) { 
            out.println("MATCH_RANDOM");
        } else if (n == 1) { 
            out.println("CREATE_ROOM");
        } else if (n == 2) { 
            String roomId = JOptionPane.showInputDialog(this, "請輸入 4 位數房號:");
            if (roomId != null && roomId.matches("\\d{4}")) {
                out.println("JOIN_ROOM|" + roomId);
            } else if (roomId != null) {
                JOptionPane.showMessageDialog(this, "格式錯誤，請輸入 4 位數字");
            }
        }
    }

    private void initGame() {
        JPanel game = new JPanel(new BorderLayout(5, 5));
        
        // --- 修正處：使用間距 (Gap) 來製造格線 ---
        // 8x8 格子，水平間距 2，垂直間距 2
        JPanel boardPanel = new JPanel(new GridLayout(8, 8, 2, 2));
        // 底板設為黑色，這樣間距就會顯示出黑色線條
        boardPanel.setBackground(Color.BLACK);
        // 外框也設為黑色
        boardPanel.setBorder(BorderFactory.createLineBorder(Color.BLACK, 2));
        boardPanel.setPreferredSize(new Dimension(640, 640));

        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                JButton btn = new JButton();
                
                // --- 按鈕外觀設定 ---
                btn.setBackground(new Color(210, 180, 140)); // 淺棕色 (Tan)
                btn.setOpaque(true);
                // 不畫按鈕的邊框，改由 GridLayout 的間距來呈現格線
                btn.setBorderPainted(false); 
                // 關鍵：取消對焦狀態，避免出現藍色/白色框框
                btn.setFocusable(false); 
                // ----------------
                
                final int r = i;
                final int c = j;
                btn.addActionListener(e -> {
                    if (myColor == turnColor && isValidMove(r, c, myColor)) {
                        out.println("MOVE|" + r + "|" + c);
                    }
                });
                boardBtns[i][j] = btn;
                boardPanel.add(btn);
            }
        }
        game.add(boardPanel, BorderLayout.CENTER);

        JPanel sidePanel = new JPanel(new BorderLayout());
        sidePanel.setPreferredSize(new Dimension(300, 0));
        sidePanel.setBorder(new EmptyBorder(10, 10, 10, 10));

        JPanel infoBox = new JPanel(new GridLayout(4, 1));
        statusInfo.setFont(new Font("微軟正黑體", Font.BOLD, 18));
        scoreInfo.setFont(new Font("微軟正黑體", Font.PLAIN, 16));
        JButton exitBtn = new JButton("投降 / 離開");
        
        infoBox.add(new JLabel("--- 對戰資訊 ---"));
        infoBox.add(statusInfo);
        infoBox.add(scoreInfo);
        infoBox.add(exitBtn);
        sidePanel.add(infoBox, BorderLayout.NORTH);

        gameChat.setEditable(false);
        sidePanel.add(new JScrollPane(gameChat), BorderLayout.CENTER);

        JPanel chatInputPanel = new JPanel(new BorderLayout());
        chatInputPanel.add(gameInput, BorderLayout.CENTER);
        JButton gameSendBtn = new JButton("送出");
        chatInputPanel.add(gameSendBtn, BorderLayout.EAST);
        sidePanel.add(chatInputPanel, BorderLayout.SOUTH);

        game.add(sidePanel, BorderLayout.EAST);

        exitBtn.addActionListener(e -> {
            if(JOptionPane.showConfirmDialog(this, "確定要離開遊戲嗎？(將視為投降)") == JOptionPane.YES_OPTION) {
                out.println("EXIT");
            }
        });
        
        ActionListener chatAction = e -> {
            if(!gameInput.getText().trim().isEmpty()){
                out.println("CHAT|" + gameInput.getText());
                gameInput.setText("");
            }
        };
        gameSendBtn.addActionListener(chatAction);
        gameInput.addActionListener(chatAction);

        mainPanel.add(game, "GAME");
    }

    private void connect() {
        myName = JOptionPane.showInputDialog(this, "請輸入你的暱稱:", "登入", JOptionPane.QUESTION_MESSAGE);
        if (myName == null || myName.trim().isEmpty()) System.exit(0);

        try {
            socket = new Socket("localhost", 8888);
            out = new PrintWriter(socket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out.println("LOGIN|" + myName);
            new Thread(this::listen).start();
        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, "連線失敗");
            System.exit(0);
        }
    }

    private void listen() {
        try {
            String line;
            while ((line = in.readLine()) != null) {
                String[] parts = line.split("\\|");
                String type = parts[0];
                
                SwingUtilities.invokeLater(() -> {
                    switch (type) {
                        case "LOBBY_CHAT":
                            lobbyChat.append(parts[1] + ": " + parts[2] + "\n");
                            break;
                        case "ROOM_CREATED": 
                            showWaitingDialog(parts[1]);
                            break;
                        case "ERROR":
                            JOptionPane.showMessageDialog(this, parts[1]);
                            break;
                        case "START":
                            if(waitingDialog != null) waitingDialog.dispose(); 
                            myColor = parts[1].equals("BLACK") ? 1 : 2;
                            statusInfo.setText("你是: " + (myColor==1?"黑棋":"白棋"));
                            gameChat.setText("系統: 遊戲開始！\n");
                            cardLayout.show(mainPanel, "GAME");
                            break;
                        case "UPDATE": 
                            parseBoard(parts[1]);
                            turnColor = Integer.parseInt(parts[2]);
                            scoreInfo.setText("黑: " + parts[3] + "  |  白: " + parts[4]);
                            refreshBoardUI(); 
                            if (turnColor == myColor) {
                                statusInfo.setText("輪到你了！(" + (myColor==1?"黑":"白") + ")");
                                statusInfo.setForeground(Color.RED);
                            } else {
                                statusInfo.setText("對手思考中...");
                                statusInfo.setForeground(Color.BLACK);
                            }
                            break;
                        case "MSG_PASS":
                            JOptionPane.showMessageDialog(this, parts[1] + " 無子可下，Pass！");
                            break;
                        case "GAME_CHAT":
                            gameChat.append(parts[1] + ": " + parts[2] + "\n");
                            break;
                        case "GAME_OVER":
                            JOptionPane.showMessageDialog(this, "遊戲結束: " + parts[1]);
                            cardLayout.show(mainPanel, "LOBBY");
                            break;
                        case "FORCE_LOBBY":
                            if(waitingDialog != null) waitingDialog.dispose();
                            cardLayout.show(mainPanel, "LOBBY");
                            break;
                    }
                });
            }
        } catch (IOException e) { e.printStackTrace(); }
    }

    private void showWaitingDialog(String roomId) {
        JOptionPane pane = new JOptionPane("房間已建立，房號：" + roomId + "\n等待對手加入...", 
                                           JOptionPane.INFORMATION_MESSAGE, 
                                           JOptionPane.DEFAULT_OPTION, null, new Object[]{}, null);
        waitingDialog = pane.createDialog(this, "等待中");
        waitingDialog.setModal(false); 
        waitingDialog.setVisible(true);
    }

    private void parseBoard(String boardStr) {
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                localBoard[i][j] = boardStr.charAt(i * 8 + j) - '0';
            }
        }
    }

    private void refreshBoardUI() {
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                int val = localBoard[i][j];
                JButton btn = boardBtns[i][j];
                
                // 刷新時保持顏色
                btn.setBackground(new Color(210, 180, 140)); 
                
                if (val == 1) {
                    btn.setIcon(new PieceIcon(Color.BLACK));
                } else if (val == 2) {
                    btn.setIcon(new PieceIcon(Color.WHITE));
                } else {
                    if (myColor == turnColor && isValidMove(i, j, myColor)) {
                        btn.setIcon(new HintIcon());
                    } else {
                        btn.setIcon(null);
                    }
                }
            }
        }
    }

    private boolean isValidMove(int r, int c, int color) {
        if (localBoard[r][c] != 0) return false;
        int opponent = (color == 1) ? 2 : 1;
        boolean valid = false;
        int[][] dirs = {{-1,0},{1,0},{0,-1},{0,1},{-1,-1},{-1,1},{1,-1},{1,1}};

        for (int[] d : dirs) {
            int i = r + d[0], j = c + d[1];
            boolean sawOpponent = false;
            while (i >= 0 && i < 8 && j >= 0 && j < 8) {
                if (localBoard[i][j] == opponent) sawOpponent = true;
                else if (localBoard[i][j] == color) {
                    if (sawOpponent) valid = true;
                    break;
                } else break;
                i += d[0]; j += d[1];
            }
            if (valid) return true;
        }
        return false;
    }

    class PieceIcon implements Icon {
        Color color;
        public PieceIcon(Color c) { this.color = c; }
        public int getIconWidth() { return 50; }
        public int getIconHeight() { return 50; }
        public void paintIcon(Component c, Graphics g, int x, int y) {
            Graphics2D g2 = (Graphics2D) g;
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g2.setColor(color);
            g2.fillOval(x+5, y+5, 40, 40);
            g2.setColor(new Color(255,255,255,50));
            g2.fillOval(x+10, y+10, 15, 15);
            g2.setColor(Color.DARK_GRAY);
            g2.drawOval(x+5, y+5, 40, 40);
        }
    }

    class HintIcon implements Icon {
        public int getIconWidth() { return 50; }
        public int getIconHeight() { return 50; }
        public void paintIcon(Component c, Graphics g, int x, int y) {
            Graphics2D g2 = (Graphics2D) g;
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g2.setColor(new Color(0, 0, 0, 50));
            g2.fillOval(x+20, y+20, 10, 10);
        }
    }
}