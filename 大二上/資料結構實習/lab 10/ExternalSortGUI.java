import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.util.Random;

public class ExternalSortGUI extends JFrame {
    private JTextField fileNameField;
    private JTextField dataCountField;
    private JTextField arrayCapacityField;
    private JTextField minValueField;
    private JTextField maxValueField;
    private JTextArea resultArea;
    private JButton generateButton;
    private JButton sortButton;
    private JButton verifyButton;
    
    private String currentDataFile = "";
    private int currentDataCount = 100000;
    private int currentArrayCapacity = 10000;
    
    public ExternalSortGUI() {
        setTitle("外部排序系統 - External Sort Simulation");
        setSize(900, 700);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout(10, 10));
        
        // 建立上方面板（資料產生）
        JPanel topPanel = createTopPanel();
        add(topPanel, BorderLayout.NORTH);
        
        // 建立中間面板（結果顯示）
        JPanel centerPanel = createCenterPanel();
        add(centerPanel, BorderLayout.CENTER);
        
        // 建立下方面板（操作按鈕）
        JPanel bottomPanel = createBottomPanel();
        add(bottomPanel, BorderLayout.SOUTH);
        
        setLocationRelativeTo(null);
    }
    
    private JPanel createTopPanel() {
        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(6, 2, 10, 10));
        panel.setBorder(BorderFactory.createTitledBorder("資料產生設定"));
        
        panel.add(new JLabel("輸出檔名:"));
        fileNameField = new JTextField("data100k.txt");
        panel.add(fileNameField);
        
        panel.add(new JLabel("資料筆數:"));
        dataCountField = new JTextField("100000");
        panel.add(dataCountField);
        
        panel.add(new JLabel("陣列容量:"));
        arrayCapacityField = new JTextField("10000");
        panel.add(arrayCapacityField);
        
        panel.add(new JLabel("最小值:"));
        minValueField = new JTextField("0");
        panel.add(minValueField);
        
        panel.add(new JLabel("最大值:"));
        maxValueField = new JTextField("1000000");
        panel.add(maxValueField);
        
        generateButton = new JButton("產生資料");
        generateButton.addActionListener(e -> generateData());
        panel.add(generateButton);
        
        panel.add(new JLabel("")); // 空白
        
        return panel;
    }
    
    private JPanel createCenterPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBorder(BorderFactory.createTitledBorder("執行結果"));
        
        resultArea = new JTextArea();
        resultArea.setEditable(false);
        resultArea.setFont(new Font("Monospaced", Font.PLAIN, 12));
        JScrollPane scrollPane = new JScrollPane(resultArea);
        panel.add(scrollPane, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JPanel createBottomPanel() {
        JPanel panel = new JPanel(new FlowLayout());
        
        sortButton = new JButton("執行外部排序");
        sortButton.setEnabled(false);
        sortButton.addActionListener(e -> performSort());
        panel.add(sortButton);
        
        verifyButton = new JButton("驗證結果");
        verifyButton.setEnabled(false);
        verifyButton.addActionListener(e -> verifyResults());
        panel.add(verifyButton);
        
        JButton clearButton = new JButton("清除結果");
        clearButton.addActionListener(e -> resultArea.setText(""));
        panel.add(clearButton);
        
        return panel;
    }
    
    private void generateData() {
        try {
            String fileName = fileNameField.getText().trim();
            int dataCount = Integer.parseInt(dataCountField.getText().trim());
            int minValue = Integer.parseInt(minValueField.getText().trim());
            int maxValue = Integer.parseInt(maxValueField.getText().trim());
            
            currentDataFile = fileName;
            currentDataCount = dataCount;
            currentArrayCapacity = Integer.parseInt(arrayCapacityField.getText().trim());
            
            resultArea.append("正在產生資料...\n");
            resultArea.append("檔名: " + fileName + "\n");
            resultArea.append("資料筆數: " + dataCount + "\n");
            resultArea.append("數值範圍: [" + minValue + ", " + maxValue + "]\n");
            resultArea.append("陣列容量: " + currentArrayCapacity + "\n\n");
            
            // 檢查範圍是否足夠產生不重複的數字
            if (maxValue - minValue + 1 < dataCount) {
                JOptionPane.showMessageDialog(this,
                    "數值範圍不足！需要 " + dataCount + " 個不重複數字，\n" +
                    "但範圍 [" + minValue + ", " + maxValue + "] 只能提供 " + 
                    (maxValue - minValue + 1) + " 個數字。",
                    "錯誤",
                    JOptionPane.ERROR_MESSAGE);
                return;
            }
            
            resultArea.append("產生不重複的隨機數字...\n");
            
            // 建立包含所有數字的陣列
            int[] numbers = new int[dataCount];
            for (int i = 0; i < dataCount; i++) {
                numbers[i] = minValue + i;
            }
            
            // Fisher-Yates 洗牌演算法：隨機打亂陣列
            Random random = new Random();
            for (int i = dataCount - 1; i > 0; i--) {
                int j = random.nextInt(i + 1);
                // 交換 numbers[i] 和 numbers[j]
                int temp = numbers[i];
                numbers[i] = numbers[j];
                numbers[j] = temp;
            }
            
            // 寫入檔案
            PrintWriter writer = new PrintWriter(new FileWriter(fileName));
            for (int i = 0; i < dataCount; i++) {
                writer.println(numbers[i]);
            }
            writer.close();
            
            resultArea.append("資料產生完成！（每個數字唯一且隨機排列）\n");
            resultArea.append("========================================\n\n");
            
            sortButton.setEnabled(true);
            
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, 
                "資料產生失敗: " + ex.getMessage(), 
                "錯誤", 
                JOptionPane.ERROR_MESSAGE);
        }
    }
    
    private void performSort() {
        try {
            resultArea.append("開始執行外部排序...\n\n");
            
            // 編譯C程式
            resultArea.append("編譯C程式...\n");
            compileC();
            resultArea.append("編譯完成！\n\n");
            
            // 執行方法一：Merge Sort
            resultArea.append("執行方法一：基於 Merge Sort 的外部排序\n");
            resultArea.append("----------------------------------------\n");
            long time1 = executeMergeSort();
            
            // 執行方法二：Min-Heap
            resultArea.append("\n執行方法二：使用 Min-Heap 的外部排序\n");
            resultArea.append("----------------------------------------\n");
            long time2 = executeHeapSort();
            
            // 比較結果
            resultArea.append("\n========================================\n");
            resultArea.append("效能比較結果\n");
            resultArea.append("========================================\n");
            resultArea.append(String.format("方法一 (Merge Sort): %.2f 毫秒\n", time1 / 1000.0));
            resultArea.append(String.format("方法二 (Min-Heap):   %.2f 毫秒\n", time2 / 1000.0));
            resultArea.append("----------------------------------------\n");
            
            if (time1 > time2) {
                double ratio = (double) time1 / time2;
                double diff = (time1 - time2) / 1000.0;
                resultArea.append(String.format("Min-Heap 比 Merge Sort 快 %.2f 倍\n", ratio));
                resultArea.append(String.format("時間差異: %.2f 毫秒\n", diff));
            } else {
                double ratio = (double) time2 / time1;
                double diff = (time2 - time1) / 1000.0;
                resultArea.append(String.format("Merge Sort 比 Min-Heap 快 %.2f 倍\n", ratio));
                resultArea.append(String.format("時間差異: %.2f 毫秒\n", diff));
            }
            resultArea.append("========================================\n\n");
            
            verifyButton.setEnabled(true);
            
        } catch (Exception ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(this, 
                "排序執行失敗: " + ex.getMessage(), 
                "錯誤", 
                JOptionPane.ERROR_MESSAGE);
        }
    }
    
    private void compileC() throws Exception {
        // 編譯 Merge Sort 版本
        Process p1 = Runtime.getRuntime().exec(
            "gcc -o external_sort_merge external_sort_merge.c -lm");
        p1.waitFor();
        
        // 編譯 Heap 版本
        Process p2 = Runtime.getRuntime().exec(
            "gcc -o external_sort_heap external_sort_heap.c -lm");
        p2.waitFor();
    }
    
    private long executeMergeSort() throws Exception {
        Process process = Runtime.getRuntime().exec(
            "./external_sort_merge " + currentDataFile + " sorted_merge.dat");
        
        BufferedReader reader = new BufferedReader(
            new InputStreamReader(process.getInputStream()));
        String line;
        while ((line = reader.readLine()) != null) {
            resultArea.append(line + "\n");
        }
        process.waitFor();
        
        // 讀取時間
        BufferedReader timeReader = new BufferedReader(new FileReader("time_merge.txt"));
        String timeStr = timeReader.readLine();
        timeReader.close();
        
        return (long) (Double.parseDouble(timeStr) * 1000);
    }
    
    private long executeHeapSort() throws Exception {
        Process process = Runtime.getRuntime().exec(
            "./external_sort_heap " + currentDataFile + " sorted_heap.dat");
        
        BufferedReader reader = new BufferedReader(
            new InputStreamReader(process.getInputStream()));
        String line;
        while ((line = reader.readLine()) != null) {
            resultArea.append(line + "\n");
        }
        process.waitFor();
        
        // 讀取時間
        BufferedReader timeReader = new BufferedReader(new FileReader("time_heap.txt"));
        String timeStr = timeReader.readLine();
        timeReader.close();
        
        return (long) (Double.parseDouble(timeStr) * 1000);
    }
    
    private void verifyResults() {
        try {
            resultArea.append("\n驗證排序結果...\n");
            resultArea.append("========================================\n");
            
            // 驗證 Merge Sort 結果
            boolean valid1 = verifySortedFile("sorted_merge.dat");
            resultArea.append("方法一 (Merge Sort) 結果: " + 
                (valid1 ? "✓ 正確" : "✗ 錯誤") + "\n");
            
            // 驗證 Heap Sort 結果
            boolean valid2 = verifySortedFile("sorted_heap.dat");
            resultArea.append("方法二 (Min-Heap) 結果: " + 
                (valid2 ? "✓ 正確" : "✗ 錯誤") + "\n");
            
            // 比較兩個檔案是否相同
            boolean same = compareFiles("sorted_merge.dat", "sorted_heap.dat");
            resultArea.append("兩個結果檔案: " + 
                (same ? "✓ 完全相同" : "✗ 不同") + "\n");
            
            resultArea.append("========================================\n\n");
            
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, 
                "驗證失敗: " + ex.getMessage(), 
                "錯誤", 
                JOptionPane.ERROR_MESSAGE);
        }
    }
    
    private boolean verifySortedFile(String fileName) throws Exception {
        BufferedReader reader = new BufferedReader(new FileReader(fileName));
        String line;
        int prev = Integer.MIN_VALUE;
        int count = 0;
        
        while ((line = reader.readLine()) != null) {
            int curr = Integer.parseInt(line.trim());
            if (curr < prev) {
                reader.close();
                return false;
            }
            prev = curr;
            count++;
        }
        reader.close();
        
        // 確認資料筆數正確
        return count == currentDataCount;
    }
    
    private boolean compareFiles(String file1, String file2) throws Exception {
        BufferedReader r1 = new BufferedReader(new FileReader(file1));
        BufferedReader r2 = new BufferedReader(new FileReader(file2));
        
        String line1, line2;
        while ((line1 = r1.readLine()) != null) {
            line2 = r2.readLine();
            if (line2 == null || !line1.equals(line2)) {
                r1.close();
                r2.close();
                return false;
            }
        }
        
        line2 = r2.readLine();
        r1.close();
        r2.close();
        
        return line2 == null;
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            ExternalSortGUI gui = new ExternalSortGUI();
            gui.setVisible(true);
        });
    }
}
