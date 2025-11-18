
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