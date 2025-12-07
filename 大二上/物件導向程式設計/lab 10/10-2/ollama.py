import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": 
    """
    請寫一個全新、完整且可直接執行的 Java Swing 井字遊戲（Tic-Tac-Toe）。 由於你沒有記憶，請不要參考之前的對話。請嚴格遵守以下 6 點開發規範，不要隨意發揮：

    1. 類別定義與 Main 方法

    類別必須定義為：public class TicTacToe extends JFrame implements ActionListener

    必須包含 main 方法用來啟動程式。

    2. 成員變數

    使用一維陣列：private JButton[] buttons = new JButton[9];

    玩家變數：private String currentPlayer = "X";

    遊戲狀態：private boolean gameOver = false;

    3. 建構子初始化 (請完全照抄以下程式碼)

    Java

    public TicTacToe() {
        super("Tic Tac Toe");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(400, 400);
        setLayout(new GridLayout(3, 3));

        buttons = new JButton[9];
        for (int i = 0; i < 9; i++) {
            buttons[i] = new JButton("");
            buttons[i].setFont(new Font("Arial", Font.BOLD, 60));
            buttons[i].setFocusPainted(false);
            buttons[i].addActionListener(this); // 這裡需要類別 implements ActionListener 才能運作
            add(buttons[i]);
        }
        setVisible(true);
    }
    4. 事件處理 (actionPerformed)

    取得按鈕：JButton clickedBtn = (JButton) e.getSource();

    邏輯順序：

    若 gameOver 為 true，直接 return。

    若按鈕文字不為空 (!clickedBtn.getText().equals(""))，直接 return。

    設定文字：clickedBtn.setText(currentPlayer);

    呼叫 checkWin()。若獲勝，顯示 JOptionPane 並設定 gameOver=true。

    呼叫 checkTie()。若平手，顯示 JOptionPane 並設定 gameOver=true。

    切換玩家：currentPlayer = (currentPlayer.equals("X")) ? "O" : "X";

    5. 勝負判斷 (checkWin) - 請直接照抄以免出錯 不要使用複雜迴圈計算索引，請直接使用以下列舉法：

    Java

    private boolean checkWin() {
        int[][] winConditions = {
            {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
            {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
            {0, 4, 8}, {2, 4, 6}
        };
        for (int[] c : winConditions) {
            String b1 = buttons[c[0]].getText();
            String b2 = buttons[c[1]].getText();
            String b3 = buttons[c[2]].getText();
            if (!b1.equals("") && b1.equals(b2) && b2.equals(b3)) {
                return true;
            }
        }
        return false;
    }
    6. 平手判斷 (checkTie)

    遍歷 buttons 陣列，只要發現任何一個按鈕文字是空字串 ""，就回傳 false。

    如果迴圈跑完都沒有空字串，回傳 true。

    請產生完整的 Java 程式碼，確保只有一個 Class。
    不要用沒有定義的function，checkwin等
    """,
    "stream": False
}

def get_response():
    r = requests.post(url, json=payload, timeout=600)
    r.raise_for_status()
    data = r.json()
    return data["response"]

if __name__ == "__main__":
    response = get_response()
    print(f'{response}')

    with open("response.java", "w", encoding="utf-8") as f:
        f.write(response)
    print("程式碼存成 response.java")
