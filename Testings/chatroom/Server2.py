from socket import *
from threading import *

def accept_incoming():
    while True:
        client,client_addr=SERVER.accept()
        print(client addr+" has connected")
        client.send(bytes("Greetings"))
        addresses[client]=client_addr
        Thread(target=handle_client, args=(client,)).start())

def handle_client(client):
    name=client.recv(BUFSIZ).decode("utf8")
    client.send(bytes("welcome","utf8"))
    broadcast(bytes(name+" has joined"))
    clients[client]=name
              

while True:
    msg=client.recv(BUFSIZ)
    if msg!=bytes("{quit}","utf8"):
        broadcast(msg,name+": ")
    else:
        client.send(bytes("{quit}","utf8"))
        client.close()
        del clients[client]
        broadcast(bytes(name+" has left"))
        break

def broadcast(msg):
    ock.send(bytes(msg))

clients={}
addresses={}

HOST=''
PORT=33000
BUFSIZ=1024
ADDR=(HOST,PORT)

SERVER=socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
              
    
