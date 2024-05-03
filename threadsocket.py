import socket
import select
import sys
import threading
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_client = []
def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(2048)
            if message:
                print("<" + addr[0] + ">" + message)
                message_to_send = "<" + addr[0] + ">" + message
                for i in message.split():
                    if i in ['+','-','*','/'] or i.isdigit():
                        result = 0
                        operation_list = []

                        for letter in message:
                            operation_list.append(letter)
                        oprnd1 = operation_list[0]
                        operation = operation_list[1]
                        oprnd2 = operation_list[2]

                        num1 = int(oprnd1)
                        num2 = int(oprnd2)

                        if operation == "+":
                            result = num1 + num2
                        elif operation == "-":
                            result = num1 - num2
                        elif operation == "/":
                            result = num1 / num2
                        elif operation == "*":
                            result = num1 * num2


                        output = str(result)
                        message = message + "=" + output + "\n"
                broadcast(message_to_send, conn)

            else:
                remove(conn)
        except:
            continue
def broadcast(message, connection):
    for clients in list_of_client:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)
def remove(connection):
    if connection in list_of_client:
        list_of_client.remove(connection)
        
while True:
    conn, addr = server.accept()
    list_of_client.append(conn)
    print(addr[0] + " connected")
    threading.Thread(target=clientthread,args=(conn,addr)).start()
    
conn.close()