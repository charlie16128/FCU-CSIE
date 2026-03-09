import requests

# url = "https://ollama7.fcuhpc.isyziv.cc/api/generate"
# url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"
url = "https://ollama8.fcuhpc.isyziv.cc/api/generate"

payload = {
    "model": "gemma3n:e2b",
    "prompt": 
    """
    Please act as a senior Java software engineer and computer science instructor to provide a comprehensive and detailed code analysis of the two provided Java files, MyBroadcastServer.java and Lab2_TCPClient.java, which together form a multi-threaded TCP chat application. I need you to explain the underlying architecture and logic in a single continuous explanation, covering how the ServerSocket accepts connections in a loop, the purpose of wrapping the client output streams in a Collections.synchronizedList to ensure thread safety during the broadcast method, and how the server spawns a new ChatHandler thread for every connected client to handle blocking I/O operations without freezing the main server loop; additionally, please analyze the client-side code by explaining the Swing GUI initialization, the critical necessity of using a separate background thread to read messages from the server to avoid blocking the Event Dispatch Thread (EDT), the role of SwingUtilities.invokeLater in updating UI components safely from that background thread, and finally, trace the complete lifecycle of a message from the moment a user types text and clicks "Send" in the client, detailing how it travels through the socket output stream to the server, gets processed by the handler, broadcasted to all writers, and received back by the client's input stream to be displayed in the JTextArea. Here is the code:

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
