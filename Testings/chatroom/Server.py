from socket import *
import select
import sys
from threading import *

server= socket(AF_INET,SOCK_STREAM)
server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

if len(sys.argv)!=3:
    print ("Correct")
    exit()

IP_add = tuple(sys.argv[1])

port=int(sys.argv[2])

server.bind(IP_add)#ip add is string

server.listen(10)

list_of_clients=[]

def clientthread(conn,addr):
    conn.send("Welcome")

    while True:
        try:
            message=conn.recv(2048)
            if message:
                print(IP_add+":"+message)

                broadcast(IP_add+":"+message,conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn,addr = server.accept()
    list_of_clients.append(conn)#appends socket object for each client
    print (addr[0] + " connected")

    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()


