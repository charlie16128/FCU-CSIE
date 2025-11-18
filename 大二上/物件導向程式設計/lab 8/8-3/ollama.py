import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": 
    """
請你實作一個可以井字遊戲的物件，該物件可以儲存井字遊戲的盤面，並提供 set 方法供玩家輪流設定擺放 (O/X) 的位置
擺放位置的描述方式沒有限制，需實作 evaluate 方法，是得在 set 時該物件能夠判斷遊戲是否結束 (O 勝利、X 勝利或平手) 
實作完成後，需要撰寫一份Junit測試，建立一份workflow，讓github能在Push時自動進行Junit測試
        assertEquals('X', game.getBoard()); 請使用這個測試方法
你需要給我兩個程式碼，第一個是TicTacToe.java(用來放主要程式碼)，第二個是TicTacToeTest.java(用來放junit測試的程式碼)，請確保所有程式碼絕對不能有語法錯誤如同名function，且tictactoetest.java必須可以通過，必須可執行，且你的test要根據TicTacToe.java裡面有的function來製作，且給我3個@test就好絕對不可以超過
test.yml如下這是放在github上的.github/workflows中
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
          curl -L -o libs/junit-platform-console-standalone.jar \
            https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/1.10.2/junit-platform-console-standalone-1.10.2.jar

          # 編譯所有 .java
          javac -cp "libs/junit-platform-console-standalone.jar:." *.java

          # 執行 JUnit 測試
          java -jar libs/junit-platform-console-standalone.jar \
            -cp "libs/junit-platform-console-standalone.jar:." --scan-classpath

    import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TicTacToeTest {
  三個就好
    @Test
    @Test
    @Test
}

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
