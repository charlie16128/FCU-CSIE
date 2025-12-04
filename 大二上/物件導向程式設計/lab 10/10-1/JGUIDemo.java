import java.awt.*;
import java.awt.event.*;
import java.io.*;
import javax.swing.*; // 匯入 IO 套件以處理檔案儲存與讀取

public class JGUIDemo extends JFrame implements ActionListener {
    
    private static final int FRAME_WIDTH    = 350; // 稍微加寬以符合圖片比例
    private static final int FRAME_HEIGHT   = 300;
    private static final int FRAME_X_ORIGIN = 150;
    private static final int FRAME_Y_ORIGIN = 250;
    
    private static final String NEWLINE = System.getProperty("line.separator");
	private static final String FILE_NAME = "content.txt";

    private JButton clearButton;
    private JButton addButton;

    private JTextField inputLine; // 使用者輸入文字的地方
    private JTextArea  textArea;  // 顯示文字的地方
    
    private JMenuItem saveMenuItem;
    private JMenuItem loadMenuItem;
   
    public JGUIDemo(String title) {
        super(title);
        
        // 設定視窗屬性
        this.setSize      (FRAME_WIDTH, FRAME_HEIGHT);
        this.setResizable (true);
        this.setLocation  (FRAME_X_ORIGIN, FRAME_Y_ORIGIN);

        Container contentPane = getContentPane();
        // 修改版面配置：使用 BorderLayout 讓元件由上而下排列更像圖片
        contentPane.setLayout(new BorderLayout());
        
        // 1. 文字顯示區 (TextArea) - 放中間 (CENTER)
        textArea = new JTextArea();
        textArea.setEditable(false); // 設定不可直接編輯，只能透過輸入框加入
        JScrollPane scrollText= new JScrollPane(textArea);
        // 設定垂直卷軸總是顯示 (依照圖片樣式)
        scrollText.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
        contentPane.add(scrollText, BorderLayout.CENTER);
        
        // 建立一個南方的 Panel 來放 輸入框 和 按鈕
        JPanel bottomPanel = new JPanel();
        bottomPanel.setLayout(new BorderLayout());
        
        // 2. 輸入框 (TextField) - 放南方 Panel 的上方
        inputLine = new JTextField();
        inputLine.addActionListener(this); // 讓按下 Enter 也能觸發事件
        bottomPanel.add(inputLine, BorderLayout.NORTH);
        
        // 3. 按鈕區 (Buttons) - 放南方 Panel 的下方
        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new FlowLayout()); // 按鈕並排
        
        addButton = new JButton("ADD");
        addButton.addActionListener(this);
        buttonPanel.add(addButton);
        
        clearButton = new JButton("CLEAR");
        clearButton.addActionListener(this);
        buttonPanel.add(clearButton);
        
        bottomPanel.add(buttonPanel, BorderLayout.SOUTH);
        
        // 將整個 bottomPanel 放入主視窗的南方
        contentPane.add(bottomPanel, BorderLayout.SOUTH);
        
        // 選單列設定
        JMenuBar menuBar = new JMenuBar();
        this.setJMenuBar(menuBar);
        JMenu funcMenu = new JMenu("FUNC");
        
        saveMenuItem = new JMenuItem("Save");
        saveMenuItem.addActionListener(this);
        funcMenu.add(saveMenuItem);
        
        loadMenuItem = new JMenuItem("Load");
        loadMenuItem.addActionListener(this);
        funcMenu.add(loadMenuItem);
        
        menuBar.add(funcMenu);
        
        setDefaultCloseOperation( EXIT_ON_CLOSE );
        
        this.setVisible(true);
    }
    
    public static void main(String arg[]) {
        new JGUIDemo("D1349111 lab 10"); // 修改標題以符合圖片
    }
    
    public void actionPerformed(ActionEvent event) {
        Object source = event.getSource();

        // --- 邏輯 1: 加入文字 (ADD 按鈕 或 在輸入框按 Enter) ---
        if (source == addButton || source == inputLine) {
            String text = inputLine.getText();
            if (!text.isEmpty()) {
                textArea.append(text + NEWLINE); // 加入文字並換行
                inputLine.setText(""); // 清空輸入框
            }
            System.out.println("User added: " + text);
        } 
        
        // --- 邏輯 2: 清除文字 (CLEAR 按鈕) ---
        else if (source == clearButton) {
            textArea.setText("");
            System.out.println("Text area cleared");
        } 
        
        // --- 邏輯 3: 載入檔案 (Load) ---
        else if (source == loadMenuItem) {
            try {
                File file = new File(FILE_NAME);
                if (!file.exists()) {
                    JOptionPane.showMessageDialog(this, "找不到檔案: " + FILE_NAME);
                    return;
                }
                
                // 使用 BufferedReader 讀取檔案
                BufferedReader reader = new BufferedReader(new FileReader(file));
                textArea.setText(""); // 載入前先清空
                String line;
                while ((line = reader.readLine()) != null) {
                    textArea.append(line + NEWLINE);
                }
                reader.close();
                System.out.println("Content loaded from " + FILE_NAME);
                
            } catch (IOException e) {
                e.printStackTrace();
                JOptionPane.showMessageDialog(this, "讀取錯誤: " + e.getMessage());
            }
        } 
        
        // --- 邏輯 4: 儲存檔案 (Save) ---
        else if (source == saveMenuItem) {
            try {
                // 使用 BufferedWriter 寫入檔案
                BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_NAME));
                writer.write(textArea.getText());
                writer.close();
                System.out.println("Content saved to " + FILE_NAME);
                JOptionPane.showMessageDialog(this, "儲存成功！");
                
            } catch (IOException e) {
                e.printStackTrace();
                JOptionPane.showMessageDialog(this, "寫入錯誤: " + e.getMessage());
            }
        }
    }
}