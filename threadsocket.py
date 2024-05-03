import socket
import select
import sys
import threading
import re

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
            message = conn.recv(2048).decode()
            if message:
                print(f"Received message from <{addr[0]}>: {message}")

                splitted_message = message.split()
                for i in splitted_message:
                    if i in ['+', '-', '*', '/'] or i.isdigit():
                        result = None
                        operation_list = []
                        for letter in splitted_message:
                            operation_list.append(letter)
                        operand_1 = operation_list[0]
                        operator = operation_list[1]
                        operand_2 = operation_list[2]
                        
                        if operator == '+':
                            result = int(operand_1) + int(operand_2)
                        elif operator == '-':
                            result = int(operand_1) - int(operand_2)
                        elif operator == '*':
                            result = int(operand_1) * int(operand_2)
                        elif operator == '/':
                            result = int(operand_1) / int(operand_2)
                    if result is not None:

                        message_to_send = f"{operand_1}{operator}{operand_2}={result}\n".encode()
                    else:
                        message_to_send = "Invalid operation.\n".encode()
                else:

                    message_to_send = message.encode()
                

                print(f"Sending: {message_to_send.decode()}")
                broadcast(message_to_send, conn)

            else:
                remove(conn)
        except Exception as e:
            print(f"An error occurred: {e}")
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