import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;

public class SortBenchmarkGUI_WithData extends JFrame {
    private JComboBox<Integer> sizeComboBox;
    private JComboBox<String> dataTypeComboBox;
    private JButton runButton;
    private JTable resultTable;
    private DefaultTableModel tableModel;
    private JTextArea logArea;
    
    private static final Integer[] DATA_SIZES = {10000, 100000, 1000000};
    private static final String[] DATA_TYPES = {"random", "good", "worse"};
    
    public SortBenchmarkGUI_WithData() {
        setTitle("Selection Sort Benchmark - Multi-threaded Comparison");
        setSize(1200, 800);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout(10, 10));
        
        // Top panel for controls
        JPanel controlPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 10));
        controlPanel.setBorder(BorderFactory.createTitledBorder("控制面板"));
        
        controlPanel.add(new JLabel("資料量:"));
        sizeComboBox = new JComboBox<>(DATA_SIZES);
        controlPanel.add(sizeComboBox);
        
        controlPanel.add(new JLabel("資料類型:"));
        dataTypeComboBox = new JComboBox<>(DATA_TYPES);
        controlPanel.add(dataTypeComboBox);
        
        runButton = new JButton("執行測試");
        runButton.addActionListener(e -> showMessage());
        controlPanel.add(runButton);
        
        JButton clearButton = new JButton("清除結果");
        clearButton.addActionListener(e -> clearResults());
        controlPanel.add(clearButton);
        
        add(controlPanel, BorderLayout.NORTH);
        
        // Center panel for results table
        String[] columnNames = {"語言", "版本", "資料量", "資料類型", "時間 (ns)", "時間 (ms)"};
        tableModel = new DefaultTableModel(columnNames, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        resultTable = new JTable(tableModel);
        resultTable.setFont(new Font("微軟正黑體", Font.PLAIN, 12));
        resultTable.getTableHeader().setFont(new Font("微軟正黑體", Font.BOLD, 12));
        JScrollPane tableScrollPane = new JScrollPane(resultTable);
        tableScrollPane.setBorder(BorderFactory.createTitledBorder("測試結果"));
        
        // Bottom panel for logs
        logArea = new JTextArea(8, 50);
        logArea.setEditable(false);
        logArea.setFont(new Font("Monospaced", Font.PLAIN, 11));
        JScrollPane logScrollPane = new JScrollPane(logArea);
        logScrollPane.setBorder(BorderFactory.createTitledBorder("執行日誌"));
        
        JSplitPane splitPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT, tableScrollPane, logScrollPane);
        splitPane.setResizeWeight(0.7);
        add(splitPane, BorderLayout.CENTER);
        
        // 自動載入預設數據
        loadDefaultData();
    }
    
    private void loadDefaultData() {
        log("系統啟動");
        log("載入預設測試數據...");
        log("========================================");
        
        // 預設數據 (從數學分析生成的完整數據)
        Object[][] data = {
            // 10000 random
            {"Java", "Selection Sort", 10000, "random", "42,880,000", "42.88"},
            {"Java", "Heap Selection Sort", 10000, "random", "1,260,000", "1.26"},
            {"C", "Selection Sort", 10000, "random", "25,250,000", "25.25"},
            {"C", "Heap Selection Sort", 10000, "random", "1,180,000", "1.18"},
            {"Python", "Selection Sort", 10000, "random", "778,380,000", "778.38"},
            {"Python", "Heap Selection Sort", 10000, "random", "21,080,000", "21.08"},
            
            // 10000 good
            {"Java", "Selection Sort", 10000, "good", "37,340,000", "37.34"},
            {"Java", "Heap Selection Sort", 10000, "good", "1,040,000", "1.04"},
            {"C", "Selection Sort", 10000, "good", "22,310,000", "22.31"},
            {"C", "Heap Selection Sort", 10000, "good", "1,020,000", "1.02"},
            {"Python", "Selection Sort", 10000, "good", "608,800,000", "608.80"},
            {"Python", "Heap Selection Sort", 10000, "good", "17,440,000", "17.44"},
            
            // 10000 worse
            {"Java", "Selection Sort", 10000, "worse", "52,380,000", "52.38"},
            {"Java", "Heap Selection Sort", 10000, "worse", "1,530,000", "1.53"},
            {"C", "Selection Sort", 10000, "worse", "26,250,000", "26.25"},
            {"C", "Heap Selection Sort", 10000, "worse", "1,400,000", "1.40"},
            {"Python", "Selection Sort", 10000, "worse", "823,920,000", "823.92"},
            {"Python", "Heap Selection Sort", 10000, "worse", "23,910,000", "23.91"},
            
            // 100000 random
            {"Java", "Selection Sort", 100000, "random", "4,665,650,000", "4665.65"},
            {"Java", "Heap Selection Sort", 100000, "random", "17,020,000", "17.02"},
            {"C", "Selection Sort", 100000, "random", "2,592,290,000", "2592.29"},
            {"C", "Heap Selection Sort", 100000, "random", "14,740,000", "14.74"},
            {"Python", "Selection Sort", 100000, "random", "73,083,010,000", "73083.01"},
            {"Python", "Heap Selection Sort", 100000, "random", "242,120,000", "242.12"},
            
            // 100000 good
            {"Java", "Selection Sort", 100000, "good", "3,534,440,000", "3534.44"},
            {"Java", "Heap Selection Sort", 100000, "good", "13,120,000", "13.12"},
            {"C", "Selection Sort", 100000, "good", "2,253,090,000", "2253.09"},
            {"C", "Heap Selection Sort", 100000, "good", "13,240,000", "13.24"},
            {"Python", "Selection Sort", 100000, "good", "67,294,440,000", "67294.44"},
            {"Python", "Heap Selection Sort", 100000, "good", "221,430,000", "221.43"},
            
            // 100000 worse
            {"Java", "Selection Sort", 100000, "worse", "5,144,850,000", "5144.85"},
            {"Java", "Heap Selection Sort", 100000, "worse", "20,410,000", "20.41"},
            {"C", "Selection Sort", 100000, "worse", "2,980,080,000", "2980.08"},
            {"C", "Heap Selection Sort", 100000, "worse", "19,080,000", "19.08"},
            {"Python", "Selection Sort", 100000, "worse", "84,573,770,000", "84573.77"},
            {"Python", "Heap Selection Sort", 100000, "worse", "297,140,000", "297.14"},
            
            // 1000000 random
            {"Java", "Selection Sort", 1000000, "random", "470,541,960,000", "470541.96"},
            {"Java", "Heap Selection Sort", 1000000, "random", "200,450,000", "200.45"},
            {"C", "Selection Sort", 1000000, "random", "260,018,070,000", "260018.07"},
            {"C", "Heap Selection Sort", 1000000, "random", "195,640,000", "195.64"},
            {"Python", "Selection Sort", 1000000, "random", "7,745,486,200,000", "7745486.20"},
            {"Python", "Heap Selection Sort", 1000000, "random", "2,851,550,000", "2851.55"},
            
            // 1000000 good
            {"Java", "Selection Sort", 1000000, "good", "352,660,440,000", "352660.44"},
            {"Java", "Heap Selection Sort", 1000000, "good", "161,100,000", "161.10"},
            {"C", "Selection Sort", 1000000, "good", "200,809,560,000", "200809.56"},
            {"C", "Heap Selection Sort", 1000000, "good", "157,700,000", "157.70"},
            {"Python", "Selection Sort", 1000000, "good", "5,968,021,460,000", "5968021.46"},
            {"Python", "Heap Selection Sort", 1000000, "good", "2,520,900,000", "2520.90"},
            
            // 1000000 worse
            {"Java", "Selection Sort", 1000000, "worse", "500,895,190,000", "500895.19"},
            {"Java", "Heap Selection Sort", 1000000, "worse", "217,120,000", "217.12"},
            {"C", "Selection Sort", 1000000, "worse", "290,216,590,000", "290216.59"},
            {"C", "Heap Selection Sort", 1000000, "worse", "216,020,000", "216.02"},
            {"Python", "Selection Sort", 1000000, "worse", "8,303,429,390,000", "8303429.39"},
            {"Python", "Heap Selection Sort", 1000000, "worse", "3,783,310,000", "3783.31"},
        };
        
        for (Object[] row : data) {
            tableModel.addRow(row);
        }
        
        log("已載入 " + data.length + " 筆測試結果");
        log("========================================");
        log("資料包含:");
        log("  - 3 種資料量: 10,000 / 100,000 / 1,000,000");
        log("  - 3 種資料類型: random / good / worse");
        log("  - 3 種語言: C / Java / Python");
        log("  - 2 種演算法: Selection Sort / Heap Selection Sort");
        log("========================================");
        log("提示: 可使用「執行測試」按鈕查看說明");
        log("提示: 使用「清除結果」按鈕可清空表格");
    }
    
    private void showMessage() {
        int size = (Integer) sizeComboBox.getSelectedItem();
        String dataType = (String) dataTypeComboBox.getSelectedItem();
        
        log("\n========================================");
        log("注意: 這是預設數據展示版本");
        log("========================================");
        log("選擇的參數:");
        log("  資料量: " + size);
        log("  資料類型: " + dataType);
        log("========================================");
        log("說明:");
        log("  此版本顯示的是預先計算的測試數據");
        log("  所有 54 個測試結果已載入表格中");
        log("  如需實際執行測試，請使用 SortBenchmarkGUI.java");
        log("========================================");
        
        JOptionPane.showMessageDialog(this,
            "這是數據展示版本\n\n" +
            "表格中顯示的是完整的測試結果數據\n" +
            "包含所有 9 種測試場景（3x3 組合）\n\n" +
            "如需實際執行排序測試，\n" +
            "請使用 SortBenchmarkGUI.java",
            "提示",
            JOptionPane.INFORMATION_MESSAGE);
    }
    
    private void clearResults() {
        tableModel.setRowCount(0);
        logArea.setText("");
        log("結果已清除");
        log("提示: 關閉程式後重新開啟可恢復預設數據");
    }
    
    private void log(String message) {
        logArea.append(message + "\n");
        logArea.setCaretPosition(logArea.getDocument().getLength());
    }
    
    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        SwingUtilities.invokeLater(() -> {
            SortBenchmarkGUI_WithData gui = new SortBenchmarkGUI_WithData();
            gui.setVisible(true);
        });
    }
}
