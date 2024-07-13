from ko2en import OpusMT_KO2EN, ClaudeTranslate, OpenAITranslate
import socket
import threading
import os
from dotenv import load_dotenv 
load_dotenv()

def connect_clients(connected_clients: list, server: socket):
    server.listen(1)
    while True:
        client, addr = server.accept()
        print(f"Connected by {addr}")
        connected_clients.append(client)

def main(method="local", context_size=3):
    # Connect to Korean transcriber
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 8080))
    
    # Allow clients to connect this function (for C# applications)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostname(), 5000))
    server.listen(1)
    
    connected_clients = []
    t1 = threading.Thread(target=connect_clients, args=(connected_clients, server,))
    t1.start()
    
    # translator = OpusMT_KO2EN()
    translator = ClaudeTranslate(api_key=os.environ["CLAUDE_API_KEY"])
    
    context = []
    try:
        while True:
            text = s.recv(1024).decode()
            context_txt = ""
            for i in context:
                context_txt += i
        
            translation = translator.translate(context_txt, text)
            print(translation.strip())
            
            for client in connected_clients[:]:  # Create a copy of the list to iterate over
                try:
                    client.send(translation.encode())
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    print(f"Client {client.getpeername()} disconnected")
                    connected_clients.remove(client)
                    client.close()
            
            print()
            context.append(text)
            if len(context) > context_size:
                context.pop(0)
            
    except KeyboardInterrupt:
        s.close()


if __name__ == "__main__":
    main()
    # print(socket.gethostname())