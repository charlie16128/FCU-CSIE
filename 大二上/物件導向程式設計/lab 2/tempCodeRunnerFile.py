import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama9.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": "請用 Java 撰寫一個容量為 5 的堆疊類別，需實作 isFull、isEmpty、push、pop、top、popall 方法，並在 push 超過容量或 pop 空堆疊時輸出錯誤訊息 The Stack is FULL!!! 或 The Stack is EMPTY!!!，在 main 中依序測試 push(1,2,3)、top()、pop()、push(4,5)、再 push(6,7,8)、pop()、popall()、pop()，不需要system.out.println 在main內，pop()function不須印出，但popall要印出，輸出結果如下 3 The Stack is FULL!!! The Stack is FULL!!! 5 4 2 1 The Stack is EMPTY!!! The Stack is EMPTY!!! 相同。",
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
