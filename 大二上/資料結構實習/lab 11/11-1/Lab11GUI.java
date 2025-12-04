import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Lab11GUI extends JFrame {

    private JTextArea logArea;
    private JTable resultTable;
    private DefaultTableModel resultModel;
    private JTable dataTable; // 新增：顯示資料用的表格
    private DefaultTableModel dataModel;
    private JButton btnGenerate;
    private JButton btnRun;

    private static final String C_PROGRAM_NAME = "search_lab"; 
    private static final String DATA_FILE = "data.csv";

    public Lab11GUI() {
        setTitle("Lab 11-1: 搜尋演算法效能比較");
        setSize(900, 700);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // --- 上方控制區 ---
        JPanel controlPanel = new JPanel();
        btnGenerate = new JButton("1. 產生 100 萬筆資料");
        btnRun = new JButton("2. 執行搜尋測試 (C語言)");
        btnRun.setEnabled(false); // 預設不能按

        controlPanel.add(btnGenerate);
        controlPanel.add(btnRun);
        add(controlPanel, BorderLayout.PAGE_START);

        // --- 中央顯示區 (使用 Tab 分頁) ---
        JTabbedPane tabbedPane = new JTabbedPane();

        // 分頁 1: 效能結果
        String[] resCols = {"演算法", "情境", "平均時間 (ns)", "與線性比較 (倍數)"};
        resultModel = new DefaultTableModel(resCols, 0);
        resultTable = new JTable(resultModel);
        resultTable.setRowHeight(25);
        resultTable.setFont(new Font("SansSerif", Font.PLAIN, 14));
        tabbedPane.addTab("效能比較結果", new JScrollPane(resultTable));

        // 分頁 2: 資料預覽 (新增功能)
        String[] dataCols = {"交易代碼 (ID)", "日期", "客戶代碼", "物品名稱", "價格"};
        dataModel = new DefaultTableModel(dataCols, 0);
        dataTable = new JTable(dataModel);
        tabbedPane.addTab("資料預覽 (前 100 筆)", new JScrollPane(dataTable));

        add(tabbedPane, BorderLayout.CENTER);

        // --- 底部 Log 區 ---
        logArea = new JTextArea(6, 50);
        logArea.setEditable(false);
        JScrollPane logScroll = new JScrollPane(logArea);
        logScroll.setBorder(BorderFactory.createTitledBorder("系統訊息"));
        add(logScroll, BorderLayout.SOUTH);

        // --- 事件綁定 ---
        btnGenerate.addActionListener(e -> generateData());
        btnRun.addActionListener(e -> runCBenchmark());
    }

    private void log(String msg) {
        SwingUtilities.invokeLater(() -> {
            logArea.append(msg + "\n");
            logArea.setCaretPosition(logArea.getDocument().getLength());
        });
    }

    private void generateData() {
        new Thread(() -> {
            btnGenerate.setEnabled(false);
            log("正在產生資料，請稍候...");
            
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(DATA_FILE))) {
                Random rand = new Random();
                long currentId = 100000;
                
                // 清空預覽表格
                SwingUtilities.invokeLater(() -> dataModel.setRowCount(0));

                for (int i = 0; i < 1000000; i++) {
                    currentId += (rand.nextInt(5) + 1); // 確保 ID 遞增且不重複 (適合插補搜尋)
                    
                    String date = "2025-12-04";
                    String custId = "C" + (1000 + rand.nextInt(9000));
                    String item = "Item-" + rand.nextInt(500);
                    double price = 10 + rand.nextDouble() * 990;

                    String line = String.format("%d,%s,%s,%s,%.2f", currentId, date, custId, item, price);
                    writer.write(line);
                    writer.newLine();

                    // 只顯示前 100 筆到 GUI 以免卡頓
                    if (i < 100) {
                        final String[] rowData = {String.valueOf(currentId), date, custId, item, String.format("%.2f", price)};
                        SwingUtilities.invokeLater(() -> dataModel.addRow(rowData));
                    }
                }
                
                log("資料產生完成！(已儲存為 data.csv)");
                log("前 100 筆資料已顯示在「資料預覽」分頁中。");
                btnGenerate.setEnabled(true);
                btnRun.setEnabled(true);

            } catch (IOException ex) {
                log("錯誤: " + ex.getMessage());
                ex.printStackTrace();
            }
        }).start();
    }

    private void runCBenchmark() {
        new Thread(() -> {
            log("正在啟動 C 程式進行運算...");
            log("由於快速搜尋演算法需要重複執行數十萬次以求精確時間，請耐心等待約 3-5 秒...");
            
            SwingUtilities.invokeLater(() -> resultModel.setRowCount(0));

            try {
                // 判斷作業系統
                String os = System.getProperty("os.name").toLowerCase();
                String exeName = os.contains("win") ? C_PROGRAM_NAME + ".exe" : "./" + C_PROGRAM_NAME;
                
                File exeFile = new File(os.contains("win") ? C_PROGRAM_NAME + ".exe" : C_PROGRAM_NAME);
                if (!exeFile.exists()) {
                    log("錯誤：找不到 C 執行檔！");
                    log("請務必先編譯 C 程式：gcc search_lab.c -o search_lab");
                    return;
                }

                ProcessBuilder pb = new ProcessBuilder(exeName);
                pb.redirectErrorStream(true); // 合併錯誤輸出
                Process process = pb.start();

                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line;
                
                double linearExistTime = 0;
                double linearNotExistTime = 0;

                while ((line = reader.readLine()) != null) {
                    if (line.startsWith("ERROR") || line.contains("Error")) {
                        log("C 程式錯誤: " + line);
                        continue;
                    }
                    
                    // 解析輸出: Name Time1 Time2
                    String[] parts = line.split(" ");
                    if (parts.length >= 3) {
                        String algo = parts[0];
                        try {
                            double tExist = Double.parseDouble(parts[1]);
                            double tNotExist = Double.parseDouble(parts[2]);
                            
                            if (algo.equals("Linear")) {
                                linearExistTime = tExist;
                                linearNotExistTime = tNotExist;
                            }

                            // 計算倍數
                            String diffExist = (linearExistTime > 0) ? String.format("%.1f X", linearExistTime / tExist) : "-";
                            String diffNotExist = (linearNotExistTime > 0) ? String.format("%.1f X", linearNotExistTime / tNotExist) : "-";

                            // 如果倍數是 1.0 (自己比自己)，顯示基準
                            if (algo.equals("Linear")) {
                                diffExist = "(基準)";
                                diffNotExist = "(基準)";
                            }

                            // 更新 GUI
                            final String r1 = algo;
                            final String r2 = String.format("%.2f", tExist);
                            final String r3 = diffExist;
                            final String r4 = String.format("%.2f", tNotExist);
                            final String r5 = diffNotExist;
                            
                            SwingUtilities.invokeLater(() -> {
                                resultModel.addRow(new Object[]{r1, "Key 存在", r2, r3});
                                resultModel.addRow(new Object[]{r1, "Key 不存在", r4, r5});
                            });
                            
                        } catch (NumberFormatException e) {
                            log("解析錯誤: " + line); // 忽略非數據行
                        }
                    } else {
                        // 顯示 Debug 訊息 (如果有的話)
                         // log("C Message: " + line);
                    }
                }
                
                process.waitFor();
                log("測試完成！請查看「效能比較結果」分頁。");

            } catch (Exception ex) {
                log("執行失敗: " + ex.getMessage());
            }
        }).start();
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new Lab11GUI().setVisible(true));
    }
}