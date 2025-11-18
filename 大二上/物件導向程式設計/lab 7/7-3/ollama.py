import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": 
    """
    實作一個 Fraction Class 其 attribute 包含除數與被除數，其 method 包含設定除數與被除數以及實際進行除法，實作兩種不同之進行除法的 method，其中一個在該 method 內處理除數為零的 Exception ，另一種將 Exception 扔出，交由外層程式處理，在 main 中展示兩種不同的 Exception Handling 處理方法
    
    class Fraction {
    private double numerator;   // 被除數
    private double denominator; // 除數

    public void setNumerator(double numerator) {
        this.numerator = numerator;
    }

    public void setDenominator(double denominator) {
        this.denominator = denominator;
    }

    // 方式一：在方法內部處理 Exception
    public void divideInside() {

    }

    // 方式二：讓外層來處理 Exception
    public double divideOutside() throws ArithmeticException {

    }
}

public class FractionDemo {
    public static void main(String[] args) {

        // -------- 方式一：在方法內部處理  --------


        // -------- 方式二：外部處理例外 --------


        // -------- 正常運作情況 --------

    }
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
