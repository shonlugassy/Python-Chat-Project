import socket
import threading

Host = '127.0.0.1' 
Port= 8765 

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((Host,Port))

server.listen()

clients = []
nicknames = []

def brodcast(message): 
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message= client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            brodcast(message)
        except:
            index=clients.index(client)
            clients.remove(client) 
            client.close()
            nickname= nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client,address =server.accept()

        client.send("username".encode('utf-8'))
        nickname = client.recv(1024) 
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is {nickname}")
        brodcast(f"{nickname}joined the chat! \n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()
print("Server Running...")
receive()



