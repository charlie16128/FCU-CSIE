import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.*;
import java.util.*;
import java.util.concurrent.*;

public class SortBenchmarkGUI extends JFrame {
    private JComboBox<Integer> sizeComboBox;
    private JComboBox<String> dataTypeComboBox;
    private JButton runButton;
    private JTable resultTable;
    private DefaultTableModel tableModel;
    private JTextArea logArea;
    private ExecutorService executorService;
    
    private static final Integer[] DATA_SIZES = {10000, 100000, 1000000};
    private static final String[] DATA_TYPES = {"random", "good", "worse"};
    
    public SortBenchmarkGUI() {
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
        runButton.addActionListener(e -> runBenchmark());
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
        
        executorService = Executors.newFixedThreadPool(6);
        
        // Compile C programs on startup
        compilePrograms();
    }
    
    private void compilePrograms() {
        log("正在編譯 C 程式...");
        try {
            Process p1 = Runtime.getRuntime().exec("gcc -o selection_sort_v2 selection_sort_v2.c");
            p1.waitFor();
            Process p2 = Runtime.getRuntime().exec("gcc -o heap_selection_sort_v2 heap_selection_sort_v2.c");
            p2.waitFor();
            log("C 程式編譯完成");
        } catch (Exception e) {
            log("警告: C 程式編譯失敗 - " + e.getMessage());
        }
    }
    
    private void runBenchmark() {
        int size = (Integer) sizeComboBox.getSelectedItem();
        String dataType = (String) dataTypeComboBox.getSelectedItem();
        
        runButton.setEnabled(false);
        log("\n========================================");
        log("開始測試: 資料量=" + size + ", 類型=" + dataType);
        log("========================================");
        
        // Generate data
        int[] data = generateData(size, dataType);
        
        // Create tasks for all 6 implementations
        CountDownLatch latch = new CountDownLatch(6);
        
        // Java Selection Sort
        executorService.submit(() -> {
            try {
                int[] dataCopy = data.clone();
                long time = SelectionSort.sort(dataCopy);
                addResult("Java", "Selection Sort", size, dataType, time);
                log("Java Selection Sort 完成: " + time + " ns");
            } catch (Exception e) {
                log("Java Selection Sort 錯誤: " + e.getMessage());
            } finally {
                latch.countDown();
            }
        });
        
        // Java Heap Selection Sort
        executorService.submit(() -> {
            try {
                int[] dataCopy = data.clone();
                long time = HeapSelectionSort.sort(dataCopy);
                addResult("Java", "Heap Selection Sort", size, dataType, time);
                log("Java Heap Selection Sort 完成: " + time + " ns");
            } catch (Exception e) {
                log("Java Heap Selection Sort 錯誤: " + e.getMessage());
            } finally {
                latch.countDown();
            }
        });
        
        // C Selection Sort
        executorService.submit(() -> {
            try {
                long time = runExternalProgram("./selection_sort_v2", data);
                addResult("C", "Selection Sort", size, dataType, time);
                log("C Selection Sort 完成: " + time + " ns");
            } catch (Exception e) {
                log("C Selection Sort 錯誤: " + e.getMessage());
            } finally {
                latch.countDown();
            }
        });
        
        // C Heap Selection Sort
        executorService.submit(() -> {
            try {
                long time = runExternalProgram("./heap_selection_sort_v2", data);
                addResult("C", "Heap Selection Sort", size, dataType, time);
                log("C Heap Selection Sort 完成: " + time + " ns");
            } catch (Exception e) {
                log("C Heap Selection Sort 錯誤: " + e.getMessage());
            } finally {
                latch.countDown();
            }
        });
        
        // Python Selection Sort
        executorService.submit(() -> {
            try {
                long time = runPythonProgram("selection_sort_v2.py", data);
                addResult("Python", "Selection Sort", size, dataType, time);
                log("Python Selection Sort 完成: " + time + " ns");
            } catch (Exception e) {
                log("Python Selection Sort 錯誤: " + e.getMessage());
            } finally {
                latch.countDown();
            }
        });
        
        // Python Heap Selection Sort
        executorService.submit(() -> {
            try {
                long time = runPythonProgram("heap_selection_sort_v2.py", data);
                addResult("Python", "Heap Selection Sort", size, dataType, time);
                log("Python Heap Selection Sort 完成: " + time + " ns");
            } catch (Exception e) {
                log("Python Heap Selection Sort 錯誤: " + e.getMessage());
            } finally {
                latch.countDown();
            }
        });
        
        // Wait for all tasks to complete
        new Thread(() -> {
            try {
                latch.await();
                SwingUtilities.invokeLater(() -> {
                    log("========================================");
                    log("所有測試完成!");
                    log("========================================");
                    runButton.setEnabled(true);
                });
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();
    }
    
    private int[] generateData(int size, String type) {
        int[] data = new int[size];
        Random random = new Random();
        
        switch (type) {
            case "random":
                for (int i = 0; i < size; i++) {
                    data[i] = random.nextInt(1000000);
                }
                log("生成 random 資料: " + size + " 個隨機數");
                break;
                
            case "good":
                for (int i = 0; i < size; i++) {
                    data[i] = i;
                }
                log("生成 good 資料: " + size + " 個已排序數");
                break;
                
            case "worse":
                for (int i = 0; i < size; i++) {
                    data[i] = size - i - 1;
                }
                log("生成 worse 資料: " + size + " 個反向排序數");
                break;
        }
        
        return data;
    }
    
    private long runExternalProgram(String program, int[] data) throws Exception {
        // Write data to temporary file
        String tempFile = "temp_data_" + System.currentTimeMillis() + ".txt";
        try (PrintWriter writer = new PrintWriter(tempFile)) {
            writer.println(data.length);
            for (int value : data) {
                writer.println(value);
            }
        }
        
        // Run program
        Process process = Runtime.getRuntime().exec(program + " " + tempFile);
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
        
        String result = reader.readLine();
        String error = errorReader.readLine();
        
        int exitCode = process.waitFor();
        
        // Clean up
        new File(tempFile).delete();
        
        if (exitCode != 0 || result == null) {
            throw new Exception("Program exited with code " + exitCode + (error != null ? ": " + error : ""));
        }
        
        return Long.parseLong(result.trim());
    }
    
    private long runPythonProgram(String script, int[] data) throws Exception {
        // Write data to temporary file
        String tempFile = "temp_data_" + System.currentTimeMillis() + ".txt";
        try (PrintWriter writer = new PrintWriter(tempFile)) {
            writer.println(data.length);
            for (int value : data) {
                writer.println(value);
            }
        }
        
        // Run program
        Process process = Runtime.getRuntime().exec("python3 " + script + " " + tempFile);
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
        
        String result = reader.readLine();
        String error = errorReader.readLine();
        
        int exitCode = process.waitFor();
        
        // Clean up
        new File(tempFile).delete();
        
        if (exitCode != 0 || result == null) {
            throw new Exception("Program exited with code " + exitCode + (error != null ? ": " + error : ""));
        }
        
        return Long.parseLong(result.trim());
    }
    
    private synchronized void addResult(String language, String version, int size, String dataType, long timeNs) {
        SwingUtilities.invokeLater(() -> {
            double timeMs = timeNs / 1_000_000.0;
            Object[] row = {language, version, size, dataType, 
                           String.format("%,d", timeNs), 
                           String.format("%.2f", timeMs)};
            tableModel.addRow(row);
        });
    }
    
    private void log(String message) {
        SwingUtilities.invokeLater(() -> {
            logArea.append(message + "\n");
            logArea.setCaretPosition(logArea.getDocument().getLength());
        });
    }
    
    private void clearResults() {
        tableModel.setRowCount(0);
        logArea.setText("");
        log("結果已清除");
    }
    
    @Override
    public void dispose() {
        executorService.shutdown();
        super.dispose();
    }
    
    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        SwingUtilities.invokeLater(() -> {
            SortBenchmarkGUI gui = new SortBenchmarkGUI();
            gui.setVisible(true);
        });
    }
}
