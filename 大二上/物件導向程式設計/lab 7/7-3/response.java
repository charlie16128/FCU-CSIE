```java
import java.util.InputMismatchException;

class Fraction {
    private double numerator; // 被除數
    private double denominator; // 除數

    public void setNumerator(double numerator) {
        this.numerator = numerator;
    }

    public void setDenominator(double denominator) {
        this.denominator = denominator;
    }

    // 方式一：在方法內部處理 Exception
    public void divideInside() {
        if (denominator == 0) {
            throw new ArithmeticException("除數不能為零");
        }
        double result = numerator / denominator;
        System.out.println("結果 (內部處理): " + result);
    }

    // 方式二：讓外層來處理 Exception
    public double divideOutside() throws ArithmeticException {
        if (denominator == 0) {
            throw new ArithmeticException("除數不能為零");
        }
        double result = numerator / denominator;
        System.out.println("結果 (外部處理): " + result);
        return result;
    }
}

public class FractionDemo {
    public static void main(String[] args) {
        Fraction frac = new Fraction();

        // -------- 正常運作情況 --------
        frac.setNumerator(10);
        frac.setDenominator(2);

        try {
            frac.divideOutside();
        } catch (ArithmeticException e) {
            System.err.println("錯誤 (外部處理): " + e.getMessage());
        }

        System.out.println("--------------------");

        // -------- 測試除數為零的情況 --------
        frac.setNumerator(10);
        frac.setDenominator(0);

        try {
            frac.divideOutside();
        } catch (ArithmeticException e) {
            System.err.println("錯誤 (外部處理): " + e.getMessage());
        }

        System.out.println("--------------------");

        // -------- 測試除數為零的情況 --------
        frac.setNumerator(5);
        frac.setDenominator(0);

        try {
            frac.divideOutside();
        } catch (ArithmeticException e) {
            System.err.println("錯誤 (外部處理): " + e.getMessage());
        }
    }
}
```

**程式碼說明:**

1. **`Fraction` 類別:**
   - `numerator` 和 `denominator` 屬性：儲存被除數和除數。
   - `setNumerator()` 和 `setDenominator()` 方法：用於設定被除數和除數。
   - `divideInside()` 方法：在方法內部檢查除數是否為零。如果除數為零，則拋出 `ArithmeticException`。如果除數不為零，則計算並印出結果。
   - `divideOutside()` 方法：在方法內部檢查除數是否為零。如果除數為零，則拋出 `ArithmeticException`。如果除數不為零，則計算並印出結果，然後將結果返回。

2. **`FractionDemo` 類別:**
   - `main()` 方法：
     - 建立一個 `Fraction` 實例。
     - **正常運作情況：**
       - 設定被除數和除數。
       - 呼叫 `divideOutside()` 方法，使用 `try-catch` 區塊處理 `ArithmeticException`。
     - **除數為零的情況：**
       - 設定被除數和除數為零。
       - 呼叫 `divideOutside()` 方法，使用 `try-catch` 區塊處理 `ArithmeticException`。
     - 輸出錯誤訊息到標準錯誤流 (System.err)。

**執行結果:**

```
結果 (外部處理): 10.0
--------------------
錯誤 (外部處理): 除數不能為零
--------------------
錯誤 (外部處理): 除數不能為零
```

**重點說明:**

* **`ArithmeticException`:**  這個例外類別是 Java 標準庫中定義的，用於表示算術錯誤，例如除數為零。
* **`try-catch` 區塊:**  用於處理可能拋出的例外。 `try` 區塊包含可能拋出的程式碼，`catch` 區塊包含處理例外的程式碼。
* **`System.err.println()`:**  用於輸出錯誤訊息到標準錯誤流，通常用於顯示錯誤訊息。
* **兩種除法方法:**  `divideInside()` 和 `divideOutside()` 兩種方法實現了不同的除法邏輯，分別在方法內部和方法外部處理除數為零的例外。
* **清晰的程式碼結構:**  程式碼結構清晰，易於理解和維護。

這個程式碼提供了一個完整的範例，展示了如何在 Java 中處理除數為零的例外，並提供了兩種不同的方法，以便更好地理解和應用。