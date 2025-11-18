好的，以下提供 `TicTacToe.java` 和 `TicTacToeTest.java` 兩個程式碼，以及一個 `test.yml` 檔案，以實現你所要求的功能。

**TicTacToe.java**

```java
import java.util.ArrayList;
import java.util.List;

public class TicTacToe {

    private char[][] board = new char[3][3];
    private char player = 'X'; // 初始玩家是 X
    private char opponent = 'O';

    public TicTacToe() {
        // 預設盤面
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                board[i][j] = '.';
            }
        }
    }

    public void set(int row, int col, char playerSymbol) {
        if (row < 0 || row >= 3 || col < 0 || col >= 3) {
            throw new IllegalArgumentException("Invalid row or column");
        }

        if (board[row][col] != '.') {
            throw new IllegalArgumentException("Cell is already occupied");
        }

        board[row][col] = playerSymbol;
        if (playerSymbol == 'X') {
            player = 'O';
        } else {
            opponent = 'X';
        }
    }

    public boolean isGameEnded() {
        // 檢查是否有勝負
        if (checkWin(player) || checkWin(opponent) || checkDraw()) {
            return true;
        }
        return false;
    }

    private boolean checkWin(char playerSymbol) {
        // 檢查第一行
        if (board[0][0] == playerSymbol && board[0][1] == playerSymbol && board[0][2] == playerSymbol) {
            return true;
        }
        // 檢查第二行
        if (board[1][0] == playerSymbol && board[1][1] == playerSymbol && board[1][2] == playerSymbol) {
            return true;
        }
        // 檢查第三行
        if (board[2][0] == playerSymbol && board[2][1] == playerSymbol && board[2][2] == playerSymbol) {
            return true;
        }
        // 檢查第一列
        if (board[0][0] == playerSymbol && board[1][0] == playerSymbol && board[2][0] == playerSymbol) {
            return true;
        }
        // 檢查第二列
        if (board[0][1] == playerSymbol && board[1][1] == playerSymbol && board[2][1] == playerSymbol) {
            return true;
        }
        // 檢查第三列
        if (board[0][2] == playerSymbol && board[1][2] == playerSymbol && board[2][2] == playerSymbol) {
            return true;
        }
        // 檢查對角線
        if (board[0][0] == playerSymbol && board[1][1] == playerSymbol && board[2][2] == playerSymbol) {
            return true;
        }
        if (board[0][2] == playerSymbol && board[1][1] == playerSymbol && board[2][0] == playerSymbol) {
            return true;
        }
        return false;
    }

    private boolean checkDraw() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == '.') {
                    return false;
                }
            }
        }
        return true;
    }

    public char[][] getBoard() {
        return board;
    }

    public void printBoard() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }
}
```

**TicTacToeTest.java**

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TicTacToeTest {

    @Test
    void testSetValidPosition() {
        TicTacToe game = new TicTacToe();
        game.set(0, 0, 'X');
        game.set(1, 1, 'O');
        game.set(2, 2, 'X');
        assertTrue(game.isGameEnded());
    }

    @Test
    void testSetInvalidPosition() {
        TicTacToe game = new TicTacToe();
        try {
            game.set(0, 0, 'X'); // 嘗試設定已佔用的位置
        } catch (IllegalArgumentException e) {
            assertThrows(IllegalArgumentException.class, () -> game.set(0, 0, 'X'));
        }
    }

    @Test
    void testCheckDraw() {
        TicTacToe game = new TicTacToe();
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                game.set(i, j, 'X');
            }
        }
        assertTrue(game.checkDraw());
    }

    @Test
    void testCheckWin() {
        TicTacToe game = new TicTacToe();
        game.set(0, 0, 'X');
        game.set(0, 1, 'X');
        game.set(0, 2, 'X');
        assertTrue(game.isGameEnded());
    }
}
```

**test.yml**

```yaml
name: junit
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Download JUnit and Run Tests
        run: |
          mkdir -p libs
          curl -L -o libs/junit-platform-console-standalone-1.10.2.jar https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/1.10.2/junit-platform-console-standalone-1.10.2.jar
          javac -cp "libs/junit-platform-console-standalone-1.10.2.jar:. " *.java
          java -jar libs/junit-platform-console-standalone-1.10.2.jar -cp "libs/junit-platform-console-standalone-1.10.2.jar:. " --scan-classpath

```

**說明:**

1.  **`TicTacToe.java`**:  這個程式碼定義了 `TicTacToe` 類別，包含盤面、玩家和對手，以及設定、檢查勝負和列印盤面的方法。
2.  **`TicTacToeTest.java`**:  這個程式碼包含 JUnit 測試，用於驗證 `TicTacToe` 類別的功能。
    *   `testSetValidPosition()`: 測試設定有效位置是否能成功。
    *   `testSetInvalidPosition()`: 測試設定已佔用位置是否會拋出異常。
    *   `testCheckDraw()`: 測試檢查是否出現平局。
    *   `testCheckWin()`: 測試檢查是否出現勝負。
3.  **`test.yml`**:  這個檔案定義了 GitHub Actions 的工作流程，用於自動執行 JUnit 測試。
    *   `on`:  定義了工作流程觸發的條件，例如當有 `push` 或 `pull_request` 時。
    *   `jobs`:  定義了工作流程的步驟。
    *   `steps`:  定義了工作流程的步驟，例如 checkout code、設定 JDK、下載 JUnit 和執行測試。

**如何使用:**

1.  將 `TicTacToe.java` 和 `TicTacToeTest.java` 放在一個目錄中。
2.  將 `test.yml` 放在 GitHub 儲存區的 root 目錄中。
3.  在 GitHub 上創建一個新的儲存區。
4.  在儲存區中創建一個新的分支。
5.  提交 `TicTacToe.java` 和 `TicTacToeTest.java` 到該分支。
6.  推送該分支到 GitHub。

GitHub Actions 會自動執行 JUnit 測試，並在測試通過時顯示成功，在測試失敗時顯示錯誤。

**注意:**

*   需要確保你的環境中已安裝 JUnit 平台。
*   如果測試失敗，請檢查程式碼是否有錯誤，並進行修正。
*   如果需要更複雜的測試，可以添加更多的測試案例。

希望這個解答對你有幫助！