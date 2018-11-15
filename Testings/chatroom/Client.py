from socket import *
import select
import sys

server=socket(AF_INET,SOCK_STREAM)

if len(sys.argv)!=3:
    print "Correct"
    exit()

IP_add=str(sys.argv[1])
port=int(sys.argv[2])
server.connect((IP_add,port))

while True:
    sockets_list=[sys.stdin,server]

    read_sockets,write_socket,error_socket=select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            message=socks.recv(2048)
            print(message)
        else:
            message=sys.stdin.readline()
            server.send(message)
            sys.stdout.write()
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()
            
