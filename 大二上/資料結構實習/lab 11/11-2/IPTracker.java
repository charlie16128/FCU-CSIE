import javax.swing.*;
import java.awt.*;
import java.io.PrintWriter;
import java.util.Random;
import java.util.Scanner;

public class IPTracker extends JFrame {

    private boolean isRunning = false;
    private Thread workerThread;
    private Random random = new Random();

    // IPC 通訊變數
    private Process cProcess;
    private PrintWriter cInput;
    private Scanner cOutput;

    // 限制 IP 總數不超過 10,000
    private String[] ipPool = new String[10000];
    private boolean isPoolInitialized = false;

    // 計時相關變數
    private long systemStartTime = 0; // 記錄開始時間

    // GUI 元件
    private JLabel lblSeqTime, lblHashTime, lblDiff, lblTotalDiff, lblSpeedup;
    private JLabel lblElapsedTime; // 新增：顯示執行時間
    private JTextArea logArea;
    private long totalSeqTime = 0;
    private long totalHashTime = 0;
    private int requestCount = 0;

    public IPTracker() {
        setTitle("Lab 11-2: IP Hash Experiment (Optimized)");
        setSize(600, 500); //稍微加高視窗高度以容納新標籤
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // --- 上方控制區 ---
        JPanel controlPanel = new JPanel();
        JButton btnStart = new JButton("Start");
        JButton btnStop = new JButton("Stop");
        controlPanel.add(btnStart);
        controlPanel.add(btnStop);
        add(controlPanel, BorderLayout.NORTH);

        // --- 中間數據區 ---
        // 改為 6 列 2 行，多一列給執行時間
        JPanel statsPanel = new JPanel(new GridLayout(6, 2)); 
        statsPanel.setBorder(BorderFactory.createTitledBorder("Performance Metrics"));
        
        lblSeqTime = new JLabel("0 ns");
        lblHashTime = new JLabel("0 ns");
        lblDiff = new JLabel("0 ns");
        lblTotalDiff = new JLabel("0 ns");
        lblSpeedup = new JLabel("0.00x");
        lblElapsedTime = new JLabel("0 s"); // 初始化

        statsPanel.add(new JLabel("Elapsed Time:")); // 新增標籤
        statsPanel.add(lblElapsedTime);              // 新增數值顯示

        statsPanel.add(new JLabel("Sequential Search Time:"));
        statsPanel.add(lblSeqTime);
        statsPanel.add(new JLabel("Hash Search Time:"));
        statsPanel.add(lblHashTime);
        statsPanel.add(new JLabel("Difference (Seq - Hash):"));
        statsPanel.add(lblDiff);
        statsPanel.add(new JLabel("Total Time Difference (Cumulative):"));
        statsPanel.add(lblTotalDiff);
        statsPanel.add(new JLabel("Total Speedup (Seq / Hash):"));
        statsPanel.add(lblSpeedup);

        add(statsPanel, BorderLayout.CENTER);

        // --- 下方記錄區 ---
        logArea = new JTextArea(10, 40);
        add(new JScrollPane(logArea), BorderLayout.SOUTH);

        // 按鈕事件
        btnStart.addActionListener(e -> startSystem());
        btnStop.addActionListener(e -> stopSystem());

        // 視窗關閉時清理
        addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(java.awt.event.WindowEvent e) {
                stopSystem();
            }
        });
    }

    private void startSystem() {
        if (isRunning) return;

        // 1. 初始化 IP 池
        if (!isPoolInitialized) {
            logArea.append("Initializing IP Pool (10,000 items)...\n");
            for (int i = 0; i < 10000; i++) {
                ipPool[i] = "140." + random.nextInt(256) + "." + 
                                     random.nextInt(256) + "." + 
                                     random.nextInt(256);
            }
            isPoolInitialized = true;
        }

        try {
            // 2. 啟動 C 程式
            ProcessBuilder pb = new ProcessBuilder("ip_search.exe"); 
            cProcess = pb.start();
            
            cInput = new PrintWriter(cProcess.getOutputStream(), true);
            cOutput = new Scanner(cProcess.getInputStream());
            
            logArea.append("Connected to C module. Starting benchmark...\n");

        } catch (Exception e) {
            logArea.append("Error: " + e.getMessage() + "\n");
            logArea.append("Check if 'ip_search.exe' exists in the folder!\n");
            return;
        }

        isRunning = true;
        totalSeqTime = 0;
        totalHashTime = 0;
        requestCount = 0;
        
        // ★★★ 記錄開始時間 ★★★
        systemStartTime = System.currentTimeMillis();

        // 3. 啟動執行緒
        workerThread = new Thread(() -> {
            while (isRunning && cProcess.isAlive()) {
                try {
                    String ip = ipPool[random.nextInt(10000)];
                    cInput.println(ip);

                    if (cOutput.hasNextLong()) {
                        long seqTime = cOutput.nextLong();
                        long hashTime = cOutput.nextLong();
                        updateStats(ip, seqTime, hashTime);
                    }

                    Thread.sleep(5); 

                } catch (Exception ex) {
                    // 忽略
                }
            }
        });
        workerThread.start();
    }

    private void stopSystem() {
        isRunning = false;
        if (cProcess != null && cProcess.isAlive()) {
            cInput.println("EXIT");
            cProcess.destroy();
            logArea.append("System Stopped.\n");
            
            double speedup = (totalHashTime == 0) ? 0 : (double) totalSeqTime / totalHashTime;
            // 停止時也計算最後一次總秒數
            long elapsedSeconds = (System.currentTimeMillis() - systemStartTime) / 1000;
            logArea.append(String.format("Total Run Time: %d s | Final Speedup: %.2fx\n", elapsedSeconds, speedup));
        }
    }

    private void updateStats(String ip, long seqTime, long hashTime) {
        SwingUtilities.invokeLater(() -> {
            totalSeqTime += seqTime;
            totalHashTime += hashTime;
            requestCount++;

            // ★★★ 計算經過時間 (秒) ★★★
            long currentElapsed = (System.currentTimeMillis() - systemStartTime) / 1000;
            lblElapsedTime.setText(currentElapsed + " s");

            lblSeqTime.setText(seqTime + " ns");
            lblHashTime.setText(hashTime + " ns");
            lblDiff.setText((seqTime - hashTime) + " ns");
            lblTotalDiff.setText((totalSeqTime - totalHashTime) + " ns");
            
            double speedup = (totalHashTime == 0) ? 0 : (double) totalSeqTime / totalHashTime;
            lblSpeedup.setText(String.format("%.2fx", speedup));

            if (requestCount % 100 == 0) {
                logArea.append("Processed " + requestCount + " requests. Time: " + currentElapsed + "s. Speedup: " + String.format("%.2f", speedup) + "x\n");
                logArea.setCaretPosition(logArea.getDocument().getLength());
            }
        });
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new IPTracker().setVisible(true));
    }
}